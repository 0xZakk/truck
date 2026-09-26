#!/usr/bin/env python3
"""Plan by default; --stage exports isolated artifacts; --apply explicitly installs."""
from pathlib import Path
import argparse,copy,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_cable_integration as integration

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate_candidate(manifest,already=False):
 p=ROOT/'inventory/engine/throttle-cable-candidate-validation.json';r=json.loads(p.read_text());assert r['status']=='PASS' and r['full_sweep'] and r['final_current_neighbor_addendum']['status']=='PASS'
 required=['cad/engine/throttle_cable_candidate.py','scripts/check-throttle-cable-candidate.py','reference/engine/throttle-cable-review.json']
 for path in required:assert sha(ROOT/path)==r['input_hashes'][path],'Stale candidate input: '+path
 for path,h in r['output_hashes'].items():assert sha(ROOT/path)==h,'Candidate export changed: '+path
 viewer=json.loads((ROOT/'inventory/engine/throttle-cable-viewer-validation.json').read_text());motion=json.loads((ROOT/'inventory/engine/throttle-cable-motion-validation.json').read_text());assert viewer['status']=='PASS' and motion['status']=='PASS';assert sha(ROOT/'viewer/throttle-cable-motion.json')==viewer['table_sha256']==motion['output_sha256'];assert sha(ROOT/'viewer/throttle-cable-motion.js')==viewer['module_sha256'];return dict(candidate_report_sha256=sha(p),candidate_source_sha256=sha(ROOT/required[0]),review_sha256=sha(ROOT/required[2]),motion_report_sha256=sha(ROOT/'inventory/engine/throttle-cable-motion-validation.json'),viewer_report_sha256=sha(ROOT/'inventory/engine/throttle-cable-viewer-validation.json'),proof_scope_sha256=sha(ROOT/'inventory/engine/throttle-cable-candidate-proof-scope.json'))
def proof_scope():
 path=ROOT/'inventory/engine/throttle-cable-candidate-proof-scope.json';proof=json.loads(path.read_text());assert proof['candidate_report_sha256']==sha(ROOT/'inventory/engine/throttle-cable-candidate-validation.json');return proof
def scoped(manifest,ids,occids):
 ds={d['id']:d for d in manifest['definitions']};os={o['id']:o for o in manifest['occurrences']};aa={a['id']:a for a in manifest['assemblies']};parents=set()
 for key in occids:
  p=os[key]['parent']
  while p in aa:parents.add(p);p=aa[p]['parent']
 return dict(definitions={i:ds[i] for i in sorted(ids)},occurrences={i:os[i] for i in sorted(occids)},assemblies={i:aa[i] for i in sorted(parents)})
def assert_scope(before,after,changed):
 for kind,allowed in [('definitions',integration.CHANGED_IDS),('occurrences',set(changed['changed_occurrences'])),('assemblies',set())]:
  assert {r['id']:r for r in before[kind] if r['id'] not in allowed}=={r['id']:r for r in after[kind] if r['id'] not in allowed},'Unrelated '+kind
  assert len(after[kind])==len({r['id'] for r in after[kind]}),'Duplicate '+kind
 old={o['id']:o for o in before['occurrences']};new={o['id']:o for o in after['occurrences']}
 for ident in integration.REPLACED:
  for o in [o for o in before['occurrences'] if o['definition']==ident]:
   for key in ['parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:assert o.get(key)==new[o['id']].get(key)
def main():
 p=argparse.ArgumentParser(description=__doc__);mode=p.add_mutually_exclusive_group();mode.add_argument('--stage',action='store_true');mode.add_argument('--apply',action='store_true');p.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/throttle-cable-integration-stage');args=p.parse_args()
 if not(args.stage or args.apply):print('Plan only: replace distal cable bracket; add seven illustrative cable definitions and occurrences. No writes.');return
 import full_engine as engine
 target=ROOT/'inventory/engine/full-assembly.json';raw=target.read_bytes();before=json.loads(raw);manifest=copy.deepcopy(before);already=any(d['id'] in integration.NEW_IDS for d in before['definitions']);evidence=validate_candidate(before,already)
 if already:
  prior=json.loads((ROOT/'inventory/engine/throttle-cable-installation.json').read_text())
  assert prior['candidate_evidence']==evidence,'Candidate changed since install: fresh upstream-base review required'
  assert scoped(before,integration.CHANGED_IDS,prior['changed_occurrences'])['occurrences']==prior['installed_scope']['occurrences'],'Installed local part frames changed'
  for path,h in prior['canonical_artifact_sha256'].items():assert sha(ROOT/path)==h,path
 out=args.stage_dir.resolve()
 if ROOT not in out.parents or 'generated' not in out.parts:raise ValueError('Stage must be inside repository generated artifacts')
 out.mkdir(parents=True,exist_ok=True);(out/'baseline-manifest.json').write_bytes(raw);engine.STEP=out/'step';engine.OUT=out/'models';engine.STEP.mkdir(exist_ok=True);engine.OUT.mkdir(exist_ok=True)
 engine.defs[:]=manifest['definitions'];engine.occurrences[:]=manifest['occurrences'];engine.assemblies[:]=manifest['assemblies'];engine.shapes.clear()
 (out/'baseline-step').mkdir(exist_ok=True)
 for d in before['definitions']:
  if d['id'] in integration.REPLACED:(out/'baseline-step'/(d['id']+'.step')).write_bytes((ROOT/d['step'].lstrip('/')).read_bytes())
 changed=integration.install(engine.define,engine.add,engine.defs,engine.occurrences,engine.assemblies,engine.shapes)
 for definition in engine.defs:
  if definition['id'] in integration.CHANGED_IDS:definition['model_bounds_mm']=list(engine.shapes[definition['id']].bounding_box().size)
 manifest.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies);manifest['sources'].update(integration.source());manifest['coverage'].update(modeled_definitions=len(engine.defs),modeled_occurrences=len(engine.occurrences));assert_scope(before,manifest,changed)
 stage=out/'full-assembly.json';stage.write_text(json.dumps(manifest,indent=2)+'\n')
 record=dict(status='STAGED; educational integration acceptance pending',before_manifest_sha256=hashlib.sha256(raw).hexdigest(),staged_manifest_sha256=sha(stage),baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),candidate_evidence=evidence,candidate_proof_scope=prior['candidate_proof_scope'] if already else proof_scope(),**changed,installed_scope=scoped(manifest,integration.CHANGED_IDS,changed['changed_occurrences']),before_occurrences=[o for o in before['occurrences'] if o['id'] in changed['changed_occurrences']],baseline_step_sha256={str(p.relative_to(out)):sha(p) for p in (out/'baseline-step').glob('*.step')},stage_directory=str(out.relative_to(ROOT)),canonical_modified=False,unrelated_inventory_unchanged=True,installer_sha256=sha(__file__),checker_sha256=sha(ROOT/'scripts/check-throttle-cable-installed.py'),adapter_sha256=sha(ROOT/'cad/engine/throttle_cable_integration.py'),learning_sha256=sha(ROOT/'inventory/engine/throttle-cable-learning.json'),exporter_sha256=sha(ROOT/'cad/engine/full_engine.py'),motion_table_sha256=sha(ROOT/'viewer/throttle-cable-motion.json'),motion_module_sha256=sha(ROOT/'viewer/throttle-cable-motion.js'),staged_artifact_sha256={str(path.relative_to(out)):sha(path) for folder in ['step','models'] for path in (out/folder).iterdir() if path.stem in integration.CHANGED_IDS})
 (out/'installation.json').write_text(json.dumps(record,indent=2)+'\n');assert target.read_bytes()==raw,'Assembly changed while staging';validate_candidate(before,already)
 if args.apply:
  subprocess.run([sys.executable,str(ROOT/'scripts/check-throttle-cable-installed.py'),'--stage-dir',str(out)],check=True)
  assert target.read_bytes()==raw,'Assembly changed during preflight';validate_candidate(before,already)
  assert sha(ROOT/'cad/engine/full_engine.py')==record['exporter_sha256'],'Exporter changed during preflight'
  writes={target:stage.read_bytes()}
  for ident in integration.CHANGED_IDS:
   writes[ROOT/f'cad/engine/generated/{ident}.step']=(engine.STEP/f'{ident}.step').read_bytes();writes[ROOT/f'models/engine/{ident}.glb']=(engine.OUT/f'{ident}.glb').read_bytes()
  record.update(status='INSTALLED; browser/factory acceptance pending',canonical_modified=True,after_manifest_sha256=sha(stage),stage_validation_sha256=sha(out/'validation.json'),canonical_artifact_sha256={str(path.relative_to(ROOT)):hashlib.sha256(data).hexdigest() for path,data in writes.items() if path!=target})
  writes[ROOT/'inventory/engine/throttle-cable-installation.json']=(json.dumps(record,indent=2)+'\n').encode();backups={path:path.read_bytes() if path.exists() else None for path in writes}
  try:
   for path,data in writes.items():tmp=path.with_suffix(path.suffix+'.pending');tmp.write_bytes(data);tmp.replace(path)
  except Exception:
   for path,data in backups.items():
    if data is None:path.unlink(missing_ok=True)
    else:path.write_bytes(data)
   raise
 print(json.dumps(dict(status=record['status'],stage=str(out),definitions=len(manifest['definitions']),occurrences=len(manifest['occurrences']),changed=changed),indent=2))
if __name__=='__main__':main()
