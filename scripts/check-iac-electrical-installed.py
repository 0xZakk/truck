#!/usr/bin/env python3
"""Electrical binding with explicit final attachment/closure coexistence."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,itertools,json,sys
import build123d as b,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import iac_electrical_integration as adapter
import iac_electrical_candidate as candidate
import iac_attachment_integration as attachment
import iac_closure_integration as closure
from assembly_math import transforms
from cad_metrics import solid_volume

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
def difference(a,c):return vol(a-c)+vol(c-a)
def bounds(s):r=s.bounding_box();return np.array([tuple(r.min),tuple(r.max)])
def overlap(a,c):
 x,y=bounds(a),bounds(c)
 return vol(a.intersect(c)) if np.all(x[0]<=y[1]+1e-6) and np.all(y[0]<=x[1]+1e-6) else 0.
def area(a,c,kind=b.GeomType.PLANE):
 result=0.
 for f in a.faces():
  if f.geom_type!=kind:continue
  for g in c.faces():
   if g.geom_type!=kind or f.distance_to(g)>1e-6:continue
   q=f.intersect(g)
   if q:result+=q.area
 return result

def replay(m,shapes,chain=True):
 data=copy.deepcopy(m);old={d['id']:d for d in m['definitions']};work=dict(shapes);calls=[]
 def define(i,s,n,f,system,color,sources,gaps,claims,prepared=False):
  assert prepared
  d=copy.deepcopy(old[i]);d.update(name=n,function=f,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims);data['definitions'].append(d);work[i]=s;calls.append(i)
 def add(i,d,p,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
  row=next(x for x in data['definitions'] if x['id']==d);data['occurrences'].append(dict(id=i,definition=d,parent=p,name=name or row['name'],function=row['function'],position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode)))
 def group(*a,**k):raise AssertionError('No new groups')
 if chain:
  attachment.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],work)
  closure.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],work)
 adapter.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],work)
 for key in ['definitions','occurrences','assemblies']:
  assert len(data[key])==len({r['id'] for r in data[key]})
  assert {r['id']:r for r in data[key]}=={r['id']:r for r in m[key]},'Replay metadata '+key
 ids=adapter.CHANGED_IDS|(closure.CHANGED_IDS if chain else set())
 return {i:difference(work[i],shapes[i]) for i in ids},calls

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--installed',action='store_true');p.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/iac-electrical-integration-stage');args=p.parse_args();out=args.stage_dir.resolve()
 mp=ROOT/'inventory/engine/full-assembly.json' if args.installed else out/'full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);record=json.loads((ROOT/'inventory/engine/iac-electrical-installation.json' if args.installed else out/'installation.json').read_text())
 if not args.installed:assert sha(mp)==record['staged_manifest_sha256']
 assert sha(ROOT/'cad/engine/cad_metrics.py')==record['metrics_sha256']
 for key,path in [('installer_sha256','scripts/install-iac-electrical.py'),('checker_sha256','scripts/check-iac-electrical-installed.py'),('adapter_sha256','cad/engine/iac_electrical_integration.py'),('learning_sha256','inventory/engine/iac-electrical-learning.json')]:assert sha(ROOT/path)==record[key]
 spec=importlib.util.spec_from_file_location('electrical_installer',ROOT/'scripts/install-iac-electrical.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
 assert installer.evidence(args.installed)==record['candidate_evidence'];assert installer.scoped(m,set(record['installed_scope']['definitions']),record['guard_occurrences'])==record['installed_scope']
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m);frame=attachment.static_frame('idle-air',m['assemblies']);inv=frame.inverse();shapes={};hashes={}
 def track(p):hashes[str(p.relative_to(ROOT))]=sha(p);return p
 def loaddef(i):
  if i not in shapes:
   path=ROOT/D[i]['step'].lstrip('/') if args.installed or i not in adapter.GEOMETRY_IDS else out/'step'/(i+'.step');shapes[i]=b.import_step(track(path))
  return shapes[i]
 def local(i):return (inv*poses[i])*loaddef(O[i]['definition'])
 parts={k:local(k) for k in O if k.startswith('iac-')};parts['throttle-housing']=local('throttle-housing');parts['efi-upper-intake']=local('efi-upper-intake');checks=[]
 # The body and plug are bound to final closure candidate. All remaining
 # attachment solids retain their known reference, rather than waiving hashes.
 refs={i:('iac-electrical-candidate',i) for i in adapter.CHANGED_IDS}
 refs.update({i:('iac-closure-candidate',i) for i in closure.GEOMETRY_IDS})
 refs.update({('iac-mount-screw-1-estimated' if i==attachment.SCREW else i):('iac-attachment-candidate','iac-mount-screw-1-estimated' if i==attachment.SCREW else i) for i in attachment.CHANGED_IDS-closure.GEOMETRY_IDS})
 for oid,(folder,name) in refs.items():
  ref=b.import_step(track(ROOT/'cad/engine/generated'/folder/(name+'.step')));delta=difference(parts[oid],ref);bad=difference(b.Pos(1,0,0)*parts[oid],ref);assert delta<.02 and bad>1,(oid,delta,bad)
  checks.append(dict(id=oid,symmetric_difference_mm3=delta,translation_fault_mm3=bad,reference=f'{folder}/{name}.step'))
 original=json.loads((ROOT/'cad/engine/generated/iac-electrical-candidate/validation.json').read_text())['relevant_pose_snapshot']
 old_frame=attachment.static_frame('idle-air',list(original['assemblies'].values()))
 for oid,o in original['occurrences'].items():
  old_local=old_frame.inverse()*attachment.occurrence_frame(o,list(original['assemblies'].values()))
  assert attachment.frame_error(inv*poses[oid],old_local)<1e-6,'Changed original electrical relative pose '+oid
 exports={}
 for i in adapter.GEOMETRY_IDS:
  sp=ROOT/D[i]['step'].lstrip('/') if args.installed else out/'step'/(i+'.step');gp=ROOT/D[i]['glb'].lstrip('/') if args.installed else out/'models'/(i+'.glb');declared=record['canonical_artifact_sha256'] if args.installed else record['staged_artifact_sha256']
  for path in [sp,gp]:assert sha(path)==declared[str(path.relative_to(ROOT if args.installed else out))];track(path)
  mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.nondegenerate_faces().all() and mesh.unique_faces().all()
  vv=np.array(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;s=loaddef(i);err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-bounds(s))));assert err<.2 and s.is_valid and len(s.solids())==1
  assert np.max(abs(np.diff(bounds(s),axis=0)[0]-np.array(D[i]['model_bounds_mm'])))<.01
  exports[i]=dict(mesh_bounds_error_mm=err,watertight_after_position_weld=True)
 collisions=[]
 for a,c in itertools.combinations(parts,2):
  v=overlap(parts[a],parts[c])
  if v>1e-5:collisions.append(dict(a=a,b=c,volume_mm3=v))
 term=[parts[i] for i in candidate.TERMINALS];cap=parts['iac-connector-cap'];coil=parts['iac-coil'];carrier=parts['iac-coil-carrier-estimated'];body=parts['iac-valve-body'];plug=parts['iac-end-plug'];spring=parts[attachment.SPRING]
 contacts=dict(terminal_coil_mm2=[area(t,coil) for t in term],carrier_body_mm2=area(carrier,body),carrier_cap_mm2=area(carrier,cap),spring_plug_mm2=area(spring,plug),spring_pintle_mm2=area(spring,parts['iac-pintle']),closure_axial_mm2=area(body,plug),closure_radial_mm2=area(body,plug,b.GeomType.CYLINDER))
 assert min(contacts['terminal_coil_mm2'])>.28 and min(contacts[k] for k in contacts if k!='terminal_coil_mm2')>1
 assert contacts['closure_axial_mm2']>77 and contacts['closure_radial_mm2']>39
 isolation=dict(terminal_separation_mm=term[0].distance_to(term[1]),case_gaps_mm=[t.distance_to(parts['iac-solenoid-can']) for t in term]);assert isolation['terminal_separation_mm']>1 and min(isolation['case_gaps_mm'])>3
 retention=[overlap(b.Pos(dx,0,0)*t,cap) for t in term for dx in [-1,1]];assert min(retention)>4
 gauge=candidate.mating_witness();correct=overlap(gauge,cap)+sum(overlap(gauge,t) for t in term);reverse=overlap(b.Rot(180,0,0)*gauge,cap)
 bridge=b.Pos(76,0,0)*b.Box(1,1,4.6);short=[overlap(bridge,t) for t in term];opened=term[0]-b.Pos(32.9,0,0)*b.Box(65.8,30,30);open_gap=opened.distance_to(coil)
 faults=dict(correct_key_overlap_mm3=correct,reversed_key_overlap_mm3=reverse,bridge_contact_mm3=short,open_tail_gap_mm=open_gap);assert correct<1e-5 and reverse>3 and min(short)>.6 and open_gap>.2
 motion={str(dx):sum(overlap(b.Pos(dx,0,0)*parts['iac-armature'],parts[i]) for i in adapter.CHANGED_IDS) for dx in np.linspace(-1,1,5)};assert max(motion.values())<1e-5
 # Closure and attachment retained geometry have already passed their full
 # port/fastener/throttle sweeps. Exact binding above plus contained electrical
 # envelope isolates the changed region; rerun each affected electrical pair.
 envelope=candidate.cx(12,24,70)+b.Pos(75,0,0)*b.Box(10,14,12);outside={i:vol(parts[i]-envelope) for i in adapter.CHANGED_IDS};assert max(outside.values())<1e-5
 lessons=json.loads((ROOT/'inventory/engine/iac-electrical-learning.json').read_text())
 for k,v in adapter.sources().items():assert m['sources'][k]==v
 for k,v in lessons.items():
  assert k in D and set(v['sources'])<=set(m['sources'])
  for section in ['steps','troubleshooting']:
   for item in v.get(section,[]):
    if 'part' in item:assert item['part'] in O
 errors,calls=replay(m,shapes);assert max(errors.values())<.02,errors
 standalone,_=replay(m,shapes,False);assert max(standalone.values())<.02
 shifted=copy.deepcopy(m);next(a for a in shifted['assemblies'] if a['id']=='throttle-assembly')['position_cad_mm'][0]-=17
 translated,_=replay(shifted,shapes);assert max(translated.values())<.02
 rotated=copy.deepcopy(m);parent=next(a for a in rotated['assemblies'] if a['id']=='throttle-assembly');parent.setdefault('rotation_cad_deg',[0,0,0])[2]+=13
 rotated_errors,_=replay(rotated,shapes);assert max(rotated_errors.values())<.02
 bad=copy.deepcopy(m);next(o for o in bad['occurrences'] if o['id']=='iac-connector-cap')['position_cad_mm'][0]+=.5
 rejected=False
 try:replay(bad,shapes,False)
 except ValueError as e:rejected='relative frame' in str(e)
 assert rejected,'Changed component datum was not rejected'
 stable=mp.read_bytes()==raw and all(sha(ROOT/p)==h for p,h in hashes.items());passed=stable and not collisions
 report=dict(status='PASS' if passed else 'FAIL',installed=args.installed,manifest_sha256=sha(mp),candidate_evidence=record['candidate_evidence'],adaptation_chain=record['adaptation_chain'],part_bindings=checks,exports=exports,contacts=contacts,isolation=isolation,terminal_withdrawal_overlap_mm3=retention,negative_controls=faults,armature_motion_overlap_mm3=motion,internal_and_intake_collisions=collisions,existing_envelope_outside_mm3=outside,full_chain_replay_difference_mm3=errors,standalone_replay_difference_mm3=standalone,translated_chain_replay_difference_mm3=translated,rotated_chain_replay_difference_mm3=rotated_errors,changed_cap_frame_rejected=rejected,chain_callback_order=calls,learning_references_valid=True,relevant_inputs_stable=stable,artifact_sha256=hashes,limits=adapter.GAPS)
 dest=ROOT/'inventory/engine/iac-electrical-installed-validation.json' if args.installed else out/'validation.json';dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','contacts','internal_and_intake_collisions','full_chain_replay_difference_mm3','translated_chain_replay_difference_mm3']},indent=2));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
