#!/usr/bin/env python3
"""Isolated stop feasibility; no canonical writes. Default0/45/90 plus sensitivities."""
from pathlib import Path
import sys,json,hashlib,itertools,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/throttle-stop-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');fig=plt.figure(figsize=(16,8))
 for panel,angle in enumerate([0,90],1):
  ax=fig.add_subplot(1,2,panel,projection='3d');names=json.loads(str(a[f'names{angle}']))
  for i,key in enumerate(names):
   color='#d2a54e' if 'screw' in key else '#476b88' if 'lever' in key else '#bcc1c3';alpha=.22 if key=='baseline-housing' else 1
   ax.add_collection3d(Poly3DCollection(a[f'v{angle}_{i}'][a[f'f{angle}_{i}']],facecolors=color,edgecolor='none',shade=True,alpha=alpha))
  ax.set(xlim=(370,420),ylim=(72,100),zlim=(475,520),xlabel='Parent X mm',ylabel='Y mm',zlabel='Z mm',title=f'{angle}° educational endpoint');ax.set_box_aspect((50,28,45));ax.view_init(24,55)
 fig.suptitle('Isolated throttle stop feasibility\nIdle screw/pad supported by factory topology; WOT lug, dimensions and0/90 calibration illustrative');fig.tight_layout();fig.subplots_adjust(top=.87);fig.savefig(OUT/'candidate-endpoints.png',dpi=140);raise SystemExit
import build123d as b
import trimesh
sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_stop_candidate as c
import throttle_cable_candidate as cable
import throttle_return_spring_candidate as spring
from assembly_math import transforms
from cad_metrics import solid_volume,support_bounds
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
mp=ROOT/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};inputs={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(c.__file__),Path(cable.__file__),Path(spring.__file__),mp]};cache={}
def local(oid):
 did=O[oid]['definition']
 if did not in cache:
  p=ROOT/D[did]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=sha(p);cache[did]=b.import_step(p)
 return cache[did]
volume_refinements=[]
def vol(q):
 if not q:return 0.
 result=0.
 for shape in q.solids():
  try:value=solid_volume(shape,'adaptive')
  except ValueError:
   from OCP.BRepGProp import BRepGProp
   from OCP.GProp import GProp_GProps
   trials=[]
   for eps in [1e-10,1e-11,1e-12]:
    props=GProp_GProps();error=BRepGProp.VolumeProperties_s(shape.wrapped,props,eps,True,False);trials.append(dict(eps=eps,error=error,value=props.Mass()))
   good=[x['value'] for x in trials if 0<=x['error']<=1e-7]
   if len(good)<2:
    for eps in [1e-9,1e-10]:
     props=GProp_GProps();error=BRepGProp.VolumePropertiesGK_s(shape.wrapped,props,eps,True,True);trials.append(dict(method='adaptive Gauss-Kronrod with spline spans',eps=eps,error=error,value=props.Mass()))
    good=[x['value'] for x in trials if 0<=x['error']<=1e-7]
   if len(good)<2 or max(good)-min(good)>1e-5:raise ValueError('Refined volume failed: '+str(trials))
   value=good[-1];volume_refinements.append(trials)
  result+=abs(value)
 return result
def bb(q):z=q.bounding_box();return np.array([tuple(z.min),tuple(z.max)])
def overlap(a,z):return bool(np.all(a[0]<=z[1]+1e-6) and np.all(z[0]<=a[1]+1e-6))
def area(a,z):
 total=0.
 for f in a.faces():
  for g in z.faces():
   if overlap(bb(f),bb(g)):
    x=f.intersect(g)
    if x:total+=x.area if hasattr(x,'area') else sum(v.area for v in x)
 return total
OUT.mkdir(parents=True,exist_ok=True);oldh=local('throttle-housing');oldl=local('throttle-lever-estimated');pieces,features=c.parts(oldh,oldl);output_hashes={};exports={}
for key,q in pieces.items():
 sp=OUT/(key+'.step');b.export_step(q,sp);actual=b.import_step(sp);v,f=q.tessellate(.04,.15);mesh=trimesh.Trimesh(np.array([tuple(x) for x in v])[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(key+'.glb');mesh.export(gp);pieces[key]=actual
 exports[key]=dict(valid=actual.is_valid,solids=len(actual.solids()),watertight=mesh.is_watertight,step_volume_error_mm3=abs(vol(q)-vol(actual)))
 for p in [sp,gp]:output_hashes[str(p.relative_to(ROOT))]=sha(p)
h=pieces['throttle-housing-stop-proposal'];l=pieces['throttle-lever-stop-proposal'];screw=pieces['throttle-idle-stop-screw-illustrative'];dh=b.Compound(children=list(h.cut(oldh).solids()));dl=b.Compound(children=list(l.cut(oldl).solids()))
protected=dict(original_housing_removed_mm3=vol(oldh.cut(h)),original_lever_removed_mm3=vol(oldl.cut(l)))
key_guard=b.Pos(0,65,0)*b.Rot(90,0,0)*b.Cylinder(7.5,12)
hook_guard=b.Pos(0,65,18)*b.Rot(90,0,0)*b.Cylinder(2,12)
ball_guard=b.Pos(0,66,24)*b.Rot(90,0,0)*b.Cylinder(4,14)
protected['lever_key_hook_ball_changes_mm3']=sum(vol(x.intersect(guard)) for x in dl.solids() for guard in [key_guard,hook_guard,ball_guard])
bores=[b.Pos(397.5,y,490)*c.cx(20,60) for y in [-2,52]];protected['new_housing_in_flow_bores_mm3']=sum(vol(x.intersect(z)) for x in dh.solids() for z in bores)
# Added casting must overlap actual existing housing, not hang in empty space.
anchors={key:vol(q.intersect(oldh)) for key,q in features.items() if key in ['idle_boss','wot_lug']}
angles=sorted(set(range(0,91,2))|{45}) if '--full' in sys.argv else [0,45,90];collisions=[];contacts=[];preview={};tested=0
for angle in angles:
 poses=transforms(m,throttle_degrees=angle);parent=poses['throttle-housing'];lever_pose=poses['throttle-lever-estimated'];full={'housing':h.moved(parent),'lever':l.moved(lever_pose),'screw':screw.moved(parent)};deltas={'housing':dh.moved(parent),'lever':dl.moved(lever_pose),'screw':screw.moved(parent)}
 dynamic=cable.stationary()|cable.moving(angle)[0];dynamic={k:q.moved(parent) for k,q in dynamic.items()};dynamic['throttle-return-spring-illustrative']=spring.spring(angle).moved(parent)
 for oid,o in O.items():
  if oid in ['throttle-housing','throttle-lever-estimated']:continue
  # Mesh broad phase then actual current STEP/deforming CAD; candidate additions
  # only for revised housing/lever, whose existing material is preserved above.
  q=dynamic.get(oid)
  if q is None:
   gp=ROOT/D[o['definition']]['glb'].lstrip('/');mesh=trimesh.load(gp,force='mesh');v=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;corners=itertools.product(*zip(v.min(0),v.max(0)));vv=np.array([tuple(b.Vertex(*p).moved(poses[oid]).center()) for p in corners]);bounds=np.array([vv.min(0),vv.max(0)])
   if not any(overlap(bb(a),bounds) for a in deltas.values()):continue
   q=local(oid).moved(poses[oid])
  for ident,a in deltas.items():
   if overlap(bb(a),bb(q)):
    tested+=1;volume=vol(a.intersect(q))
    if volume>1e-5:collisions.append(dict(angle=angle,a=ident,b=oid,overlap_mm3=volume))
 for (a,q),(z,r) in itertools.combinations(full.items(),2):
  if overlap(bb(q),bb(r)):
   volume=vol(q.intersect(r));tested+=1
   if volume>1e-5:collisions.append(dict(angle=angle,a=a,b=z,overlap_mm3=volume))
 contacts.append(dict(angle_deg=angle,idle_contact_mm2=area(full['screw'],full['lever']),wot_contact_mm2=area(full['housing'],full['lever'])))
 if angle in [0,90]:
  # Parent-local actual geometry; baseline casting translucent, additions visible.
  pp={'baseline-housing':oldh,'housing-additions':dh,'lever':l.moved(parent.inverse()*lever_pose),'idle-screw':screw};preview[f'names{angle}']=np.array(json.dumps(list(pp)))
  for i,q in enumerate(pp.values()):v,f=q.tessellate(.06,.2);preview[f'v{angle}_{i}']=np.array([tuple(x) for x in v]);preview[f'f{angle}_{i}']=np.array(f)
 print(angle,'collisions',collisions,'contacts',contacts[-1],flush=True)
np.savez_compressed(OUT/'preview.npz',**preview)
sensitivity=[]
for angle in [-1,1,89,91]:
 poses=transforms(m,throttle_degrees=angle);lp=l.moved(poses['throttle-housing'].inverse()*poses['throttle-lever-estimated']);sensitivity.append(dict(angle_deg=angle,idle_overlap_mm3=vol(lp.intersect(screw)),housing_overlap_mm3=vol(lp.intersect(h))))
neutral_l=l.moved(transforms(m)['throttle-housing'].inverse()*transforms(m)['throttle-lever-estimated']);controls=dict(detached_screw_contact_mm2=area(screw.moved(b.Pos(-10,0,0)),neutral_l));retention_run='--thread-retention' in sys.argv or '--full' in sys.argv
if retention_run:
 # A contained sphere proves a strict overlap lower bound without integrating
 # ill-conditioned thin trimmed helix solids. Exact cuts must leave no solid.
 controls['capture_witnesses']=[]
 for delta,wy,label in [(.125,91.12583302491977,'positive'),(-.125,88.87416697508023,'negative')]:
  center=(380.,wy,501.35);radius=.03;witness=b.Pos(*center)*b.Sphere(radius);shifted=screw.moved(b.Pos(delta,0,0))
  contained=not witness.cut(shifted).solids() and not witness.cut(h).solids()
  lower=4*math.pi*radius**3/3 if contained else 0.
  controls[label+'_axial_capture_mm3']=lower
  controls['capture_witnesses'].append(dict(delta_x_mm=delta,center_mm=center,radius_mm=radius,exact_containment=contained,overlap_lower_bound_mm3=lower))
 y,z=c.PARAMS['idle_axis_y'],c.PARAMS['idle_axis_z'];turn=b.Pos(.125,y,z)*b.Rot(90,0,0)*b.Pos(0,-y,-z);controls['quarter_turn_thread_path_overlap_mm3']=vol(screw.moved(turn).intersect(h))
retention_pass=not retention_run or (min(controls['positive_axial_capture_mm3'],controls['negative_axial_capture_mm3'])>1e-4 and controls['quarter_turn_thread_path_overlap_mm3']<1e-5)
passed=not collisions and max(protected.values())<1e-5 and min(anchors.values())>1e-4 and contacts[0]['idle_contact_mm2']>1e-4 and contacts[-1]['wot_contact_mm2']>1e-4 and all(v['valid'] and v['solids']==1 and v['watertight'] and v['step_volume_error_mm3']<.001 for v in exports.values()) and controls['detached_screw_contact_mm2']<1e-6 and retention_pass and sensitivity[0]['idle_overlap_mm3']>1e-4 and sensitivity[-1]['housing_overlap_mm3']>1e-4 and sensitivity[1]['idle_overlap_mm3']<1e-5 and sensitivity[-2]['housing_overlap_mm3']<1e-5
assert all(sha(ROOT/p)==v for p,v in inputs.items()),'Input changed during feasibility'
r=dict(status='PASS' if passed else 'FAIL',scope='Isolated estimated idle screw/pad and illustrative WOT lug; no factory dimensions, thread, torque or stop-angle calibration.',readiness='ISOLATED CANDIDATE; integration and browser checks not performed' if '--full' in sys.argv else 'FEASIBILITY ONLY; full sweep not performed',thread_retention_status='PASS' if retention_run and retention_pass else 'FAIL' if retention_run else 'NOT RUN: deferred until cheap geometry/source comparison review',full_sweep='--full' in sys.argv,input_hashes=inputs,output_hashes=output_hashes,parameters=c.PARAMS,volume_measurement_refinements=volume_refinements,protected_regions=protected,casting_attachment_overlap_mm3=anchors,contacts=contacts,overtravel_sensitivity=sensitivity,retention_controls=controls,collisions=collisions,exact_pairs=tested,exports=exports,all_current_occurrences_considered=len(O),source_ledger='reference/engine/throttle-stop-review.json')
(ROOT/'inventory/engine/throttle-stop-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r,flush=True);raise SystemExit(0 if passed else 1)
