"""Freeze only authored common-face research; never package source photographs."""
from pathlib import Path
import sys,json,hashlib,platform
import numpy,scipy,matplotlib
R=Path(__file__).resolve().parents[1];P='pump-cover-joint-20261003';dest=R/f'reference/engine/{P}-delivery.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--verify' in sys.argv:
 d=json.loads(dest.read_text());bad=[]
 for group in ['authored','guarded_inputs']:
  for q in d[group]:
   p=R/q['path']
   if not p.is_file() or sha(p)!=q['sha256']:bad.append(q['path'])
 print(json.dumps({'status':'PASS'if not bad else'FAIL','bad':bad,'authored_count':len(d['authored']),'guarded_count':len(d['guarded_inputs'])},indent=2));sys.exit(bool(bad))
files=[]
for folder in ['docs/components','reference/engine','scripts']:
 files.extend(p for p in(R/folder).glob(P+'*')if p.is_file()and p!=dest)
inputs={}
for file in ['measurements','joint-fit','datums']:
 j=json.loads((R/f'reference/engine/{P}-{file}.json').read_text())
 for path,h in j.get('inputs_sha256',j.get('input_sha256',{})).items():
  if not Path(path).name.startswith(P):inputs[path]=h
for path,h in inputs.items():assert sha(R/path)==h,path
records=lambda paths:[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(paths)]
d={'status':'Frozen research; contract pending root review; no CAD','baseline':'0e9d513794e7bab3dfcab45c7da06a669bb44878','authored':records(files),'guarded_inputs':[{'path':p,'sha256':h}for p,h in sorted(inputs.items())],'distribution':'Author-created scripts/reports/plots only. Source photographs listed as guardedinputs are EXCLUDED from Git and releases.','environment':{'python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'live_handles':[]}
dest.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'ledger':str(dest.relative_to(R)),'sha256':sha(dest),'authored':len(files),'guarded':len(inputs)},indent=2))
