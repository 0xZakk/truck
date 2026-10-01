#!/usr/bin/env python3
"""Read-only lower passage conflict map; no lower-region CAD changes exported."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_valvetrain_adapter_candidate as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};frames=c.poses(m)
paths={k:ROOT/defs[k]['step'].lstrip('/') for k in ['cylinder-head','head-gasket','block','pushrod']}
paths['migrated-block']=ROOT/'cad/engine/generated/timing-block-support-machining-candidate/block.step'
assert sha(paths['migrated-block'])=='2880d7873e14c8407d40b219d06753be554c069db51da3bdf2ef300724544cfb'
inputs={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'cad/engine/timing_valvetrain_adapter_candidate.py',ROOT/'inventory/engine/full-assembly.json']+list(paths.values())}
sh={k:(frames['block' if k=='migrated-block' else k]*b.import_step(p) if k!='pushrod' else b.import_step(p)) for k,p in paths.items()}
r={'status':'RESEARCH conflict map; no passage revision authorized by this checker','inputs':inputs,'rows':[],'limits':['Block candidate separately uninstalled; guide bore continues through deck in supplied model.','No traced coolant network exists in supplied head/gasket; absence of a modeled coolant hole is not evidence of production separation.','Proposed radius6 envelope is a geometric study, not a measured port.','No new lower head/gasket/block CAD exported.']}
# Rejected upper-only drilling intrudes into +Y valve-cover gasket support.
# Existing gasket inner/outer straight edges areY98/104; head topZ333.5.
rejected=ROOT/'cad/engine/generated/timing-valvetrain-adapter-candidate/rejected-upper-passage-v1/cylinder-head.step'
inputs[str(rejected.relative_to(ROOT))]=sha(rejected)
old_removed=b.Compound(children=list(sh['cylinder-head'].cut(frames['cylinder-head']*b.import_step(rejected)).solids()))
ledge=b.Pos(0,101,333)*b.Box(1000,6,1)
r['rejected_upper_passage_lost_cover_ledge_mm3']=vol(old_removed.intersect(ledge))
assert r['rejected_upper_passage_lost_cover_ledge_mm3']>1
for i,kind,x in c.stations(m):
 tag=f'c{i}-{kind}';center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(i)*120;theta=(center-150)%720
 rod=c.poses(m,theta)[tag+'-pushrod']*sh['pushrod'];row={'id':tag,'crank_degrees':theta,'actual_rod_overlaps_mm3':{}}
 for k in ['cylinder-head','head-gasket','block','migrated-block']:
  intersection=rod.intersect(sh[k]);row['actual_rod_overlaps_mm3'][k]=vol(intersection)
  if vol(intersection)>.1:row[k+'_overlap_bounds_mm']=[list(intersection.bounding_box().min),list(intersection.bounding_box().max)]
 # Tiny exhaust pushrod tilt exposes an OCC Boolean false negative. A point
 # strictly inside both solids independently proves collision even if common
 # unexpectedly returnsNone; never accept that zero as clearance.
 row['interior_collision_witnesses']={}
 for key,zprobe in [('head-gasket',254.75),('cylinder-head',280.)]:
  point=(x+2,98.,zprobe)
  inside_rod=rod.is_inside(point);inside_neighbor=sh[key].is_inside(point)
  row['interior_collision_witnesses'][key]={'point_mm':point,'inside_pushrod':inside_rod,'inside_neighbor':inside_neighbor,'boolean_false_negative':inside_rod and inside_neighbor and row['actual_rod_overlaps_mm3'][key]<.1}
  assert inside_rod and inside_neighbor
 # Proposed swept-passage study starts with restR6 and must later cover swing.
 y=c.P['PUSHROD_Y'];probe=b.Pos(x,y,254.75)*b.Cylinder(6,1.5)
 row['proposed_R6_gasket_removed_mm3']=vol(probe.intersect(sh['head-gasket']))
 # Explicit model-land distances: existing boreR51.5, bolt holeR7 and +Yedge109.
 cylxs=[a['position_cad_mm'][0] for a in m['assemblies'] if a['id'].startswith('piston-group-')]
 bolts=[o for o in m['occurrences'] if o['id'].startswith('head-bolt-')]
 row['proposed_circle_to_combustion_aperture_min_mm']=min(math.hypot(x-z,y)-6-51.5 for z in cylxs)
 row['proposed_circle_to_head_bolt_aperture_min_mm']=min(math.hypot(x-o['position_cad_mm'][0],y-o['position_cad_mm'][1])-6-7 for o in bolts)
 row['proposed_circle_to_plusY_outer_edge_mm']=109-y-6
 # Entire proposed annulus6..8 over block deck: missing material is a support
 # gap, not a collision. Demonstrate the inherited full-size guide opening.
 ann=(b.Pos(x,y,253.995)*b.Cylinder(8,.01)).cut(b.Pos(x,y,253.995)*b.Cylinder(6,.03))
 row['R6_to_R8_block_deck_support_probe_volume_mm3']=vol(ann)
 row['R6_to_R8_migrated_block_missing_support_mm3']=vol(ann.cut(sh['migrated-block']))
 r['rows'].append(row);print(tag,row['actual_rod_overlaps_mm3'],flush=True)
assert all(sha(ROOT/p)==h for p,h in inputs.items())
(ROOT/'inventory/engine/timing-valvetrain-passage-contract-validation.json').write_text(json.dumps(r,indent=2)+'\n')
