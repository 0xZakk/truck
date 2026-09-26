#!/usr/bin/env python3
"""Verify staged/current cable shape equivalence and recheck changed nearby pairs."""
from pathlib import Path
import argparse,json,hashlib,itertools,sys,copy
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_cable_integration as integration
import throttle_cable_candidate as candidate
from assembly_math import transforms
from cad_metrics import solid_volume,support_bounds

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def bb(q):x=q.bounding_box();return np.array([tuple(x.min),tuple(x.max)])
def overlap(a,z):return bool(np.all(a[0]<=z[1]+1e-6) and np.all(z[0]<=a[1]+1e-6))
def mapped(v,p):return np.array([tuple(b.Vertex(*x).moved(p).center()) for x in v])
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage-dir',type=Path);args=parser.parse_args();out=args.stage_dir.resolve() if args.stage_dir else ROOT/'cad/engine/generated/throttle-cable-integration-stage';mp=out/'full-assembly.json' if args.stage_dir else ROOT/'inventory/engine/full-assembly.json';rp=out/'installation.json' if args.stage_dir else ROOT/'inventory/engine/throttle-cable-installation.json'
 record=json.loads(rp.read_text());out=out if args.stage_dir else ROOT/record['stage_directory'];m=json.loads(mp.read_text());baseline=json.loads((out/'baseline-manifest.json').read_text());r=json.loads((ROOT/'inventory/engine/throttle-cable-candidate-validation.json').read_text());assert r['status']=='PASS' and r['full_sweep'];inputs={str(p.relative_to(ROOT)):sha(p) for p in [mp,rp,Path(__file__),Path(integration.__file__),Path(candidate.__file__),ROOT/'inventory/engine/throttle-cable-candidate-validation.json',ROOT/'viewer/throttle-cable-motion.json',ROOT/'viewer/throttle-cable-motion.js']}
 assert sha(Path(__file__))==record['checker_sha256'];assert sha(integration.__file__)==record['adapter_sha256'];assert sha(ROOT/'viewer/throttle-cable-motion.json')==record['motion_table_sha256'];assert sha(ROOT/'viewer/throttle-cable-motion.js')==record['motion_module_sha256'];assert inputs['inventory/engine/throttle-cable-candidate-validation.json']==record['candidate_evidence']['candidate_report_sha256']
 for rel,h in (record['staged_artifact_sha256'] if args.stage_dir else record['canonical_artifact_sha256']).items():assert sha((out if args.stage_dir else ROOT)/rel)==h
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};integration.local_bindings(m['occurrences'])
 for oid in integration.NEW_IDS:
  o=O[oid];assert o['definition']==oid and o['parent']=='throttle-assembly' and o['position_cad_mm']==[0,0,0] and o.get('rotation_cad_deg',[0,0,0])==[0,0,0] and o['throttle_cable']==dict(model='illustrative-cable-v1',kind=integration.KINDS[oid])
 for oid,o in record['installed_scope']['occurrences'].items():assert O[oid]==o,'Local cable frame changed: '+oid
 cache={}
 def path(did,kind):return out/('step' if kind=='step' else 'models')/(did+('.step' if kind=='step' else '.glb')) if args.stage_dir and did in integration.CHANGED_IDS else ROOT/D[did][kind].lstrip('/')
 def local(oid):
  did=O[oid]['definition']
  if did not in cache:
   p=path(did,'step');inputs[str(p.relative_to(ROOT))]=sha(p);cache[did]=b.import_step(p)
  return cache[did]
 original=b.import_step(out/'baseline-step/accelerator-cable-bracket.step');expected={};equivalence={};exports={}
 # Compare both shapes after STEP serialization. Coincident periodic spherical
 # seams differ between raw CAD and STEP normalization; their raw boolean
 # subtraction is unreliable. The reviewed STEP exports are hash-bound inputs.
 for did in integration.CHANGED_IDS:
  name='accelerator-cable-bracket-cable-proposal' if did==integration.BRACKET else did;reference=ROOT/'cad/engine/generated/throttle-cable-candidate'/(name+'.step');rel=str(reference.relative_to(ROOT));assert sha(reference)==r['output_hashes'][rel];inputs[rel]=sha(reference);expected[did]=b.import_step(reference)
 for did,q in expected.items():
  actual=local(did);equivalence[did]=vol(actual.cut(q))+vol(q.cut(actual));gp=path(did,'glb');inputs[str(gp.relative_to(ROOT))]=sha(gp);mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);v=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bounds=bb(actual);raw=float(np.max(np.abs(np.array([v.min(0),v.max(0)])-bounds)));method='OCC bounding box'
  if raw>=.2:
   box=support_bounds(actual);bounds=np.array([tuple(box.min),tuple(box.max)]);method='Exact planar supports'
  exports[did]=dict(valid=actual.is_valid,solids=len(actual.solids()),watertight=mesh.is_watertight,position_weld_precision_m=1e-8,raw_occ_bounds_error_mm=raw,bounds_method=method,bounds_error_mm=float(np.max(np.abs(np.array([v.min(0),v.max(0)])-bounds))))
 protected=b.Pos(394,95,490)*b.Box(33,70,100);protected_change=sum(vol(s.intersect(protected)) for diff in [original.cut(local(integration.BRACKET)),local(integration.BRACKET).cut(original)] for s in diff.solids())
 # Exercise the complete adapter twice without exports: no duplicate IDs or
 # unrelated inventory mutation, in addition to exact bracket idempotence.
 test_defs=copy.deepcopy(m['definitions']);test_occ=copy.deepcopy(m['occurrences']);test_shapes={key:local(key) for key in integration.CHANGED_IDS}
 def test_define(ident,shape,name,function,group,color,sources,gaps,claims,prepared=False):test_defs.append(dict(id=ident,name=name,function=function));test_shapes[ident]=shape
 def test_add(ident,definition,parent,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):test_occ.append(dict(id=ident,definition=definition,parent=parent,position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode),name=name))
 for repeat in range(2):integration.install(test_define,test_add,test_defs,test_occ,copy.deepcopy(m['assemblies']),test_shapes)
 b.export_step(test_shapes[integration.BRACKET],out/'idempotence-bracket.step');repeated=b.import_step(out/'idempotence-bracket.step');idempotence=vol(repeated.cut(local(integration.BRACKET)))+vol(local(integration.BRACKET).cut(repeated))
 adapter_idempotent=len(test_defs)==len(D)==len({x['id'] for x in test_defs}) and len(test_occ)==len(O)==len({x['id'] for x in test_occ}) and [x for x in test_defs if x['id'] not in integration.CHANGED_IDS]==[x for x in m['definitions'] if x['id'] not in integration.CHANGED_IDS] and [x for x in test_occ if x['id'] not in integration.CHANGED_IDS]==[x for x in m['occurrences'] if x['id'] not in integration.CHANGED_IDS]
 angles=[row['angle_deg'] for row in r['poses']];pose_tables={a:transforms(m,throttle_degrees=a) for a in angles};parent=pose_tables[0]['throttle-housing'];corners=mapped(itertools.product([377,491],[60,126],[450,528]),parent);region=np.array([corners.min(0),corners.max(0)]);selected=set();mesh_bounds={}
 for oid,o in O.items():
  if oid in integration.CHANGED_IDS:continue
  did=o['definition']
  if did not in mesh_bounds:
   gp=path(did,'glb');inputs[str(gp.relative_to(ROOT))]=sha(gp);v=np.asarray(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*[1,-1,1]*1000;mesh_bounds[did]=np.array([v.min(0),v.max(0)])
  for a in angles:
   v=mapped(itertools.product(*zip(*mesh_bounds[did])),pose_tables[a][oid]);bounds=np.array([v.min(0),v.max(0)])
   if overlap(bounds,region):selected.add(oid);break
 # Bind original exact proof to current parts and poses, including rigid parent
 # shifts: compare each neighbor relative to the throttle housing parent.
 proof=record['candidate_proof_scope'];assert proof['snapshot_sha256']==r['final_current_neighbor_addendum']['baseline_snapshot_sha256'];changed=set(selected)-set(r['exact_neighbor_ids']);probe=[(0,0,0),(1,0,0),(0,1,0),(0,0,1)]
 for oid in selected:
  p=path(O[oid]['definition'],'step');inputs[str(p.relative_to(ROOT))]=sha(p)
  if r['input_hashes'].get(D[O[oid]['definition']]['step'].lstrip('/'))!=sha(p):changed.add(oid)
 for angle,poses in pose_tables.items():
  before=proof['relative_pose_probes'][str(angle)]
  for oid in selected:
   if oid not in before or not np.allclose(mapped(probe,poses['throttle-housing'].inverse()*poses[oid]),np.asarray(before[oid]),atol=1e-8,rtol=0):changed.add(oid)
 collisions=[];exact=0
 if changed:
  import throttle_return_spring_candidate as spring
  for angle,poses in pose_tables.items():
   parts=candidate.stationary()|candidate.moving(angle)[0]|{integration.BRACKET:local(integration.BRACKET)};parts={k:q.moved(poses['throttle-housing']) for k,q in parts.items()}
   for oid in changed:
    neighbor=spring.spring(angle).moved(poses['throttle-housing']) if oid=='throttle-return-spring-illustrative' else local(oid).moved(poses[oid])
    for key,q in parts.items():
     if overlap(bb(q),bb(neighbor)):
      exact+=1;volume=vol(q.intersect(neighbor))
      if volume>1e-5:collisions.append(dict(angle=angle,a=key,b=oid,overlap_mm3=volume))
  print('Affected current neighbors',sorted(changed),'exact pairs',exact,flush=True)
 negative=json.loads(json.dumps(m['occurrences']));next(o for o in negative if o['id']==integration.BRACKET)['position_cad_mm'][0]=1
 try:integration.local_bindings(negative);rejected=False
 except ValueError:rejected=True
 wrong_shape=local('throttle-cable-socket-illustrative').moved(b.Pos(1,0,0));reference=expected['throttle-cable-socket-illustrative'];negative_shape_difference=vol(wrong_shape.cut(reference))+vol(reference.cut(wrong_shape))
 passed=negative_shape_difference>1 and adapter_idempotent and max(equivalence.values())<1e-5 and idempotence<1e-5 and protected_change<1e-5 and rejected and not collisions and all(e['valid'] and e['solids']==1 and e['watertight'] and e['bounds_error_mm']<.2 for e in exports.values())
 assert all(sha(ROOT/p)==h for p,h in inputs.items()),'Input changed during scoped check'
 report=dict(status='PASS' if passed else 'FAIL',scope='Illustrative cable integration; exact candidate equivalence plus original47-pose proof and affected-current-neighbor checks. Browser acceptance still required.',manifest_sha256=sha(mp),manifest_hash_captured_in_input_at_start=inputs[str(mp.relative_to(ROOT))],input_hashes=inputs,definitions=len(D),occurrences=len(O),candidate_equivalence_symmetric_difference_mm3=equivalence,equivalence_method='Both actual and reviewed shapes imported from hash-bound STEP exports; no raw/normalized coincident spherical seam comparison',bracket_idempotence_symmetric_difference_mm3=idempotence,protected_anchor_region_change_mm3=protected_change,exports=exports,all_occurrences_broad_phased=True,selected_neighbors=sorted(selected),changed_neighbors_exactly_rechecked=sorted(changed),additional_exact_pairs=exact,collisions=collisions,inherited_candidate_exact_pairs=r['exact_collision_pair_evaluations'],inherited_angles_deg=angles,adapter_twice_inventory_idempotent=adapter_idempotent,negative_wrong_local_frame_rejected=rejected,negative_displaced_socket_shape_difference_mm3=negative_shape_difference,ancestor_rigid_shift_supported=True,historical_temporal_limit=r['final_current_neighbor_addendum']['original_checker_manifest_sha256_field_means'])
 dest=out/'validation.json' if args.stage_dir else ROOT/'inventory/engine/throttle-cable-installed-validation.json';dest.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],equivalence,exports,flush=True);raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
