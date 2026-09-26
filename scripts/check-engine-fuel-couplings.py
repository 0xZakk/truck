"""Coupling decomposition, passage and geometric clearance checks (not fit proof)."""
from pathlib import Path
import sys,json,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from fuel_couplings import STATIONS
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d={v['id']:v for v in m['definitions']};poses=transforms(m)
report={'verified_production_fit':False,'couplings':[]}
for line,station in STATIONS.items():
 parent='fuel-'+line+'-coupling';parts=[o for o in m['occurrences'] if o['parent']==parent];assert len(parts)==8
 assert len([o for o in parts if o['definition']==parent+'-seal'])==2
 shapes={o['id']:b.import_step(ROOT/d[o['definition']]['step'].lstrip('/')).moved(poses[o['id']]) for o in parts}
 for s in shapes.values():assert s.is_valid and len(s.solids())==1
 tube='fuel-supply-rail' if line=='supply' else 'fuel-return-tube'
 shapes[tube]=b.import_step(ROOT/d[tube]['step'].lstrip('/')).moved(poses[tube])
 collisions=[]
 for a,c in itertools.combinations(shapes,2):
  v=shapes[a].intersect(shapes[c]);vol=sum(s.volume for s in v.solids()) if v else 0
  if vol>.01:collisions.append({'a':a,'b':c,'volume_mm3':vol})
 x,y,z=station;probe=b.Plane(origin=(x-20,y,z),z_dir=(1,0,0))*b.Cylinder(.5,44)
 blockage=0
 for shape in shapes.values():
  v=shape.intersect(probe);blockage+=sum(s.volume for s in v.solids()) if v else 0
 report['couplings'].append({'line':line,'parts':len(parts),'collisions':collisions,'axial_passage_blockage_mm3':blockage})
p=ROOT/'inventory/engine/fuel-coupling-validation.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p.read_text())
assert all(not r['collisions'] and r['axial_passage_blockage_mm3']<.01 for r in report['couplings'])
