"""Validate teaching-switch solids, isolation and contact state; not calibration."""
from pathlib import Path
import json,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d={x['id']:x for x in m['definitions']}
parts=[o for o in m['occurrences'] if o['parent']=='oil-pressure-switch-assembly'];assert len(parts)==9
s={o['id']:b.import_step(ROOT/d[o['definition']]['step'].lstrip('/')) for o in parts}
for x in s.values():assert x.is_valid and len(x.solids())==1

def volume(a,c):
 v=a.intersect(c);return sum(x.volume for x in v.solids()) if v else 0
collisions=[{'a':a,'b':c,'mm3':v} for a,c in itertools.combinations(s,2) if (v:=volume(s[a],s[c]))>.01]
assert not collisions,collisions
# Pressure inlet remains open up to the sealed diaphragm.
inlet=b.Pos(0,0,9.5)*b.Cylinder(.5,19)
assert volume(s['oil-pressure-body'],inlet)<.001
assert volume(s['oil-pressure-diaphragm'],b.Pos(0,0,20.15)*b.Cylinder(.5,.2))>.15
# The electrical teaching pose is open; a 1mm displacement closes the gap.
contact=s['oil-pressure-moving-contact'];fixed=s['oil-pressure-terminal']
assert abs(fixed.bounding_box().min.Z-contact.bounding_box().max.Z-1)<.001
closed=b.Pos(0,0,1)*contact
assert closed.distance_to(fixed)<.001
assert contact.distance_to(fixed)>.99
# The stud stays clear of both grounded case and retaining rim.
assert fixed.distance_to(s['oil-pressure-body'])>1
assert fixed.distance_to(s['oil-pressure-rim'])>1
report={'parts':len(s),'collisions':collisions,'inlet_open':True,'diaphragm_separates_oil':True,'open_contact_gap_mm':contact.distance_to(fixed),'closed_contact_distance_mm':closed.distance_to(fixed),'verified_production_fit':False,'limits':'Checks the illustrative arrangement only; no threshold, flexure, production construction or installed interface validation.'}
p=ROOT/'inventory/engine/oil-pressure-validation.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p.read_text())
