#!/usr/bin/env python3
"""Check staged/current local plate retention and current all-occurrence sweep."""
from pathlib import Path
import argparse,copy,hashlib,itertools,json,sys
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_plate_fasteners_integration as integration
import throttle_plate_fasteners_candidate as candidate
from assembly_math import transforms
from cad_metrics import solid_volume

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def bb(q):z=q.bounding_box();return np.array([tuple(z.min),tuple(z.max)])
def overlap(a,z,pad=.2):return bool(np.all(a[0]<=z[1]+pad) and np.all(z[0]<=a[1]+pad))
def contact(q,r):
 total=0.
 for f in q.faces():
  for g in r.faces():
   if overlap(bb(f),bb(g),1e-6):
    x=f.intersect(g)
    if x:total+=x.area if hasattr(x,'area') else sum(v.area for v in x)
 return total

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stage-dir',type=Path);p.add_argument('--quick',action='store_true');args=p.parse_args()
 out=args.stage_dir.resolve() if args.stage_dir else ROOT/'cad/engine/generated/throttle-plate-fasteners-integration-stage'
 manifest_path=out/'full-assembly.json' if args.stage_dir else ROOT/'inventory/engine/full-assembly.json'
 record_path=out/'installation.json' if args.stage_dir else ROOT/'inventory/engine/throttle-plate-fasteners-installation.json'
 record=json.loads(record_path.read_text());out=out if args.stage_dir else ROOT/record['stage_directory'];m=json.loads(manifest_path.read_text());baseline=json.loads((out/'baseline-manifest.json').read_text())
 inputs={str(manifest_path.relative_to(ROOT)):sha(manifest_path),str(record_path.relative_to(ROOT)):sha(record_path)}
 for path in [Path(__file__),Path(candidate.__file__),Path(integration.__file__),ROOT/'cad/engine/assembly_math.py']:inputs[str(path.relative_to(ROOT))]=sha(path)
 assert sha(Path(__file__))==record['checker_sha256'] and sha(Path(integration.__file__))==record['adapter_sha256']
 assert sha(Path(candidate.__file__))==record['candidate_evidence']['candidate_source_sha256']
 if args.stage_dir:
  assert sha(manifest_path)==record['staged_manifest_sha256'];assert sha(out/'baseline-manifest.json')==record['before_manifest_sha256']
  for rel,h in record['staged_artifact_sha256'].items():assert sha(out/rel)==h
 else:
  for rel,h in record['canonical_artifact_sha256'].items():assert sha(ROOT/rel)==h
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};parent=integration.local_bindings(m['occurrences']);ids=set(record['changed_occurrences'])
 for oid,pos in integration.POSITIONS.items():
  o=O[oid];assert o['definition']==integration.SCREW and o['parent']==parent and o['position_cad_mm']==list(pos) and o.get('rotation_cad_deg',[0,0,0])==[0,0,0],oid
 # Global parents may move; local replaced/new occurrences must remain bound.
 for oid,o in record['installed_scope']['occurrences'].items():
  assert O[oid]==o,'Changed retained local occurrence: '+oid
 if args.stage_dir:
  for kind,allowed in [('definitions',integration.CHANGED_IDS),('occurrences',ids),('assemblies',set())]:
   assert {x['id']:x for x in baseline[kind] if x['id'] not in allowed}=={x['id']:x for x in m[kind] if x['id'] not in allowed},kind
 cache={};mesh_bounds={}
 def path(did,kind):
  if args.stage_dir and did in integration.CHANGED_IDS:return out/('step' if kind=='step' else 'models')/(did+('.step' if kind=='step' else '.glb'))
  return ROOT/D[did][kind].lstrip('/')
 def local(oid):
  did=O[oid]['definition']
  if did not in cache:
   pp=path(did,'step');inputs[str(pp.relative_to(ROOT))]=sha(pp);cache[did]=b.import_step(pp)
  return cache[did]
 shaft=local('throttle-shaft');plate=local('throttle-plate-1');screw=local(next(iter(integration.NEW_OCCURRENCES)))
 # Regeneration from already modified local parts proves geometric idempotence.
 again,_=candidate.parts(shaft,plate);idempotence={}
 for ident,q,r in [('shaft',shaft,again['throttle-shaft-plate-retention-illustrative']),('plate',plate,again['throttle-plate-drilled-illustrative'])]:idempotence[ident]=vol(q.cut(r))+vol(r.cut(q))
 # Scope proof against original stage-time local shaft preserves keyed linkage.
 for rel,h in record['baseline_step_sha256'].items():assert sha(out/rel)==h
 original=b.import_step(out/'baseline-step/throttle-shaft.step');allowed=[b.Pos(0,y,0)*candidate.cx(2.01,8) for y in [-35,-19,19,35]]
 outside=sum(vol(s.cut(*allowed)) for diff in [shaft.cut(original),original.cut(shaft)] for s in diff.solids())
 exports={}
 for did in integration.CHANGED_IDS:
  q=next(local(oid) for oid,o in O.items() if o['definition']==did);gp=path(did,'glb');inputs[str(gp.relative_to(ROOT))]=sha(gp);mesh=trimesh.load(gp,force='mesh');raw_vertices=len(mesh.vertices);mesh.merge_vertices(digits_vertex=8);v=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000
  exports[did]=dict(valid=q.is_valid,solids=len(q.solids()),watertight=mesh.is_watertight,position_weld_precision_m=1e-8,export_vertex_count=raw_vertices,welded_vertex_count=len(mesh.vertices),glb_bounds_error_mm=float(np.max(np.abs(np.array([v.min(0),v.max(0)])-bb(q)))))
 # Transform every occurrence's mesh bounds at all requested motion poses.
 # This broad phase includes moving neighbors, then exact STEP intersections.
 angles=[0,45,90] if args.quick else sorted(set(range(0,91,2))|{45});pose_tables={a:transforms(m,throttle_degrees=a) for a in angles};neighbors=set();moving_bounds={a:[bb(local(key).moved(poses[key])) for key in ids] for a,poses in pose_tables.items()}
 for oid,o in O.items():
  if oid in ids:continue
  did=o['definition']
  if did not in mesh_bounds:
   mesh=trimesh.load(path(did,'glb'),force='mesh');v=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;mesh_bounds[did]=np.array([v.min(0),v.max(0)])
  corners=list(itertools.product(*zip(*mesh_bounds[did])))
  for angle,poses in pose_tables.items():
   vv=np.array([tuple(b.Vertex(*v).moved(poses[oid]).center()) for v in corners]);bounds=np.array([vv.min(0),vv.max(0)])
   if any(overlap(bounds,z) for z in moving_bounds[angle]):neighbors.add(oid);break
 print('exact neighbors',sorted(neighbors),flush=True)
 springid='throttle-return-spring-illustrative'
 if springid in neighbors:
  import throttle_return_spring_candidate as spring
  inputs[str(Path(spring.__file__).relative_to(ROOT))]=sha(spring.__file__)
 collisions=[];sweep=[];exact=0
 for angle,poses in pose_tables.items():
  moving={oid:local(oid).moved(poses[oid]) for oid in ids};near={oid:local(oid).moved(poses[oid]) for oid in neighbors}
  if springid in near:near[springid]=spring.spring(angle).moved(poses[springid])
  for a,q in moving.items():
   for z,r in near.items():
    if overlap(bb(q),bb(r)):
     exact+=1;v=vol(q.intersect(r))
     if v>1e-5:collisions.append(dict(a=a,b=z,angle=angle,overlap_mm3=v))
  if angle==0:
   for (a,q),(z,r) in itertools.combinations(moving.items(),2):
    if overlap(bb(q),bb(r)):
     v=vol(q.intersect(r))
     if v>1e-5:collisions.append(dict(a=a,b=z,angle=angle,overlap_mm3=v))
  sweep.append(angle);print('pose',angle,'collisions',len(collisions),flush=True)
 contacts={};negative={};capture={}
 for oid,pos in integration.POSITIONS.items():
  q=b.Pos(*pos)*screw;index=oid.split('-')[3];pp=b.Pos(0,-27 if index=='1' else 27,0)*plate
  contacts[oid]=contact(q,pp);negative[oid]=contact(b.Pos(-5,0,0)*q,pp);capture[oid]=vol((b.Pos(-.125,0,0)*q).intersect(shaft))
 supports={str(y):contact(b.Pos(0,y,0)*plate,shaft) for y in [-27,27]}
 bad=copy.deepcopy(m['occurrences']);next(o for o in bad if o['id']=='throttle-plate-1')['position_cad_mm'][0]=1
 try:integration.local_bindings(bad);wrong_frame=False
 except ValueError:wrong_frame=True
 passed=not collisions and outside<1e-5 and max(idempotence.values())<1e-5 and min(contacts.values())>1 and max(negative.values())<1e-6 and min(capture.values())>.01 and min(supports.values())>1 and wrong_frame and all(e['valid'] and e['solids']==1 and e['watertight'] and e['glb_bounds_error_mm']<.2 for e in exports.values())
 assert all(sha(ROOT/pp)==h for pp,h in inputs.items()),'Input changed during check'
 report=dict(status='PASS' if passed else 'FAIL',scope='Four-screw educational hypothesis; no Ford count, pitch, locking, preload or strength claim.',full_sweep=not args.quick,angles_deg=sweep,manifest_sha256=sha(manifest_path),input_hashes=inputs,local_parent=parent,global_parent_rigid_shift_permitted=True,broad_phase_occurrences=len(O),exact_neighbors=sorted(neighbors),exact_pairs=exact,collisions=collisions,exports=exports,idempotent_symmetric_difference_mm3=idempotence,keyed_shaft_change_outside_seats_mm3=outside,head_plate_contact_mm2=contacts,rear_plate_support_mm2=supports,axial_withdrawal_capture_mm3=capture,displaced_head_negative_contact_mm2=negative,wrong_local_frame_rejected=wrong_frame)
 destination=out/'validation.json' if args.stage_dir else ROOT/'inventory/engine/throttle-plate-fasteners-installed-validation.json';destination.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],json.dumps(collisions[:20]));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
