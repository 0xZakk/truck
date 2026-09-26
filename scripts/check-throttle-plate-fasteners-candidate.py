"""Isolated estimated plate screw retention; relevant dependencies only guarded."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/throttle-plate-fasteners-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(14,7))
 for idx,(el,az) in enumerate([(20,-35),(20,145)],1):
  ax=fig.add_subplot(1,2,idx,projection='3d')
  for i,key in enumerate(names):
   color='#ca9b4c' if 'plate-' in key and 'screw' not in key else '#596d7e' if 'shaft' in key else '#d8dce0'
   ax.add_collection3d(Poly3DCollection(a[f'v{i}'][a[f'f{i}']],facecolors=color,edgecolor='none',shade=True,alpha=.45 if 'shaft' in key else 1))
  ax.set(xlim=(-5,5),ylim=(-49,49),zlim=(-22,22),xlabel='Local X mm',ylabel='Local Y mm',zlabel='Local Z mm',title='Illustrative two screws per plate; shaft translucent');ax.set_box_aspect((30,98,44));ax.view_init(el,az)
 fig.subplots_adjust(top=.85,bottom=.08,left=.03,right=.97);fig.savefig(OUT/'candidate-context.png',dpi=150)
 fig=plt.figure(figsize=(10,5));i=names.index('throttle-plate-screw-1-1-illustrative');v=a[f'v{i}']+np.array([0,35,0]);f=a[f'f{i}']
 for j,az in enumerate([-55,135],1):
  ax=fig.add_subplot(1,2,j,projection='3d');ax.add_collection3d(Poly3DCollection(v[f],facecolors='#91a6b5',edgecolor='none',shade=True));ax.set(xlim=(-2,4),ylim=(-2,2),zlim=(-2,2),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title='Illustrative screw;0.5 mm pitch');ax.set_box_aspect((6,4,4));ax.view_init(20,az)
 fig.subplots_adjust(top=.85,bottom=.12,left=.04,right=.96);fig.savefig(OUT/'candidate-screw-detail.png',dpi=160);raise SystemExit
import build123d as b
import trimesh
sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_plate_fasteners_candidate as c
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';raw=M.read_bytes();m=json.loads(raw);D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m)
inputs={}
def track(path):inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();return path
for p in [Path(__file__),Path(c.__file__),ROOT/'reference/engine/throttle-plate-fasteners-review.json']:track(p)
cache={}
def local(oid):
 did=O[oid]['definition']
 if did not in cache:cache[did]=b.import_step(track(ROOT/D[did]['step'].lstrip('/')))
 return cache[did]
def vol(q):return sum(abs(solid_volume(x,'adaptive')) for x in q.solids()) if q else 0.
def bb(q):z=q.bounding_box();return np.array([tuple(z.min),tuple(z.max)])
def overlap(a,z,pad=.2):return bool(np.all(a[0]<=z[1]+pad) and np.all(z[0]<=a[1]+pad))
def contact(q,r):
 total=0.
 for f in q.faces():
  for g in r.faces():
   if not overlap(bb(f),bb(g),1e-6):continue
   x=f.intersect(g)
   if x:total+=x.area if hasattr(x,'area') else sum(v.area for v in x)
 return total
prior_path=ROOT/'inventory/engine/throttle-plate-fasteners-candidate-validation.json';prior_raw=prior_path.read_bytes() if '--reuse-sweep' in sys.argv else None;prior=json.loads(prior_raw) if prior_raw else None
parts,screws=c.parts(local('throttle-shaft'),local('throttle-plate-1'))
shaft=parts['throttle-shaft-plate-retention-illustrative'];plate=parts['throttle-plate-drilled-illustrative']
allowed=[b.Pos(0,y,0)*c.cx(2.01,8) for y in [-35,-19,19,35]]
# Boolean subtraction can return ShapeList; never apply its list subtraction
# operator as though it were a second geometric cut.
shaft_outside_change=sum(vol(solid.cut(*allowed)) for diff in [shaft.cut(local('throttle-shaft')),local('throttle-shaft').cut(shaft)] for solid in diff.solids())
assert shaft_outside_change<1e-5
assert O['throttle-plate-1']['position_cad_mm']==[0,-27,0] and O['throttle-plate-2']['position_cad_mm']==[0,27,0]
assembly={'shaft':shaft,'plate-1':b.Pos(0,-27,0)*plate,'plate-2':b.Pos(0,27,0)*plate,**screws}
OUT.mkdir(exist_ok=True);exports={};output_hashes={}
for key,obj in {**parts,'throttle-plate-screw-illustrative':c.screw()}.items():
 sp=OUT/(key+'.step');b.export_step(obj,sp);v,f=obj.tessellate(.05,.12);v=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,np.array(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(key+'.glb');mesh.export(gp)
 loaded=trimesh.load(gp,force='mesh');vv=np.asarray(loaded.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
 exports[key]={'valid':obj.is_valid,'solids':len(obj.solids()),'watertight':mesh.is_watertight,'step_volume_error_mm3':abs(vol(b.import_step(sp))-vol(obj)),'glb_bounds_error_mm':float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bb(obj))))}
 for path in [sp,gp]:output_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 print('export',key,exports[key],flush=True)
# All occurrences enter mesh-AABB broad phase for the entire swept region.
# Far-away mesh files are not dependency guards: root may integrate unrelated
# components concurrently. Exact selected STEP dependencies are guarded.
region=np.array([[373.5,-38,469.5],[414.5,94,510.5]]);bounds_cache={};neighbors={};skipped={'throttle-shaft','throttle-plate-1','throttle-plate-2'}
for oid,o in O.items():
 if oid in skipped:continue
 did=o['definition']
 if did not in bounds_cache:
  mesh=trimesh.load(ROOT/D[did]['glb'].lstrip('/'),force='mesh');v=np.asarray(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;bounds_cache[did]=np.array([v.min(0),v.max(0)])
 corners=np.array([tuple(b.Vertex(*v).moved(poses[oid]).center()) for v in itertools.product(*zip(*bounds_cache[did]))]);bounds=np.array([corners.min(0),corners.max(0)])
 if overlap(bounds,region):neighbors[oid]=local(oid).moved(poses[oid])
print('neighbors',list(neighbors),flush=True)
if 'throttle-return-spring-illustrative' in neighbors:
 import throttle_return_spring_candidate as spring_candidate
 track(Path(spring_candidate.__file__))
collisions=[];internal=[];exact=0
for (a,q),(z,r) in itertools.combinations(assembly.items(),2):
 if overlap(bb(q),bb(r)):
  v=vol(q.intersect(r));internal.append({'a':a,'b':z,'overlap_mm3':v})
  if v>1e-5:collisions.append({'a':a,'b':z,'angle':None,'overlap_mm3':v})
sweep_proof=None
if prior is not None:
 assert len(prior['sweep'])==47 and not prior['collisions']
 assert prior['manifest_snapshot_sha256']==hashlib.sha256(raw).hexdigest()
 for path,digest in prior['input_hashes'].items():
  if path not in [str(Path(__file__).relative_to(ROOT)),str(Path(c.__file__).relative_to(ROOT))]:assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
 old_parts,old_screws=c.parts(local('throttle-shaft'),local('throttle-plate-1'),finite_thread_cutter=True)
 old_shaft=old_parts['throttle-shaft-plate-retention-illustrative']
 # Regenerate the finite-thread geometry whose47 poses were actually tested.
 # The corrected tap only removes shaft material. A subset cannot create a
 # new neighbor collision under any of the same rigid transforms.
 added=vol(shaft.cut(old_shaft));same_plate=vol(plate.cut(old_parts['throttle-plate-drilled-illustrative']))+vol(old_parts['throttle-plate-drilled-illustrative'].cut(plate))
 same_screws=sum(vol(q.cut(old_screws[key]))+vol(old_screws[key].cut(q)) for key,q in screws.items())
 assert added<1e-8 and same_plate<1e-8 and same_screws<1e-8
 sweep=[{'angle_deg':row['angle_deg'],'minimum_nearby_distance_lower_bound_mm':row.get('minimum_nearby_distance_mm',row.get('minimum_nearby_distance_lower_bound_mm'))} for row in prior['sweep']]
 exact=prior['exact_sweep_pairs']
 sweep_proof={'method':'Prior47 exact poses plus regenerated finite-thread baseline and current-shaft subset proof; no added matter can introduce a collision.','prior_report_sha256':hashlib.sha256(prior_raw).hexdigest(),'prior_candidate_sha256':prior['input_hashes'][str(Path(c.__file__).relative_to(ROOT))],'prior_input_hashes':prior['input_hashes'],'prior_output_hashes':prior['output_hashes'],'new_shaft_outside_prior_mm3':added,'plate_symmetric_difference_mm3':same_plate,'screw_symmetric_difference_mm3':same_screws,'prior_collision_count':0,'prior_sweep_proof':prior.get('sweep_proof')}
else:
 angles=[0,45,90] if '--quick' in sys.argv else sorted(set(range(0,91,2))|{45});sweep=[]
 for angle in angles:
  angle_poses=transforms(m,throttle_degrees=angle);pose=angle_poses['throttle-shaft'];minimum=float('inf')
  posed_neighbors={oid:local(oid).moved(angle_poses[oid]) for oid in neighbors}
  if 'throttle-return-spring-illustrative' in posed_neighbors:posed_neighbors['throttle-return-spring-illustrative']=spring_candidate.spring(angle)
  for key,q in assembly.items():
   world=q.moved(pose)
   for oid,r in posed_neighbors.items():
    if overlap(bb(world),bb(r)):
     exact+=1;v=vol(world.intersect(r));minimum=min(minimum,world.distance_to(r))
     if v>1e-5:collisions.append({'a':key,'b':oid,'angle':angle,'overlap_mm3':v})
  sweep.append({'angle_deg':angle,'minimum_nearby_distance_mm':minimum if np.isfinite(minimum) else None})
  print('pose',angle,'collisions',len(collisions),flush=True)
contacts={};retention={}
for key,screw in screws.items():
 p=assembly['plate-'+key.split('-')[3]]
 contacts[key]={'head_plate_mm2':contact(screw,p),'thread_shaft_mm2':contact(screw,shaft),'nominal_thread_clearance_mm':screw.distance_to(shaft)}
 shifted=b.Pos(-.125,0,0)*screw
 y=(-27 if key.split('-')[3]=='1' else 27)+(-8 if key.split('-')[4]=='1' else 8)
 coupled={str(sign):vol((b.Pos(-.125,y,0)*b.Rot(sign*90,0,0)*b.Pos(0,-y,0)*screw).intersect(shaft)) for sign in [-1,1]}
 retention[key]={'coupled_quarter_turn_withdrawal_interference_mm3':coupled,'axial_thread_withdrawal_interference_mm3':vol(shifted.intersect(shaft)),'detached_head_plate_contact_mm2':contact(b.Pos(-5,0,0)*screw,p)}
print('contacts',contacts,flush=True)
plate_clamps={}
for index in [1,2]:
 p=assembly[f'plate-{index}'];owned=[v for k,v in screws.items() if f'screw-{index}-' in k]
 plate_clamps[str(index)]={'rear_support_contact_mm2':contact(p,shaft),'forward_escape_interference_mm3':sum(vol((b.Pos(-.25,0,0)*p).intersect(v)) for v in owned),'backward_escape_interference_mm3':vol((b.Pos(.25,0,0)*p).intersect(shaft)),'sideways_escape_interference_mm3':sum(vol((b.Pos(0,1,0)*p).intersect(v)) for v in owned)}
# Remove helical female flanks to prove a smooth clearance bore cannot pass
# the thread-retention test, even with identical nominal screw coordinates.
smooth=shaft
for y in [-35,-19,19,35]:smooth-=b.Pos(0,y,0)*c.cx(c.PARAMS['thread_major_radius']+.02,10)
smooth_control={key:vol((b.Pos(-.125,0,0)*q).intersect(smooth)) for key,q in screws.items()}
preview={'names':np.array(json.dumps(list(assembly)))}
for i,q in enumerate(assembly.values()):
 v,f=q.tessellate(.08,.15);preview[f'v{i}']=np.array([tuple(x) for x in v]);preview[f'f{i}']=np.array(f)
np.savez_compressed(OUT/'preview.npz',**preview)
passed=not collisions and all(e['valid'] and e['solids']==1 and e['watertight'] and e['step_volume_error_mm3']<.001 and e['glb_bounds_error_mm']<.2 for e in exports.values()) and all(v['head_plate_mm2']>1 and 0<v['nominal_thread_clearance_mm']<.05 for v in contacts.values()) and all(v['axial_thread_withdrawal_interference_mm3']>.01 and v['detached_head_plate_contact_mm2']<1e-6 and min(v['coupled_quarter_turn_withdrawal_interference_mm3'].values())<1e-5 for v in retention.values()) and all(all(value>.01 for value in p.values()) for p in plate_clamps.values()) and max(smooth_control.values())<1e-5
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in inputs.items()),'Relevant CAD dependency changed; rerun candidate check.'
r=dict(status='PASS' if passed else 'FAIL',scope='Isolated four-screw educational retention; real Ford count, dimensions, threads, locking and strength unresolved.',manifest_snapshot_sha256=hashlib.sha256(raw).hexdigest(),input_hashes=inputs,output_hashes=output_hashes,parameters=c.PARAMS,shaft_change_outside_four_seat_regions_mm3=shaft_outside_change,plate_pose_preservation='PASS: localY±27 unchanged',exports=exports,broad_phase_occurrences=len(O),exact_neighbor_ids=list(neighbors),exact_sweep_pairs=exact,sweep_proof=sweep_proof,internal_pairs=internal,sweep=sweep,collisions=collisions,contacts=contacts,retention=retention,plate_clamps=plate_clamps,smooth_bore_negative_control=smooth_control)
(ROOT/'inventory/engine/throttle-plate-fasteners-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],json.dumps(collisions[:20]),plate_clamps,smooth_control);raise SystemExit(0 if passed else 1)
