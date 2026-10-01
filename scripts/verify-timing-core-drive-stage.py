#!/usr/bin/env python3
"""In-memory serialized replay and fault controls. Never writes canonical files."""
from pathlib import Path
import sys,json,copy,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import trimesh
from assembly_math import transforms
from timing_coupled_core_candidate import AXIS
import oil_drive_layout as drive
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=R/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());digest=sha(mp)
paths=[R/f'inventory/engine/timing-{s}-integration-patch.json'for s in ['core','conditional-drive']]+[R/'inventory/engine/timing-corrected-slider-neutral-patch.json']
patches=[json.loads(p.read_text())for p in paths]
def apply(base,patches):
 out=copy.deepcopy(base);owned=set()
 for patch in patches:
  if patch['manifest_sha256']!=digest:raise ValueError('Stale manifest')
  for field in ['definitions','assemblies','occurrences']:
   for change in patch[field]:
    identity=change['id'];key=(field,identity)
    if key in owned:raise ValueError('Overlapping patch ownership')
    owned.add(key);source=next(x for x in base[field]if x['id']==identity)
    if source!=change['before']:raise ValueError('Stale before object')
    if source['id']!=change['after']['id']or source.get('parent')!=change['after'].get('parent'):raise ValueError('Identity or parent change')
    for asset in change.get('copy_assets',{}).values():
     if sha(R/asset['from'])!=asset['sha256']:raise ValueError('Asset hash failure')
    out[field][next(i for i,x in enumerate(out[field])if x['id']==identity)]=change['after']
 return out
new=apply(m,patches);poses=transforms(new);oldposes=transforms(m);report=R/'inventory/engine/timing-core-drive-stage-review.json';stage=json.loads(report.read_text())
for name,h in stage['input_sha256'].items():assert sha(R/name)==h,name
for name,h in stage['patches_sha256'].items():assert sha(R/name)==h,name
def matrix(p):
 t=p.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
core_errors=[]
for row in stage['core_parts']:
 e=float(np.max(abs(matrix(poses[row['occurrence']])-row['target_world_matrix'])));assert e<1e-9;core_errors.append(e)
# Explicit world vertices of new distributor asset through original definition frame.
sp=R/'cad/engine/generated/crossed-oil-drive-corrected-pair/distributor-drive-gear-local.glb';tp=R/'cad/engine/generated/timing-core-drive-integration-stage/distributor-drive-gear.glb'
a=trimesh.load(sp,force='mesh');z=trimesh.load(tp,force='mesh');assert np.array_equal(a.faces,z.faces)
v=a.vertices[:,[0,2,1]]*[1,-1,1]*1000;w=z.vertices[:,[0,2,1]]*[1,-1,1]*1000
f=matrix(b.Pos(0,AXIS[0]-90,AXIS[1]-72)*drive.GEAR_FRAME);p=matrix(poses['distributor-drive-gear']);expected=v@f[:,:3].T+f[:,3];actual=w@p[:,:3].T+p[:,3];mesh_error=float(np.max(abs(actual-expected)));assert mesh_error<.01
wrong=v@p[:,:3].T+p[:,3];frame_fault=float(np.max(abs(wrong-expected)));assert frame_fault>75
controls={}
for label in ['manifest','before','asset','duplicate']:
 bad=copy.deepcopy(patches)
 if label=='manifest':bad[0]['manifest_sha256']='0'*64
 if label=='before':bad[0]['assemblies'][0]['before']['position_cad_mm'][0]+=1
 if label=='asset':bad[0]['definitions'][0]['copy_assets']['step']['sha256']='0'*64
 if label=='duplicate':bad.append(copy.deepcopy(bad[0]))
 try:apply(m,bad);controls[label]=False
 except ValueError:controls[label]=True
assert all(controls.values())
# Every unchanged occurrence and all identity/parent fields remain byte-object equal.
modified={x['id']for p in patches for x in p['occurrences']};newocc={o['id']:o for o in new['occurrences']}
assert all(newocc[o['id']]==o for o in m['occurrences']if o['id']not in modified)
assert sha(mp)==digest
inputs=[Path(__file__),mp,report,*paths,sp,tp,R/'cad/engine/assembly_math.py',R/'cad/engine/oil_drive_layout.py',R/'cad/engine/timing_coupled_core_candidate.py']
# Bind retained canonical branch assets even though this patch moves only parents.
occ={o['id']:o for o in m['occurrences']};defs={d['id']:d for d in m['definitions']}
for row in stage['conditional_branch_occurrences']:
 definition=defs[occ[row['id']]['definition']]
 for key in ['step','glb']:inputs.append(R/definition[key].lstrip('/'))
# Explicitly check ownership disjoint from root's neutral linkage/asset stages.
for path,field in [('inventory/engine/clockwise-linkage-pose-patch.json','occurrences'),('inventory/engine/clockwise-linkage-asset-patch.json','definitions')]:
 rp=R/path;rootpatch=json.loads(rp.read_text());our_ids={x['id']for p in patches for x in p[field]};root_ids={x['id']for x in rootpatch[field]};assert not our_ids&root_ids;inputs.append(rp)
r={'status':'PASS serialized replay; conditional drive remains unresolved','definitions':sum(len(p['definitions'])for p in patches),'assembly_rows':sum(len(p['assemblies'])for p in patches),'occurrence_rows':sum(len(p['occurrences'])for p in patches),'core_frame_max_error':max(core_errors),'distributor_mesh_world_vertex_error_mm':mesh_error,'wrong_gear_definition_frame_fault_mm':frame_fault,'controls':controls,'slider_runtime_limit':'Physical neutral frame contract verified separately; legacy transforms is not acceptance for rods/pistons','canonical_modified':False,'input_sha256':{str(p.relative_to(R)):sha(p)for p in inputs}}
(R/'inventory/engine/timing-core-drive-stage-replay.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
