"""Exact sampled check of a coordinated, estimated linkage interface revision."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/throttle-linkage-candidate'
if '--render' in sys.argv:
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(13,6))
 for idx,(el,az) in enumerate([(25,125),(15,-60)],1):
  ax=fig.add_subplot(1,2,idx,projection='3d')
  for n,key in enumerate(names):
   color='#be994d' if 'lever' in key else '#3578ad' if 'ball' in key else '#759b72' if 'bracket' in key else '#999999'
   alpha=.18 if key=='throttle-housing' else .45 if key.endswith('-90') else 1
   ax.add_collection3d(Poly3DCollection(a[f'v{n}'][a[f'f{n}']],facecolor=color,alpha=alpha,edgecolor='none'))
  ax.set(xlim=(355,470),ylim=(-40,125),zlim=(450,530),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((115,165,80));ax.view_init(el,az)
 fig.suptitle('Estimated keyed linkage + offset bracket candidate; translucent parts show90° pose');fig.tight_layout();fig.savefig(OUT/'candidate-context.png',dpi=150)
 fig=plt.figure(figsize=(9,7));ax=fig.add_subplot(111,projection='3d')
 for n,key in enumerate(names):
  if key.endswith('-0') and ('lever-' in key or 'ball-' in key):
   ax.add_collection3d(Poly3DCollection(a[f'v{n}'][a[f'f{n}']],facecolor='#be994d' if 'lever-estimated' in key else '#3578ad',edgecolor='#333333',linewidth=.12))
 ax.set(xlim=(386,402),ylim=(87,100),zlim=(482,520),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((16,13,38));ax.view_init(20,-60)
 fig.suptitle('Estimated lever, outward ball and retaining pin; D-shaped hub bore visible');fig.tight_layout();fig.savefig(OUT/'candidate-linkage-detail.png',dpi=150)
 raise SystemExit
import build123d as b
import trimesh
sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_linkage_candidate as c
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';raw=M.read_bytes();m=json.loads(raw);D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};OUT.mkdir(exist_ok=True)
inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [M,Path(__file__),Path(c.__file__),ROOT/'reference/engine/throttle-linkage-review.json',ROOT/'cad/engine/pilot/throttle-bracket/candidate.py']}
cache={}
def local(oid):
 did=O[oid]['definition']
 if did not in cache:
  p=ROOT/D[did]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();cache[did]=b.import_step(p)
 return cache[did]
def vol(q):return sum(solid_volume(s,'adaptive') for s in q.solids()) if q else 0.
def area(a,c):
 return sum(q.area if hasattr(q,'area') else sum(i.area for i in q) for f in a.faces() for g in c.faces() if (q:=f.intersect(g)))
def bounds(q):
 z=q.bounding_box();return np.array([tuple(z.min),tuple(z.max)])
def broad(a,c):
 x,y=bounds(a),bounds(c);return bool(np.all(x[0]<=y[1]+1e-6) and np.all(y[0]<=x[1]+1e-6))
parts=c.parts(local('throttle-shaft'));bracket=c.bracket_proposal();export_checks={};outputs={}
for key,obj in {**parts,'accelerator-bracket-offset-estimated':bracket}.items():
 assert obj.is_valid and len(obj.solids())==1,key
 p=OUT/(key+'.step');b.export_step(obj,p);reopened=b.import_step(p)
 v,f=obj.tessellate(.12,.15);v=np.array([tuple(vv) for vv in v]);f=np.array(f)
 mesh=trimesh.Trimesh(vertices=v[:,[0,2,1]]*np.array([1,1,-1])/1000,faces=f)
 mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices()
 q=OUT/(key+'.glb');mesh.export(q);reloaded=trimesh.load(q,force='mesh');vv=np.asarray(reloaded.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
 error=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bounds(obj))))
 assert error<.2 and mesh.is_watertight and abs(vol(reopened)-vol(obj))<.001,(key,error,mesh.is_watertight)
 export_checks[key]={'valid':True,'solids':1,'mesh_watertight':True,'glb_bounds_error_mm':error,'volume_mm3':vol(obj)}
 for file in [p,q]:outputs[str(file.relative_to(ROOT))]=hashlib.sha256(file.read_bytes()).hexdigest()
lever=parts['throttle-lever-estimated'];ball=parts['throttle-cable-ball-stud-estimated'];shaft=parts['throttle-shaft-keyed-estimated'];pin=parts['throttle-lever-retaining-pin-estimated']
contact=area(lever,shaft);ballcontact=area(lever,ball);negative=area(b.Pos(0,10,0)*lever,shaft)
assert contact>1 and ballcontact>1 and negative<1e-6
assert lever.distance_to(pin)<1e-6
assert area(shaft,pin)>1
# Positive and negative axial moves are physically blocked by pin/shoulder.
axial_positive=vol((b.Pos(0,.25,0)*lever).intersect(pin));axial_negative=vol((b.Pos(0,-.25,0)*lever).intersect(shaft))
assert axial_positive>.1 and axial_negative>.1,(axial_positive,axial_negative)
# A small relative rotation must meet the noncircular D-section shaft.
torque_negative=vol((b.Rot(0,5,0)*lever).intersect(shaft));assert torque_negative>.1
neighbors=[oid for oid in O if oid.startswith(('throttle-','tps-','iac-')) and oid!='throttle-shaft' or oid=='efi-upper-intake']
collisions=[];cable_checks=[];original_bracket_conflicts=[];exact=0;pose_checks=[];preview={}
for angle in range(0,91,2):
 poses=transforms(m,throttle_degrees=angle);pose=poses['throttle-shaft'];candidates={key:obj.moved(pose) for key,obj in parts.items()}
 # Lever initially points+Z. Pull toward fixed bracket round-hole datum must
 # produce opening torque at every sampled angle (no over-center workaround).
 theta=np.radians(angle);ballcenter=np.array([394+24*np.sin(theta),95,490+24*np.cos(theta)])
 tangent=np.array([np.cos(theta),0,-np.sin(theta)]);pull=np.array([465,110,467])-ballcenter
 opening_projection=float(np.dot(pull,tangent));assert opening_projection>0
 cable=b.Plane(origin=tuple(ballcenter),z_dir=tuple(pull))*b.Cylinder(c.PARAMS['cable_envelope_radius'],float(np.linalg.norm(pull)),align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 cable_overlap=vol(cable.intersect(bracket));cable_checks.append({'angle_deg':angle,'bracket_overlap_mm3':cable_overlap})
 if cable_overlap>1e-6:collisions.append({'candidate':'direct-cable-envelope','neighbor':'proposed-bracket','angle_deg':angle,'overlap_mm3':cable_overlap})
 for key,obj in candidates.items():
  for oid in neighbors+['proposed-bracket']:
   n=bracket if oid=='proposed-bracket' else local(oid).moved(poses[oid])
   if not broad(obj,n):continue
   exact+=1;v=vol(obj.intersect(n))
   if v>.1:collisions.append({'candidate':key,'neighbor':oid,'angle_deg':angle,'overlap_mm3':v})
  old=local('accelerator-cable-bracket').moved(poses['accelerator-cable-bracket'])
  if broad(obj,old):
   v=vol(obj.intersect(old))
   if v>.1:original_bracket_conflicts.append({'part':key,'angle_deg':angle,'overlap_mm3':v})
 for i,key in enumerate(candidates):
  for other in list(candidates)[i+1:]:
   a,d=candidates[key],candidates[other]
   if broad(a,d):
    v=vol(a.intersect(d));exact+=1
    if v>.1:collisions.append({'candidate':key,'neighbor':other,'angle_deg':angle,'overlap_mm3':v})
 pose_checks.append({'angle_deg':angle,'cable_opening_projection_mm':opening_projection})
 if angle in [0,90]:
  for key,obj in candidates.items():preview[f'{key}-{angle}']=obj
poses=transforms(m);mount_contacts={}
for oid in ['throttle-housing','throttle-nut-3','throttle-nut-4']:
 n=local(oid).moved(poses[oid]);mount_contacts[oid]=area(bracket,n);assert mount_contacts[oid]>1
# Revised bracket itself against explicit current local neighbors.
for oid in neighbors:
 n=local(oid).moved(poses[oid])
 if broad(bracket,n):
  v=vol(bracket.intersect(n));exact+=1
  if v>.1:collisions.append({'candidate':'proposed-bracket','neighbor':oid,'angle_deg':0,'overlap_mm3':v})
preview['throttle-housing']=local('throttle-housing').moved(poses['throttle-housing']);preview['proposed-bracket']=bracket
arrays={};names=[]
for key,obj in preview.items():
 v,f=obj.tessellate(.3,.3);idx=len(names);names.append(key);arrays[f'v{idx}']=np.array([tuple(q) for q in v]);arrays[f'f{idx}']=np.array(f)
arrays['names']=np.array(json.dumps(names));np.savez_compressed(OUT/'preview.npz',**arrays)
assert raw==M.read_bytes() and all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in inputs.items())
r={'status':'PASS' if not collisions else 'FAIL','readiness':'candidate; requires coordinated shaft/bracket replacement and independent integration review','scope':'Estimated physical D-key, shoulder and transverse pin; sampled0–90° against current throttle/IAC/TPS/hardware/intake and revised bracket. No real strength/spring/stop calibration claims.','input_hashes':inputs,'output_hashes':outputs,'parameters':c.PARAMS,'export_checks':export_checks,'shaft_hub_contact_mm2':contact,'ball_stud_seat_contact_mm2':ballcontact,'pin_lever_distance_mm':lever.distance_to(pin),'shaft_pin_contact_mm2':area(shaft,pin),'negative_controls':{'disconnected_anchor_contact_mm2':negative,'relative_rotation5deg_collision_mm3':torque_negative,'axial_positive025mm_blocked_mm3':axial_positive,'axial_negative025mm_blocked_mm3':axial_negative},'pose_checks':pose_checks,'direct_cable_envelope_checks':cable_checks,'neighbors':neighbors,'exact_pair_count':exact,'collisions':collisions,'original_bracket_conflicts':original_bracket_conflicts,'revised_bracket_contact_mm2':mount_contacts,'integration':{'moving_parent':'throttle-moving','position_cad_mm':[0,0,0],'rotation_cad_deg':[0,0,0],'bracket_parent':'throttle-assembly','bracket_web_delta_y_mm':11.},'limitations':c.GAPS}
(ROOT/'inventory/engine/throttle-linkage-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],exact,'pairs',len(collisions),'collisions; old bracket conflicts',len(original_bracket_conflicts));print(json.dumps(collisions[:10]));assert not collisions
