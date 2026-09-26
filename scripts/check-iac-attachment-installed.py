#!/usr/bin/env python3
"""Strict stage/installed IAC binding, local interfaces, new neighbors and replay."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,itertools,json,sys
import build123d as b,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import iac_attachment_integration as adapter
import iac_attachment_candidate as candidate
from assembly_math import transforms
from cad_metrics import solid_volume

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
def difference(a,c):return vol(a-c)+vol(c-a)
def bounds(s):r=s.bounding_box();return np.array([tuple(r.min),tuple(r.max)])
def broad(a,c):x,y=bounds(a),bounds(c);return bool(np.all(x[0]<=y[1]+1e-6) and np.all(y[0]<=x[1]+1e-6))
def overlap(a,c):return vol(a.intersect(c)) if broad(a,c) else 0.
def contact(a,c):
 area=0.
 for f in a.faces():
  if f.geom_type!=b.GeomType.PLANE:continue
  for g in c.faces():
   if g.geom_type!=b.GeomType.PLANE or f.distance_to(g)>1e-6:continue
   common=f.intersect(g)
   if common:area+=common.area
 return area

def replay(manifest,shapes):
 data=copy.deepcopy(manifest);old={d['id']:d for d in data['definitions']};captured={}
 def define(ident,shape,name,function,system,color,sources,gaps,claims,prepared=False):
  assert prepared
  d=old[ident]
  for key,value in dict(name=name,function=function,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims).items():assert d.get(key,[])==value,(ident,key)
  data['definitions'].append(copy.deepcopy(d));captured[ident]=shape
 def add(ident,definition,parent,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
  d=old[definition];data['occurrences'].append(dict(id=ident,definition=definition,parent=parent,name=name or d['name'],function=d['function'],position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode)))
 def group(*args,**kwargs):raise AssertionError('IAC does not add assembly groups')
 adapter.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],shapes)
 for key in ['definitions','occurrences','assemblies']:assert data[key]==manifest[key],key
 return captured

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--installed',action='store_true');p.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/iac-attachment-integration-stage');args=p.parse_args();stage=args.stage_dir.resolve()
 mp=ROOT/'inventory/engine/full-assembly.json' if args.installed else stage/'full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);record=json.loads((ROOT/'inventory/engine/iac-attachment-installation.json' if args.installed else stage/'installation.json').read_text())
 if not args.installed:assert sha(mp)==record['staged_manifest_sha256']
 for key,path in [('installer_sha256','scripts/install-iac-attachment.py'),('checker_sha256','scripts/check-iac-attachment-installed.py'),('adapter_sha256','cad/engine/iac_attachment_integration.py'),('learning_sha256','inventory/engine/iac-attachment-learning.json')]:assert sha(ROOT/path)==record[key],path
 spec=importlib.util.spec_from_file_location('iac_installer',ROOT/'scripts/install-iac-attachment.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
 assert installer.validate_candidate(m,already=True)==record['candidate_evidence']
 assert installer.scoped(m,adapter.CHANGED_IDS,record['changed_occurrences'])==record['installed_scope'],'Relevant installed definitions/poses changed'
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m);frame=adapter.static_frame('idle-air',m['assemblies']);inv=frame.inverse();shapes={};hashes={};checks=[]
 def track(path):hashes[str(path.relative_to(ROOT))]=sha(path);return path
 def loaddef(ident):
  if ident not in shapes:
   path=ROOT/D[ident]['step'].lstrip('/') if args.installed or ident not in adapter.CHANGED_IDS else stage/'step'/(ident+'.step');shapes[ident]=b.import_step(track(path))
  return shapes[ident]
 def local(oid,ps=poses):return (inv*ps[oid])*loaddef(O[oid]['definition'])
 reference_root=ROOT/'cad/engine/generated/iac-attachment-candidate'
 for ident in sorted(adapter.CHANGED_IDS):
  actual=loaddef(ident);gp=ROOT/D[ident]['glb'].lstrip('/') if args.installed else stage/'models'/(ident+'.glb');sp=ROOT/D[ident]['step'].lstrip('/') if args.installed else stage/'step'/(ident+'.step')
  declared=record['canonical_artifact_sha256'] if args.installed else record['staged_artifact_sha256']
  for path in [sp,gp]:assert sha(path)==declared[str(path.relative_to(ROOT if args.installed else stage))];track(path)
  oid='iac-mount-screw-1-estimated' if ident==adapter.SCREW else ident
  reference=b.import_step(track(reference_root/(oid+'.step')));placed=local(oid);delta=difference(placed,reference);shift=difference(b.Pos(1,0,0)*placed,reference)
  assert actual.is_valid and len(actual.solids())==1 and delta<.02 and shift>1,(ident,delta,shift)
  mesh=trimesh.load(gp,force='mesh');raw_vertex_count=len(mesh.vertices);mesh.merge_vertices(digits_vertex=8);assert mesh.nondegenerate_faces().all() and mesh.unique_faces().all();vv=np.array(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;err=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bounds(actual))))
  assert mesh.is_watertight and err<.2,(ident,err)
  assert max(abs(np.diff(bounds(actual),axis=0)[0]-np.array(D[ident]['model_bounds_mm'])))<.01
  checks.append(dict(id=ident,symmetric_difference_mm3=delta,shift_control_mm3=shift,mesh_bounds_error_mm=err,watertight_after_position_weld=True,export_vertex_count=raw_vertex_count,welded_vertex_count=len(mesh.vertices),position_weld_precision_m=1e-8))
 for i,(x,y) in enumerate(candidate.BOLTS,1):
  o=O[f'iac-mount-screw-{i}-estimated'];assert o['definition']==adapter.SCREW and o['parent']=='idle-air' and o['position_cad_mm']==[x,y,0] and o['rotation_cad_deg']==[0,0,0]
 assert len([o for o in O.values() if o['definition']==adapter.SCREW])==2
 assert O[adapter.SPRING]['parent']=='idle-air' and O[adapter.SPRING]['position_cad_mm']==[0,0,0]
 for prior in record['before_occurrences']:
  if prior['id'] in adapter.NEW_OCCURRENCES:continue
  for key in ['parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:assert O[prior['id']].get(key)==prior.get(key)
 parts={k:local(k) for k in O if k.startswith('iac-')};parts['throttle-housing']=local('throttle-housing');collisions=[]
 for a,c in itertools.combinations(parts,2):
  value=overlap(parts[a],parts[c])
  if value>1e-5:collisions.append(dict(a=a,b=c,volume_mm3=value))
 contacts={}
 for a,c in [('iac-mount-screw-1-estimated','iac-valve-body'),('iac-mount-screw-2-estimated','iac-valve-body'),('iac-gasket','iac-valve-body'),('iac-gasket','throttle-housing'),(adapter.SPRING,'iac-end-plug'),(adapter.SPRING,'iac-pintle')]:contacts[a+' / '+c]=dict(gap_mm=parts[a].distance_to(parts[c]),area_mm2=contact(parts[a],parts[c]))
 assert all(r['gap_mm']<1e-5 and r['area_mm2']>.01 for r in contacts.values())
 assert parts['iac-armature'].distance_to(parts['iac-pintle'])<1e-5
 ports=[sum(overlap(candidate.zc(4.9,-16,-7,x,0),parts[k]) for k in ['iac-valve-body','iac-gasket','throttle-housing']) for x in [-12,12]];assert max(ports)<1e-5
 # Discover neighbors from every current manifest mesh, including relocated intake.
 lo=np.min([bounds(s)[0] for s in parts.values()],axis=0)-10;hi=np.max([bounds(s)[1] for s in parts.values()],axis=0)+[10,10,45];near={};mesh_boxes={}
 for k,o in O.items():
  if k in parts:continue
  ident=o['definition'];gp=ROOT/D[ident]['glb'].lstrip('/')
  if ident not in mesh_boxes:
   vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;mesh_boxes[ident]=(vv.min(0),vv.max(0))
  low,high=mesh_boxes[ident];loc=inv*poses[k];corners=np.array([tuple(b.Vertex(*v).moved(loc).center()) for v in itertools.product(*zip(low,high))])
  if np.all(corners.min(0)<=hi+.2) and np.all(lo<=corners.max(0)+.2):near[k]=local(k);track(gp)
 changed_parts=adapter.REPLACED|adapter.NEW_OCCURRENCES;neighbors=[]
 for k in changed_parts:
  for n,s in near.items():
   value=overlap(parts[k],s)
   if value>1e-5:neighbors.append(dict(a=k,b=n,volume_mm3=value))
 throttle=[]
 for angle in range(0,91,5):
  ps=transforms(m,throttle_degrees=angle)
  for n in near:
   if adapter.frame_error(ps[n],poses[n])<1e-8:continue
   moving=local(n,ps)
   for k in changed_parts:
    value=overlap(parts[k],moving)
    if value>1e-5:throttle.append(dict(angle=angle,a=k,b=n,volume_mm3=value))
 withdrawal=[]
 for dz in [0,5,10,20,30,40]:
  for k in ['iac-mount-screw-1-estimated','iac-mount-screw-2-estimated']:
   moved=b.Pos(0,0,dz)*parts[k]
   for n,s in {**near,**parts}.items():
    if n==k:continue
    value=overlap(moved,s)
    if value>1e-5:withdrawal.append(dict(lift_mm=dz,a=k,b=n,volume_mm3=value))
 x,y=candidate.BOLTS[0];negative=dict(oversize_screw_mm3=overlap(b.Pos(x,y,0)*candidate.screw(3.1),parts['iac-valve-body'])+overlap(b.Pos(x,y,0)*candidate.screw(3.1),parts['throttle-housing']),lost_spring_seat_mm=(b.Pos(1,0,0)*parts[adapter.SPRING]).distance_to(parts['iac-end-plug']))
 assert negative['oversize_screw_mm3']>.01 and negative['lost_spring_seat_mm']>.5
 for key,value in adapter.sources().items():assert m['sources'][key]==value
 lessons=json.loads((ROOT/'inventory/engine/iac-attachment-learning.json').read_text())
 for key,lesson in lessons.items():
  assert key in D or key in O;assert set(lesson['sources'])<=set(m['sources'])
  for section in ['steps','troubleshooting']:
   for entry in lesson.get(section,[]):
    if 'part' in entry:assert entry['part'] in O
 captured=replay(m,shapes);errors={k:difference(s,shapes[k]) for k,s in captured.items()};assert max(errors.values())<.02,errors
 # A synthetic entire-subtree shift must leave every emitted definition unchanged.
 shifted=copy.deepcopy(m);next(a for a in shifted['assemblies'] if a['id']=='throttle-assembly')['position_cad_mm'][0]-=17
 translated=replay(shifted,shapes);translation_errors={k:difference(s,shapes[k]) for k,s in translated.items()};assert max(translation_errors.values())<.02
 stable=mp.read_bytes()==raw and all(sha(ROOT/path)==h for path,h in hashes.items())
 passed=stable and not collisions and not neighbors and not throttle and not withdrawal
 report=dict(status='PASS' if passed else 'FAIL',installed=args.installed,scope='Artifact-bound educational IAC interfaces and current spatial neighbors; not browser/manufacturing acceptance',manifest_sha256=sha(mp),candidate_evidence=record['candidate_evidence'],parts=checks,internal_collisions=collisions,neighbor_collisions=neighbors,throttle_motion_collisions=throttle,screw_withdrawal_collisions=withdrawal,contacts=contacts,port_obstruction_mm3=ports,negative_controls=negative,replay_symmetric_difference_mm3=errors,translated_subtree_replay_difference_mm3=translation_errors,learning_references_valid=True,relevant_inputs_stable=stable,neighbor_ids=sorted(near),relevant_pose_snapshot=installer.scoped(m,{O[k]['definition'] for k in set(parts)|set(near)},set(parts)|set(near)),input_artifact_sha256=hashes,limits=adapter.GAPS)
 dest=ROOT/'inventory/engine/iac-attachment-installed-validation.json' if args.installed else stage/'validation.json';dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','installed','parts','internal_collisions','neighbor_collisions','throttle_motion_collisions','screw_withdrawal_collisions','replay_symmetric_difference_mm3','translated_subtree_replay_difference_mm3']},indent=2));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
