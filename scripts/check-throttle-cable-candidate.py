"""Cheap exact cable-end feasibility; isolated output, no canonical writes."""
from pathlib import Path
import sys,json,itertools,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/throttle-cable-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(15,8));ax=fig.add_subplot(1,2,1,projection='3d')
 for i,name in enumerate(names):
  color='#b8c0c5' if 'compression-spring' in name or 'fixed-guide' in name else '#20272d' if 'socket' in name or 'seat' in name or 'retainer' in name or 'sheath' in name else '#929a9f'
  alpha=.14 if name in ('accelerator-cable-bracket-cable-proposal','throttle-linkage-shield-estimated') else 1
  ax.add_collection3d(Poly3DCollection(a[f'v{i}'][a[f'f{i}']],facecolors=color,shade=True,edgecolor='none',alpha=alpha))
 ax.set(xlim=(387,488),ylim=(87,119),zlim=(459,526),xlabel='Parent X mm',ylabel='Y mm',zlabel='Z mm',title='Revised proportional cable-end candidate\nDimensions/retention still illustrative')
 ax.set_box_aspect((101,32,67));ax.view_init(22,-65)
 ax2=fig.add_subplot(1,2,2);ax2.imshow(plt.imread(ROOT/'cad/engine/generated/cable-reference-study/pioneer-ca8806-detail.jpg'));ax2.set_xlim(0,1500);ax2.set_ylim(1120,800);ax2.axis('off');ax2.set_title('Pioneer CA-8806 replacement comparison\nNo dimensional scale or verified owner-installed identity')
 fig.tight_layout();fig.subplots_adjust(top=.87);fig.savefig(OUT/'feasibility-reference-comparison.png',dpi=160);raise SystemExit

import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_cable_candidate as c
from assembly_math import transforms
from cad_metrics import solid_volume,support_bounds
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};cache={};inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(c.__file__),ROOT/'reference/engine/throttle-cable-review.json']}
def local(oid):
 did=O[oid]['definition']
 if did not in cache:
  p=ROOT/D[did]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();cache[did]=b.import_step(p)
 return cache[did]
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def bb(q):a=q.bounding_box();return np.array([tuple(a.min),tuple(a.max)])
def overlap(a,z):return bool(np.all(a[0]<z[1]+1e-6) and np.all(z[0]<a[1]+1e-6))
stationary=c.stationary();proposed_bracket=c.bracket_proposal(local('accelerator-cable-bracket'));rows=[];hits=[];invalid=[];OUT.mkdir(parents=True,exist_ok=True)
# All current occurrences enter a conservative parent-frame mesh broad phase.
poses0=transforms(m);parent0=poses0['throttle-housing'];bounds_cache={};neighbor_ids=[]
region_corners=np.array([tuple(b.Vertex(*v).moved(parent0).center()) for v in itertools.product([377,491],[60,126],[450,528])]);region=np.array([region_corners.min(0),region_corners.max(0)])
for oid,o in O.items():
 if oid=='accelerator-cable-bracket':continue
 did=o['definition']
 if did not in bounds_cache:
  mesh=trimesh.load(ROOT/D[did]['glb'].lstrip('/'),force='mesh');vv=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bounds_cache[did]=np.array([vv.min(0),vv.max(0)])
 vv=np.array([tuple(b.Vertex(*v).moved(poses0[oid]).center()) for v in itertools.product(*zip(*bounds_cache[did]))]);bounds=np.array([vv.min(0),vv.max(0)])
 if overlap(bounds,region) or o['parent']=='throttle-moving':neighbor_ids.append(oid)
exact_pairs=0
angles=sorted(set(range(0,91,2))|{45}) if '--full' in sys.argv else [0,45,90]
for angle in angles:
 moving,meta=c.moving(angle);parts=stationary|moving|{'accelerator-cable-bracket-cable-proposal':proposed_bracket}
 if angle==0:
  preview_parts=parts|{'throttle-linkage-shield-estimated':local('throttle-linkage-shield-estimated')};preview={'names':np.array(json.dumps(list(preview_parts)))}
  for i,q in enumerate(preview_parts.values()):
   v,f=q.tessellate(.025,.12);preview[f'v{i}']=np.array([tuple(x) for x in v]);preview[f'f{i}']=np.array(f)
  np.savez_compressed(OUT/'preview.npz',**preview)
 poses=transforms(m,throttle_degrees=angle);parent=poses['throttle-housing'];parts={k:v.moved(parent) for k,v in parts.items()};neighbors={oid:local(oid).moved(poses[oid]) for oid in neighbor_ids}
 import throttle_return_spring_candidate as spring
 neighbors['throttle-return-spring-illustrative']=spring.spring(angle).moved(parent)
 for k,q in parts.items():
  assert np.all(bb(q)[0]>=region[0]) and np.all(bb(q)[1]<=region[1]),'Broad envelope missed candidate geometry'
  if not q.is_valid or len(q.solids())!=1:invalid.append((angle,k,q.is_valid,len(q.solids())))
  for oid,r in neighbors.items():
   if overlap(bb(q),bb(r)):
    exact_pairs+=1
    try:v=vol(q.intersect(r))
    except ValueError as error:hits.append(dict(angle=angle,a=k,b=oid,measurement_error=str(error)));continue
    if v>1e-5:hits.append(dict(angle=angle,a=k,b=oid,overlap_mm3=v))
 for (k,q),(oid,r) in itertools.combinations(parts.items(),2):
  if overlap(bb(q),bb(r)):
   exact_pairs+=1
   try:v=vol(q.intersect(r))
   except ValueError as error:hits.append(dict(angle=angle,a=k,b=oid,measurement_error=str(error)));continue
   if v>1e-5:hits.append(dict(angle=angle,a=k,b=oid,overlap_mm3=v))
 rows.append(meta);print(angle,meta,'hits',hits,'invalid',invalid,flush=True)
# Physical capture controls in the actual proposed parent-local stack.
def area(q,r):
 total=0.
 for f in q.faces():
  for g in r.faces():
   if overlap(bb(f),bb(g)):
    x=f.intersect(g)
    if x:total+=x.area if hasattr(x,'area') else sum(v.area for v in x)
 return total
neutral,meta=c.moving(0);ball,u,frame,fixed,L=c.state(0);retainer=stationary['throttle-cable-snap-retainer-illustrative'];sheath=stationary['throttle-cable-sheath-stub-illustrative'];socket=neutral['throttle-cable-socket-illustrative'];cup=neutral['throttle-cable-swivel-seat-illustrative'];core=neutral['throttle-cable-core-illustrative'];guide=neutral['throttle-cable-fixed-guide-illustrative'];coil=neutral['throttle-cable-compression-spring-illustrative']
# Existing ball is local to throttle-moving; express it in parent coordinates.
actual_ball=local('throttle-cable-ball-stud-estimated').moved(poses0['throttle-cable-ball-stud-estimated']).moved(parent0.inverse())
contacts=dict(retainer_bracket_mm2=area(retainer,proposed_bracket),sheath_retainer_mm2=area(sheath,retainer),guide_seat_mm2=area(guide,cup),core_terminal_mm2=area(core,socket),spring_moving_seat_mm2=area(coil,socket),spring_fixed_seat_mm2=area(coil,cup))
controls=dict(retainer_positive_x_capture_mm3=vol(retainer.moved(b.Pos(.5,0,0)).intersect(proposed_bracket)),retainer_negative_x_capture_mm3=vol(retainer.moved(b.Pos(-.5,0,0)).intersect(proposed_bracket)),sheath_positive_x_capture_mm3=vol(sheath.moved(b.Pos(.25,0,0)).intersect(retainer)),sheath_negative_x_capture_mm3=vol(sheath.moved(b.Pos(-.25,0,0)).intersect(retainer)),core_terminal_capture_mm3=vol(core.moved(b.Pos(*(u*.25))).intersect(socket)),guide_positive_capture_mm3=vol(guide.moved(b.Pos(*(u*.25))).intersect(cup)),guide_negative_capture_mm3=vol(guide.moved(b.Pos(*(-u*.25))).intersect(cup)),socket_ball_capture_mm3=vol(socket.moved(b.Pos(*(u*.25))).intersect(actual_ball)),swivel_ball_capture_mm3=vol(cup.moved(b.Pos(*(-u*.5))).intersect(retainer)),detached_retainer_contact_mm2=area(retainer.moved(b.Pos(12,0,0)),proposed_bracket),detached_socket_ball_distance_mm=socket.moved(b.Pos(0,15,0)).distance_to(actual_ball))
protected=b.Pos(394,95,490)*b.Box(33,70,100);old=local('accelerator-cable-bracket');protected_change=sum(vol(s.intersect(protected)) for diff in [old.cut(proposed_bracket),proposed_bracket.cut(old)] for s in diff.solids())
exports={};output_hashes={}
for key,q in (stationary|neutral|{'accelerator-cable-bracket-cable-proposal':proposed_bracket}).items():
 sp=OUT/(key+'.step');gp=OUT/(key+'.glb');b.export_step(q,sp);v,f=q.tessellate(.025,.12);vv=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(vv[:,[0,2,1]]*[1,1,-1]/1000,np.array(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();mesh.export(gp);loaded=trimesh.load(gp,force='mesh');vertices=np.asarray(loaded.vertices)[:,[0,2,1]]*[1,-1,1]*1000
 raw_error=float(np.max(np.abs(np.array([vertices.min(0),vertices.max(0)])-bb(q))))
 bounds=bb(q);method='OCC bounding box'
 if raw_error>=.2:
  box=support_bounds(q);bounds=np.array([tuple(box.min),tuple(box.max)]);method='Exact planar support distances; multiple offsets agree'
 exports[key]=dict(raw_occ_bounds_error_mm=raw_error,bounds_method=method,valid=q.is_valid,solids=len(q.solids()),watertight=mesh.is_watertight,glb_bounds_error_mm=float(np.max(np.abs(np.array([vertices.min(0),vertices.max(0)])-bounds))),step_volume_error_mm3=abs(vol(q)-vol(b.import_step(sp))))
 for path in [sp,gp]:output_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
lengths=[r['spring_cad_centerline_length_mm'] for r in rows];length_delta=max(lengths)-min(lengths);smallest_pitch=min(c.state(a)[4]/c.PARAMS['coil_turns'] for a in range(91));return_projection=[float(np.dot(-c.state(a)[1],np.array([24*np.cos(np.radians(a)),0,-24*np.sin(np.radians(a))]))) for a in range(91)]
# Minimum nonlocal separation on each circular helix, solving the adjacent-turn
# distance stationary point; exclude the contiguous local strand neighborhood.
spacing=[]
for angle in range(91):
 L=c.state(angle)[4];N=c.PARAMS['coil_turns'];r=np.sqrt((2*np.pi*N*c.PARAMS['coil_radius_neutral'])**2+c.state(0)[4]**2-L**2)/(2*np.pi*N);h=L/(2*np.pi*N)
 lo,hi=1.5*np.pi,2*np.pi
 for _ in range(70):
  mid=(lo+hi)/2
  if r*r*np.sin(mid)+h*h*mid<0:lo=mid
  else:hi=mid
 d=(lo+hi)/2;separation=np.sqrt(2*r*r*(1-np.cos(d))+h*h*d*d)
 spacing.append(dict(angle_deg=angle,adjacent_turn_surface_gap_mm=float(separation-2*c.PARAMS['wire_radius'])))
control_pass=all(v>.0001 for k,v in controls.items() if 'capture' in k) and controls['detached_retainer_contact_mm2']<1e-6 and controls['detached_socket_ball_distance_mm']>1
passed=min(v['adjacent_turn_surface_gap_mm'] for v in spacing)>0 and not hits and not invalid and control_pass and min(contacts.values())>.0001 and protected_change<1e-5 and length_delta<1e-5 and smallest_pitch>2*c.PARAMS['wire_radius'] and max(return_projection)<0 and all(v['valid'] and v['solids']==1 and v['watertight'] and v['glb_bounds_error_mm']<.2 and v['step_volume_error_mm3']<.001 for v in exports.values())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in inputs.items()),'Relevant input changed during check'
r=dict(status='PASS' if passed else 'FAIL',scope='Isolated photo-proportioned educational engine-end candidate; source supports topology, dimensions/internal retention/rate remain inferred',full_sweep='--full' in sys.argv,manifest_sha256=hashlib.sha256((ROOT/'inventory/engine/full-assembly.json').read_bytes()).hexdigest(),exact_collision_pair_evaluations=exact_pairs,integer_pose_helix_spacing=spacing,broad_phase_occurrences=len(O),exact_neighbor_ids=neighbor_ids,input_hashes=inputs,output_hashes=output_hashes,parameters=c.PARAMS,poses=rows,collisions=hits,invalid=invalid,contacts=contacts,controls=controls,exports=exports,protected_anchor_region_symmetric_difference_mm3=protected_change,spring_exact_centerline_length_variation_mm=length_delta,minimum_integer_pose_pitch_mm=smallest_pitch,maximum_closing_projection_mm=max(return_projection),core_material_transport='Visible segment shortens as core is drawn into fixed sheath; its open cut boundary is not a material endpoint. No stretch or full firewall route claimed.',bracket_revision=dict(exit_delta_mm=[5,2,0],new_exit_mm=c.EXIT.tolist(),mount_shield_and_shaft_spring_anchors_preserved=True))
(ROOT/'inventory/engine/throttle-cable-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],contacts,controls,exports,flush=True);raise SystemExit(0 if passed else 1)
