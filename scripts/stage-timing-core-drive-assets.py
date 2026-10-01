#!/usr/bin/env python3
"""Hash-guarded neutral core stage plus separate conditional drive proposal."""
from pathlib import Path
import sys,json,hashlib,copy,importlib.util
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import trimesh
from assembly_math import transforms
from timing_coupled_core_candidate import AXIS,MOVING,STATIONARY
from cad_metrics import solid_volume
spec=importlib.util.spec_from_file_location('stagehelper',R/'scripts/stage-front-seal-2692-assets.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
O=R/'cad/engine/generated/timing-core-drive-integration-stage';O.mkdir(exist_ok=True)
sha=h.sha;bounds=h.bounds;watched={}
def watch(p):watched[p]=sha(p)
def bind(p):
 watch(p);r=json.loads(p.read_text())
 for name,v in h.bindings(r):
  path=R/name;assert path.exists()and sha(path)==v,name;watched[path]=v
 return r
manifest=R/'inventory/engine/full-assembly.json';watch(manifest);m=json.loads(manifest.read_text());occ={x['id']:x for x in m['occurrences']};defs={x['id']:x for x in m['definitions']};assemblies={x['id']:x for x in m['assemblies']};oldposes=transforms(m)
proofs={}
for name in ['cam-composed-drive-proof-binding','cam-composed-drive-delivery','timing-coupled-core-candidate-validation','crank-clockwise-candidate-validation','crank-clockwise-render-review','crossed-oil-drive-endplay-review','crossed-oil-drive-direction-review']:
 proofs[name]=bind(R/'inventory/engine'/(name+'.json'))
for p in [Path(__file__),R/'scripts/stage-front-seal-2692-assets.py',R/'cad/engine/assembly_math.py',R/'cad/engine/timing_coupled_core_candidate.py']:watch(p)
delta=np.array([0,AXIS[0]-90,AXIS[1]-72]);new=copy.deepcopy(m);group_changes=[];occ_changes=[]
for a in new['assemblies']:
 if a['id'] in ['cam-motion','cam-retention-assembly']:
  before=copy.deepcopy(a);a['position_cad_mm']=(np.array(a['position_cad_mm'])+delta).tolist();group_changes.append({'id':a['id'],'before':before,'after':copy.deepcopy(a)})
for o in new['occurrences']:
 if o['id'] in [f'cam-bearing-{i}'for i in range(1,5)]+['rear-cam-plug']:
  before=copy.deepcopy(o);o['position_cad_mm']=(np.array(o['position_cad_mm'])+delta).tolist();occ_changes.append({'id':o['id'],'before':before,'after':copy.deepcopy(o)})
poses=transforms(new);rows=[];staged={};definition_changes=[]
ids=['crankshaft']+sorted(MOVING|set(STATIONARY)|{'crank-timing-gear'})
for oid in ids:
 identity=occ[oid]['definition'];pose=poses[oid]
 folder=R/'cad/engine/generated'/('crank-clockwise-candidate'if oid=='crankshaft'else 'cam-composed-drive-candidate'if oid=='camshaft'else 'timing-coupled-core-candidate')
 sp=folder/(oid+'.step');gp=folder/(oid+'.glb')
 # Composed cam has world STEP and definition-local GLB explicitly.
 local_mesh=oid=='camshaft'
 if local_mesh:gp=folder/'camshaft-local.glb'
 watch(sp);watch(gp);source=b.import_step(sp);local=pose.inverse()*source
 t=pose.wrapped.Transformation();rot=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);translation=np.array([t.Value(i,4)for i in range(1,4)])
 repeated=identity in staged
 if repeated:
  read=b.import_step(O/(identity+'.step'));same=solid_volume(read.cut(local))+solid_volume(local.cut(read));assert same<1e-5,(identity,same)
 else:
  outstep=O/(identity+'.step');b.export_step(local,outstep);read=b.import_step(outstep);staged[identity]=read;same=0
  original=trimesh.load(gp,force='mesh');v=original.vertices[:,[0,2,1]]*[1,-1,1]*1000
  lv=v if local_mesh else (v-translation)@rot
  mesh=trimesh.Trimesh(lv[:,[0,2,1]]*[1,1,-1]/1000,original.faces,process=False);mesh.export(O/(identity+'.glb'))
 assert read.is_valid and len(read.solids())==len(source.solids()) and len(read.faces())==len(source.faces())
 restored=pose*read;step_error=float(np.max(abs(bounds(restored)-bounds(source))));assert step_error<.01
 volume_error=abs(read.volume-source.volume);assert volume_error<.1
 mesh=trimesh.load(O/(identity+'.glb'),force='mesh');welded=mesh.copy();welded.merge_vertices(digits_vertex=8);assert welded.is_watertight and welded.is_winding_consistent and welded.volume>0
 lv=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;wv=lv@rot.T+translation;original=trimesh.load(gp,force='mesh');ov=original.vertices[:,[0,2,1]]*[1,-1,1]*1000
 if local_mesh:ov=ov@rot.T+translation
 if not repeated:
  assert np.array_equal(mesh.faces,original.faces);vertex_error=float(np.max(abs(wv-ov)));assert vertex_error<.01
 else:vertex_error=None
 world_bounds_error=float(np.max(abs(np.array([wv.min(0),wv.max(0)])-bounds(source))));assert world_bounds_error<.15
 row={'occurrence':oid,'definition':identity,'source_world_step':str(sp.relative_to(R)),'target_world_matrix':[[t.Value(i,j)for j in range(1,5)]for i in range(1,4)],'step_world_bounds_error_mm':step_error,'mesh_world_bounds_error_mm':world_bounds_error,'mesh_world_vertex_error_mm':vertex_error,'volume_roundtrip_error_mm3':volume_error,'repeated_definition_difference_mm3':same,'solids':len(read.solids()),'faces':len(read.faces())};rows.append(row)
 if not repeated:
  before=defs[identity];after=copy.deepcopy(before);after.update(volume_mm3=read.volume,solid_count=len(read.solids()),triangle_count=len(mesh.faces),model_bounds_mm=list(bounds(read)[1]-bounds(read)[0]));after['unresolved']=list(before.get('unresolved',[]))+['Coordinated corrected-direction timing candidate. Dimensions retain source/estimate limits; full assembly, corrected motion implementation and browser acceptance remain pending.']
  definition_changes.append({'id':identity,'before':before,'after':after,'copy_assets':{ext:{'from':str((O/(identity+'.'+ext)).relative_to(R)),'to':before['step'if ext=='step'else'glb'].lstrip('/'),'sha256':sha(O/(identity+'.'+ext))}for ext in ['step','glb']}})
 print(oid,'staged',flush=True)
# Conditional drive branch; source geometry only, no implied external attachment pass.
branch=copy.deepcopy(new);branch_groups=[]
for a in branch['assemblies']:
 if a['id'] in ['distributor-assembly','oil-pump-assembly','oil-drive-assembly']:
  before=copy.deepcopy(a);a['position_cad_mm']=(np.array(a['position_cad_mm'])+delta).tolist();branch_groups.append({'id':a['id'],'before':before,'after':copy.deepcopy(a)})
bposes=transforms(branch);identity='distributor-drive-gear';p=R/'cad/engine/generated/crossed-oil-drive-corrected-pair/distributor-drive-gear-local.step';gp=p.with_suffix('.glb');watch(p);watch(gp)
source=b.import_step(p);local=b.Pos(0,0,-85)*source;b.export_step(local,O/(identity+'.step'));read=b.import_step(O/(identity+'.step'));assert read.is_valid and len(read.solids())==1
mesh=trimesh.load(gp,force='mesh');mesh.vertices[:,1]-=.085;mesh.export(O/(identity+'.glb'));back=trimesh.load(O/(identity+'.glb'),force='mesh');assert back.is_watertight
import oil_drive_layout as drive
expected=b.Pos(*delta)*drive.GEAR_FRAME*source;actual=bposes[identity]*read;branch_error=float(np.max(abs(bounds(actual)-bounds(expected))));assert branch_error<.01
before=defs[identity];after=copy.deepcopy(before);after.update(volume_mm3=read.volume,solid_count=1,triangle_count=len(back.faces),model_bounds_mm=list(bounds(read)[1]-bounds(read)[0]));after['unresolved']=list(before.get('unresolved',[]))+['Estimated corrected tooth lead. Connected drive translation and endplay phase are conditional on external pickup/outlet/clamp interface resolution.']
bdef={'id':identity,'before':before,'after':after,'copy_assets':{ext:{'from':str((O/(identity+'.'+ext)).relative_to(R)),'to':before['step'if ext=='step'else'glb'].lstrip('/'),'sha256':sha(O/(identity+'.'+ext))}for ext in ['step','glb']}}
map_path=R/'inventory/engine/timing-integration-map.json';watch(map_path);mapping=json.loads(map_path.read_text());branch_rows=[]
for group,children in mapping['rigid_drive_hypothesis']['groups'].items():
 for oid in children:
  expected=b.Pos(*delta)*oldposes[oid];a=bposes[oid].wrapped.Transformation();z=expected.wrapped.Transformation();error=max(abs(a.Value(i,j)-z.Value(i,j))for i in range(1,4)for j in range(1,5));assert error<1e-9;branch_rows.append({'id':oid,'matrix_error':error,'parent_preserved':True})
for oid in mapping['external_drive_dependencies']['oil-pickup-assembly']:
 a=bposes[oid].wrapped.Transformation();z=oldposes[oid].wrapped.Transformation();assert max(abs(a.Value(i,j)-z.Value(i,j))for i in range(1,4)for j in range(1,5))<1e-10
requirements=['Neutral serialization only; current canonical motion tags still need root corrected crank/cam/endplay implementation.','Preserve existing IDs, parents, explode fields and stationary thrust hardware.','Coordinate block/frontjoint and valvetrain/spring assets owned by other stages; this patch alone is not an installation.']
core={'schema':'truck-guarded-integration-proposal-v1','scope':'Ready neutral core serialization only','manifest_sha256':watched[manifest],'definitions':definition_changes,'assemblies':group_changes,'occurrences':occ_changes,'requirements':requirements,'motion_contract':{'event':'q crank event degrees','crank':'−q about +X','cam':'q/2 + degrees(K*x) about +X; x∈[−0.1,0]mm','stationary':list(STATIONARY)}}
conditional={'schema':'truck-guarded-integration-proposal-v1','scope':'CONDITIONAL drive branch, not ready installation','manifest_sha256':watched[manifest],'definitions':[bdef],'assemblies':branch_groups,'occurrences':[],'requires_core_patch':True,'unresolved':['Pickup inlet endpoint is not moved: connection displacement equals DELTA; tube rerouting or another coordinated solution required','Pump outlet/block oil path not established','Distributor clamp/seat, harness and ignition wire reach need coordinated checks','Pump foot candidate supports require exact chosen block binding','Pickup/screen pan-floor placement must not be inferred from branch rigid translation'],'motion_contract':{'distributor_intermediate_inner':'−q/2 + degrees((1/18−K)*x)','pump_outer':'4/5 of inner rotor angle','no_distributor_axial_translation':True}}
patches={}
for name,obj in [('core',core),('conditional-drive',conditional)]:
 p=R/f'inventory/engine/timing-{name}-integration-patch.json';p.write_text(json.dumps(obj,indent=2)+'\n');patches[str(p.relative_to(R))]=sha(p)
assert all(sha(p)==v for p,v in watched.items())
r={'status':'PASS local serialization, branch conditional','core_parts':rows,'definition_count':len(definition_changes),'conditional_branch_occurrences':branch_rows,'distributor_original_frame_reconstruction_error_mm':branch_error,'pickup_unmoved_connection_displacement_mm':float(np.linalg.norm(delta)),'input_sha256':{str(p.relative_to(R)):v for p,v in watched.items()},'patches_sha256':patches,'canonical_modified':False}
(R/'inventory/engine/timing-core-drive-stage-review.json').write_text(json.dumps(r,indent=2)+'\n')
