"""Preserve frozen online-research candidates; exact allowlists, no publishing."""
from pathlib import Path
import argparse, gzip, hashlib, json, subprocess, tarfile
R=Path(__file__).resolve().parents[1]
M=R/'docs/online-research-candidates-checkpoint.json'
LEDGERS=['inventory/engine/online-heater-route-delivery.json','reference/engine/online-airbox-duct-delivery.json']
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def row(p): return {'path':p,'sha256':sha(R/p),'size_bytes':(R/p).stat().st_size}
def hashes(x):
    if isinstance(x,dict):
        for key in ('path','file'):
            if isinstance(x.get(key),str) and isinstance(x.get('sha256'),str): yield x[key],x['sha256']
        for k,v in x.items():
            if '/' in k and isinstance(v,str) and len(v)==64 and all(c in '0123456789abcdef' for c in v): yield k,v
            else: yield from hashes(v)
    elif isinstance(x,list):
        for v in x: yield from hashes(v)
def prepare():
    owned=set(LEDGERS); excluded=[]
    for p in LEDGERS:
        d=json.loads((R/p).read_text()); files=d.get('files',d.get('files_sha256'))
        assert isinstance(files,dict),p
        for target,h in files.items():
            assert sha(R/target)==h,(p,target)
            # Ingest output is capture metadata, not required authored candidate content.
            if '/online-heater-ingest-' in target or target.endswith('online-heater-ocr.log'):
                excluded.append(row(target)); continue
            assert not any(s in target for s in ['/captures/','-captures/','kb/.raw/'])
            if not target.startswith('cad/engine/generated/'):
                assert Path(target).suffix in ('.py','.json','.md','.log'),target
            owned.add(target)
    index={}; metadata=[]
    for p in sorted(R.glob('docs/*checkpoint*.json')):
        if p==M: continue
        metadata.append(row(str(p.relative_to(R))))
        for target,h in hashes(json.loads(p.read_text())): index.setdefault((target,h),set()).add(str(p.relative_to(R)))
    ext={}
    for p in sorted(owned):
        if not p.endswith('.json'): continue
        for target,h in hashes(json.loads((R/p).read_text())):
            if target in owned or target.startswith('/'): continue
            local=R/target
            if not local.is_file(): continue # URL/provenance-only records remain in frozen ledgers.
            assert sha(local)==h,(p,target)
            ext.setdefault((target,h),set()).add(p)
    external=[]
    for (p,h),uses in sorted(ext.items()):
        source=('/captures/' in p or '-captures/' in p or p.startswith(('manuals/','kb/.raw/')) or (p.startswith('reference/') and Path(p).suffix not in ('.json','.md','.log')))
        capture=('/online-heater-ingest-' in p or p.endswith('online-heater-ocr.log'))
        kind='excluded capture metadata' if capture else ('excluded source original' if source else 'repository input')
        if p.startswith('cad/engine/generated/') and not source: kind='prior exact hash' if (p,h) in index else 'UNRESOLVED generated prerequisite'
        if kind=='repository input':
            subprocess.run(['git','ls-files','--error-unmatch','--',p],cwd=R,check=True,stdout=subprocess.DEVNULL)
        external.append({'path':p,'sha256':h,'classification':kind,'used_by':sorted(uses),'matching_metadata':sorted(index.get((p,h),[]))})
    used_metadata={p for r in external for p in r['matching_metadata']}
    metadata=[r for r in metadata if r['path'] in used_metadata]
    assets=sorted(p for p in owned if p.startswith('cad/engine/generated/'))
    assert all(Path(p).suffix in ('.step','.glb','.png','.npz','.json','.log','.py') for p in assets)
    d={'status':'UNPUBLISHED; root owns publication','baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'asset':'truck-online-research-candidates-20261001.tar.gz','packaging_script':row(str(Path(__file__).relative_to(R))),'packaging_handoff':row('docs/components/online-research-candidates-checkpoint.md'),'scope':'Conditional heater route and uninstalled airbox duct specimen; preserved estimates and rejected constructions; no installed acceptance','artifact_files':[row(p) for p in assets],'source_report_handoff_files':[row(p) for p in sorted(owned-set(assets))],'external_inputs':external,'prerequisite_metadata':metadata,'excluded_capture_metadata':excluded,'exclusions':['All source originals, photos, PDFs, raw captures and source-image composites','No model or shared inventory changes'],'image_provenance':[{'path':p,'kind':'Project-authored actual CAD/mesh render; no source pixels'} for p in assets if p.endswith('.png')],'restore_order':'Repository at recorded baseline plus candidate source allowlist; published neck-core and supplements through waterpump studies, accessory-layout and accessory-stage-v4; then this archive. See matching prerequisite metadata and CAD-ARTIFACTS for release URLs.','limits':['Preservation checks only; no CAD checks rerun','Heater is conditional and radial projection remains unregistered','Airbox specimen has no vehicle pose or installed interface acceptance','Prior hashes matched to metadata; prior archives not freshly reopened','Excluded source originals must be reacquired by source-ledger URLs; not needed to view exported candidate solids']}
    M.write_text(json.dumps(d,indent=2)+'\n')
def build(verify):
    d=json.loads(M.read_text()); assert sha(R/d['packaging_script']['path'])==d['packaging_script']['sha256']
    assert sha(R/d['packaging_handoff']['path'])==d['packaging_handoff']['sha256']
    for r in d['artifact_files']+d['source_report_handoff_files']+d['external_inputs']+d['prerequisite_metadata']:
        if r.get('classification') in ('excluded source original','excluded capture metadata') and not (R/r['path']).exists(): continue
        if r.get('classification')=='repository input':
            subprocess.run(['git','ls-files','--error-unmatch','--',r['path']],cwd=R,check=True,stdout=subprocess.DEVNULL)
        assert sha(R/r['path'])==r['sha256'],r['path']
    assert not [r for r in d['external_inputs'] if r['classification'].startswith('UNRESOLVED')]
    rows=d['artifact_files']; assert [r['path'] for r in rows]==sorted({r['path'] for r in rows})
    out=R/'cad/engine/generated/online-research-candidates-checkpoint'/d['asset']; out.parent.mkdir(exist_ok=True)
    if not verify:
        with out.open('wb') as raw,gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as tar:
            for r in rows:
                p=R/r['path']; assert not p.is_symlink(); info=tarfile.TarInfo(r['path']); info.size=r['size_bytes']; info.mode=0o644; info.mtime=0
                with p.open('rb') as f: tar.addfile(info,f)
    count=0
    with tarfile.open(out,'r|gz') as tar:
        for member in tar:
            r=rows[count]; assert member.isfile() and member.name==r['path']
            assert hashlib.sha256(tar.extractfile(member).read()).hexdigest()==r['sha256']; count+=1
    assert count==len(rows)
    result={'path':str(out.relative_to(R)),'sha256':sha(out),'size_bytes':out.stat().st_size,'members':count,'member_verification':'PASS','publication':'NOT RUN'}
    if verify: assert result==d['archive']
    else: d['archive']=result; M.write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
    if a.prepare: prepare()
    build(a.verify_only)
