#!/usr/bin/env python3
"""Read-only localization; proposed analytic cutter is never applied to block."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from cad_metrics import solid_volume
import timing_block_axis_feature_candidate as guards
import timing_block_support_machining_candidate as support
import oil_pan_joint_v9_candidate as pan
import timing_cover_front_joint_candidate as front
OUT=ROOT/'cad/engine/generated/timing-front-crank-clearance-research';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def bounds(q):
 if q is None or not q.solids():return None
 bb=q.bounding_box();return [list(bb.min),list(bb.max)]
paths={'block':ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step','gear':ROOT/'cad/engine/generated/timing-thrust-land-candidate/crank-timing-gear.step','future-land':ROOT/'cad/engine/generated/timing-cover-attachment-v2/future-block-land.step'}
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()}
for p in [Path(__file__),Path(guards.__file__),Path(support.__file__),Path(pan.__file__),Path(front.__file__),ROOT/'inventory/engine/timing-pump-foot-faceted-validation.json']:inputs[str(p.relative_to(ROOT))]=sha(p)
parts={k:b.import_step(p) for k,p in paths.items()};block=parts['block'];gear=parts['gear'];cutter=pan.x_cylinder(44.18,378.009375,392.509375)
collision=block.intersect(gear);removal=block.intersect(cutter)
mask,spec=guards.protected_masks();mask={k:v for k,v in mask.items() if k.startswith(('main-','pan-'))}
mask['old-front-entire-annular-support']=pan.low_half(pan.x_cylinder(59.4,365,381)-pan.x_cylinder(42,364,382))
mask['old-front-outer-2mm-seal-backing']=pan.low_half(pan.x_cylinder(59.4,365,381)-pan.x_cylinder(57.4,364,382))
mask['future-block-land']=parts['future-land']
for i,(x,y,z) in enumerate(pan.STATIONS,1):mask[f'physical-pan-boss-{i}']=b.Pos(x,y)*pan.cylinder(10 if y>0 or (x in(-371.,371.) and y!=0) else 7,z+7.6,z+25)
for i,s in support.backing_shells().items():mask[f'cam-bearing-backing-{i}']=s
stations=[(365.5,y,front.PLANE-7.6) for y in (-132.,196.)]+[(390.,y,front.top(y)-7.6) for y in(-110.,0.,180.)]
for i,(x,y,head) in enumerate(stations,1):mask[f'future-front-fastener-boss-{i}']=front.disk(10,x,y,head+7.6,head+23.6)
rows=[]
for name,m in mask.items():
 hit=removal.intersect(m);row={'name':name,'proposed_removed_material_mm3':vol(hit),'intersection_bounds_mm':bounds(hit),'distance_from_proposed_removal_mm':removal.distance_to(m),'unchanged':vol(hit)<1e-5};rows.append(row)
 if not row['unchanged']:print(row,flush=True)
for name,s in [('collision',collision),('proposed-removal',removal),('analytic-envelope',cutter)]:b.export_step(s,OUT/(name+'.step'))
r={'status':'RESEARCH ONLY; no block cut performed','input_sha256':inputs,'block_valid':block.is_valid,'gear_valid':gear.is_valid,'collision_mm3':vol(collision),'collision_bounds_mm':bounds(collision),'collision_outside_envelope_mm3':vol(collision.cut(cutter)),'estimated_envelope':{'radius_mm':44.18,'x_mm':[378.009375,392.509375],'axis_yz_mm':[0,0]},'proposed_removal_mm3':vol(removal),'proposed_removal_bounds_mm':bounds(removal),'guards':rows,'negative_control_no_cutter_collision_mm3':vol(collision),'limits':['No geometry candidate or installation approval','Entire old front support and broad guards remain reported even if exact sealing band stays clear','2mm seal-support band is an estimated inspection guard, not manufacturer strength evidence','Future front land/fasteners are uninstalled estimates'],'artifacts':{p.name:sha(p) for p in OUT.glob('*.step')}}
assert inputs=={p:sha(ROOT/p) for p in inputs}
(ROOT/'inventory/engine/timing-front-crank-clearance-research.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['input_sha256','guards','artifacts']},indent=2),flush=True)
