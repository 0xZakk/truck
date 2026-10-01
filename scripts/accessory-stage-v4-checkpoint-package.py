"""Package explicit frozen PS/AC and v4 allowlists; never extract or publish."""
from pathlib import Path
import argparse,gzip,hashlib,json,tarfile,subprocess
from urllib.parse import unquote
R=Path(__file__).resolve().parents[1];M=R/'docs/accessory-stage-v4-checkpoint-draft.json'
LEDGER='inventory/engine/accessory-psac-carrier-delivery.json'
SOURCE=['scripts/engine-exterior-fidelity-audit-render.py','inventory/engine/engine-exterior-fidelity-audit.json','inventory/engine/engine-exterior-fidelity-audit-render.json','docs/components/engine-exterior-fidelity-audit.md','scripts/reconcile-accessory-stage-v4-conflicts.py','inventory/engine/accessory-stage-v4-remaining-conflicts.json',LEDGER,'inventory/engine/corrected-engine-stage-v4.json',
 *['inventory/engine/'+n+'.json'for n in ['accessory-coordinated-stage-contract','accessory-pose-serialization','accessory-stage-v4-composition','accessory-stage-v4-navigation','accessory-stage-v4-interfaces','accessory-stage-v4-solids','accessory-stage-v4-solids-summary','accessory-stage-v4-solids-fault','accessory-stage-v4-render']],
 *['scripts/'+n for n in ['check-accessory-pose-serialization.py','compose-accessory-stage-v4.py','check-accessory-stage-v4-navigation.mjs','check-accessory-stage-v4-interfaces.py','check-accessory-stage-v4-solids.py','check-accessory-stage-v4-solids-fault.py','render-accessory-stage-v4.py']],
 *['docs/components/'+n+'.md'for n in ['accessory-coordinated-stage-contract','accessory-pose-serialization','accessory-stage-v4-integration','accessory-stage-v4-interfaces','accessory-stage-v4-solids']]]
ARTIFACTS=['cad/engine/generated/engine-exterior-fidelity-audit/whole-engine-review.png','cad/engine/generated/accessory-stage-v4-solids-fault.log','cad/engine/generated/accessory-stage-v4-solids.log',*['cad/engine/generated/accessory-stage-v4-visual/'+n for n in ['comparison.png','mesh-data.npz','mesh-inputs.json']]]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def hashes(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str)and isinstance(x.get('sha256'),str):yield x['path'],x['sha256']
  if isinstance(x.get('file'),str)and isinstance(x.get('sha256'),str):yield x['file'],x['sha256']
  for k,v in x.items():
   if isinstance(v,str)and len(v)==64 and all(c in '0123456789abcdef'for c in v)and '/'in k:yield k,v
   else:yield from hashes(v)
 elif isinstance(x,list):
  for v in x:yield from hashes(v)
def row(p):return {'path':p,'sha256':sha(R/p),'size_bytes':(R/p).stat().st_size}
def prepare():
 ledger=json.loads((R/LEDGER).read_text());owned=set(SOURCE+ARTIFACTS)
 for p,h in ledger['files_sha256'].items():assert sha(R/p)==h,p;owned.add(p)
 fault=json.loads((R/'inventory/engine/accessory-stage-v4-solids-fault.json').read_text())
 assert fault['status'].startswith('PASS')
 # Authored negative-control witnesses, explicitly named by the frozen report.
 for p,h in hashes(fault):
  if p.startswith('cad/engine/generated/accessory-stage-v4-solids')and p.endswith('.step'):owned.add(p);assert sha(R/p)==h
 # Witness path may be a plain field beside its hash.
 for k,v in fault.items():
  if isinstance(v,str)and v.startswith('cad/engine/generated/accessory-stage-v4-solids')and v.endswith('.step'):owned.add(v)
 for p in owned:
  assert not any(s in p for s in ['aborted','interrupted','manuals/','reference/photos/'])
  assert not (p.startswith('reference/')or'/reference/'in p)
 metadata=[];index={}
 for p in sorted(R.glob('docs/*checkpoint*.json')):
  if p==M:continue
  metadata.append(row(str(p.relative_to(R))))
  doc=json.loads(p.read_text())
  for field in ['artifact_files','file_sha256','files_sha256']:
   for target,h in hashes(doc.get(field,{})):index.setdefault((target,h),set()).add(str(p.relative_to(R)))
 p='inventory/engine/waterpump-prerequisite-archive-audit.json';metadata.append(row(p))
 for r in json.loads((R/p).read_text())['members']:index.setdefault((r['path'],r['archive_member_sha256']),set()).add(p)
 ext={};web_claims=[]
 for p in sorted(owned):
  if not p.endswith('.json'):continue
  for target,h in hashes(json.loads((R/p).read_text())):
   if target.startswith('/'):
    local=target.lstrip('/')
    if not (R/local).is_file()and(R/unquote(local)).is_file():local=unquote(local)
    actual=sha(R/local)if(R/local).is_file()else None
    web_claims.append({'manifest':p,'reference':target,'expected_sha256':h,'resolved_local_path':local,'actual_sha256':actual,'matches':actual==h,'scope':'Inherited manifest provenance only; not packaged source original or fresh source review'})
    continue
   assert (R/target).is_file(),(p,target)
   assert sha(R/target)==h,(p,target)
   if target not in owned:ext.setdefault(target,set()).add(h)
 external=[]
 for p,hs in sorted(ext.items()):
  assert len(hs)==1
  source=p.startswith(('manuals/','reference/'))and not p.endswith('.json')or'/reference/'in p
  kind='excluded source original'if source else 'repository input'
  if p.startswith('cad/engine/generated/')and not source:kind='predecessor exact hash match'if all((p,h)in index for h in hs)else'UNRESOLVED prerequisite'
  external.append({'path':p,'sha256':next(iter(hs)),'classification':kind,'matching_metadata':sorted({x for h in hs for x in index.get((p,h),[])})})
 artifact=sorted(p for p in owned if p.startswith('cad/engine/generated/'));sources=sorted(owned-set(artifact))
 j={'inherited_manifest_web_reference_claims':web_claims,'status':'UNPUBLISHED checkpoint; root publication owner','baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'asset':'truck-accessory-stage-v4-20261001.tar.gz','scope':'Frozen PS/AC trial1 and rejected trial0; private coordinated v4 composition, navigation, invariant interfaces, q0 solids, actual wrong-pose control and authored render; earlier exterior audit preserved; no installation','packaging_script':row(str(Path(__file__).relative_to(R))),'artifact_files':[row(p)for p in artifact],'source_report_handoff_files':[row(p)for p in sources],'external_inputs':external,'prerequisite_metadata':metadata,'required_base_release':'studies-2026-10-01-accessory-layout','required_base_release_id':401248087,'required_base_archive_sha256':'dd374011c14bec494f0647c3e84b8ff56ff3fd4e337e0f2fc6ad57bf9ac47d7b','restore_order':'Published neck-core and ordered supplements through published waterpump, then published accessory-layout, then this unpublished archive. Frozen draft filenames do not override published release status in CAD-ARTIFACTS.','excluded':['Every source photograph/manual/catalog and source-image composite','Aborted redundant-load and interrupted pre-broadphase v4 reports/logs; historical mentions in final reports remain context only'],'image_provenance':[{'path':p,'kind':'Project-authored actual mesh/STEP render; no source image pixels'}for p in artifact if p.endswith('.png')],'limits':['No new CAD or solid checks; verifies preservation only','Seven pulley-blocked tool approaches and three alternate-pump access failures retained','Exact predecessor metadata matching; predecessor archives not freshly reopened','No browser, factory fidelity or installed acceptance']}
 M.write_text(json.dumps(j,indent=2)+'\n')
def build(verify):
 j=json.loads(M.read_text());assert sha(R/j['packaging_script']['path'])==j['packaging_script']['sha256']
 for r in j['artifact_files']+j['source_report_handoff_files']+j['prerequisite_metadata']+j['external_inputs']:
  assert sha(R/r['path'])==r['sha256'],r['path']
  if 'size_bytes'in r:assert (R/r['path']).stat().st_size==r['size_bytes']
 for r in j['inherited_manifest_web_reference_claims']:
  if r['actual_sha256'] is not None:assert sha(R/r['resolved_local_path'])==r['actual_sha256']
 assert not [r for r in j['external_inputs']if r['classification']=='UNRESOLVED prerequisite']
 rows=j['artifact_files'];assert [r['path']for r in rows]==sorted({r['path']for r in rows})
 out=R/'cad/engine/generated/accessory-stage-v4-checkpoint'/j['asset'];out.parent.mkdir(exist_ok=True)
 if not verify:
  with out.open('wb')as raw,gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0)as gz,tarfile.open(fileobj=gz,mode='w')as tar:
   for r in rows:
    assert not (R/r['path']).is_symlink();info=tarfile.TarInfo(r['path']);info.size=r['size_bytes'];info.mode=0o644;info.mtime=0
    with (R/r['path']).open('rb')as f:tar.addfile(info,f)
 seen=[]
 with tarfile.open(out,'r|gz')as tar:
  for member in tar:
   r=rows[len(seen)];assert member.isfile()and member.name==r['path'];h=hashlib.sha256()
   with tar.extractfile(member)as f:
    for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
   assert h.hexdigest()==r['sha256'];seen.append(member.name)
 assert len(seen)==len(rows)
 result={'path':str(out.relative_to(R)),'sha256':sha(out),'size_bytes':out.stat().st_size,'members':len(rows),'source_files_verified':len(j['source_report_handoff_files']),'member_verification':'PASS','publication':'NOT RUN'}
 if verify:assert result==j['archive']
 else:j['archive']=result;M.write_text(json.dumps(j,indent=2)+'\n')
 print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 build(a.verify_only)
