from pathlib import Path
import json,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];prefix='fuel-rail-candidate-20261003';out=ROOT/'reference/engine'/f'{prefix}-delivery.json'
authored=[]
for folder in ['cad/engine','scripts','docs/components','reference/engine']:
 authored.extend(p for p in (ROOT/folder).glob(prefix+'*') if p.is_file() and p!=out)
for p in authored:
 if p.suffix=='.py':ast.parse(p.read_text())
generated=[p for p in (ROOT/'cad/engine/generated'/prefix).rglob('*') if p.is_file()]
record=lambda p:{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
d={'readiness':'candidate; installation and pressure enclosure FAIL','baseline':'5584306a595f87b60b29eca9ea82b527ade5ae98','authored':[record(p) for p in sorted(authored)],'generated':[record(p) for p in sorted(generated)],'syntax_checked_python_files':sum(p.suffix=='.py' for p in authored),'source_originals':'excluded; evidence URLs/hashes in existing intake-return-interface ledger','release':'root-owned pending','running_processes':'none at worker handoff','summary':{}}
for label in ['plus','minus']:
 c=json.loads((ROOT/'cad/engine/generated'/prefix/'r4'/label/'context.json').read_text());d['summary'][label]={'context':c['summary'],'input_guard_pass':c['input_guard_pass']}
out.write_text(json.dumps(d,indent=2)+'\n');print(len(authored),'authored',len(generated),'generated',d['syntax_checked_python_files'],'syntax PASS')
