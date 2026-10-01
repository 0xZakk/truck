#!/usr/bin/env python3
"""Bind isolated proposal and verify existing report input hashes without rebuilding."""
from pathlib import Path
import hashlib,json,ast
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out=R/'inventory/engine/accessory-constrained-layout-delivery.json';count=0;bad=[]
for p in R.glob('inventory/engine/accessory-constrained-layout*.json'):
 if p==out:continue
 for name,h in json.loads(p.read_text()).get('input_sha256',{}).items():
  count+=1;q=R/name
  if not q.exists()or sha(q)!=h:bad.append([str(p.relative_to(R)),name])
assert not bad,bad
for p in R.glob('scripts/accessory-constrained-layout*.py'):ast.parse(p.read_text())
files=[]
for folder in ['scripts','docs/components','inventory/engine']:
 files.extend(p for p in (R/folder).glob('accessory-constrained-layout*')if p.is_file()and p!=out)
files.extend(p for p in (R/'cad/engine/generated/accessory-constrained-layout').rglob('*')if p.is_file())
r={'status':'FROZEN conditional numerical feasibility and support proposal; no installation or replacement carriers','verified_report_input_bindings':count,'binding_mismatches':bad,'python_syntax':'PASS','stage_sha256':sha(R/'inventory/engine/corrected-engine-stage-v3.json'),'canonical_sha256':sha(R/'inventory/engine/full-assembly.json'),'actual_q0_pairs':47,'pump_sensitivity_pairs':10,'review':'Actual mesh/front route image inspected by author; root support review pending','running_processes':'none','files_sha256':{str(p.relative_to(R)):sha(p)for p in sorted(set(files))}}
out.write_text(json.dumps(r,indent=2)+'\n');print(sha(out),len(files),count)
