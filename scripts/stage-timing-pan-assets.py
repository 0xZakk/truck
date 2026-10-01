#!/usr/bin/env python3
"""Guarded local assets and in-memory manifest patch; no canonical writes."""
from pathlib import Path
import sys,json,hashlib,copy,shutil
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'));sys.path.insert(0,str(R/'scripts'))
import build123d as b
import trimesh
from assembly_math import transforms
from timing_cover_attachment_v2 import RELOCATIONS
from oil_pan_joint_v9_candidate import STATIONS
from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('seal_stage',R/'scripts/stage-front-seal-2692-assets.py');helper=module_from_spec(spec);spec.loader.exec_module(helper)
O=R/'cad/engine/generated/timing-pan-integration-stage';O.mkdir(exist_ok=True)
sha=helper.sha;bounds=helper.bounds;watched={}
def watch(p):watched[p]=sha(p);return watched[p]
def check_bindings(path):
 obj=json.loads(path.read_text());watch(path)
 for name,expected in helper.bindings(obj):
  p=R/name
  assert p.exists() and sha(p)==expected,'Stale bound evidence: '+name
  watched[p]=expected
 return obj
manifest=R/'inventory/engine/full-assembly.json';watch(manifest);m=json.loads(manifest.read_text());poses=transforms(m);occ={q['id']:q for q in m['occurrences']};defs={q['id']:q for q in m['definitions']}
proof_paths=['inventory/engine/timing-pan-expanded-seat-v2-candidate-validation.json','inventory/engine/timing-front-expanded-seat-v3-pair.json','inventory/engine/timing-pan-perimeter-contact-summary.json','inventory/engine/timing-pan-upper-contact-summary.json']
proofs={p:check_bindings(R/p) for p in proof_paths}
base=R/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate';fast=R/'cad/engine/generated/pan-fastener-thread-candidate';frozen=R/'cad/engine/generated/timing-cover-attachment-v2'
for p in [Path(__file__),R/'scripts/stage-front-seal-2692-assets.py',R/'cad/engine/assembly_math.py',R/'cad/engine/timing_cover_attachment_v2.py',R/'cad/engine/oil_pan_joint_v9_candidate.py']:watch(p)
# Compute occurrence-local proposals from the actual ancestor transform; never assume identity.
new=copy.deepcopy(m);proposal=[]
for q in new['occurrences']:
 for number,world in RELOCATIONS.items():
  if q['id'] in [f'oil-pan-mounting-screw-{number}',f'oil-pan-mounting-washer-{number}']:
   old=occ[q['id']];local=b.Pos(*old['position_cad_mm'])*b.Rot(*old['rotation_cad_deg']);parent=poses[q['id']]*local.inverse();target=parent.inverse()*b.Pos(*world);t=target.wrapped.Transformation();rot=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);assert np.max(abs(rot-np.eye(3)))<1e-10
   q['position_cad_mm']=[t.Value(i,4)for i in range(1,4)];q['rotation_cad_deg']=[0,0,0];proposal.append({'id':q['id'],'before':old,'after':copy.deepcopy(q),'world_target_mm':list(world)})
newposes=transforms(new);assert len(proposal)==10
# Local source hardware is checked against the frozen world occurrence before export.
specs=[('oil-pan',base/'pan.step',base/'pan.glb',poses['oil-pan']),('oil-pan-molded-gasket',base/'pan-gasket.step',base/'pan-gasket.glb',poses['oil-pan-molded-gasket']),('oil-pan-mounting-screw',fast/'pan-screw.step',fast/'pan-screw.glb',b.Location()),('oil-pan-mounting-washer',R/'cad/engine/generated/oil-pan-mounting-washer.step',R/'models/engine/oil-pan-mounting-washer.glb',b.Location())]
rows=[];staged={};changes=[]
for identity,sp,gp,pose in specs:
 watch(sp);watch(gp);source=b.import_step(sp);local=pose.inverse()*source
 t=pose.wrapped.Transformation();rotation=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);assert np.max(abs(rotation-np.eye(3)))<1e-10;translation=np.array([t.Value(i,4)for i in range(1,4)])
 outstep=O/(identity+'.step');b.export_step(local,outstep);read=b.import_step(outstep);assert read.is_valid and len(read.solids())==len(source.solids()) and len(read.faces())==len(source.faces());volume_error=abs(read.volume-source.volume);assert volume_error<.1
 error=float(np.max(abs(bounds(pose*read)-bounds(source))));assert error<.01
 mesh=trimesh.load(gp,force='mesh');offset=translation[[0,2,1]]*[1,1,-1]/1000;mesh_local=mesh.copy();mesh_local.vertices-=offset;outglb=O/(identity+'.glb');trimesh.Scene(mesh_local).export(outglb);back=trimesh.load(outglb,force='mesh');assert np.array_equal(back.faces,mesh.faces) and back.is_winding_consistent
 welded=back.copy();welded.merge_vertices(digits_vertex=8);assert welded.is_watertight and welded.is_winding_consistent
 if identity!='oil-pan-mounting-washer':assert back.is_watertight
 mesh_error=float(np.max(abs(back.vertices+offset-mesh.vertices)))*1000;assert mesh_error<.01
 row={'id':identity,'source_step':str(sp.relative_to(R)),'source_coordinate_frame':'world' if identity in ['oil-pan','oil-pan-molded-gasket'] else 'definition-local','localization_translation_mm':translation.tolist(),'step_world_bounds_error_mm':error,'mesh_world_vertex_error_mm':mesh_error,'volume_roundtrip_error_mm3':volume_error,'raw_mesh_watertight':bool(back.is_watertight),'welded_mesh_watertight':bool(welded.is_watertight),'solids':len(read.solids()),'faces':len(read.faces()),'triangles':len(back.faces),'step':str(outstep.relative_to(R)),'step_sha256':sha(outstep),'glb':str(outglb.relative_to(R)),'glb_sha256':sha(outglb)}
 rows.append(row);staged[identity]=read
 # Canonical paths stay stable; root applies guarded asset copies separately.
 before=defs[identity];after=copy.deepcopy(before);after.update(volume_mm3=read.volume,solid_count=len(read.solids()),triangle_count=len(back.faces),model_bounds_mm=list(bounds(read)[1]-bounds(read)[0]))
 after['unresolved']=list(before.get('unresolved',[]))+['Coordinated timing candidate: estimated revised front seat and five relocated pan axes. Lower/upper contact evidence is bounded; overhangs, rear-cap ownership, production dimensions, pressure sealing and browser acceptance remain unresolved.']
 if identity!='oil-pan-mounting-washer':changes.append({'id':identity,'before':before,'after':after,'copy_assets':{'step':{'from':row['step'],'to':before['step'].lstrip('/'),'sha256':row['step_sha256']},'glb':{'from':row['glb'],'to':before['glb'].lstrip('/'),'sha256':row['glb_sha256']}}})
 print(identity,'localized',flush=True)
# Existing washers must remain geometrically identical to frozen candidate washer definition.
oldwasher=b.import_step(fast/'existing-pan-washer.step');watch(fast/'existing-pan-washer.step');w=staged['oil-pan-mounting-washer'];assert np.max(abs(bounds(w)-bounds(oldwasher)))<1e-8 and abs(w.volume-oldwasher.volume)<1e-7
assert sum(abs(s.volume)for s in w.cut(oldwasher).solids())<1e-7 and sum(abs(s.volume)for s in oldwasher.cut(w).solids())<1e-7
# All25 actual world poses, plus direct comparison with each frozen relocated STEP.
pose_rows=[]
for number,original in enumerate(STATIONS,1):
 target=RELOCATIONS.get(number,original)
 for kind in ['screw','washer']:
  identity='oil-pan-mounting-'+kind;oid=identity+'-'+str(number);placed=newposes[oid]*staged[identity];t=newposes[oid].wrapped.Transformation();xyz=np.array([t.Value(i,4)for i in range(1,4)]);assert np.max(abs(xyz-target))<1e-8
  row={'id':oid,'world_position_mm':xyz.tolist(),'parent_preserved':occ[oid]['parent']==next(q for q in new['occurrences']if q['id']==oid)['parent'],'relocated':number in RELOCATIONS}
  if number in RELOCATIONS:
   sp=frozen/(oid+'.step');watch(sp);expected=b.import_step(sp);e=float(np.max(abs(bounds(placed)-bounds(expected))));ve=abs(placed.volume-expected.volume);assert e<.01 and ve<.01 and len(placed.faces())==len(expected.faces());row.update(frozen_world_bounds_error_mm=e,frozen_world_volume_error_mm3=ve,face_count=len(placed.faces()))
  else:assert next(q for q in new['occurrences']if q['id']==oid)==occ[oid]
  pose_rows.append(row)
# Pose-specific proof reuse is guarded; old overall FAIL is deliberately not promoted.
panproof=proofs[proof_paths[0]];pair=proofs[proof_paths[1]]
assert len(panproof['retained_20_stations'])==20 and len(panproof['hardware_tool_and_separation'])==5 and pair['local_status']=='PASS'
assert all(r[k]<.01 for r in panproof['retained_20_stations'] for k in ['male_pan_overlap_mm3','washer_pan_overlap_mm3','washer_seat_missing_mm3','gasket_seat_missing_mm3'])
assert all(r[k]<.01 for r in panproof['hardware_tool_and_separation'] for k in ['screw_overlap_mm3','washer_overlap_mm3','seat_missing_mm3','nominal_tool_overlap_mm3'])
# Coordinate/patch fault controls.
pan_pose=poses['oil-pan'];double_error=float(np.max(abs(bounds(pan_pose*pan_pose*staged['oil-pan'])-bounds(b.import_step(base/'pan.step')))));assert double_error>90
wrong_pose_error=max(abs(np.array(occ['oil-pan-mounting-screw-20']['position_cad_mm'])-np.array(RELOCATIONS[20])));assert wrong_pose_error>20
assert all(sha(p)==expected for p,expected in watched.items())
patch={'schema':'truck-guarded-integration-proposal-v1','scope':'Uninstalled pan/gasket/threaded screw asset replacements plus10 poses; washer definition unchanged','manifest_sha256':watched[manifest],'definitions':changes,'occurrences':proposal,'preserved_occurrences':[occ['oil-pan'],occ['oil-pan-molded-gasket']],'requirements':['Reject if manifest hash or any before object differs.','Copy only hash-verified staged assets; never apply world STEP directly to local canonical paths.','Apply all10 pose changes together with coordinated block/cover/seal changes owned by root.','Preserve all IDs/parents and remaining20 screw/washer poses.','Existing explosion stages retained but not revalidated for whole assembly.']}
patchpath=R/'inventory/engine/timing-pan-integration-patch.json';patchpath.write_text(json.dumps(patch,indent=2)+'\n')
r={'status':'PASS serialized local-coordinate stage; not installed','parts':rows,'all_25_screw_washer_poses':pose_rows,'proof_reuse':{'pan_report_status_retained':panproof['local_status'],'retained_20_fasteners':'PASS reused after input bindings','relocated_5_fasteners_tools_seats':'PASS reused after pose/world-shape comparison','block_v3_pair':pair['local_status'],'lower_upper_contact':'Bounded evidence only; original full-face failures retained'},'controls':{'double_pan_placement_error_mm':double_error,'old_station20_pose_error_mm':float(wrong_pose_error)},'inputs':{str(p.relative_to(R)):h for p,h in watched.items()},'patch':str(patchpath.relative_to(R)),'patch_sha256':sha(patchpath),'canonical_modified':False,'limits':['No installation/browser pass','Rear cap ownership remains illustrative','Whole-fluid containment/pressure/production dimensions unresolved','Existing explosion stages not revalidated for entireassembly']}
(R/'inventory/engine/timing-pan-integration-stage-validation.json').write_text(json.dumps(r,indent=2)+'\n')
