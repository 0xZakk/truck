#!/usr/bin/env python3
"""Mount/contact and protected-region gates before broader linkage sweeps."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_valvetrain_inclined_candidate as c
OUT=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate';OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'inventory/engine/timing-valvetrain-inclined-candidate-validation.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d={x['id']:x for x in m['definitions']};o={x['id']:x for x in m['occurrences']}
keys=['cylinder-head','rocker-arm','rocker-fulcrum','rocker-guide','rocker-bolt','pushrod','intake-valve','exhaust-valve','lifter-pushrod-cup','lifter-body','head-gasket','block','valve-cover']
paths={k:ROOT/d[k]['step'].lstrip('/') for k in keys}
watch=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/timing_valvetrain_contract.py',ROOT/'cad/engine/valve_source_layout.py',ROOT/'inventory/engine/full-assembly.json']+list(paths.values())
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
r={'status':'RUNNING','inputs':inputs,'failures':[],'mounts':[],'contacts':[]}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
save();shapes={k:b.import_step(p) for k,p in paths.items()}
newrocker=c.rocker();assert newrocker.is_valid and len(newrocker.solids())==1
print('New common rocker valid',flush=True)
newhead=c.head_adapter(shapes['cylinder-head'],m);assert newhead.is_valid and len(newhead.solids())==1
print('New head valid; protected difference next',flush=True)
allowed=c.allowed_regions(m)
removed=b.Compound(children=list(shapes['cylinder-head'].cut(newhead).solids()));added=b.Compound(children=list(newhead.cut(shapes['cylinder-head']).solids()))
r['head_change']={'removed_mm3':vol(removed),'added_mm3':vol(added),'removed_outside_allowed_mm3':vol(removed.cut(allowed)),'added_outside_allowed_mm3':vol(added.cut(allowed))}
assert max(r['head_change']['removed_outside_allowed_mm3'],r['head_change']['added_outside_allowed_mm3'])<1e-5
r['exports']={}
for key,q in [('rocker-arm',newrocker),('cylinder-head',newhead)]:
 path=OUT/(key+'.step');b.export_step(q,path);reload=b.import_step(path)
 assert reload.is_valid and len(reload.solids())==1
 r['exports'][key]={'step_sha256':sha(path),'volume_mm3':vol(q),'roundtrip_volume_error_mm3':abs(vol(q)-vol(reload))}
 assert r['exports'][key]['roundtrip_volume_error_mm3']<.01
save();shapes.update({'rocker-arm':newrocker,'cylinder-head':newhead})
frames=c.poses(m);head=frames['cylinder-head']*newhead
for i,kind,x in c.stations(m):
 tag=f'c{i}-{kind}'
 placed={suffix:frames[tag+'-'+suffix]*shapes[o[tag+'-'+suffix]['definition']] for suffix in ['guide','fulcrum','rocker-bolt']}
 row={'id':tag,'guide_head_gap_mm':placed['guide'].distance_to(head),'guide_fulcrum_gap_mm':placed['guide'].distance_to(placed['fulcrum']),'bolt_fulcrum_gap_mm':placed['rocker-bolt'].distance_to(placed['fulcrum']),'bolt_head_overlap_mm3':vol(placed['rocker-bolt'].intersect(head)),'estimated_shank_insertion_mm':15.,'radial_bore_clearance_mm':.1,'true_thread_engagement':'NOT MODELED: retained smooth-shank bolt and smooth4.6mm-radius hole'}
 # Pedestal annulus immediately below its guide proves area support, not only a point.
 z=c.P['rest'](kind,c.P['PIVOT_Y'])['pivot_z']-20
 probe=(b.Pos(x,c.P['PIVOT_Y'],z-.005)*b.Cylinder(9,.01)).cut(b.Pos(x,c.P['PIVOT_Y'],z-.005)*b.Cylinder(5.01,.03))
 row['support_annulus_missing_mm3']=vol(probe.cut(head))
 row['up0p1_guide_fault_gap_mm']=(b.Pos(0,0,.1)*placed['guide']).distance_to(head)
 if max(row['guide_head_gap_mm'],row['guide_fulcrum_gap_mm'],row['bolt_fulcrum_gap_mm'])>.002 or row['support_annulus_missing_mm3']>1e-5 or row['bolt_head_overlap_mm3']>.1:r['failures'].append({'mount':row})
 assert row['up0p1_guide_fault_gap_mm']>.05
 r['mounts'].append(row)
print('Mounts complete',len(r['failures']),flush=True);save()
# Event-relative sampled contacts at each actual branch, with both cam axial endpoints.
for i,kind,x in c.stations(m):
 tag=f'c{i}-{kind}';center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(i)*120
 for off in [-150,-96,0,96,150]:
  for axial in [0,-.1]:
   theta=(center+off)%720;frames=c.poses(m,theta,axial);s=c.contract.state(theta,i,kind,axial)
   placed={suffix:frames[tag+'-'+suffix]*shapes[o[tag+'-'+suffix]['definition']] for suffix in ['rocker','valve','pushrod','lifter-pushrod-cup','fulcrum']}
   point=b.Vertex(x,s['pad_y'],261+c.v.LENGTHS[kind]-s['valve_lift'])
   gaps={'pad_valve':max(point.distance_to(placed['rocker']),point.distance_to(placed['valve']))}
   for a,z in [('rocker','pushrod'),('pushrod','lifter-pushrod-cup'),('rocker','fulcrum')]:gaps[a+'__'+z]=placed[a].distance_to(placed[z])
   row={'id':tag,'crank_degrees':theta,'axial_mm':axial,'gaps_mm':gaps}
   if max(gaps.values())>.002:r['failures'].append({'contact':row})
   r['contacts'].append(row)
 print(tag,'contacts',len(r['failures']),flush=True);save()
# First neighbor gate: actual retained lower head passage, before broader sweeps.
r['lower_passage_probe']=[]
for i,kind,x in c.stations(m):
 tag=f'c{i}-{kind}';theta=((468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(i)*120-150)%720
 frames=c.poses(m,theta,0);rod=frames[tag+'-pushrod']*shapes['pushrod'];over=rod.intersect(head)
 row={'id':tag,'crank_degrees':theta,'head_overlap_mm3':vol(over)}
 if vol(over)>.1:
  bb=over.bounding_box();row['overlap_bounds_mm']=[list(bb.min),list(bb.max)];r['failures'].append({'lower_passage':row})
 r['lower_passage_probe'].append(row)
assert all(sha(ROOT/p)==h for p,h in inputs.items())
r['status']='FAIL first gates' if r['failures'] else 'PASS first mount/contact gates; deck and gasket checks separate'
r['limits']=['No source/manufacturer casting fidelity claim.','Smooth bolt insertion is not true thread engagement.','GLB/render and broad passage/neighbor/piston sweeps pending first-gate review.','Lower head passage expanded only in approved mask; deck/gasket checked separately.']
save();print(r['status'],flush=True)
