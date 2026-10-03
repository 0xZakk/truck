from pathlib import Path
import json,hashlib,sys,platform
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ex=json.loads((R/'reference/engine/pump-functional-20261003-build.json').read_text())
parts={}
mesh_reports=['non-spring-mesh']if (R/'reference/engine/pump-functional-20261003-non-spring-mesh.json').exists()else['relative-mesh-partial','tail-mesh']
for name in mesh_reports:
 q=json.loads((R/f'reference/engine/pump-functional-20261003-{name}.json').read_text())
 parts.update(q['parts'])
sp=R/'reference/engine/pump-functional-20261003-spring-export.json'
if sp.exists():
 spring=json.loads(sp.read_text())
 if 'result'in spring:parts['water-pump-seal-spring']=spring['result']
for n,v in parts.items():
 assert sha(R/v['path'])==v['sha256'],n
 assert sha(R/ex['parts'][n]['path'])==v['step_sha256'],n
 # Reuse only byte-identical individual STEP/GLB pairs, never just a changed build-report hash.
missing=sorted(set(ex['parts'])-set(parts))
failed=[n for n,v in parts.items()if not(v['watertight']and v['winding']and v['cad_bounds_error_mm']<=.025)]
r={'status':'PASS scoped52meshes only'if not missing and not failed else'INCOMPLETE/FAIL export','parts':parts,'missing':missing,'failed':failed,'threshold_mm':.025,'reuse_contract':'Individual STEP/GLB hashes verified; unaffected translated parts preserved through housing-only revision. Original47 and tail4 reports retained; spring separately qualified.','whole_component_acceptance':False}
(R/'reference/engine/pump-functional-20261003-mesh-final.json').write_text(json.dumps(r,indent=2)+'\n')
# Direct selected report input assertions. Historical failed attempts are retained as history, not current passes.
guard={}
for suffix in ['build','check','fifth','seats','neighbors']:
 p=R/f'reference/engine/pump-functional-20261003-{suffix}.json';q=json.loads(p.read_text())
 for path,h in q.get('inputs',{}).items():
  assert sha(R/path)==h,(suffix,path)
  guard[path]=h
guard.update({str(p.relative_to(R)):sha(p)for p in[
 R/'inventory/engine/full-assembly.json',R/'reference/engine/pump-junction-online-20261002-evidence.json',
 R/'reference/engine/pump-height-20261002-delivery.json',R/'reference/engine/pump-metric-20261002-contract.json']})
authored={}
for directory in ['cad/engine','scripts','docs/components','reference/engine']:
 for p in (R/directory).glob('pump*functional*20261003*'):
  if not p.is_file()or p.name=='pump-functional-20261003-delivery.json':continue
  authored[str(p.relative_to(R))]=sha(p)
assets={str(p.relative_to(R)):sha(p)for p in (R/'cad/engine/generated/pump-functional-20261003').glob('*')if p.is_file()}
ledger={'status':'candidate FAIL installation; selected assets frozen','authored_files':authored,'generated_assets':assets,'guarded_inputs':guard,'selected_build':'reference/engine/pump-functional-20261003-build.json','mesh_status':r['status'],'mesh_missing':missing,'mesh_failed':failed,'canonical_sha256':sha(R/'inventory/engine/full-assembly.json'),'v4_sha256':sha(R/'inventory/engine/corrected-engine-stage-v4.json'),'manufacturer_originals_included':False,'no_running_process':('--no-running-process'in sys.argv),'publication_owner':'root','usage_model_effort':'unavailable'}
(R/'reference/engine/pump-functional-20261003-delivery.json').write_text(json.dumps(ledger,indent=2)+'\n')
print('authored',len(authored),'assets',len(assets),'guarded',len(guard),'meshes',len(parts),'missing',missing,'failed',failed,flush=True)
