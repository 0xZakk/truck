#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,ast
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out=R/'inventory/engine/accessory-psac-carrier-delivery.json';count=0;bad=[]
for p in (R/'inventory/engine').glob('accessory-psac-carrier*.json'):
 if p==out:continue
 j=json.loads(p.read_text())
 if not isinstance(j,dict):continue
 for n,h in j.get('inputs',{}).items():
  count+=1
  if not(R/n).exists()or sha(R/n)!=h:bad.append([str(p.relative_to(R)),n])
assert not bad,bad
files=[]
for folder,pattern in [('cad/engine','accessory_psac_carrier*.py'),('scripts','accessory-psac-carrier*.py'),('docs/components','accessory-psac-carrier*.md'),('inventory/engine','accessory-psac-carrier*.json'),('cad/engine/generated','accessory-psac-carrier*.log')]:files.extend(p for p in (R/folder).glob(pattern)if p!=out)
files.extend(p for p in (R/'cad/engine/generated/accessory-psac-carrier').rglob('*')if p.is_file())
for p in files:
 if p.suffix=='.py':ast.parse(p.read_text())
canonical=R/'inventory/engine/full-assembly.json';assert sha(canonical)=='91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6'
r={'status':'FROZEN trial1 estimated load-path prototype; seven installed pulley/tool FAILs, threads/service/strength/silhouette open; no installation','selected_step':'cad/engine/generated/accessory-psac-carrier/trial1-carrier.step','selected_glb':'cad/engine/generated/accessory-psac-carrier/trial1-carrier.glb','verified_report_input_bindings':count,'binding_mismatches':bad,'syntax':'PASS','canonical_sha256':sha(canonical),'stage_sha256':sha(R/'inventory/engine/corrected-engine-stage-v3.json'),'review':'Author inspected actual STEP context and failed tool witnesses; root review pending','running_processes':'none','rejected_trial0':'cover/cartridge/side-head-tool interference; solid nut-tool proxy falsely included stud tips; all evidence retained','distance_limitation':'Impossible raw zero preserved; exact CAD partition proves v3 pump separation lower bound7mm','files_sha256':{str(p.relative_to(R)):sha(p)for p in sorted(set(files))}}
out.write_text(json.dumps(r,indent=2)+'\n');print(sha(out),len(files),count)
