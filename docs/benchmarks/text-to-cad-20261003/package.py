"""Archive only this experiment's generated artifacts, never source originals."""
import argparse, gzip, hashlib, json, tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);a=ap.parse_args()
paths=sorted(p for p in (ROOT/'cad/engine/generated/text-to-cad-20261003').rglob('*') if p.is_file() and p.suffix in {'.step','.glb','.npz'})
assert paths
def norm(info):
    info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0;return info
with a.output.open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as t:
    for p in paths:t.add(p,arcname=str(p.relative_to(ROOT)),filter=norm)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
members={str(p.relative_to(ROOT)):sha(p) for p in paths}
with tarfile.open(a.output,'r:gz') as t:
    assert {m.name:hashlib.sha256(t.extractfile(m).read()).hexdigest() for m in t.getmembers()}==members
report={'archive':a.output.name,'sha256':sha(a.output),'bytes':a.output.stat().st_size,'members':members,'source_originals_included':False,'release_url':'https://github.com/0xZakk/truck/releases/tag/studies-2026-10-03-cad-plugin-pilot','published':False}
(ROOT/'reference/engine/text-to-cad-20261003/package.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='members'},indent=2))
