#!/usr/bin/env python3
"""Scoped staged/installed EVR binding, neighbor and discrete-pose audit."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys,itertools
import numpy as np,build123d as b,trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import evr,evr_mechanism_candidate as candidate,evr_mechanism_integration as adapter
import iac_attachment_integration as frames
from assembly_math import transforms
from cad_metrics import solid_volume,support_bounds
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
def difference(a,d):return vol(a-d)+vol(d-a)
def overlap(a,d):
 aa=a.bounding_box();dd=d.bounding_box()
 if any(tuple(aa.max)[i]<tuple(dd.min)[i]-1e-7 or tuple(dd.max)[i]<tuple(aa.min)[i]-1e-7 for i in range(3)):return 0.
 op=BRepAlgoAPI_Common(a.wrapped,d.wrapped);op.Build();assert op.IsDone(),'CAD common failed'
 return 0. if op.Shape().IsNull() else vol(b.Compound(op.Shape()))
def replay(m):
 data=copy.deepcopy(m);old={d['id']:d for d in m['definitions']};shapes={}
 def define(i,s,n,f,system,color,sources,gaps,claims,prepared=False):
  assert prepared;d=copy.deepcopy(old[i]);d.update(name=n,function=f,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims);data['definitions'].append(d);shapes[i]=s
 def add(i,d,p,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
  row=next(x for x in data['definitions'] if x['id']==d);data['occurrences'].append(dict(id=i,definition=d,parent=p,name=name or row['name'],function=row['function'],position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode)))
 def group(*a,**k):raise AssertionError('No new groups')
 adapter.install(define,add,group,data['definitions'],data['occurrences'],data['assemblies'],shapes)
 for kind in ['definitions','occurrences','assemblies']:
  assert len(data[kind])==len({r['id'] for r in data[kind]});assert {r['id']:r for r in data[kind]}=={r['id']:r for r in m[kind]},'Idempotence '+kind
 return data,shapes

def main():
 p=argparse.ArgumentParser();p.add_argument('--installed',action='store_true');p.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/evr-mechanism-integration-stage');args=p.parse_args();out=args.stage_dir.resolve()
 mp=ROOT/'inventory/engine/full-assembly.json' if args.installed else out/'full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);rec=json.loads((ROOT/'inventory/engine/evr-mechanism-installation.json' if args.installed else out/'installation.json').read_text())
 spec=importlib.util.spec_from_file_location('evr_installer',ROOT/'scripts/install-evr-mechanism.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
 assert installer.evidence()==rec['candidate_evidence'];assert installer.scoped(m,rec['guard_occurrences'])==rec['installed_scope']
 for q,h in rec['input_sha256'].items():assert sha(ROOT/q)==h,q
 for q,h in rec['neighbor_artifact_sha256'].items():assert sha(ROOT/q)==h,q
 assert sha(out/'before.json')==rec['baseline_snapshot_sha256'];before=json.loads((out/'before.json').read_text());installer.assert_scope(before,m)
 if not args.installed:
  assert sha(mp)==rec['staged_manifest_sha256']
  current=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());assert installer.scoped(current,list(rec['input_scope']['occurrences']))==rec['input_scope']
  for q,h in rec['original_artifact_sha256'].items():assert sha(ROOT/q)==h,q
 else:current=m
 assert adapter.neighbor_ids(current)==rec['neighbor_ids'],'New/changed spatial neighbor requires restaging'
 declared=rec['canonical_artifact_sha256'] if args.installed else rec['staged_artifact_sha256']
 for q,h in declared.items():assert sha((ROOT if args.installed else out)/q)==h,q
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m);inv=poses['evr-body'].inverse();shapes={};bindings={};exports={}
 for ident in sorted(adapter.CHANGED_IDS):
  sp=ROOT/D[ident]['step'].lstrip('/') if args.installed else out/'step'/(ident+'.step');gp=ROOT/D[ident]['glb'].lstrip('/') if args.installed else out/'models'/(ident+'.glb');s=b.import_step(sp);shapes[ident]=s
  assert frames.frame_error(inv*poses[ident],b.Location())<1e-6,ident
  ref=b.import_step(ROOT/f'cad/engine/generated/evr-mechanism-candidate/{ident}.step');delta=difference(s,ref);assert delta<.02,(ident,delta)
  mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.unique_faces().all() and mesh.nondegenerate_faces().all(),ident
  box=support_bounds(s);vv=np.array(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(box.min),tuple(box.max)]))));assert err<.2 and s.is_valid and len(s.solids())==1
  assert np.max(abs(np.array(list(box.size))-np.array(D[ident]['model_bounds_mm'])))<.01
  bindings[ident]=delta;exports[ident]=dict(watertight=True,bounds_error_mm=err)
 # Original baseline geometry and all original placements are explicit inputs.
 baseline_refs=candidate.build(.8) if adapter.SOURCE_IDS[0] in before['sources'] else {i:v[0] for i,v in evr.parts().items()}
 baseline_deltas={i:difference(b.import_step(out/'baseline'/(i+'.step')),baseline_refs[i]) for i in adapter.REPLACED};assert max(baseline_deltas.values())<.02
 neighbors={k:b.import_step(ROOT/D[O[k]['definition']]['step'].lstrip('/')).moved(inv*poses[k]) for k in rec['neighbor_ids']};hits=[]
 for i,s in shapes.items():
  for k,t in neighbors.items():
   value=overlap(s,t)
   if value>1e-5:hits.append(dict(part=i,neighbor=k,volume_mm3=value))
 assert not hits,hits
 _,replayed=replay(m)
 moved=copy.deepcopy(m);a=next(x for x in moved['assemblies'] if x['id']=='egr-vacuum-regulator');a['position_cad_mm']=[13,-7,5];a['rotation_cad_deg']=[0,0,17]
 _,shifted=replay(moved);replay_deltas={i:abs(vol(replayed[i])-vol(shifted[i])) for i in adapter.CHANGED_IDS};assert max(replay_deltas.values())<1e-6
 bad=copy.deepcopy(m);next(o for o in bad['occurrences'] if o['id']=='evr-cap')['position_cad_mm'][0]+=.5
 try:replay(bad)
 except ValueError:pose_fault=True
 else:pose_fault=False
 assert pose_fault
 motion_dir=ROOT/'models/engine/evr-motion' if args.installed else out/'motion';data=json.loads((motion_dir/'poses.json').read_text());assert [r['travel_mm'] for r in data['poses']]==[0,.2,.4,.6,.8]
 motion=[]
 for row in data['poses']:
  index=row['index'];t=row['travel_mm'];gp=motion_dir/f'spring-{index}.glb';sp=ROOT/f'cad/engine/generated/evr-motion/spring-{index}.step' if args.installed else motion_dir/f'spring-{index}.step';assert sha(gp)==row['spring_sha256'] and sha(sp)==row['step_sha256']
  spring=b.import_step(sp);expected=candidate.spring(t);delta=difference(spring,expected);assert delta<.02
  disc=b.Pos(0,0,.8-t)*shapes['evr-disc-illustrative'];assert difference(disc,candidate.moving(t)['evr-disc-illustrative'])<.001
  assert row['disc_offset_cad_mm']==[0,0,.8-t] and np.max(abs(np.array(row['disc_offset_viewer_m'])-np.array([0,(.8-t)/1000,0])))<1e-12
  for k,neighbor in neighbors.items():assert overlap(spring,neighbor)<1e-5 and overlap(disc,neighbor)<1e-5,(t,k)
  mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight
  motion.append(dict(index=index,travel_mm=t,spring_symmetric_difference_mm3=delta,watertight=True))
 assert installer.evidence()==rec['candidate_evidence'] and mp.read_bytes()==raw
 for q,h in rec['input_sha256'].items():assert sha(ROOT/q)==h,q
 for q,h in rec['neighbor_artifact_sha256'].items():assert sha(ROOT/q)==h,q
 result=dict(status='PASS',installed=args.installed,scope='Source-bound illustrative EVR; no factory calibration or browser acceptance',candidate_evidence=rec['candidate_evidence'],bindings_mm3=bindings,original_geometry_binding_mm3=baseline_deltas,exports=exports,neighbor_ids=rec['neighbor_ids'],neighbor_collisions=hits,replay_volume_delta_mm3=replay_deltas,changed_relative_pose_rejected=pose_fault,motion=motion,input_sha256=rec['input_sha256'],relevant_inputs_stable=True)
 rp=ROOT/'inventory/engine/evr-mechanism-installed-validation.json' if args.installed else out/'validation.json';rp.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
