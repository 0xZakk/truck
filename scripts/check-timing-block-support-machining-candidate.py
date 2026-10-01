#!/usr/bin/env python3
"""Build isolated backing/machining candidate; preserve all historical guard results."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np,trimesh
import timing_block_support_machining_candidate as c
from timing_block_axis_feature_candidate import protected_masks
from timing_block_physical_interface_contract import physical_masks
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-support-machining-candidate';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def comp(q):return b.Compound(children=list(q.solids()))
p=ROOT/'inventory/engine/timing-block-boolean-topology-full.json';proof=json.loads(p.read_text());inputs=dict(proof['input_sha256']);assert inputs=={p:sha(ROOT/p) for p in inputs}
for path in [p,Path(__file__),Path(c.__file__),ROOT/'cad/engine/timing_block_boolean_topology_candidate.py',ROOT/'cad/engine/generated/block.step']:inputs[str(path.relative_to(ROOT))]=sha(path)
broad,spec=protected_masks();physical,pspec=physical_masks();(OUT/'predeclared-contract.json').write_text(json.dumps({'backing_mm':c.BACKING_MM,'width_mm':c.WIDTH_MM,'stations':c.JOURNAL_STATIONS,'broad':spec,'physical':pspec,'carrier_revision':'whole support historical failure retained; current seat/backing and minimum5mm socket separation required','pan8':'actual radius10 boss and bore/hardware diagnosis; original radius12 broad guard retained'},indent=2)+'\n')
q,data=c.build();q=comp(q);print('built',q.is_valid,len(q.solids()),flush=True)
for name,shape in [('block',q),('base',data['base']),('supported',data['supported'])]:b.export_step(shape,OUT/(name+'.step'))
canonical=b.import_step(ROOT/'cad/engine/generated/block.step')
with b.SkipClean():
 extra=comp(q.cut(canonical));missing=comp(canonical.cut(q));added_vs_base=comp(q.cut(data['base']));removed_vs_base=comp(data['base'].cut(q))
 for name,shape in [('added-vs-base',added_vs_base),('removed-vs-base',removed_vs_base)]:
  if shape.solids():b.export_step(shape,OUT/(name+'.step'))
 supports=[]
 for i,shell in data['shells'].items():
  error=vol(shell.cut(q));supports.append({'journal':i,'required_shell_volume_mm3':vol(shell),'missing_shell_mm3':error,'complete':error<1e-5});print('support',supports[-1],flush=True)
 results={}
 for label,masks in [('original79',broad),('original91',physical)]:
  rows=[]
  for name,mask in masks.items():
   a=vol(extra.intersect(mask));d=vol(missing.intersect(mask));rows.append({'name':name,'added_mm3':a,'removed_mm3':d,'unchanged':a+d<1e-5})
   if a+d>=1e-5:print(label,rows[-1],flush=True)
  results[label]=rows
sp=OUT/'block.step';rt=b.import_step(sp)
with b.SkipClean():readback=vol(q.cut(rt))+vol(rt.cut(q))
v,f=q.tessellate(.12,.15);v=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/'block.glb';mesh.export(gp);actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8)
vv=np.asarray(actual.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();boundserror=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([list(bb.min),list(bb.max)]))))
r={'status':'CANDIDATE built; interface/attachment checks required','input_sha256':inputs,'original_cad_valid':q.is_valid,'solid_count':len(q.solids()),'step_readback_valid':rt.is_valid,'readback_symmetric_difference_mm3':readback,'direct_mesh_watertight':actual.is_watertight,'mesh_bounds_error_mm':boundserror,'triangles':len(actual.faces),'step_sha256':sha(sp),'glb_sha256':sha(gp),'support_shells':supports,'historical_guards':results,'added_vs_base_mm3':vol(added_vs_base),'removed_vs_base_mm3':vol(removed_vs_base),'limits':['2mm backing is educational estimate, not source/factory/strength evidence','Historical whole-support and broad guard results retained, not reclassified as passes','No canonical writes; no front land union; no browser or installed acceptance']}
assert inputs=={p:sha(ROOT/p) for p in inputs}
(ROOT/'inventory/engine/timing-block-support-machining-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
