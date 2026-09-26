"""Verify saved throttle solids at sampled opening angles and their inlet connection."""
from pathlib import Path
import sys,json,itertools,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
parts=[o for o in m['occurrences'] if o['id'].startswith(('throttle-','tps-','iac-')) or o['id']=='efi-upper-intake']
shapes={o['definition']:b.import_step(ROOT/'cad/engine/generated'/f"{o['definition']}.step") for o in parts}
angles=[0,15,30,45,60,75,90]
checks=0
for angle in angles:
    pose=transforms(m,throttle_degrees=angle)
    placed={o['id']:shapes[o['definition']].moved(pose[o['id']]) for o in parts}
    bounds={id:s.bounding_box() for id,s in placed.items()}
    for (aid,a),(bid,c) in itertools.combinations(placed.items(),2):
        if not all(min(getattr(bounds[aid].max,k),getattr(bounds[bid].max,k))-max(getattr(bounds[aid].min,k),getattr(bounds[bid].min,k))>.001 for k in ['X','Y','Z']):continue
        overlap=a.intersect(c);volume=sum(s.volume for s in overlap.solids()) if overlap else 0
        assert volume<.1,(angle,aid,bid,volume)
        checks+=1
    if angle==90:
        # Offset from the shaft/edge-on plates: both inlet paths must be open.
        for y in [-2,52]:
            probe=b.Pos(390,y,500)*b.Rot(0,90,0)*b.Cylinder(2,74)
            for id,shape in placed.items():
                overlap=shape.intersect(probe);volume=sum(s.volume for s in overlap.solids()) if overlap else 0
                assert volume<.01,('open inlet',id,y,volume)
report={'status':'pass','manifest_sha256':hashlib.sha256((ROOT/'inventory/engine/full-assembly.json').read_bytes()).hexdigest(),'sampled_throttle_degrees':angles,'pair_checks':checks,'open_inlet_probes':2,'scope':'Idealized mechanism, seven sampled positions; no production stop calibration or airflow validation.'}
(ROOT/'inventory/engine/throttle-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
