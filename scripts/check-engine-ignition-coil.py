"""Check independent coil solids/clearances; not a winding or fit validation."""
from pathlib import Path
import json,itertools,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
d={d['id']:d for d in m['definitions']}
parts=[o for o in m['occurrences'] if o['parent']=='ignition-coil-assembly']
loc=transforms(m)
shapes={o['id']:b.import_step(ROOT/d[o['definition']]['step'].lstrip('/')).moved(loc[o['id']]) for o in parts}
assert len(parts)==10
collisions=[]
for a,c in itertools.combinations(shapes,2):
 intersection=shapes[a].intersect(shapes[c]);volume=sum(s.volume for s in intersection.solids()) if intersection else 0
 if volume>.1:collisions.append({'a':a,'b':c,'volume_mm3':round(volume,4)})
report={'occurrences':len(parts),'collisions':collisions,'verified_production_geometry':False,'limits':'Solid separation only. Winding packs and lamination stacks are aggregates with unverified dimensions; no electromagnetic or installed-mount validation.'}
(ROOT/'inventory/engine/ignition-coil-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));assert not collisions
