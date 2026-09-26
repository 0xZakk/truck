"""Check modeled filter envelope and passages, not OEM construction/calibration."""
from pathlib import Path
import json,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d={x['id']:x for x in m['definitions']}
parts=[o for o in m['occurrences'] if o['parent']=='oil-filter-assembly'];assert len(parts)==13
shapes={o['id']:b.import_step(ROOT/d[o['definition']]['step'].lstrip('/')) for o in parts}
for s in shapes.values():assert s.is_valid and len(s.solids())==1
box=b.Compound(children=list(shapes.values())).bounding_box()
assert abs(box.size.X-93)<.01 and abs(box.size.Z-132)<.01
seal=shapes['oil-filter-gasket'].bounding_box();assert abs(seal.size.X-72)<.01 and abs(seal.size.Z-5)<.01
collisions=[]
for a,c in itertools.combinations(shapes,2):
 v=shapes[a].intersect(shapes[c]);vol=sum(s.volume for s in v.solids()) if v else 0
 if vol>.01:collisions.append({'a':a,'b':c,'volume_mm3':vol})
probes={'central-outlet':(shapes['oil-filter-baseplate'],b.Pos(0,0,4)*b.Cylinder(.5,10)),'inlet':(shapes['oil-filter-baseplate'],b.Pos(27,0,4)*b.Cylinder(.5,10)),'center-tube-perforation':(shapes['oil-filter-center-tube'],b.Plane(origin=(22.6,0,26),z_dir=(1,0,0))*b.Cylinder(.5,4))}
blocked={}
for name,(s,probe) in probes.items():
 v=s.intersect(probe);blocked[name]=sum(t.volume for t in v.solids()) if v else 0
report={'parts':13,'envelope_mm':[box.size.X,box.size.Y,box.size.Z],'comparison':'Published WIX51515 metric envelope; not an OEM Ford drawing','collisions':collisions,'passage_blockage_mm3':blocked,'verified_production_fit':False,'limits':'No filter performance, calibrated bypass, adapter connection or OEM internal-geometry validation.'}
# A radial path from the dirty bypass pocket to the central outlet must meet
# the standpipe wall below the valve seat. An open path here defeats the media.
wall_checks={}
for z in (7,11,15):
 probe=b.Plane(origin=(10,0,z),z_dir=(1,0,0))*b.Cylinder(.2,4)
 v=shapes['oil-filter-bypass-housing'].intersect(probe)
 wall_checks[str(z)]=sum(t.volume for t in v.solids()) if v else 0
report['outlet_separator_intersections_mm3']=wall_checks
assert min(wall_checks.values())>.03, 'Dirty bypass pocket leaks directly to clean outlet'
seat_probe=b.Pos(16,0,18.75)*b.Cylinder(.5,.4)
seated=shapes['oil-filter-bypass-poppet'].intersect(seat_probe)
lifted=(b.Pos(0,0,1)*shapes['oil-filter-bypass-poppet']).intersect(seat_probe)
seat_vol=sum(t.volume for t in seated.solids()) if seated else 0
lift_vol=sum(t.volume for t in lifted.solids()) if lifted else 0
report['bypass_seat_probe_mm3']={'closed':seat_vol,'lifted_1mm':lift_vol}
assert seat_vol>.3 and lift_vol<.001, 'Bypass disc must close its seat and release it when lifted'
p=ROOT/'inventory/engine/oil-filter-validation.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p.read_text());assert not collisions and max(blocked.values())<.01
