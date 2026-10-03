"""Preserve exact authored ACT registration outputs; exclude source pixels."""
from pathlib import Path
import gzip,hashlib,io,json,tarfile
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=R/'reference/engine/act-host-estimate-20261002-delivery.json'
d=json.loads(ledger.read_text())
for p,h in d['files'].items():
    assert sha(R/p)==h,p
members=sorted(p for p in d['files'] if p.startswith('cad/engine/generated/'))
assert len(members)==3
out=R/'cad/engine/generated/host-research-20261003/truck-host-research-20261003.tar.gz'
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('wb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as t:
    for p in members:
        data=(R/p).read_bytes();i=tarfile.TarInfo(p);i.size=len(data);i.mode=0o644;i.mtime=0;t.addfile(i,io.BytesIO(data))
with tarfile.open(out) as t:
    assert t.getnames()==members
    for i in t:
        assert i.isfile() and hashlib.sha256(t.extractfile(i).read()).hexdigest()==d['files'][i.name]
record={'scope':'Authored registration sensitivity figure/logs only; no CAD acceptance','asset':out.name,'sha256':sha(out),'size_bytes':out.stat().st_size,'members':{p:d['files'][p] for p in members},'source_ledger':str(ledger.relative_to(R)),'source_ledger_sha256':sha(ledger),'verification':'PASS exact3members','publication':'NOT RUN','source_originals_included':False,'reproduction':'Repository scripts/contracts/reports are required alongside archive. Numerical CAD-host replay requires the hash-bound installed neck-core STEP and separately authorized manual source. Archive preservation verification needs neither source pixels nor CAD.'}
(R/'reference/engine/host-research-20261003-package.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['asset','sha256','size_bytes','verification']}))
