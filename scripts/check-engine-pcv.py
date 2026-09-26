"""PCV study clearance and open-passage checks; no calibration or OEM fit claim."""
from pathlib import Path
import json,sys,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from pcv import POSITION
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};poses=transforms(m)
occ=[o for o in m['occurrences'] if o['parent']=='pcv-valve-assembly'];assert len(occ)==6
shapes={o['id']:b.import_step(ROOT/defs[o['definition']]['step'].lstrip('/')).moved(poses[o['id']]) for o in occ}
for s in shapes.values():assert s.is_valid and len(s.solids())==1
collisions=[]
for a,c in itertools.combinations(shapes,2):
 v=shapes[a].intersect(shapes[c]);vol=sum(s.volume for s in v.solids()) if v else 0
 if vol>.01:collisions.append({'a':a,'b':c,'volume_mm3':vol})
for target in ['valve-cover','efi-upper-intake']:
 shape=b.import_step(ROOT/defs[target]['step'].lstrip('/')).moved(poses[target])
 for ident,s in shapes.items():
  v=s.intersect(shape);vol=sum(t.volume for t in v.solids()) if v else 0
  if vol>.01:collisions.append({'a':ident,'b':target,'volume_mm3':vol})
# Outlet centerline probes only: the plunger intentionally occupies the core axis.
x,y,z=POSITION;blocks=[]
for height in (12,24):
 probe=b.Plane(origin=(x,y-10,z+height),z_dir=(0,1,0))*b.Cylinder(.5,20)
 v=shapes['pcv-outlet-head'].intersect(probe);blocks.append(sum(s.volume for s in v.solids()) if v else 0)
report={'parts':6,'collisions':collisions,'outlet_bore_blockage_mm3':blocks,'verified_production_fit':False,'limits':'Static provisional geometry only. No spring force, airflow, seal compression, plunger travel or installed-identity verification.'}
p=ROOT/'inventory/engine/pcv-validation.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p.read_text());assert not collisions and max(blocks)<.01
