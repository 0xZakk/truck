#!/usr/bin/env python3
"""Replay serialized proposal and reject stale before-values/assets; no writes to canonical files."""
from pathlib import Path
import sys,json,hashlib,copy
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import trimesh
from assembly_math import transforms
M=R/'inventory/engine/full-assembly.json';P=R/'inventory/engine/timing-pan-integration-patch.json';V=R/'inventory/engine/timing-pan-integration-stage-validation.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();base=json.loads(M.read_text());patch=json.loads(P.read_text());stage=json.loads(V.read_text())
def replay(p):
 assert sha(M)==p['manifest_sha256'],'manifest binding'
 m=copy.deepcopy(base)
 for group in ['definitions','occurrences']:
  items={x['id']:x for x in m[group]}
  for q in p[group]:
   assert items[q['id']]==q['before'],'before mismatch'
   assert q['after']['id']==q['id']
   if group=='occurrences':assert q['after']['parent']==q['before']['parent']
   for asset in q.get('copy_assets',{}).values():assert sha(R/asset['from'])==asset['sha256'],'asset binding'
   items[q['id']].clear();items[q['id']].update(q['after'])
 return m
new=replay(patch);pose=transforms(new);checks=[]
for row in stage['parts']:
 sp=R/row['step'];gp=R/row['glb'];assert sha(sp)==row['step_sha256'] and sha(gp)==row['glb_sha256'];shape=b.import_step(sp);mesh=trimesh.load(gp,force='mesh');cad=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000
 for occurrence in [q for q in new['occurrences']if q['definition']==row['id']]:
  t=pose[occurrence['id']].wrapped.Transformation();rot=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);translation=np.array([t.Value(i,4)for i in range(1,4)]);world=cad@rot.T+translation;bb=(pose[occurrence['id']]*shape).bounding_box();error=float(np.max(abs(np.array([world.min(0),world.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert error<.025;checks.append({'id':occurrence['id'],'mesh_to_step_world_bounds_error_mm':error})
controls=[]
for label in ['stale-manifest','wrong-before-pose','changed-asset']:
 bad=copy.deepcopy(patch)
 if label=='stale-manifest':bad['manifest_sha256']='0'*64
 if label=='wrong-before-pose':bad['occurrences'][0]['before']['position_cad_mm'][0]+=1
 if label=='changed-asset':bad['definitions'][0]['copy_assets']['step']['sha256']='0'*64
 try:replay(bad)
 except AssertionError:controls.append({'fault':label,'rejected':True})
 else:raise AssertionError('Fault not rejected: '+label)
unchanged=[o for o in base['occurrences'] if o['id'] not in {q['id']for q in patch['occurrences']}]
assert all(o==next(q for q in new['occurrences']if q['id']==o['id'])for o in unchanged)
assert len(checks)==52
r={'status':'PASS serialized proposal replay and52 reconstructed world STEP/mesh bounds','canonical_modified':False,'patched_definition_ids':[q['id']for q in patch['definitions']],'patched_occurrence_ids':[q['id']for q in patch['occurrences']],'unchanged_occurrences':len(unchanged),'world_mesh_checks':checks,'negative_controls':controls,'inputs':{str(p.relative_to(R)):sha(p)for p in [Path(__file__),M,P,V,R/'cad/engine/assembly_math.py']},'limits':['Replay only, no canonical writes or installation','Pose-specific contact evidence remains scoped as recorded in stage validation','Mesh bound tolerance0.025mm; no new motion/browser proof']}
(R/'inventory/engine/timing-pan-integration-patch-replay.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
