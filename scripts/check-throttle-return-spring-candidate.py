"""Reproduce isolated illustrative one-spring mechanism; never edits assembly."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/throttle-return-spring-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');fig=plt.figure(figsize=(15,5))
 for j,angle in enumerate([0,45,90],1):
  ax=fig.add_subplot(1,3,j,projection='3d')
  names=json.loads(str(a[f'names{angle}']))
  for i,k in enumerate(names):
   color='#cf8233' if k=='spring' else '#718d73' if 'bracket' in k else '#8b97a5'
   alpha=.12 if 'shield' in k else .25 if 'bracket' in k else 1
   ax.add_collection3d(Poly3DCollection(a[f'v{angle}_{i}'][a[f'f{angle}_{i}']],facecolor=color,alpha=alpha,edgecolor='none'))
  ax.set(xlim=(379,425),ylim=(83,110),zlim=(478,523),title=f'{angle}° — illustrative ONE spring',xlabel='X',ylabel='Y',zlabel='Z');ax.set_box_aspect((46,27,45));ax.view_init(25,-55)
 fig.subplots_adjust(top=.80,bottom=.1,left=.03,right=.97,wspace=.12);fig.savefig(OUT/'candidate-context.png',dpi=160);raise SystemExit
import build123d as b
import trimesh
sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_return_spring_candidate as s
import throttle_linkage_candidate as l
import throttle_shield_candidate as sh
if '--paths' in sys.argv:
 from datetime import datetime, timezone
 path=ROOT/'viewer/throttle-return-spring-paths.json';frames=[];count=1601
 for angle in range(91):
  radius=s.radius_at(angle);wire=s.centerline(angle,radius)
  pts=np.array([tuple(wire.position_at(t)) for t in np.linspace(0,1,count)])
  quantized=np.round(pts,5);poly=float(np.linalg.norm(np.diff(quantized,axis=0),axis=1).sum())
  theta=np.radians(angle);fixed_point=np.array([389.,104.,503.]);moving_point=np.array([394+18*np.sin(theta),90,490+18*np.cos(theta)])
  def gap_to_segments(p):
   u=quantized[1:]-quantized[:-1];t=np.clip(np.sum((p-quantized[:-1])*u,axis=1)/np.sum(u*u,axis=1),0,1)
   return float(np.linalg.norm(quantized[:-1]+t[:,None]*u-p,axis=1).min())
  frames.append(dict(angle_deg=angle,radius_mm=radius,cad_length_mm=wire.length,polyline_length_mm=poly,fixed_anchor_polyline_gap_mm=gap_to_segments(fixed_point),moving_anchor_polyline_gap_mm=gap_to_segments(moving_point),coil_turn_surface_gap_mm=6/(s.PARAMS['turns']+(angle-s.PARAMS['fixed_angle_deg'])/360)-2*s.PARAMS['wire_radius'],points_cad_mm=quantized.tolist()))
  if angle%15==0:print('path',angle,flush=True)
 payload=dict(schema='illustrative-throttle-spring-paths-v1',scope='ONE illustrative spring, not Ford count or calibrated spring mechanics.',coordinate_frame='world CAD millimeters; browser conversion[X,Z,-Y]/1000',wire_radius_mm=s.PARAMS['wire_radius'],samples_per_frame=count,input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(s.__file__),Path(__file__)]},frames=frames)
 payload['validation']=dict(max_length_loss_mm=max(abs(f['cad_length_mm']-f['polyline_length_mm']) for f in frames),max_anchor_polyline_gap_mm=max(max(f['fixed_anchor_polyline_gap_mm'],f['moving_anchor_polyline_gap_mm']) for f in frames),minimum_turn_surface_gap_mm=min(f['coil_turn_surface_gap_mm'] for f in frames),fixed_endpoint_range_mm=float(np.ptp(np.array([f['points_cad_mm'][0] for f in frames]),axis=0).max()))
 assert payload['validation']['max_length_loss_mm']<.05 and payload['validation']['max_anchor_polyline_gap_mm']<.001 and payload['validation']['minimum_turn_surface_gap_mm']>0 and payload['validation']['fixed_endpoint_range_mm']<1e-5
 path.write_text(json.dumps(payload,separators=(',',':'))+'\n');print(json.dumps(payload['validation']),hashlib.sha256(path.read_bytes()).hexdigest());raise SystemExit
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';raw=M.read_bytes();m=json.loads(raw);D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m)
inputs={}
def track(p):inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return p
for p in [M,Path(__file__),Path(s.__file__),Path(l.__file__),Path(sh.__file__),ROOT/'cad/engine/pilot/throttle-bracket/candidate.py',ROOT/'reference/engine/throttle-return-spring-review.json']:track(p)
fixed,moving=s.seats(b.import_step(track(ROOT/'cad/engine/generated/throttle-shaft.step')))
bracket=fixed['accelerator-bracket-spring-seat-estimated'];lever=moving['throttle-lever-spring-seat-estimated']
def vol(q):return sum(abs(solid_volume(v,'adaptive')) for v in q.solids()) if q else 0.
def bb(q):z=q.bounding_box();return np.array([tuple(z.min),tuple(z.max)])
def broad(q,r):a,c=bb(q),bb(r);return np.all(a[0]<=c[1]+1e-6) and np.all(c[0]<=a[1]+1e-6)
# Nearby unchanged housing, TPS/IAC and fastening geometry, actual manifest poses.
neighbor_ids=[k for k in O if k.startswith(('throttle-','tps-','iac-')) and not any(x in k for x in ['lever','ball-stud','shaft','shield','spring'])]
static={k:b.import_step(track(ROOT/D[O[k]['definition']]['step'].lstrip('/'))).moved(poses[k]) for k in neighbor_ids}
OUT.mkdir(exist_ok=True);rows=[];collisions=[];preview={};exported={};exact=0
angles=[0,45,90] if '--quick' in sys.argv else sorted(set(range(0,91,10))|{45})
for angle in angles:
 spring=s.spring(angle);pose=b.Pos(394,25,490)*b.Rot(0,angle,0)
 targets={**static,**fixed,**{k:v.moved(pose) for k,v in moving.items()}}
 theta=np.radians(angle);ball=np.array([394+24*np.sin(theta),95,490+24*np.cos(theta)]);delta=np.array([465,110,467])-ball
 targets['direct-cable-envelope']=b.Plane(origin=tuple(ball),z_dir=tuple(delta))*b.Cylinder(1,float(np.linalg.norm(delta)),align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 gaps={}
 for key,target in targets.items():
  gaps[key]=spring.distance_to(target)
  if broad(spring,target):
   exact+=1;v=vol(spring.intersect(target))
   if v>1e-5:collisions.append(dict(angle_deg=angle,part=key,overlap_mm3=v))
 pts=s.path_points(angle,s.radius_at(angle));wire=s.centerline(angle,s.radius_at(angle))
 expected_fixed=np.array([389.,104.,503.]);expected_moving=np.array([394+18*np.sin(theta),90,490+18*np.cos(theta)])
 pitch=6/(s.PARAMS['turns']+(angle-s.PARAMS['fixed_angle_deg'])/360)
 row=dict(coil_turn_surface_gap_mm=pitch-2*s.PARAMS['wire_radius'],tube_volume_error_mm3=abs(vol(spring)-np.pi*s.PARAMS['wire_radius']**2*wire.length),angle_deg=angle,valid=spring.is_valid,solid_count=len(spring.solids()),radius_mm=s.radius_at(angle),polygon_centerline_length_mm=s.length(pts),analytical_centerline_length_mm=s.analytical_length(angle,s.radius_at(angle)),wire_volume_mm3=vol(spring),fixed_anchor_error_mm=wire.distance_to(b.Vertex(*expected_fixed)),moving_anchor_error_mm=wire.distance_to(b.Vertex(*expected_moving)),minimum_clearance_mm=min(gaps.values()),clearances_mm=gaps)
 rows.append(row);print(angle,row['valid'],row['solid_count'],row['minimum_clearance_mm'],flush=True)
 if angle in [0,45,90]:
  sp=OUT/f'spring-{angle}.step';b.export_step(spring,sp)
  v,f=spring.tessellate(.06,.12);v=np.array([tuple(t) for t in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,np.array(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/f'spring-{angle}.glb';mesh.export(gp)
  reopened=trimesh.load(gp,force='mesh');vv=np.array(reopened.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
  exported[str(angle)]={'watertight':mesh.is_watertight,'bounds_error_mm':float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bb(spring)))),'step_volume_error_mm3':abs(vol(b.import_step(sp))-vol(spring))}
  objs={'spring':spring,**fixed,**{k:v.moved(pose) for k,v in moving.items() if 'shaft' not in k}}
  preview[f'names{angle}']=np.array(json.dumps(list(objs)))
  for i,obj in enumerate(objs.values()):
   v,f=obj.tessellate(.2,.2);preview[f'v{angle}_{i}']=np.array([tuple(x) for x in v]);preview[f'f{angle}_{i}']=np.array(f)
np.savez_compressed(OUT/'preview.npz',**preview)
# Both straight tangs pass through real plate holes, with hooks wider than the
# hole and on the far side. Translation must cross retaining material.
closed=s.spring(0)
retention={'moving_hook_axial_withdrawal_mm3':vol((b.Pos(0,2,0)*closed).intersect(lever.moved(b.Pos(394,25,490)))),'fixed_hook_axial_withdrawal_mm3':vol((b.Pos(0,-3,0)*closed).intersect(bracket))}
a=np.radians(45);p=np.array([389.,104.,503.]);relative=p-np.array([394,25,490]);rot=np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
wrong_error=float(np.linalg.norm(rot@relative-relative))
negative={'rigidly_rotated_fixed_anchor_at45_error_mm':wrong_error,'rejected_by_anchor_tolerance':wrong_error>.05}
for name,obj in [('bracket-spring-seat',bracket),('lever-spring-seat',lever)]:b.export_step(obj,OUT/(name+'.step'))
lengths=[r['analytical_centerline_length_mm'] for r in rows];volumes=[r['wire_volume_mm3'] for r in rows]
return_direction=all(rows[i+1]['radius_mm']<rows[i]['radius_mm'] for i in range(len(rows)-1))
self_clearance=all(r['coil_turn_surface_gap_mm']>0 and r['tube_volume_error_mm3']<.001 for r in rows)
passed=return_direction and self_clearance and not collisions and all(r['valid'] and r['solid_count']==1 and max(r['fixed_anchor_error_mm'],r['moving_anchor_error_mm'])<1e-5 for r in rows) and max(lengths)-min(lengths)<.01 and all(v>.01 for v in retention.values()) and negative['rejected_by_anchor_tolerance'] and all(e['watertight'] and e['bounds_error_mm']<.2 and e['step_volume_error_mm3']<.001 for e in exported.values())
outputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.suffix in ['.step','.glb','.npz']}
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in inputs.items() if p!='inventory/engine/full-assembly.json')
report=dict(manifest_unchanged_during_check=raw==M.read_bytes(),output_hashes=outputs,winds_tighter_with_opening=return_direction,coil_spacing_and_constant_section_volume=self_clearance,status='PASS' if passed else 'FAIL',readiness='illustrative isolated candidate only',scope_decision='Integration lead explicitly authorized ONE educational torsion spring; actual Ford count, construction and anchors remain unresolved. Separate cable-end compression spring excluded.',input_hashes=inputs,parameters=s.PARAMS,samples=rows,exact_pairs=exact,collisions=collisions,exports=exported,retention=retention,negative_control=negative,length_range_mm=max(lengths)-min(lengths),volume_relative_range=(max(volumes)-min(volumes))/volumes[0],limitations=['Sampled dynamics only; not continuous collision certification.','Tangent-continuous geometric bends; bending strain, stress and material response unknown.','No force, preload, rate, friction-return or production accuracy claim.','Proposed holes and wire are illustrative; bracket and lever strength unassessed.'])
(ROOT/'inventory/engine/throttle-return-spring-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],collisions,retention,exported)

raise SystemExit(0 if passed else 1)
