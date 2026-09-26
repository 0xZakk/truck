"""Check replacement-envelope claims and thermostat artifact composition."""
import json
from pathlib import Path
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
defs={d['id']:d for d in m['definitions']}
parts=[o for o in m['occurrences'] if o['parent']=='thermostat-assembly']
assert len(parts)==9
shapes={o['id']:b.import_step(ROOT/defs[o['definition']]['step'].lstrip('/')) for o in parts}
frame=shapes['thermostat-frame'].bounding_box()
assert abs(frame.size.Y-53.85)<.01
assert abs(frame.size.Z-53.85)<.01
bb=b.Compound(children=list(shapes.values())).bounding_box()
assert abs(bb.size.X-37.85)<.01,bb.size.X
# Verify air-bleed drilling remains open through the flange, around the pin.
probe=b.Pos(0,23,0)*b.Rot(0,90,0)*b.Cylinder(1.1,1.2)
assert not shapes['thermostat-frame'].intersect(probe).solids()
report={'components':9,'flange_diameter_mm':53.85,'overall_height_mm':round(bb.size.X,3),'envelope_check':'pass','jiggle_pin_bore':'open in frame','source':'motorad-244-192','limits':'Replacement envelope checks only. No proof of installed identity, internal accuracy, thermal response or head/outlet fit.'}
(ROOT/'inventory/engine/thermostat-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
