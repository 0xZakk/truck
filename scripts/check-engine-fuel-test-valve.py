"""Validate modeled diagnostic-port continuity and internal clearance, not OEM fit."""
from pathlib import Path
import json,sys,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from fuel_test_valve import POSITION
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
d={x['id']:x for x in m['definitions']};loc=transforms(m)
parts=[o for o in m['occurrences'] if o['parent']=='fuel-test-valve'];assert len(parts)==8
shapes={o['id']:b.import_step(ROOT/d[o['definition']]['step'].lstrip('/')).moved(loc[o['id']]) for o in parts}
collisions=[]
for a,c in itertools.combinations(shapes,2):
 v=shapes[a].intersect(shapes[c]);vol=sum(s.volume for s in v.solids()) if v else 0
 if vol>.01:collisions.append({'a':a,'b':c,'volume_mm3':vol})
rail=b.import_step(ROOT/d['fuel-supply-rail']['step'].lstrip('/'))
x,y,z=POSITION
probe=b.Pos(x,y,z-4.5)*b.Cylinder(.5,9)
v=rail.intersect(probe);blocked=sum(s.volume for s in v.solids()) if v else 0
assert blocked<.01,blocked
report={'parts':len(parts),'internal_collisions':collisions,'rail_branch_blockage_mm3':blocked,'verified_production_fit':False,'limits':'Static closed-valve study. No opening travel, pressure, leak rate, material or installed-identity validation.'}
(ROOT/'inventory/engine/fuel-test-valve-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));assert not collisions
