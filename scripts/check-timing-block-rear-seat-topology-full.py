#!/usr/bin/env python3
"""Full isolated block proof: original CAD, direct mesh, and explicit readback agreement."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np,trimesh
import timing_block_rear_seat_topology_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-rear-seat-topology-candidate';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
proofpath=ROOT/'inventory/engine/timing-block-fixed-stock-validation.json';proof=json.loads(proofpath.read_text());inputs=dict(proof['input_sha256']);assert inputs=={p:sha(ROOT/p) for p in inputs}
for p in [Path(__file__),Path(c.__file__),proofpath,ROOT/'cad/engine/timing_block_rear_seat_repair_candidate.py',ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate/block.step']:inputs[str(p.relative_to(ROOT))]=sha(p)
stages=[]
def stage(name,q):
 row={'name':name,'valid_original_cad':q.is_valid,'solids':len(q.solids())};stages.append(row);print(row,flush=True)
q,edits=c.regenerate(stage=stage);sp=OUT/'block.step';b.export_step(q,sp);rt=b.import_step(sp);old=b.import_step(ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate/block.step')
def difference(a,d):
 # Preserve exact Boolean topology for the verification operation too.
 with b.SkipClean():extra=a.cut(d);missing=d.cut(a)
 return {'extra_mm3':vol(extra),'missing_mm3':vol(missing),'extra_valid':all(s.is_valid for s in extra.solids()),'missing_valid':all(s.is_valid for s in missing.solids())}
comparisons={'step_readback':difference(q,rt),'prior_fixed_stock_step':difference(q,old)}
vertices,faces=q.tessellate(.12,.15);vv=np.array([tuple(v) for v in vertices]);mesh=trimesh.Trimesh(vv[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(faces));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/'block.glb';mesh.export(gp);actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8)
r={'status':'PASS original CAD/direct mesh/readback topology repair' if q.is_valid and rt.is_valid and actual.is_watertight and all(v['extra_mm3']+v['missing_mm3']<1e-5 and v['extra_valid'] and v['missing_valid'] for v in comparisons.values()) else 'FAIL topology repair gates; preserve result','input_sha256':inputs,'stages':stages,'original_cad_valid':q.is_valid,'step_readback_valid':rt.is_valid,'direct_mesh_watertight':actual.is_watertight,'triangles':len(actual.faces),'comparisons_without_same_domain_simplification':comparisons,'step_sha256':sha(sp),'glb_sha256':sha(gp),'source_edit_counts':edits,'limits':['No installation or support/clearance approval','Fixed-stock support and interface failures remain unless material equivalence is proved','No export healing used to construct the original CAD or direct mesh','Same-domain simplification is explicitly disabled for rear-seat source Booleans and comparison Booleans only']}
assert inputs=={p:sha(ROOT/p) for p in inputs}
(ROOT/'inventory/engine/timing-block-rear-seat-topology-full.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
