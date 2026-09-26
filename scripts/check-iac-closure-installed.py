#!/usr/bin/env python3
"""Combined attachment+closure stage binding, localized proof and affected motion."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,itertools,json,sys
import build123d as b,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import iac_closure_integration as closure
import iac_closure_candidate as candidate
import iac_attachment_integration as attachment
import iac_attachment_candidate as attachment_candidate
from assembly_math import transforms
from cad_metrics import solid_volume

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
def difference(a,c):return vol(a-c)+vol(c-a)
def bounds(s):r=s.bounding_box();return np.array([tuple(r.min),tuple(r.max)])
def broad(a,c):x,y=bounds(a),bounds(c);return bool(np.all(x[0]<=y[1]+1e-6) and np.all(y[0]<=x[1]+1e-6))
def overlap(a,c):return vol(a.intersect(c)) if broad(a,c) else 0.
def common_area(a,c,kind=b.GeomType.PLANE):
 area=0.
 for f in a.faces():
  if f.geom_type!=kind:continue
  for g in c.faces():
   if g.geom_type!=kind or f.distance_to(g)>1e-6:continue
   q=f.intersect(g)
   if q:area+=q.area
 return area

def replay_chain(m,shapes):
 data=copy.deepcopy(m);old={d['id']:d for d in m['definitions']};work=dict(shapes);calls=[]
 def define(i,s,n,f,system,color,sources,gaps,claims,prepared=False):
  assert prepared
  d=copy.deepcopy(old[i]);d.update(name=n,function=f,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims);data['definitions'].append(d);work[i]=s;calls.append(i)
 def add(i,d,p,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
  row=next(x for x in data['definitions'] if x['id']==d);data['occurrences'].append(dict(id=i,definition=d,parent=p,name=name or row['name'],function=row['function'],position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode)))
 def group(*a,**k):raise AssertionError('No new groups in this chain')
 attachment.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],work)
 closure.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],work)
 for key in ['definitions','occurrences','assemblies']:
  assert {r['id']:r for r in data[key]}=={r['id']:r for r in m[key]},'Replay metadata '+key
  assert len(data[key])==len({r['id'] for r in data[key]}),'Replay duplicates'
 return {i:work[i] for i in closure.CHANGED_IDS},calls

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--installed',action='store_true');p.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/iac-closure-integration-stage');args=p.parse_args();out=args.stage_dir.resolve()
 mp=ROOT/'inventory/engine/full-assembly.json' if args.installed else out/'full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);record=json.loads((ROOT/'inventory/engine/iac-closure-installation.json' if args.installed else out/'installation.json').read_text())
 if not args.installed:assert sha(mp)==record['staged_manifest_sha256']
 for key,path in [('installer_sha256','scripts/install-iac-closure.py'),('checker_sha256','scripts/check-iac-closure-installed.py'),('adapter_sha256','cad/engine/iac_closure_integration.py'),('learning_sha256','inventory/engine/iac-closure-learning.json')]:assert sha(ROOT/path)==record[key]
 spec=importlib.util.spec_from_file_location('closure_installer',ROOT/'scripts/install-iac-closure.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
 assert installer.evidence(args.installed)==record['candidate_evidence'];assert installer.scoped(m,closure.CHANGED_IDS,record['guard_occurrences'])==record['installed_scope']
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};A={a['id']:a for a in m['assemblies']};poses=transforms(m);frame=attachment.static_frame('idle-air',m['assemblies']);inv=frame.inverse();shapes={};hashes={}
 def track(p):hashes[str(p.relative_to(ROOT))]=sha(p);return p
 def loaddef(i):
  if i not in shapes:
   path=ROOT/D[i]['step'].lstrip('/') if args.installed or i not in closure.GEOMETRY_IDS else out/'step'/(i+'.step');shapes[i]=b.import_step(track(path))
  return shapes[i]
 def local(i):return (inv*poses[i])*loaddef(O[i]['definition'])
 parts={k:local(k) for k in O if k.startswith('iac-')};parts['throttle-housing']=local('throttle-housing');parts['efi-upper-intake']=local('efi-upper-intake');checks=[]
 for i in sorted(closure.CHANGED_IDS):
  oid='iac-mount-screw-1-estimated' if i==attachment.SCREW else i
  root=ROOT/'cad/engine/generated'/('iac-closure-candidate' if i in closure.GEOMETRY_IDS else 'iac-attachment-candidate')
  ref=b.import_step(track(root/(oid+'.step')));delta=difference(parts[oid],ref);bad=difference(b.Pos(1,0,0)*parts[oid],ref);assert delta<.02 and bad>1,(i,delta,bad)
  checks.append(dict(id=i,reference=str((root/(oid+'.step')).relative_to(ROOT)),symmetric_difference_mm3=delta,translation_fault_mm3=bad))
 original=json.loads((ROOT/'cad/engine/generated/iac-closure-candidate/validation.json').read_text())['relevant_pose_snapshot']
 old_frame=attachment.static_frame('idle-air',list(original['assemblies'].values()))
 for oid,o in original['occurrences'].items():
  old_local=old_frame.inverse()*attachment.occurrence_frame(o,list(original['assemblies'].values()))
  assert attachment.frame_error(inv*poses[oid],old_local)<1e-6,'Changed original relative closure pose '+oid
 exports={}
 for i in closure.GEOMETRY_IDS:
  sp=ROOT/D[i]['step'].lstrip('/') if args.installed else out/'step'/(i+'.step');gp=ROOT/D[i]['glb'].lstrip('/') if args.installed else out/'models'/(i+'.glb');declared=record['canonical_artifact_sha256'] if args.installed else record['staged_artifact_sha256']
  for path in [sp,gp]:assert sha(path)==declared[str(path.relative_to(ROOT if args.installed else out))];track(path)
  mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.nondegenerate_faces().all() and mesh.unique_faces().all()
  vv=np.array(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;s=loaddef(i);err=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bounds(s))));assert err<.2 and s.is_valid and len(s.solids())==1
  assert np.max(np.abs(np.diff(bounds(s),axis=0)[0]-np.array(D[i]['model_bounds_mm'])))<.01
  exports[i]=dict(mesh_bounds_error_mm=err,watertight_after_position_weld=True,position_weld_precision_m=1e-8)
 base_body=b.import_step(track(ROOT/'cad/engine/generated/iac-attachment-candidate/iac-valve-body.step'));body=parts['iac-valve-body'];plug=parts['iac-end-plug'];removed=base_body-body;added=vol(body-base_body);groove=candidate.cx(9.2,-23.7,-23.3);outside=vol(removed-groove)
 proof=dict(added_volume_mm3=added,removed_volume_mm3=vol(removed),removed_outside_declared_groove_mm3=outside,baseline='checked attachment body',consequence='Final body is a subset of the checked attachment body. Removing only this recess cannot introduce body collisions with unchanged neighbors at any pose.')
 assert added<1e-5 and outside<1e-5 and abs(vol(removed)-15.56973319119)<1e-5
 collisions=[]
 for a,c in itertools.combinations(parts,2):
  v=overlap(parts[a],parts[c])
  if v>1e-5:collisions.append(dict(a=a,b=c,volume_mm3=v))
 contacts={}
 for a,c in [('iac-mount-screw-1-estimated','iac-valve-body'),('iac-mount-screw-2-estimated','iac-valve-body'),('iac-gasket','iac-valve-body'),('iac-gasket','throttle-housing'),(attachment.SPRING,'iac-end-plug'),(attachment.SPRING,'iac-pintle')]:contacts[a+' / '+c]=dict(gap_mm=parts[a].distance_to(parts[c]),area_mm2=common_area(parts[a],parts[c]))
 assert all(v['gap_mm']<1e-5 and v['area_mm2']>.01 for v in contacts.values())
 assert parts['iac-armature'].distance_to(parts['iac-pintle'])<1e-5
 closure_contacts=dict(axial_mm2=common_area(body,plug),radial_mm2=common_area(body,plug,b.GeomType.CYLINDER));assert closure_contacts['axial_mm2']>77 and closure_contacts['radial_mm2']>39
 ports=[sum(overlap(attachment_candidate.zc(4.9,-16,-7,x,0),parts[i]) for i in ['iac-valve-body','iac-gasket','throttle-housing']) for x in [-12,12]];assert max(ports)<1e-5
 # Existing bolt withdrawal checked only against local interfaces; all changed
 # body material is removed, and plug lies separately away from the screw paths.
 withdrawal=[]
 for dz in [0,5,10,20,30,40]:
  for i in ['iac-mount-screw-1-estimated','iac-mount-screw-2-estimated']:
   q=b.Pos(0,0,dz)*parts[i]
   for n,s in parts.items():
    if n==i:continue
    v=overlap(q,s)
    if v>1e-5:withdrawal.append(dict(lift=dz,a=i,b=n,volume_mm3=v))
 # Target only throttle-moving descendants. Use the unchanged hinge frame,
 # rather than rebuilding or sweeping every whole-engine occurrence per pose.
 h=A['throttle-moving'];hinge=attachment.static_frame(h['parent'],m['assemblies'])*b.Pos(*h['position_cad_mm'])*b.Rot(*h.get('rotation_cad_deg',[0,0,0]));moving=[]
 for k,o in O.items():
  parent=o['parent']
  while parent in A:
   if parent=='throttle-moving':moving.append(k);break
   parent=A[parent]['parent']
 motion=[]
 for angle in range(0,91,5):
  for n in moving:
   q=(inv*hinge*b.Rot(0,angle,0)*hinge.inverse()*poses[n])*loaddef(O[n]['definition'])
   for i in ['throttle-housing','iac-valve-body','iac-gasket','iac-end-plug']:
    v=overlap(parts[i],q)
    if v>1e-5:motion.append(dict(angle=angle,a=i,b=n,volume_mm3=v))
 # Only the new plug can add collision volume. Discover all current nearby
 # occurrences from meshes, then test it against actual CAD; body subset proof
 # above covers unchanged spatial neighbors without repeated engine sweeps.
 rb=bounds(plug);near={};mesh_boxes={}
 for k,o in O.items():
  if k in parts:continue
  ident=o['definition'];gp=ROOT/D[ident]['glb'].lstrip('/')
  if ident not in mesh_boxes:
   vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;mesh_boxes[ident]=(vv.min(0),vv.max(0))
  lo,hi=mesh_boxes[ident];loc=inv*poses[k];vv=np.array([tuple(b.Vertex(*p).moved(loc).center()) for p in itertools.product(*zip(lo,hi))])
  if np.all(vv.min(0)<=rb[1]+.2) and np.all(rb[0]<=vv.max(0)+.2):near[k]=local(k);track(gp)
 plug_neighbors=[dict(id=k,overlap_mm3=overlap(plug,s)) for k,s in near.items()];assert all(v['overlap_mm3']<1e-5 for v in plug_neighbors)
 retention={str(dx):overlap(b.Pos(dx,0,0)*plug,body) for dx in [-.1,.1]};assert min(retention.values())>3
 x,y=attachment_candidate.BOLTS[0];negative=dict(oversize_screw_mm3=overlap(b.Pos(x,y,0)*attachment_candidate.screw(3.1),body),lost_spring_seat_mm=(b.Pos(1,0,0)*parts[attachment.SPRING]).distance_to(plug));assert negative['oversize_screw_mm3']>.01 and negative['lost_spring_seat_mm']>.5
 lessons=json.loads((ROOT/'inventory/engine/iac-closure-learning.json').read_text())
 for k,v in closure.sources().items():assert m['sources'][k]==v
 for i in closure.CHANGED_IDS:assert closure.SUPERSEDED not in D[i]['unresolved'] and closure.CLOSURE_LIMIT in D[i]['unresolved']
 for k,v in lessons.items():
  assert k in D or k in O;assert set(v['sources'])<=set(m['sources'])
  for section in ['steps','troubleshooting']:
   for item in v.get(section,[]):
    if 'part' in item:assert item['part'] in O
 regenerated,calls=replay_chain(m,shapes);errors={i:difference(s,shapes[i]) for i,s in regenerated.items()};assert max(errors.values())<.02,errors
 shifted=copy.deepcopy(m);next(a for a in shifted['assemblies'] if a['id']=='throttle-assembly')['position_cad_mm'][0]-=17
 translated,_=replay_chain(shifted,shapes);shift_errors={i:difference(s,shapes[i]) for i,s in translated.items()};assert max(shift_errors.values())<.02
 stable=mp.read_bytes()==raw and all(sha(ROOT/p)==h for p,h in hashes.items());passed=stable and not collisions and not motion and not withdrawal
 relevant=set(parts)|set(near)|set(moving)
 report=dict(status='PASS' if passed else 'FAIL',installed=args.installed,manifest_sha256=sha(mp),adaptation_chain=record['adaptation_chain'],candidate_evidence=record['candidate_evidence'],part_bindings=checks,exports=exports,localized_body_proof=proof,attachment_contacts=contacts,closure_contacts=closure_contacts,port_obstruction_mm3=ports,internal_collisions=collisions,screw_withdrawal_collisions=withdrawal,throttle_motion_collisions=motion,throttle_motion_poses=19,throttle_moving_ids=moving,plug_neighbor_checks=plug_neighbors,retention_overlap_mm3=retention,negative_controls=negative,chain_replay_symmetric_difference_mm3=errors,translated_chain_replay_difference_mm3=shift_errors,chain_callback_order=calls,obsolete_gap_metadata_superseded=True,learning_references_valid=True,relevant_inputs_stable=stable,relevant_scope=installer.scoped(m,{O[k]['definition'] for k in relevant},relevant),artifact_sha256=hashes,limits=closure.GAPS)
 dest=ROOT/'inventory/engine/iac-closure-installed-validation.json' if args.installed else out/'validation.json';dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','localized_body_proof','internal_collisions','throttle_motion_collisions','screw_withdrawal_collisions','chain_replay_symmetric_difference_mm3','translated_chain_replay_difference_mm3']},indent=2));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
