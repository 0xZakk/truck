"""Freeze owned reproducible inputs/results without private source pixels or r7 work."""
from pathlib import Path
import ast,hashlib,json,tarfile
ROOT=Path(__file__).resolve().parents[1];prefix='fuel-rail-candidate-20261003'
OUT=ROOT/'reference/engine'/f'{prefix}-delivery-r2-r6.json'
archive=ROOT/'cad/engine/generated'/f'{prefix}-r2-r6.tar.gz'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[]
for folder in ['cad/engine','scripts','docs/components','reference/engine']:
 files += [p for p in (ROOT/folder).glob(prefix+'*') if p.is_file() and '-r7' not in p.name and p!=OUT and not p.name.endswith('-delivery.json') and not p.name.endswith('-archive-r2-r6.json')]
files += [p for p in (ROOT/'cad/engine/generated'/prefix).rglob('*') if p.is_file() and 'r7' not in p.parts]
files=sorted(set(files))
for p in files:
 if p.suffix=='.py':ast.parse(p.read_text())
record=lambda p:{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)}
d={'scope':'frozen r2–r6 candidate evidence; not installed or sealed regulator acceptance','baseline':'5584306a595f87b60b29eca9ea82b527ade5ae98','source_pixels':'excluded; source identifiers, URLs and hashes only','r7':'excluded; new research/proposal proceeds separately','inputs':[record(p) for p in files],'syntax_checked_python_files':sum(p.suffix=='.py' for p in files),'reproduction':'Versioned build entrypoints use frozen sources; see handoff for existing CAD runtime and repository baseline dependencies. Archive is an overlay on repository, not standalone runtime.','context':{}}
for label in ['plus','minus']:
 c=json.loads((ROOT/'cad/engine/generated'/prefix/'r6'/label/'context.json').read_text());d['context'][label]={'summary':c['summary'],'guard_pass':c['input_guard_pass']}
OUT.write_text(json.dumps(d,indent=2)+'\n')
with tarfile.open(archive,'w:gz') as tf:
 for p in files+[OUT]:tf.add(p,arcname=str(p.relative_to(ROOT)),recursive=False)
with tarfile.open(archive) as tf:
 for row in d['inputs']:
  assert hashlib.sha256(tf.extractfile(row['path']).read()).hexdigest()==row['sha256']
receipt=OUT.with_name(f'{prefix}-archive-r2-r6.json');receipt.write_text(json.dumps({'archive':str(archive.relative_to(ROOT)),'sha256':sha(archive),'bytes':archive.stat().st_size,'ledger':str(OUT.relative_to(ROOT)),'ledger_sha256':sha(OUT),'members_verified':len(files)+1},indent=2)+'\n')
print(receipt.read_text())
