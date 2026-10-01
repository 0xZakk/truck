"""Independent serialized proposal replay, transform and corruption controls."""
from pathlib import Path
import sys,json,copy,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
from assembly_math import transforms
import timing_pan21_lateral_candidate as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def matrix(loc):
 t=loc.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
def bounds(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
def bindings(o):
 if isinstance(o,dict):
  for p,v in o.items():
   if '/'in p and isinstance(v,str)and len(v)==64:yield p,v
   else:yield from bindings(v)
 elif isinstance(o,list):
  for v in o:yield from bindings(v)
manifest=R/'inventory/engine/full-assembly.json';pp=R/'inventory/engine/timing-front-coordinated-patch.json';rp=R/'inventory/engine/timing-front-coordinated-stage-validation.json';patch=json.loads(pp.read_text());stage=json.loads(rp.read_text());m=json.loads(manifest.read_text());assert sha(pp)==stage['patch_sha256'];checked={}
for p,h in stage['inputs'].items():assert sha(R/p)==h,p;checked[p]=h
for name in ['timing-pan21-lateral-delivery-validation','timing-seven-block-delivery-validation','timing-front-stage-contact-delta']:
 p=R/'inventory/engine'/f'{name}.json';o=json.loads(p.read_text())
 for path,h in bindings(o):assert sha(R/path)==h,path;checked[path]=h
def apply(p,check_assets=True):
 assert p['manifest_sha256']==sha(manifest),'stale manifest';out=copy.deepcopy(m)
 for group in ['definitions','occurrences']:
  index={x['id']:i for i,x in enumerate(out[group])}
  for change in p[group]:
   ident=change['id'];before=change['before']
   if before is None:assert ident not in index,'addition already exists';out[group].append(change['after'])
   else:assert ident in index and out[group][index[ident]]==before,'wrong before object';out[group][index[ident]]=change['after']
   if check_assets and group=='definitions':
    for asset in change['copy_assets'].values():assert sha(R/asset['from'])==asset['sha256'],'changed asset hash'
 return out
new=apply(patch);poses=transforms(new);oldocc={q['id']:q for q in m['occurrences']};newocc={q['id']:q for q in new['occurrences']};patched={q['id']for q in patch['occurrences']};assert all(newocc[k]==v for k,v in oldocc.items()if k not in patched)
rows=[];assets={}
for part in stage['parts']:
 sp=R/part['step'];gp=R/part['glb'];assert sha(sp)==part['step_sha256']and sha(gp)==part['glb_sha256'];s=b.import_step(sp);mesh=trimesh.load(gp,force='mesh');v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;assets[part['id']]=(s,v)
 if part['id']in ['block','timing-cover','oil-pan','oil-pan-molded-gasket']:
  mat=matrix(poses[part['id']]);source=b.import_step(R/part['source_step']);world=v@mat[:,:3].T+mat[:,3];e=float(np.max(abs(np.array([world.min(0),world.max(0)])-bounds(source))));assert e<.025;rows.append({'id':part['id'],'world_mesh_source_bounds_error_mm':e})
washerpath=R/'cad/engine/generated/oil-pan-mounting-washer.step';w=b.import_step(washerpath);wv,wf=w.tessellate(.08,.12);assets['oil-pan-mounting-washer']=(w,np.array([tuple(p)for p in wv]));checked[str(washerpath.relative_to(R))]=sha(washerpath)
for oid,q in newocc.items():
 if oid.startswith(('oil-pan-mounting-screw-','oil-pan-mounting-washer-','timing-cover-mounting-screw-')):
  s,v=assets[q['definition']];mat=matrix(poses[oid]);world=v@mat[:,:3].T+mat[:,3];placed=poses[oid]*s;e=float(np.max(abs(np.array([world.min(0),world.max(0)])-bounds(placed))));assert e<.025;rows.append({'id':oid,'mesh_step_world_bounds_error_mm':e})
for change in patch['occurrences']:
 mt=matrix(poses[change['id']])
 if 'world_target_transform'in change:assert np.max(abs(mt-np.array(change['world_target_transform'])))<1e-8
 else:assert np.max(abs(mt[:,3]-change['world_target_mm']))<1e-8
controls={}
for label,edit in [('stale-manifest',lambda p:p.update(manifest_sha256='0'*64)),('wrong-before-pose',lambda p:p['occurrences'][0]['before']['position_cad_mm'].__setitem__(0,999)),('changed-asset-hash',lambda p:p['definitions'][0]['copy_assets']['step'].update(sha256='0'*64))]:
 bad=copy.deepcopy(patch);edit(bad)
 try:apply(bad);controls[label]=False
 except AssertionError:controls[label]=True
assert all(controls.values());controls['old_pan21_pose_error_mm']=float(np.linalg.norm(matrix(poses['oil-pan-mounting-screw-21'])[:,3]-np.array(c.OLD)));assert controls['old_pan21_pose_error_mm']==15
cover=assets['timing-cover'][0];double=bounds(poses['timing-cover']*poses['timing-cover']*cover);correct=bounds(poses['timing-cover']*cover);controls['double_cover_placement_error_mm']=float(np.max(abs(double-correct)));assert controls['double_cover_placement_error_mm']>400
for e in patch['scope_approval']['whole_signed_deltas']+patch['scope_approval']['broad_guard_signed_witnesses']:assert sha(R/e['path'])==e['sha256']
r={'status':'PASS serialized candidate replay; dependencies/browser remain open','world_asset_checks':rows,'preserved_unpatched_occurrences':len(oldocc)-len([k for k in patched if k in oldocc]),'controls':controls,'signed_delta_hashes_match':True,'proof_inputs_current':True,'input_sha256':{**checked,str(manifest.relative_to(R)):sha(manifest),str(pp.relative_to(R)):sha(pp),str(rp.relative_to(R)):sha(rp),str(Path(__file__).relative_to(R)):sha(Path(__file__))},'canonical_modified':False};(R/'inventory/engine/timing-front-coordinated-patch-replay.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(rows))
