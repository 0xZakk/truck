#!/usr/bin/env python3
"""Isolated rebuilt block: zero-delta equivalence, predeclared protected gates."""
from pathlib import Path
import sys,json,hashlib,time,ast,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np,trimesh
import timing_block_axis_feature_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-axis-feature-candidate';OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def comp(q):return b.Compound(children=list(q.solids()))
baseproof=ROOT/'inventory/engine/timing-block-baseline-validation.json';proof=json.loads(baseproof.read_text())
assert proof['status']=='PASS exact baseline regeneration'
historical_builder=subprocess.check_output(['git','show',proof['baseline_commit']+':cad/engine/full_engine.py'],cwd=ROOT)
assert hashlib.sha256(historical_builder).hexdigest()==proof['source_modules_sha256']['cad/engine/full_engine.py']
def outside_main(source):
 tree=ast.parse(source);tree.body=[n for n in tree.body if not isinstance(n,ast.FunctionDef) or n.name!='main'];return ast.dump(tree)
assert outside_main(historical_builder)==outside_main((ROOT/'cad/engine/full_engine.py').read_text()),'Builder changes beyond integration main'
for p,h in proof['source_modules_sha256'].items():
 if p!='cad/engine/full_engine.py':assert sha(ROOT/p)==h,p
for p,h in proof['canonical_inputs_sha256'].items():
 if p!='inventory/engine/full-assembly.json':assert sha(ROOT/p)==h,p
inputs={str(baseproof.relative_to(ROOT)):sha(baseproof),str(Path(__file__).relative_to(ROOT)):sha(Path(__file__)),str(Path(c.__file__).relative_to(ROOT)):sha(Path(c.__file__))}
inputs.update({p:sha(ROOT/p) for p in proof['source_modules_sha256']});inputs.update({p:sha(ROOT/p) for p in proof['canonical_inputs_sha256']})
base=b.import_step(ROOT/next(p for p in proof['canonical_inputs_sha256'] if p.endswith('.step')))
masks,specs=c.protected_masks();(OUT/'declared-protected-regions.json').write_text(json.dumps(specs,indent=2)+'\n')
print('Protected guards declared:',len(masks),flush=True)
zero,edits=c.regenerate((0,0,0));zero_error=vol(zero.cut(base))+vol(base.cut(zero));assert zero_error<1e-5
print('Zero delta equivalent',zero_error,flush=True)
stages=[]
def stage(name,q):
 p=OUT/(name+'.step');b.export_step(q,p);stages.append({'name':name,'valid':q.is_valid,'solids':len(q.solids()),'step_sha256':sha(p)});print(name,stages[-1],flush=True)
q,edits=c.regenerate(stage=stage);sp=OUT/'block.step';b.export_step(q,sp)
extra=comp(q.cut(base));missing=comp(base.cut(q));changes=comp(extra)+comp(missing)
for name,s in [('added',extra),('removed',missing)]:
 if s and s.solids():b.export_step(comp(s),OUT/(name+'.step'))
results=[]
for name,mask in masks.items():
 added=vol(extra.intersect(mask));removed=vol(missing.intersect(mask));results.append({'name':name,'added_mm3':added,'removed_mm3':removed,'pass':added+removed<1e-5})
 print('protected',name,added,removed,flush=True);(OUT/'protected-progress.json').write_text(json.dumps(results,indent=2)+'\n')
remaining=comp(extra)+comp(missing)
for mask in c.declared_change_roi().solids():
 if not remaining.solids():break
 remaining=comp(remaining.cut(mask))
escaped=vol(remaining)
# Export integrity is recorded even when protected-region failures occur.
rt=b.import_step(sp);v,f=q.tessellate(.12,.15);v=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/'block.glb';mesh.export(gp)
actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8);vv=np.asarray(actual.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();bounds=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
export={'valid':q.is_valid,'solids':len(q.solids()),'watertight':actual.is_watertight,'duplicate_faces':int((~actual.unique_faces()).sum()),'degenerate_faces':int((~actual.nondegenerate_faces()).sum()),'bounds_error_mm':bounds,'volume_roundtrip_error_mm3':abs(vol(q)-vol(rt)),'step_sha256':sha(sp),'glb_sha256':sha(gp),'triangles':len(actual.faces)}
assert inputs=={p:sha(ROOT/p) for p in inputs},'Bound inputs changed'
r={'status':'PASS protected block-feature gates; core-interface report still required' if all(x['pass'] for x in results) and escaped<1e-5 else 'FAIL protected block-feature gates; preserve candidate and inspect conflicts','input_sha256':inputs,'baseline_reuse':{'historical_builder_verified_from_commit':proof['baseline_commit'],'all_builder_ast_outside_main_unchanged':True,'canonical_block_step_unchanged':True,'zero_delta_rechecked':True},'delta_mm':c.DELTA,'source_edit_counts':edits,'zero_delta_symmetric_difference_mm3':zero_error,'declared_protected_regions':specs,'protected_results':results,'added_volume_mm3':vol(extra),'removed_volume_mm3':vol(missing),'change_outside_declared_roi_mm3':escaped,'stages':stages,'export':export,'limits':['Isolated candidate, not installed','Front land/pan proposal not incorporated','Protected failures are not waived or removed from guards','Manual backlash0.0508–0.1016mm is a separate service-measurement requirement, not the gear model parameter or Euclidean gap']}
(ROOT/'inventory/engine/timing-block-axis-feature-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
