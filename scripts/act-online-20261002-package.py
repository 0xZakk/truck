"""Deterministic ACT specimen archive; no source originals, extraction or publication."""
from pathlib import Path
import argparse,gzip,hashlib,json,subprocess,tarfile
R=Path(__file__).resolve().parents[1];M=R/'docs/act-online-20261002-package.json';L='reference/engine/act-online-20261002-delivery.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def row(p):return {'path':p,'sha256':sha(R/p),'size_bytes':(R/p).stat().st_size}
def prepare():
 d=json.loads((R/L).read_text());owned=set(d['files'])|{L}
 for p,h in d['files'].items():assert sha(R/p)==h,p
 for p in owned:
  assert not any(t in p for t in ('/captures/','-captures/','kb/.raw/'))
  assert Path(p).suffix in ('.py','.md','.json','.log','.step','.glb','.png'),p
 assets=sorted(p for p in owned if p.startswith('cad/engine/generated/'))
 evidence=json.loads((R/'reference/engine/act-online-20261002-evidence.json').read_text());prior=[]
 for p,h in evidence['existing_identity_inputs'].items():
  assert sha(R/p)==h;subprocess.run(['git','ls-files','--error-unmatch','--',p],cwd=R,check=True,stdout=subprocess.DEVNULL);prior.append(row(p))
 m={'status':'UNPUBLISHED; root publication owner','baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'artifact_files':[row(p) for p in assets],'source_report_handoff_files':[row(p) for p in sorted(owned-set(assets))],'tracked_prior_evidence':prior,'packaging_script':row(str(Path(__file__).relative_to(R))),'packaging_handoff':row('docs/components/act-online-20261002-package.md'),'asset':'truck-act-online-20261002.tar.gz','excluded_originals':evidence['sources'],'restore':'Restore repository source allowlist plus this archive. No generated predecessor required for standalone CAD build. Prior identity reports are tracked evidence only. Source originals are optional for preservation verification and required for independent photo review.','limits':['Root accepts preservation only; no installation/thread-gauge/electrical-continuity claim','No CAD gates rerun during packaging','Original photographs, HTML and PDF excluded; local_review_path is provenance not restore prerequisite','Active pump and duct studies excluded']}
 M.write_text(json.dumps(m,indent=2)+'\n')
def build(verify):
 d=json.loads(M.read_text())
 for r in d['artifact_files']+d['source_report_handoff_files']+d['tracked_prior_evidence']+[d['packaging_script'],d['packaging_handoff']]:assert sha(R/r['path'])==r['sha256'],r['path']
 for r in d['tracked_prior_evidence']:subprocess.run(['git','ls-files','--error-unmatch','--',r['path']],cwd=R,check=True,stdout=subprocess.DEVNULL)
 rows=d['artifact_files'];assert [r['path'] for r in rows]==sorted({r['path'] for r in rows});out=R/'cad/engine/generated/act-online-20261002-package'/d['asset'];out.parent.mkdir(exist_ok=True)
 if not verify:
  with out.open('wb') as raw,gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as tar:
   for r in rows:
    p=R/r['path'];assert not p.is_symlink();info=tarfile.TarInfo(r['path']);info.size=r['size_bytes'];info.mode=0o644;info.mtime=0
    with p.open('rb') as f:tar.addfile(info,f)
 count=0
 with tarfile.open(out,'r|gz') as tar:
  for member in tar:
   r=rows[count];assert member.isfile() and member.name==r['path'];assert hashlib.sha256(tar.extractfile(member).read()).hexdigest()==r['sha256'];count+=1
 assert count==len(rows)
 result={'path':str(out.relative_to(R)),'sha256':sha(out),'size_bytes':out.stat().st_size,'members':count,'verification':'PASS exact member names/hash/order','publication':'NOT RUN'}
 if verify:assert result==d['archive']
 else:d['archive']=result;M.write_text(json.dumps(d,indent=2)+'\n')
 print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 build(a.verify_only)
