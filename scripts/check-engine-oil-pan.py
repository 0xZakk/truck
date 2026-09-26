"""Check rear-sump teaching geometry and pickup fit, not production accuracy."""
from pathlib import Path
import sys,json,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d={x['id']:x for x in m['definitions']};o={x['id']:x for x in m['occurrences']};poses=transforms(m)
ids=['oil-pan','oil-pickup-tube','oil-pickup-bell','oil-pickup-screen','oil-pan-drain-plug','oil-pan-drain-gasket']
s={i:b.import_step(ROOT/d[o[i]['definition']]['step'].lstrip('/')).moved(poses[i]) for i in ids}
for p in s.values():assert p.is_valid and len(p.solids())==1
assert abs(s['oil-pan'].bounding_box().size.Z-234.95)<.01
collisions=[]
for a,c in itertools.combinations(s,2):
 v=s[a].intersect(s[c]);vol=sum(x.volume for x in v.solids()) if v else 0
 if vol>.01:collisions.append({'a':a,'b':c,'mm3':vol})
assert not collisions,collisions
# Probe the floor directly under the screen, not just the global minimum bound.
screen_center=s['oil-pickup-screen'].bounding_box().center()
probe=b.Pos(screen_center.X,screen_center.Y,-270)*b.Cylinder(1,20)
floor=s['oil-pan'].intersect(probe);assert floor and floor.solids()
clearance=s['oil-pickup-screen'].bounding_box().min.Z-floor.bounding_box().max.Z
assert clearance>5 and clearance<25,clearance
from oil_pan import DRAIN_LOCAL,DRAIN_ROTATION
frame=b.Pos(DRAIN_LOCAL[0],-12,DRAIN_LOCAL[2]-96)*b.Rot(*DRAIN_ROTATION)
drain_probe=frame*(b.Pos(0,0,-4)*b.Cylinder(.5,25))
assert not s['oil-pan'].intersect(drain_probe), 'Drain hole is blocked with plug removed'
plug_local=b.import_step(ROOT/d['oil-pan-drain-plug']['step'].lstrip('/'))
assert plug_local.bounding_box().size.Z>14.9
r={'pan_depth_mm':s['oil-pan'].bounding_box().size.Z,'screen_floor_clearance_mm':clearance,'collisions':collisions,'verified_production_fit':False,'limits':'Depth comparison applied; flange, sump contour, pickup bends and target clearance remain assumptions. No capacity or installed-fit verification.'}
p=ROOT/'inventory/engine/oil-pan-validation.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p.read_text())
