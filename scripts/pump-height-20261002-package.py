"""Deterministic archive of frozen failed pump-height trials; no CAD execution."""
from pathlib import Path
import ast,gzip,hashlib,io,json,tarfile,subprocess
R=Path(__file__).resolve().parents[1]
D=R/'reference/engine/pump-height-20261002-delivery.json'
EXPECTED='2fb78da789a3e7e4207e822bca2aa4879067bce795d030e4c2ae2445d8241a17'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def row(p):return {'path':p,'sha256':sha(R/p),'size_bytes':(R/p).stat().st_size}
def check(mapping):
 for p,h in mapping.items():assert sha(R/p)==h,p
assert sha(D)==EXPECTED
old=json.loads(D.read_text())
for key in ['authored_files','generated_assets','guarded_inputs']:check(old[key])
extra={p:h for p,h in old['authored_files'].items()if Path(p).suffix in ['.png','.npz']}
assets={**old['generated_assets'],**extra}
assert len(assets)==584
assert all(p.startswith(('cad/engine/generated/pump-height-20261002','reference/engine/pump-height-20261002'))for p in assets)
assert not any('-captures/'in p or '/.raw/'in p for p in assets)
owned={p:h for p,h in old['authored_files'].items()if p not in assets}
for p in [str(D.relative_to(R)),str(Path(__file__).relative_to(R)),'docs/components/pump-height-20261002-package-handoff.md']:owned[p]=sha(R/p)
# Exact inherited generated-member identities, not merely occurrence names.
index={};metadata={}
for p in sorted((R/'docs').glob('*checkpoint*.json')):
 d=json.loads(p.read_text());items=[]
 for k in ['artifact_files','file_sha256']:
  v=d.get(k,[])
  items.extend(v.items()if isinstance(v,dict)else[(q['path'],q['sha256'])for q in v])
 for n,h in items:index.setdefault((n,h),set()).add(str(p.relative_to(R)))
 metadata[str(p.relative_to(R))]=d
p='inventory/engine/waterpump-prerequisite-archive-audit.json';prior=json.loads((R/p).read_text());assert prior['status'].startswith('PASS')
for q in prior['members']:index.setdefault((q['path'],q['archive_member_sha256']),set()).add(p)
# Static transitive local imports are bound without executing model builders.
sourceclosure={};queue=[p for p in owned if p.endswith('.py')]
while queue:
 p=queue.pop()
 if p in sourceclosure:continue
 sourceclosure[p]=sha(R/p)
 tree=ast.parse((R/p).read_text())
 for node in ast.walk(tree):
  modules=[a.name for a in node.names]if isinstance(node,ast.Import)else[node.module]if isinstance(node,ast.ImportFrom)and node.module else[]
  for mod in modules:
   q=R/'cad/engine'/(mod.split('.')[0]+'.py')
   if q.is_file()and str(q.relative_to(R))not in sourceclosure:queue.append(str(q.relative_to(R)))
external={**old['guarded_inputs'],**sourceclosure}
metric='reference/engine/pump-metric-20261002-delivery.json';external[metric]=sha(R/metric)
md=json.loads((R/metric).read_text());check(md['authored_files']);external.update(md['authored_files'])
external={p:h for p,h in external.items()if p not in assets and p not in owned}
rows=[];unresolved=[]
tracked=set(subprocess.check_output(['git','ls-files'],cwd=R,text=True).splitlines())
for p,h in sorted(external.items()):
 assert sha(R/p)==h,p
 matches=sorted(index.get((p,h),[]))
 if p.startswith('cad/engine/generated/'):
  kind='hash-matched predecessor member'if matches else'UNRESOLVED generated prerequisite'
  if not matches:unresolved.append(p)
 else:kind='tracked repository dependency'if p in tracked else'coordinated authored dependency for root preservation'
 rows.append({'path':p,'sha256':h,'classification':kind,'matching_metadata':matches})
# Do not hide missing restoration provenance.
assert not unresolved,unresolved
O=R/'cad/engine/generated/pump-height-20261002-package';O.mkdir(exist_ok=True)
a=O/'truck-pump-height-20261002.tar.gz';second=O/'pump-height-20261002-package-rebuild.tar.gz'
def pack(out):
 with out.open('wb')as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0)as gz:
   with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT)as tf:
    for p in sorted(assets):
     data=(R/p).read_bytes();assert hashlib.sha256(data).hexdigest()==assets[p]
     info=tarfile.TarInfo(p);info.size=len(data);info.mtime=0;info.uid=info.gid=0;info.uname=info.gname='';info.mode=0o644;tf.addfile(info,io.BytesIO(data))
pack(a);pack(second);assert sha(a)==sha(second);second.unlink()
with tarfile.open(a,'r:gz')as tf:
 assert tf.getnames()==sorted(assets)
 for member in tf:
  assert member.isfile()and not member.name.startswith('/')and'..'not in Path(member.name).parts
  assert hashlib.sha256(tf.extractfile(member).read()).hexdigest()==assets[member.name]
used=sorted({p for r in rows for p in r['matching_metadata']})
r={'status':'UNPUBLISHED preservation verified; candidate remains FAIL integration','frozen_delivery':row(str(D.relative_to(R))),'archive':{**row(str(a.relative_to(R))),'members':len(assets),'repeat_byte_identity':True,'streamed_member_hash_check':'PASS'},'artifact_files':[row(p)for p in sorted(assets)],'authored_source_report_files':[row(p)for p in sorted(owned)],'external_inputs':rows,'prerequisite_metadata':[row(p)for p in used],'dependency_verification':'Current files and exact prior member inventories verified; earlier archive stream audits reused, not freshly reopened','source_originals_excluded':True,'failure_state':'Four nominal q0 overlaps; rear preservation violated; six mesh bounds failures and nonwatertight spring; local seat/path checks bounded','next_scope':'Source-driven short-chamber housing and estimated carrier interface review','no_cad_reruns':True}
(R/'reference/engine/pump-height-20261002-package.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['archive'],indent=2));print('sources',len(owned),'dependencies',len(rows),'metadata',len(used))
