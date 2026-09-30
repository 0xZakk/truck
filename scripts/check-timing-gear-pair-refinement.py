#!/usr/bin/env python3
"""Interior-only refinement, with explicit exact tooth-ring proof inheritance."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import timing_gear_pair_candidate as base
import timing_gear_pair_refinement as c
from cad_metrics import solid_volume
STUDY=ROOT/'cad/engine/generated/timing-gear-pair-candidate';OUT=ROOT/'cad/engine/generated/timing-gear-pair-refined';OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
proof_path=ROOT/'inventory/engine/timing-gear-pair-candidate-validation.json';proof=json.loads(proof_path.read_text());assert proof['status'].startswith('PASS independent'),proof['status']
contact_path=ROOT/'inventory/engine/timing-gear-contact-diagnostic.json';contact=json.loads(contact_path.read_text());assert contact['status'].startswith('PASS')
watched=[Path(__file__),Path(c.__file__),Path(base.__file__),ROOT/'cad/engine/cad_metrics.py',proof_path,contact_path]+[STUDY/(key+'.step') for key in ['crank','cam']]
inputs={str(p.relative_to(ROOT)):sha(p) for p in watched}
for p,h in proof['inputs_sha256'].items():assert sha(ROOT/p)==h,p
for key in ['crank','cam']:assert sha(STUDY/(key+'.step'))==proof['exports'][key]['step_sha256']
for p,h in contact['input_sha256'].items():assert sha(ROOT/p)==h,p
frozen={key:b.import_step(STUDY/(key+'.step')) for key in ['crank','cam']};parts=c.parts(frozen);checks={};preview={}
for key,q in parts.items():
 assert q.is_valid and len(q.solids())==1
 teeth=base.PARAMS[key+'_teeth'];root=base.PARAMS['transverse_module_mm']*(teeth/2-1.25)
 # A purely subtractive change entirely below root cannot change tooth sweeps.
 removed=frozen[key].cut(q);added=q.cut(frozen[key]);guard=c.cylinder_x(root-.05,20)
 escaped=b.Compound(children=list(removed.solids())).cut(guard)
 assert not added.solids() and not escaped.solids()
 sp=OUT/(key+'.step');b.export_step(q,sp);r=b.import_step(sp);assert r.is_valid and len(r.solids())==1
 v,f=q.tessellate(.05,.1);vertices=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(vertices[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(key+'.glb');mesh.export(gp);actual_mesh=trimesh.load(gp,force='mesh');actual_mesh.merge_vertices(digits_vertex=8);assert actual_mesh.is_watertight and actual_mesh.nondegenerate_faces().all() and actual_mesh.unique_faces().all()
 vv=np.asarray(actual_mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();bounds_error=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert bounds_error<.15
 checks[key]=dict(step_sha256=sha(sp),glb_sha256=sha(gp),valid=True,solids=1,watertight=True,glb_bounds_error_mm=bounds_error,step_volume_error_mm3=abs(vol(q)-vol(r)),removed_volume_mm3=vol(removed),added_solids=0,removed_material_outside_protected_inner_radius_solids=0,protected_inner_radius_mm=root-.05,triangles=len(mesh.faces))
 if key=='cam':vertices+=np.array([0,*base.CAM_YZ])
 preview[key+'_vertices']=vertices;preview[key+'_faces']=np.asarray(f)
np.savez_compressed(OUT/'render-input.npz',**preview)
assert inputs=={str(p.relative_to(ROOT)):sha(p) for p in watched}
r=dict(status='PASS interior refinement; inherited independent pair diagnostics; UNINSTALLED',inputs_sha256=inputs,parameters=c.PARAMS,exports=checks,inherited_sweep=dict(report_sha256=sha(proof_path),samples=len(proof['sweep']),zero_overlap=all(x['overlap_mm3']<1e-5 for x in proof['sweep']),basis='Exact no-added-material and removed-material containment entirely below each tooth root; outer tooth rings identical.'),inherited_contact_diagnostic=dict(report_sha256=sha(contact_path),brackets=contact['brackets']),limits=['Shoulder/key/mark dimensions and relative indexing are estimates from one identified replacement photograph.','Crank keyway is new illustrative geometry; no matching shaft slot/key engagement is established.','Current cam axis and cover incompatibilities are not repaired. No installed/browser acceptance.'])
(ROOT/'inventory/engine/timing-gear-pair-refinement-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
