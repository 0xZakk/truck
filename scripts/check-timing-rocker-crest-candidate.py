#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_rocker_crest_candidate as t
c=t.c;OUT=ROOT/'cad/engine/generated/timing-rocker-crest-candidate';OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'inventory/engine/timing-rocker-crest-candidate-validation.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
paths={k:ROOT/defs[k]['step'].lstrip('/') for k in ['valve-cover','pushrod','intake-valve','exhaust-valve','rocker-fulcrum']}
watch=[Path(__file__),Path(t.__file__),Path(c.__file__),t.BASE,ROOT/'inventory/engine/full-assembly.json',ROOT/'reference/engine/oil-fill-neck-review.json']+list(paths.values())
r={'status':'RUNNING','inputs':{str(p.relative_to(ROOT)):sha(p) for p in watch},'poses':[],'failures':[]}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
a=b.import_step(t.BASE);q=t.build(a);assert q.is_valid and len(q.solids())==1
removed=a.cut(q);r['changes']={'removed_mm3':vol(removed),'added_mm3':vol(q.cut(a)),'removed_outside_mask_mm3':vol(removed.cut(t.mask()))};assert r['changes']['added_mm3']<1e-5 and r['changes']['removed_outside_mask_mm3']<1e-5
socket=(0,c.P['PUSHROD_Y']-c.P['PIVOT_Y'],c.P['CUP_Z']);masks={'fulcrum':b.Sphere(15.05),'socket':b.Pos(*socket)*b.Sphere(c.v.BALL_R+.05),'pad':b.Pos(0,c.v.VALVE_Y-c.P['PIVOT_Y'],c.v.PAD_CENTER_Z-11)*b.Box(16,16,3)}
r['protected_difference_mm3']={k:diff(a.intersect(mask),q.intersect(mask)) for k,mask in masks.items()};assert max(r['protected_difference_mm3'].values())<1e-5
sphere_top=socket[2]+c.v.BALL_R;cap=b.Pos(socket[0],socket[1],sphere_top+2)*b.Cylinder(2,4)
r['socket_backing']={'axial_sphere_top_to_crest_mm':t.NEW_TOP-sphere_top,'R2_height4_cap_volume_mm3':vol(cap),'missing_cap_mm3':vol(cap.cut(q))};assert r['socket_backing']['axial_sphere_top_to_crest_mm']>=4 and r['socket_backing']['missing_cap_mm3']<1e-5
p=OUT/'rocker-arm.step';b.export_step(q,p);q=b.import_step(p);assert q.is_valid and len(q.solids())==1
r['export']={'step_sha256':sha(p),'roundtrip_volume_error_mm3':abs(vol(t.build(a))-vol(q))};assert r['export']['roundtrip_volume_error_mm3']<.01
sh={k:b.import_step(p) for k,p in paths.items()};save()
for i,kind,x in c.stations(m):
 tag=f'c{i}-{kind}';center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(i)*120
 for off in [-150,0]:
  for axial in [0,-.1]:
   theta=(center+off)%720;frames=c.poses(m,theta,axial);rock=frames[tag+'-rocker']*q;cover=frames['valve-cover']*sh['valve-cover'];oldrock=frames[tag+'-rocker']*a
   row={'id':tag,'theta':theta,'axial':axial,'old_overlap_mm3':vol(oldrock.intersect(cover)),'new_overlap_mm3':vol(rock.intersect(cover)),'cover_distance_mm':rock.distance_to(cover),'contacts_mm':{}}
   for suffix,key in [('pushrod','pushrod'),('fulcrum','rocker-fulcrum'),('valve',kind+'-valve')]:row['contacts_mm'][suffix]=rock.distance_to(frames[tag+'-'+suffix]*sh[key])
   if row['new_overlap_mm3']>.1 or max(row['contacts_mm'].values())>.002:r['failures'].append(row)
   r['poses'].append(row)
 print(tag,'failures',len(r['failures']),flush=True);save()
assert max(z['old_overlap_mm3'] for z in r['poses'])>.1
assert all(sha(ROOT/p)==h for p,h in r['inputs'].items())
r['status']='FAIL local candidate gates' if r['failures'] else 'PASS scoped crest CAD/backing and48 actual exported rest/peak poses; broader sweep NOT RUN'
r['limits']=['2mm reduction and6mm profile remain estimates, not production dimensions or strength validation.','Entire cover and frozen kinematics unchanged.','Source morphology remains a simplified solid profile, not a faithful stamped trough.','No full-curve sidewall/spring/disassembly/browser acceptance.'];save();print(r['status'])
