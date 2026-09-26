"""Issue44 isolated attachment/return mechanism checks. Never changes assembly."""
from pathlib import Path
import json,sys,hashlib,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/iac-attachment-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(14,6))
 for j in [1,2]:
  ax=fig.add_subplot(1,2,j,projection='3d')
  for i,k in enumerate(names):
   if j==2 and k in ['throttle-housing','iac-gasket','iac-solenoid-can','iac-coil','iac-connector-cap']:continue
   v=a[f'v{i}'];f=a[f'f{i}'];alpha=.17 if k in ['iac-valve-body','iac-solenoid-can','throttle-housing'] else 1
   color='#cb782a' if 'spring' in k else '#d5ad45' if 'screw' in k else '#b7a17a' if 'gasket' in k else '#899caa'
   ax.add_collection3d(Poly3DCollection(v[f],facecolor=color,alpha=alpha,edgecolor='none'))
  ax.set(xlim=(-32,83),ylim=(-64,64) if j==1 else (-34,34),zlim=(-80,20) if j==1 else (-35,20),xlabel='IAC local X mm',ylabel='Y',zlabel='Z',title='Estimated attachment and receiver' if j==1 else 'Illustrative return element and stem joint')
  ax.set_box_aspect((115,128,100) if j==1 else (115,68,55));ax.view_init(27,-65 if j==1 else -105)
 fig.suptitle('1994 IAC topology study — dimensions / spring construction provisional');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=160);raise SystemExit
import build123d as b,trimesh
sys.path.insert(0,str(ROOT/'cad/engine'))
import iac_attachment_candidate as c
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';raw=M.read_bytes();m=json.loads(raw);D={r['id']:r for r in m['definitions']};O={r['id']:r for r in m['occurrences']};A={r['id']:r for r in m['assemblies']};poses=transforms(m);frame=b.Pos(*c.ORIGIN);inv=frame.inverse();inputs={}
def track(p):p=Path(p);inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return p
def vol(s):return sum(abs(solid_volume(x,'adaptive')) for x in s.solids()) if s else 0.
def bounds(s):q=s.bounding_box();return np.array([tuple(q.min),tuple(q.max)])
def broad(a,b):x,y=bounds(a),bounds(b);return bool(np.all(x[0]<=y[1]+1e-6) and np.all(y[0]<=x[1]+1e-6))
def overlap(a,b):return vol(a.intersect(b)) if broad(a,b) else 0.
def contact(a,b):return sum(f.intersect(g).area for f in a.faces() for g in b.faces() if f.geom_type==bld_geom_plane and g.geom_type==bld_geom_plane and f.distance_to(g)<1e-6 and f.intersect(g))
bld_geom_plane=b.GeomType.PLANE
for p in [Path(__file__),Path(c.__file__),ROOT/'reference/engine/iac-attachment-review.json',ROOT/'cad/engine/idle_air.py',ROOT/'cad/engine/throttle.py']:track(p)
review=json.loads((ROOT/'reference/engine/iac-attachment-review.json').read_text())
for source in review['sources']:
 p=ROOT/source['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256'];track(p)
def load(k):return b.import_step(track(ROOT/D[O[k]['definition']]['step'].lstrip('/'))).moved(inv*poses[k])
base={k:load(k) for k in O if k.startswith('iac-')};base['throttle-housing']=load('throttle-housing')
# Reject implicit frame drift, permitting explicitly coordinated whole-subtree move
# only after rerunning this candidate with a reviewed ORIGIN.
assert np.max(np.abs(bounds(base['iac-valve-body'])-np.array([[-24,-15,-13],[24,15,13]])))<.001
parts={**base,**c.build(base['iac-valve-body'],base['iac-gasket'],base['throttle-housing'],base['iac-armature'])}
changed=['iac-valve-body','iac-gasket','throttle-housing','iac-armature','iac-return-spring-estimated','iac-mount-screw-1-estimated','iac-mount-screw-2-estimated']
rows={k:dict(valid=s.is_valid,solids=len(s.solids()),volume_mm3=vol(s)) for k,s in parts.items()}
collisions=[]
for ka,kb in itertools.combinations(parts,2):
 v=overlap(parts[ka],parts[kb])
 if v>1e-5:collisions.append(dict(a=ka,b=kb,volume_mm3=v))
# Full local neighborhood discovery from installed bounds; relevant inputs and
# ancestor poses frozen. Distant/unrelated manifest mutations are allowed.
neighbor_ids=[];nearby={};region=b.Pos(20,0,-7)*b.Box(160,100,90)
mesh_boxes={}
def nearby_selection(manifest):
    ds={r['id']:r for r in manifest['definitions']};ps=transforms(manifest);selected=[]
    rb=bounds(region)
    for o in manifest['occurrences']:
        k=o['id']
        if k in base:continue
        d=ds[o['definition']];path=ROOT/d['glb'].lstrip('/')
        if d['id'] not in mesh_boxes:
            mesh=trimesh.load(path,force='mesh');vv=np.array(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
            mesh_boxes[d['id']]=(vv.min(0),vv.max(0))
        lo,hi=mesh_boxes[d['id']];loc=inv*ps[k]
        corners=np.array([tuple(b.Vertex(*v).moved(loc).center()) for v in itertools.product(*zip(lo,hi))])
        if np.all(corners.min(0)<=rb[1]+.2) and np.all(rb[0]<=corners.max(0)+.2):selected.append(k)
    return selected
for k in nearby_selection(m):
 s=load(k)
 if broad(region,s):nearby[k]=s;neighbor_ids.append(k)
near_collisions=[]
for k in changed:
 for n,s in nearby.items():
  v=overlap(parts[k],s)
  if v>1e-5:near_collisions.append(dict(part=k,neighbor=n,volume_mm3=v))
throttle_travel_collisions=[]
for angle in range(0,91,5):
    moving_poses=transforms(m,throttle_degrees=angle)
    for n in ['throttle-shaft','throttle-plate-1','throttle-plate-2']:
        q=b.import_step(ROOT/D[O[n]['definition']]['step'].lstrip('/')).moved(inv*moving_poses[n])
        for k in changed:
            v=overlap(parts[k],q)
            if v>1e-5:throttle_travel_collisions.append(dict(angle=angle,part=k,neighbor=n,volume_mm3=v))
withdrawal_collisions=[]
for lift_mm in [0,5,10,20,30,40]:
    for k in ['iac-mount-screw-1-estimated','iac-mount-screw-2-estimated']:
        q=b.Pos(0,0,lift_mm)*parts[k]
        for n,s in {**parts,**nearby}.items():
            if n==k:continue
            v=overlap(q,s)
            if v>1e-5:withdrawal_collisions.append(dict(lift_mm=lift_mm,part=k,neighbor=n,volume_mm3=v))
contacts={}
for i in [1,2]:
 screw=parts[f'iac-mount-screw-{i}-estimated'];contacts[f'head_{i}']=dict(gap_mm=screw.distance_to(parts['iac-valve-body']),area_mm2=contact(screw,parts['iac-valve-body']))
for a,k in [('body','iac-valve-body'),('receiver','throttle-housing')]:contacts[f'gasket_{a}']=dict(gap_mm=parts['iac-gasket'].distance_to(parts[k]),area_mm2=contact(parts['iac-gasket'],parts[k]))
for a,k in [('left','iac-end-plug'),('right','iac-pintle')]:contacts[f'spring_{a}']=dict(gap_mm=parts['iac-return-spring-estimated'].distance_to(parts[k]),area_mm2=contact(parts['iac-return-spring-estimated'],parts[k]))
contacts['stem_armature']=dict(gap_mm=parts['iac-pintle'].distance_to(parts['iac-armature']),overlap_mm3=overlap(parts['iac-pintle'],parts['iac-armature']))
ports=[]
for x in [-12,12]:
 probe=c.zc(4.9,-16,-7,x,0)
 ports.append(dict(x=x,probe_blocked_mm3=sum(overlap(probe,parts[k]) for k in ['iac-valve-body','iac-gasket','throttle-housing'])))
# Existing throttle bores must remain geometrically void after added receivers.
bores=[b.Pos(.5,y-25,-50)*c.cx(19.9,50) for y in [-2,52]]
preserved_bores=[overlap(v,parts['throttle-housing']) for v in bores]
chamber_probes=[b.Pos(x,0,0)*c.cx(8.4,21.8) for x in [-13,13]]
preserved_chambers=[overlap(v,parts['iac-valve-body']) for v in chamber_probes]
travel=[]
for dx in [-1.,0.,1.]:
 moving={k:b.Pos(dx,0,0)*parts[k] for k in ['iac-pintle','iac-armature']};sp=c.spring(dx);bad=[]
 for k,s in moving.items():
  for n,q in parts.items():
   if n in moving or n=='iac-return-spring-estimated':continue
   v=overlap(s,q)
   if v>1e-5:bad.append(dict(a=k,b=n,volume_mm3=v))
 for n,q in {**parts,**moving}.items():
  if n=='iac-return-spring-estimated':continue
  v=overlap(sp,q)
  if v>1e-5:bad.append(dict(a='spring',b=n,volume_mm3=v))
 travel.append(dict(pintle_travel_mm=dx,spring_valid=sp.is_valid,spring_solids=len(sp.solids()),collisions=bad,spring_to_pintle_gap_mm=sp.distance_to(moving['iac-pintle']),spring_to_plug_gap_mm=sp.distance_to(parts['iac-end-plug']),seat_gap_mm=moving['iac-pintle'].distance_to(parts['iac-valve-body']),axial_seat_gap_mm=1-dx,closed_seat_contact_mm2=contact(moving['iac-pintle'],parts['iac-valve-body']) if dx==1 else 0))
# Fault controls cross real material or remove actual required bearing contact.
x,y=c.BOLTS[0];oversize=b.Pos(x,y,0)*c.screw(3.1);lift=b.Pos(0,0,1)*parts['iac-mount-screw-1-estimated']
negative=dict(oversize_screw_overlap_mm3=overlap(oversize,parts['iac-valve-body'])+overlap(oversize,parts['throttle-housing']),lifted_head_gap_mm=(b.Pos(0,0,1)*parts['iac-mount-screw-1-estimated'].intersect(c.zc(5,-10,-6,x,y))).distance_to(parts['iac-valve-body']),blocked_port_overlap_mm3=overlap(c.zc(4.9,-14,-13,-12,0),c.zc(5,-14,-13,-12,0)),original_armature_stem_gap_mm=base['iac-armature'].distance_to(base['iac-pintle']),short_spring_seat_gap_mm=(b.Pos(1,0,0)*parts['iac-return-spring-estimated']).distance_to(parts['iac-end-plug']))
print(json.dumps(dict(collisions=collisions,near_collisions=near_collisions,contacts=contacts,ports=ports,travel=travel,negative=negative),indent=2),flush=True)
OUT.mkdir(parents=True,exist_ok=True);preview={'names':np.array(json.dumps(list(parts)))};exports={}
scene=trimesh.Scene()
for i,(k,s) in enumerate(parts.items()):
 print("export",k,flush=True)
 from OCP.BRepTools import BRepTools
 BRepTools.Clean_s(s.wrapped)
 v,f=s.tessellate(.05,.1);v=np.array([tuple(a) for a in v]);f=np.array(f);preview[f'v{i}']=v;preview[f'f{i}']=f
 if k not in changed:continue
 sp=OUT/(k+'.step');b.export_step(s,sp);q=b.import_step(sp)
 mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);mesh.merge_vertices();mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(k+'.glb');mesh.export(gp);scene.add_geometry(mesh,node_name=k,geom_name=k)
 vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
 exports[k]=dict(watertight=mesh.is_watertight,step_valid=q.is_valid,volume_error_mm3=abs(vol(q)-vol(s)),mesh_bounds_error_mm=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bounds(s)))))
np.savez_compressed(OUT/'preview.npz',**preview);scene.export(OUT/'candidate.glb')
relevant=set(base)|set(neighbor_ids);ancestors=set()
for k in relevant:
 p=O[k]['parent']
 while p in A:ancestors.add(p);p=A[p]['parent']
snapshot=dict(definitions={O[k]['definition']:D[O[k]['definition']] for k in sorted(relevant)},occurrences={k:O[k] for k in sorted(relevant)},assemblies={k:A[k] for k in sorted(ancestors)})
current=json.loads(M.read_bytes());cd={d['id']:d for d in current['definitions']};co={o['id']:o for o in current['occurrences']};ca={a['id']:a for a in current['assemblies']};stable=all(cd[k]==v for k,v in snapshot['definitions'].items()) and all(co[k]==v for k,v in snapshot['occurrences'].items()) and all(ca[k]==v for k,v in snapshot['assemblies'].items()) and all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in inputs.items())
passed=stable and all(r['valid'] and r['solids']==1 for r in rows.values()) and not collisions and not near_collisions and not throttle_travel_collisions and not withdrawal_collisions and all(c['gap_mm']<1e-5 and c.get('area_mm2',1)>.01 for c in contacts.values()) and all(r['probe_blocked_mm3']<1e-5 for r in ports) and max(preserved_bores)<1e-5 and max(preserved_chambers)<1e-5 and all(not r['collisions'] and r['spring_valid'] and r['spring_solids']==1 and r['spring_to_pintle_gap_mm']<1e-5 and r['spring_to_plug_gap_mm']<1e-5 for r in travel) and travel[-1]['closed_seat_contact_mm2']>90 and negative['oversize_screw_overlap_mm3']>.01 and negative['lifted_head_gap_mm']>.5 and negative['blocked_port_overlap_mm3']>.01 and negative['original_armature_stem_gap_mm']>.05 and negative['short_spring_seat_gap_mm']>.5 and all(r['watertight'] and r['step_valid'] and r['volume_error_mm3']<.001 and r['mesh_bounds_error_mm']<.2 for r in exports.values())
report=dict(schema='iac-attachment-candidate-validation-v1',passed=passed,status='isolated educational candidate; not installed; not production acceptance',manifest_sha256=hashlib.sha256(raw).hexdigest(),inputs=inputs,relevant_pose_snapshot=snapshot,relevant_inputs_stable=stable,parts=rows,internal_collisions=collisions,nearby_collisions=near_collisions,neighbor_ids=neighbor_ids,throttle_travel_collisions=throttle_travel_collisions,throttle_travel_poses=19,screw_withdrawal_collisions=withdrawal_collisions,screw_withdrawal_poses_per_screw=6,contacts=contacts,ports=ports,preserved_main_bore_overlap_mm3=preserved_bores,preserved_chamber_overlap_mm3=preserved_chambers,illustrative_travel=travel,negative_controls=negative,exports=exports,thread_envelope=dict(diameter_mm=5,radial_receiver_clearance_mm=.05,engagement_length_mm=9,blind_tip_gap_mm=1,claim='clearance envelope only; no helical threads, torque or strength acceptance'),output_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.suffix in ['.step','.glb','.npz']},limitations=review['limitations'])
(ROOT/'inventory/engine/iac-attachment-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['passed','internal_collisions','nearby_collisions','contacts','ports','illustrative_travel','negative_controls','exports']},indent=2));raise SystemExit(0 if passed else 1)
