"""Local exact CAD checks for estimated hood, pushpin and bracket-hole proposal."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/throttle-shield-candidate'
if '--render' in sys.argv:
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(13,6))
 for idx,(el,az) in enumerate([(25,-50),(20,130)],1):
  ax=fig.add_subplot(1,2,idx,projection='3d')
  for i,key in enumerate(names):
   color='#55667a' if 'shield-estimated' in key else '#c39944' if 'pushpin' in key else '#6b9270' if 'bracket' in key else '#888888'
   alpha=.4 if 'shield-estimated' in key else .2 if 'housing' in key else 1.
   ax.add_collection3d(Poly3DCollection(a[f'v{i}'][a[f'f{i}']],facecolor=color,alpha=alpha,edgecolor='none'))
  ax.set(xlim=(375,470),ylim=(70,126),zlim=(450,530),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((95,56,80));ax.view_init(el,az)
 fig.suptitle('Estimated splash hood and pushpin on proposed bracket; translucent hood exposes linkage');fig.tight_layout();fig.savefig(OUT/'candidate-context.png',dpi=150);raise SystemExit
import build123d as b
import trimesh
sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_shield_candidate as s
import throttle_linkage_candidate as l
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';raw=M.read_bytes();m=json.loads(raw);D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m)
inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [M,Path(__file__),Path(s.__file__),Path(l.__file__),ROOT/'cad/engine/pilot/throttle-bracket/candidate.py',ROOT/'reference/engine/throttle-linkage-review.json']}
cache={}
def local(oid):
 did=O[oid]['definition']
 if did not in cache:
  p=ROOT/D[did]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();cache[did]=b.import_step(p)
 return cache[did]
def volume(q):return sum(solid_volume(v,'adaptive') for v in q.solids()) if q else 0.
def bounds(q):
 bb=q.bounding_box();return np.array([tuple(bb.min),tuple(bb.max)])
def broad(a,c):
 x,y=bounds(a),bounds(c);return bool(np.all(x[0]<=y[1]+1e-6) and np.all(y[0]<=x[1]+1e-6))
def contact(a,c):
 return sum(q.area if hasattr(q,'area') else sum(v.area for v in q) for fa in a.faces() for fc in c.faces() if (q:=fa.intersect(fc)))
parts=s.parts();shield=parts['throttle-linkage-shield-estimated'];pin=parts['throttle-shield-pushpin-estimated'];bracket=parts['accelerator-bracket-shield-hole-estimated'];OUT.mkdir(exist_ok=True)
# Always construct linkage from the unchanged original shaft definition. Root
# may install a keyed replacement concurrently; do not extend it a second time.
source=ROOT/'cad/engine/generated/throttle-shaft.step';inputs[str(source.relative_to(ROOT))]=hashlib.sha256(source.read_bytes()).hexdigest();moving=l.parts(b.import_step(source))
export_checks={};outputs={}
for key,obj in parts.items():
 assert obj.is_valid and len(obj.solids())==1,(key,obj.is_valid,len(obj.solids()))
 step=OUT/(key+'.step');b.export_step(obj,step);reopened=b.import_step(step)
 v,f=obj.tessellate(.12,.15);v=np.array([tuple(t) for t in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,np.array(f))
 mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices()
 glb=OUT/(key+'.glb');mesh.export(glb);r=trimesh.load(glb,force='mesh');vv=np.asarray(r.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
 err=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bounds(obj))))
 assert err<.2 and mesh.is_watertight and abs(volume(reopened)-volume(obj))<.001
 export_checks[key]={'valid':True,'solids':1,'mesh_watertight':True,'glb_bounds_error_mm':err,'volume_mm3':volume(obj)}
 for p in [step,glb]:outputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
contacts={'shield_bracket':contact(shield,bracket),'pin_head_shield':contact(pin,shield),'pin_barb_bracket':contact(pin,bracket)}
assert all(v>1 for v in contacts.values()),contacts
for a,c in [(shield,bracket),(pin,shield),(pin,bracket)]:assert volume(a.intersect(c))<=.1
negative={'head_shield_contact_mm2':contact(b.Pos(0,8,0)*pin,shield),'barb_bracket_contact_mm2':contact(b.Pos(0,8,0)*pin,bracket)}
assert max(negative.values())<1e-6
# Withdrawn pin must cross material behind the bracket; expanded barbs retain.
withdrawal=volume((b.Pos(0,.25,0)*pin).intersect(bracket));assert withdrawal>.1,withdrawal
neighbors=[oid for oid in O if (oid.startswith(('throttle-','tps-','iac-')) and oid not in ['throttle-shaft','throttle-lever-estimated','throttle-cable-ball-stud-estimated','throttle-lever-retaining-pin-estimated']) or oid=='efi-upper-intake']
collisions=[];exact=0
for key,obj in parts.items():
 for oid in neighbors:
  n=local(oid).moved(poses[oid])
  if broad(obj,n):
   exact+=1;v=volume(obj.intersect(n))
   if v>.1:collisions.append({'a':key,'b':oid,'angle_deg':None,'overlap_mm3':v})
sweep=[]
for angle in range(0,91,2):
 pose=b.Pos(394,25,490)*b.Rot(0,angle,0)
 clearances=[]
 for key,obj in moving.items():
  obj=obj.moved(pose)
  for name,target in [('shield',shield),('pushpin',pin)]:
   clearances.append(obj.distance_to(target))
   if broad(obj,target):
    exact+=1;v=volume(obj.intersect(target))
    if v>.1:collisions.append({'a':key,'b':name,'angle_deg':angle,'overlap_mm3':v})
 theta=np.radians(angle);center=np.array([394+24*np.sin(theta),95,490+24*np.cos(theta)]);delta=np.array([465,110,467])-center
 cable=b.Plane(origin=tuple(center),z_dir=tuple(delta))*b.Cylinder(1,float(np.linalg.norm(delta)),align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 cable_vols={}
 for name,target in [('shield',shield),('pushpin',pin),('bracket',bracket)]:
  v=volume(cable.intersect(target));cable_vols[name]=v
  if v>1e-6:collisions.append({'a':'direct-cable-envelope','b':name,'angle_deg':angle,'overlap_mm3':v})
 sweep.append({'angle_deg':angle,'minimum_linkage_clearance_mm':min(clearances),'cable_overlaps_mm3':cable_vols})
mount_contacts={}
for oid in ['throttle-housing','throttle-nut-3','throttle-nut-4']:
 mount_contacts[oid]=contact(bracket,local(oid).moved(poses[oid]));assert mount_contacts[oid]>1
preview={**parts,**{k:v.moved(b.Pos(394,25,490)) for k,v in moving.items()},'throttle-housing':local('throttle-housing').moved(poses['throttle-housing'])}
a={};names=[]
for k,obj in preview.items():
 v,f=obj.tessellate(.3,.3);i=len(names);names.append(k);a[f'v{i}']=np.array([tuple(t) for t in v]);a[f'f{i}']=np.array(f)
a['names']=np.array(json.dumps(names));np.savez_compressed(OUT/'preview.npz',**a)
# Manifest changes during root integration do not invalidate the frozen candidate
# study, but explicitly record that event and require fresh installed review.
manifest_unchanged=raw==M.read_bytes()
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in inputs.items() if p!='inventory/engine/full-assembly.json')
r={'status':'PASS' if not collisions else 'FAIL','readiness':'candidate only','scope':'Estimated splash hood and compliant-barb pushpin on final coordinated linkage/bracket candidate. Static local neighbors and46 travel/cable samples; no factory dimensions, elasticity or strength certification.','input_hashes':inputs,'manifest_unchanged_during_check':manifest_unchanged,'output_hashes':outputs,'parameters':s.PARAMS,'export_checks':export_checks,'contacts_mm2':contacts,'detached_pin_negative_control':negative,'axial_withdrawal_barb_interference_mm3':withdrawal,'mount_contacts_mm2':mount_contacts,'neighbor_ids':neighbors,'exact_static_and_moving_pairs':exact,'sweep':sweep,'collisions':collisions,'integration':{'parent':'throttle-assembly','position_cad_mm':[0,0,0],'rotation_cad_deg':[0,0,0],'bracket_delta':'Y-axis hole radius2.4 atX389,Z514 through final proposed webY103–105; no mounting/cable datums moved'},'limitations':s.GAPS}
(ROOT/'inventory/engine/throttle-shield-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(collisions),'collisions',contacts);print(json.dumps(collisions[:10]));assert not collisions
