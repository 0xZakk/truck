#!/usr/bin/env python3
"""Isolated geometric closure/retention study; no shared writes or leak-rate claim."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/iac-closure-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.collections import PolyCollection
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(14,6));ax=fig.add_subplot(1,2,1,projection='3d')
 for i,k in enumerate(names):
  v=a[f'v{i}'];f=a[f'f{i}'];alpha=.12 if k=='iac-valve-body' else 1
  color='#c58b43' if k=='iac-end-plug' else '#b06f32' if 'spring' in k else '#8299ab'
  ax.add_collection3d(Poly3DCollection(v[f],facecolor=color,alpha=alpha,edgecolor='none'))
 ax.set(xlim=(-26,0),ylim=(-12,12),zlim=(-12,12),xlabel='IAC local X mm',ylabel='Y',zlabel='Z',title='Cutaway window: closure and preserved spring seat');ax.set_box_aspect((26,24,24));ax.view_init(23,-115)
 ax=fig.add_subplot(1,2,2)
 for k,color in [('iac-valve-body','#8299ab'),('iac-end-plug','#c58b43')]:
  v=a[k+'_section_v'];f=a[k+'_section_f'];tri=v[f][:,:,[0,2]];ax.add_collection(PolyCollection(tri,facecolors=color,edgecolors='none'))
 ax.set(xlim=(-24.15,-22.85),ylim=(8,9.6),xlabel='IAC local X mm',ylabel='Radius at Y=0 mm',title='Actual CAD section: upper rim (equal axis scale)');ax.set_aspect('equal');ax.grid(alpha=.2)
 for xy,text,offset in [((-23.86,8.8),'Integral lip',(-18,48)),((-23.50,8.8),'Plug flange',(0,-62)),((-23.14,8.8),'Body shoulder',(12,48))]:ax.annotate(text,xy,xytext=offset,textcoords='offset points',ha='center',arrowprops=dict(arrowstyle='->',color='#26333d'))
 fig.suptitle('Illustrative formed-lip closure — production retention and sealing method unknown');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=160);raise SystemExit
import build123d as b,trimesh
from OCP.BRepTools import BRepTools
sys.path.insert(0,str(ROOT/'cad/engine'))
import iac_closure_candidate as c
import iac_attachment_integration as frames
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';raw=M.read_bytes();m=json.loads(raw);D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};A={a['id']:a for a in m['assemblies']};poses=transforms(m);frame=frames.static_frame('idle-air',m['assemblies']);inv=frame.inverse();inputs={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def track(p):inputs[str(p.relative_to(ROOT))]=sha(p);return p
def load(k):return b.import_step(track(ROOT/D[O[k]['definition']]['step'].lstrip('/'))).moved(inv*poses[k])
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
def bounds(s):r=s.bounding_box();return np.array([tuple(r.min),tuple(r.max)])
def broad(a,d):x,y=bounds(a),bounds(d);return bool(np.all(x[0]<=y[1]+1e-6) and np.all(y[0]<=x[1]+1e-6))
def overlap(a,d):return vol(a.intersect(d)) if broad(a,d) else 0.
def common_area(a,d,kind=b.GeomType.PLANE):
 total=0.
 for f in a.faces():
  if f.geom_type!=kind:continue
  for g in d.faces():
   if g.geom_type!=kind or f.distance_to(g)>1e-6:continue
   q=f.intersect(g)
   if q:total+=q.area
 return total
for p in [Path(__file__),Path(c.__file__),ROOT/'reference/engine/iac-closure-review.json',ROOT/'cad/engine/iac_attachment_integration.py',ROOT/'cad/engine/iac_attachment_candidate.py']:track(p)
ledger=json.loads((ROOT/'reference/engine/iac-closure-review.json').read_text())
for row in ledger['sources']:assert sha(ROOT/row['path'])==row['sha256'];track(ROOT/row['path'])
assert 'iac-return-spring-estimated' in O,'Install and check the attachment study first'
base={k:load(k) for k in O if k.startswith('iac-')};base['throttle-housing']=load('throttle-housing')
changed=c.build(base['iac-valve-body']);parts={**base,**changed};body=changed['iac-valve-body'];plug=changed['iac-end-plug'];spring=parts['iac-return-spring-estimated']
collisions=[]
for a,d in itertools.combinations(parts,2):
 v=overlap(parts[a],parts[d])
 if v>1e-5:collisions.append(dict(a=a,b=d,volume_mm3=v))
# Distinct contact rings on both flange faces prove capture and geometric closure.
face_contacts={}
for x in [-23.7,-23.3]:
 plane=b.Plane(origin=(x,0,0),z_dir=(1,0,0));ring=plane*(b.Circle(9.2)-b.Circle(8.5))
 area=0.
 for face in plug.faces():
  if face.geom_type==b.GeomType.PLANE and face.distance_to(ring)<1e-6:
   q=face.intersect(ring)
   if q:area+=q.area
 face_contacts[str(x)]=area
contact=dict(axial_body_plug_mm2=common_area(body,plug),radial_body_plug_mm2=common_area(body,plug,b.GeomType.CYLINDER),spring_plug_mm2=common_area(spring,plug),spring_gap_mm=spring.distance_to(plug),body_plug_gap_mm=body.distance_to(plug),retaining_face_contacts_mm2=face_contacts)
retention={str(dx):overlap(b.Pos(dx,0,0)*plug,body) for dx in [-.1,.1]}
old_retention={str(dx):overlap(b.Pos(dx,0,0)*base['iac-end-plug'],base['iac-valve-body']) for dx in [-.1,.1]}
# Full-circumference witness for the new radial flange contact. 72 points, with
# each point exactly on both surfaces; pair contact areas above cover the faces.
radial_errors=[]
for angle in range(0,360,5):
 a=np.radians(angle);p=b.Vertex(-23.5,9.2*np.cos(a),9.2*np.sin(a));radial_errors.append(max(body.distance_to(p),plug.distance_to(p)))
# A deliberate floating undersize closure yields a connected small passage from
# outside to chamber. This is a geometric channel witness, never a leak rate.
bad=c.cx(9.1,-23.6,-23.4)+c.cx(8.4,-23.4,-23.1)
points=[(-24.5,8.45,0),(-23.65,8.45,0),(-23.65,9.15,0),(-23.35,9.15,0),(-23.35,8.45,0),(-22.8,8.45,0)]
probe=None
for a,d in zip(points,points[1:]):
 delta=b.Vector(*d)-b.Vector(*a);segment=b.Plane(origin=a,z_dir=delta)*b.Cylinder(.02,delta.length,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN));probe=segment if probe is None else probe+segment
for point in points:probe+=b.Pos(*point)*b.Sphere(.02)
negative=dict(original_radial_gap_mm=base['iac-end-plug'].distance_to(base['iac-valve-body']),bad_plug_channel_blocked_mm3=overlap(probe,body)+overlap(probe,bad),good_plug_channel_blocked_mm3=overlap(probe,body)+overlap(probe,plug),floating_plug_spring_gap_mm=bad.distance_to(spring),original_retention_overlap_mm3=old_retention)
chambers=[overlap(b.Pos(x,0,0)*c.cx(8.4,-10.9,10.9),body) for x in [-13,13]]
ports=[overlap(b.Pos(x,0,-8)*b.Cylinder(4.9,20),body) for x in [-12,12]]
# Neighbor selection covers the actual changed envelope with a5mm margin; full
# body reference is preserved outside the short groove. No subtree name filter.
region=np.array([[-29,-20,-18],[-18,20,18]]);near={};mesh_boxes={}
for k,o in O.items():
 if k in base:continue
 ident=o['definition'];gp=ROOT/D[ident]['glb'].lstrip('/')
 if ident not in mesh_boxes:
  vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;mesh_boxes[ident]=(vv.min(0),vv.max(0))
 low,high=mesh_boxes[ident];loc=inv*poses[k];vv=np.array([tuple(b.Vertex(*v).moved(loc).center()) for v in itertools.product(*zip(low,high))])
 if np.all(vv.min(0)<=region[1]+.2) and np.all(region[0]<=vv.max(0)+.2):near[k]=load(k);track(gp)
neighbors=[]
for k,s in changed.items():
 for n,t in near.items():
  v=overlap(s,t)
  if v>1e-5:neighbors.append(dict(part=k,neighbor=n,volume_mm3=v))
# Body change is a local recess only; quantify removed material and prove it is
# restricted to the declared flange station. No chamber, port or mount is moved.
added=vol(body-base['iac-valve-body']);removed=base['iac-valve-body']-body;removed_outside=vol(removed-c.cx(9.2,-23.7,-23.3))
OUT.mkdir(parents=True,exist_ok=True);exports={};preview={'names':np.array(json.dumps(['iac-valve-body','iac-end-plug','iac-return-spring-estimated','iac-pintle']))};scene=trimesh.Scene()
for i,k in enumerate(json.loads(str(preview['names']))):
 s=parts[k];BRepTools.Clean_s(s.wrapped);v,f=s.tessellate(.03,.08);v=np.array([tuple(t) for t in v]);f=np.array(f)
 display=s.intersect(b.Pos(-12.5,0,0)*b.Box(25,24,24));pv,pf=display.tessellate(.03,.08);preview[f'v{i}']=np.array([tuple(t) for t in pv]);preview[f'f{i}']=np.array(pf)
 if k not in changed:continue
 section=s.intersect(b.Pos(-23.5,0,0)*b.Box(2,.02,24));sv,sf=section.tessellate(.02,.08);preview[k+'_section_v']=np.array([tuple(t) for t in sv]);preview[k+'_section_f']=np.array(sf)
 sp=OUT/(k+'.step');b.export_step(s,sp);q=b.import_step(sp);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);mesh.merge_vertices();mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(k+'.glb');mesh.export(gp);scene.add_geometry(mesh,node_name=k,geom_name=k);vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
 exports[k]=dict(valid=s.is_valid,solids=len(s.solids()),watertight=mesh.is_watertight,step_valid=q.is_valid,step_volume_error_mm3=abs(vol(q)-vol(s)),mesh_bounds_error_mm=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bounds(s)))))
np.savez_compressed(OUT/'preview.npz',**preview);scene.export(OUT/'candidate.glb')
relevant=set(base)|set(near);ancestors=set()
for k in relevant:
 p=O[k]['parent']
 while p in A:ancestors.add(p);p=A[p]['parent']
snapshot=dict(definitions={O[k]['definition']:D[O[k]['definition']] for k in sorted(relevant)},occurrences={k:O[k] for k in sorted(relevant)},assemblies={k:A[k] for k in sorted(ancestors)})
new=json.loads(M.read_bytes());stable=all({r['id']:r for r in new[kind]}[k]==v for kind,rows in snapshot.items() for k,v in rows.items()) and all(sha(ROOT/p)==h for p,h in inputs.items())
passed=stable and not collisions and not neighbors and max(chambers+ports)<1e-5 and added<1e-5 and removed_outside<1e-5 and all(v>3 for v in retention.values()) and max(radial_errors)<1e-5 and min(face_contacts.values())>38 and contact['spring_gap_mm']<1e-5 and contact['spring_plug_mm2']>18 and contact['radial_body_plug_mm2']>39 and negative['bad_plug_channel_blocked_mm3']<1e-5 and negative['good_plug_channel_blocked_mm3']>.001 and negative['floating_plug_spring_gap_mm']>.05 and max(old_retention.values())<1e-5 and all(r['valid'] and r['solids']==1 and r['watertight'] and r['step_valid'] and r['step_volume_error_mm3']<.001 and r['mesh_bounds_error_mm']<.2 for r in exports.values())
report=dict(status='PASS' if passed else 'FAIL',scope='Isolated illustrative closure; no factory process, strength or leak-rate acceptance',manifest_sha256=hashlib.sha256(raw).hexdigest(),input_sha256=inputs,relevant_pose_snapshot=snapshot,relevant_inputs_stable=stable,contacts=contact,retention_overlap_mm3=retention,maximum_radial_contact_error_mm=max(radial_errors),negative_controls=negative,internal_collisions=collisions,neighbor_collisions=neighbors,neighbor_ids=sorted(near),chamber_obstruction_mm3=chambers,port_obstruction_mm3=ports,body_added_mm3=added,body_removed_mm3=vol(removed),body_removed_outside_declared_groove_mm3=removed_outside,exports=exports,output_sha256={str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.suffix in ['.step','.glb','.npz']},limitations=ledger['limits'])
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','contacts','retention_overlap_mm3','negative_controls','internal_collisions','neighbor_collisions','exports']},indent=2));raise SystemExit(0 if passed else 1)
