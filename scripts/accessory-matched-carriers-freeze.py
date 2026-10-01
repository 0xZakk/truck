#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,ast
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out=R/'inventory/engine/accessory-matched-carriers-delivery.json';count=0;bad=[]
for p in (R/'inventory/engine').glob('accessory-matched-carriers*.json'):
 if p==out:continue
 j=json.loads(p.read_text())
 for n,h in j.get('inputs',{}).items():
  count+=1
  if not(R/n).exists()or sha(R/n)!=h:bad.append([str(p.relative_to(R)),n])
assert not bad,bad
files=[]
for folder,pattern in [('cad/engine','accessory_matched_carriers*.py'),('scripts','accessory-matched-carriers*.py'),('docs/components','accessory-matched-carriers*.md'),('inventory/engine','accessory-matched-carriers*.json'),('cad/engine/generated','accessory-matched-carriers*.log')]:
 files.extend(p for p in (R/folder).glob(pattern)if p!=out)
files.extend(p for p in (R/'cad/engine/generated/accessory-matched-carriers').rglob('*')if p.is_file())
for p in files:
 if p.suffix=='.py':ast.parse(p.read_text())
canonical=R/'inventory/engine/full-assembly.json';assert sha(canonical)=='91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6'
r={'status':'FROZEN trial6 conditional support geometry; lower fixed engine bolt/new inlet tool FAIL; no installation','selected_step':'cad/engine/generated/accessory-matched-carriers/trial6-carrier.step','selected_glb':'cad/engine/generated/accessory-matched-carriers/trial6-carrier.glb','verified_report_input_bindings':count,'binding_mismatches':bad,'syntax':'PASS','canonical_sha256':sha(canonical),'stage_sha256':sha(R/'inventory/engine/corrected-engine-stage-v3.json'),'review':'Author inspected actual trial6 and failed tool context images; root reviewed scoped trial6 progress, factory silhouette/retention/access remain open','running_processes':'none','rejected_trials':{'trial0':'seat/head/pump collisions; AP initial mate owner wrong','trial1':'invalid rounded rib stock; numeric results rejected','trial2':'lost stock despite valid one-solid; numeric results rejected','trial3':'AP body/cartridge and fixed-seat guard failure','trial4':'AP plate/hub conflict','trial5':'AP case bolt conflict'},'files_sha256':{str(p.relative_to(R)):sha(p)for p in sorted(set(files))}}
out.write_text(json.dumps(r,indent=2)+'\n');print(sha(out),len(files),count)
