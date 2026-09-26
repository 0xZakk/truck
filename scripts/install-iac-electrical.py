#!/usr/bin/env python3
"""Dry-run plan by default. --stage is isolated; --apply requires checked staging."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import iac_electrical_integration as adapter

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def scoped(m,defs,occs):
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};A={a['id']:a for a in m['assemblies']};parents=set()
 for key in occs:
  p=O[key]['parent']
  while p in A:parents.add(p);p=A[p]['parent']
 return dict(definitions={k:D[k] for k in sorted(defs)},occurrences={k:O[k] for k in sorted(occs)},assemblies={k:A[k] for k in sorted(parents)})
def evidence(already=False):
 p=ROOT/'cad/engine/generated/iac-electrical-candidate/validation.json';r=json.loads(p.read_text());assert r['status']=='PASS' and r['relevant_inputs_stable']
 # Closure is an explicit downstream adaptation, not a waived body hash. The
 # checker binds body/plug to the frozen closure candidate and installed proof.
 adapted={'cad/engine/generated/iac-valve-body.step','cad/engine/generated/iac-end-plug.step','cad/engine/generated/efi-upper-intake.step','models/engine/efi-upper-intake.glb'}
 if already:adapted|={f'cad/engine/generated/{i}.step' for i in adapter.REPLACED}
 for key,h in r['input_sha256'].items():
  if key in adapted:continue
  assert sha(ROOT/key)==h,'Changed electrical dependency: '+key
 for key,h in r['output_sha256'].items():assert sha(ROOT/key)==h,key
 cp=ROOT/'inventory/engine/iac-closure-installed-validation.json';cr=json.loads(cp.read_text());assert cr['status']=='PASS' and cr['installed'] and cr['relevant_inputs_stable']
 for key,h in cr['artifact_sha256'].items():
  if already and key in {f'cad/engine/generated/{i}.step' for i in adapter.REPLACED}:continue
  assert sha(ROOT/key)==h,'Changed closure check input: '+key
 spec=importlib.util.spec_from_file_location('closure_evidence',ROOT/'scripts/install-iac-closure.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
 return dict(exterior_adaptation=helper.exterior_evidence(),closure_installer_sha256=sha(ROOT/'scripts/install-iac-closure.py'),electrical_report_sha256=sha(p),closure_installed_report_sha256=sha(cp),closure_source_sha256=sha(ROOT/'cad/engine/iac_closure_candidate.py'),attachment_source_sha256=sha(ROOT/'cad/engine/iac_attachment_candidate.py'))
def assert_scope(before,after,changed):
 for kind,allowed in [('definitions',adapter.CHANGED_IDS),('occurrences',set(changed['changed_occurrences'])),('assemblies',set())]:
  assert {r['id']:r for r in before[kind] if r['id'] not in allowed}=={r['id']:r for r in after[kind] if r['id'] not in allowed},kind
  assert len(after[kind])==len({r['id'] for r in after[kind]})
 old={d['id']:d for d in before['definitions']};new={d['id']:d for d in after['definitions']}
 O={o['id']:o for o in after['occurrences']}
 for o in before['occurrences']:
  if o['id'] in adapter.NEW_OCCURRENCES:continue
  for k in ['definition','parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:assert o.get(k)==O[o['id']].get(k)
def main():
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group();g.add_argument('--stage',action='store_true');g.add_argument('--apply',action='store_true');p.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/iac-electrical-integration-stage');args=p.parse_args()
 if not(args.stage or args.apply):print('Plan only: replace cap/coil; add two terminals and insulating carrier. No writes.');return
 import full_engine as engine
 target=ROOT/'inventory/engine/full-assembly.json';raw=target.read_bytes();before=json.loads(raw);m=copy.deepcopy(before);already=adapter.SOURCE_IDS[0] in before['sources'];ev=evidence(already)
 if already:
  rec=json.loads((ROOT/'inventory/engine/iac-electrical-installation.json').read_text());assert rec['candidate_evidence']==ev,'Changed candidate requires fresh upstream review'
  assert scoped(before,set(rec['installed_scope']['definitions']),rec['guard_occurrences'])==rec['installed_scope']
  for key,h in rec['canonical_artifact_sha256'].items():assert sha(ROOT/key)==h,key
 out=args.stage_dir.resolve()
 if ROOT not in out.parents or 'generated' not in out.parts:raise ValueError('Stage directory must be inside repository generated artifacts')
 out.mkdir(parents=True,exist_ok=True);engine.STEP=out/'step';engine.OUT=out/'models';engine.STEP.mkdir(exist_ok=True);engine.OUT.mkdir(exist_ok=True)
 engine.defs[:]=m['definitions'];engine.occurrences[:]=m['occurrences'];engine.assemblies[:]=m['assemblies'];engine.shapes.clear()
 changed=adapter.install(engine.define,engine.add,engine.group,engine.defs,engine.occurrences,engine.assemblies,engine.shapes)
 for row in engine.defs:
  if row['id'] in adapter.GEOMETRY_IDS:row['model_bounds_mm']=list(engine.shapes[row['id']].bounding_box().size)
 m.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies);m['sources'].update(adapter.sources());assert_scope(before,m,changed)
 guard_occurrences=sorted(o['id'] for o in m['occurrences'] if o['id'].startswith('iac-') or o['id'] in ['throttle-housing','efi-upper-intake'])
 path=out/'full-assembly.json';path.write_text(json.dumps(m,indent=2)+'\n')
 record=dict(status='STAGED; illustrative electrical construction only',before_manifest_sha256=hashlib.sha256(raw).hexdigest(),staged_manifest_sha256=sha(path),candidate_evidence=ev,**changed,guard_occurrences=guard_occurrences,installed_scope=scoped(m,{o['definition'] for o in m['occurrences'] if o['id'] in guard_occurrences},guard_occurrences),canonical_modified=False,installer_sha256=sha(__file__),checker_sha256=sha(ROOT/'scripts/check-iac-electrical-installed.py'),adapter_sha256=sha(ROOT/'cad/engine/iac_electrical_integration.py'),learning_sha256=sha(ROOT/'inventory/engine/iac-electrical-learning.json'),exporter_sha256=sha(ROOT/'cad/engine/full_engine.py'),metrics_sha256=sha(ROOT/'cad/engine/cad_metrics.py'),staged_artifact_sha256={str(p.relative_to(out)):sha(p) for folder in ['step','models'] for p in (out/folder).iterdir() if p.stem in adapter.GEOMETRY_IDS})
 (out/'installation.json').write_text(json.dumps(record,indent=2)+'\n');assert target.read_bytes()==raw;evidence(already)
 if args.apply:
  subprocess.run([sys.executable,str(ROOT/'scripts/check-iac-electrical-installed.py'),'--stage-dir',str(out)],check=True);assert target.read_bytes()==raw;evidence(already);assert sha(ROOT/'cad/engine/full_engine.py')==record['exporter_sha256'];assert sha(ROOT/'cad/engine/cad_metrics.py')==record['metrics_sha256']
  writes={target:path.read_bytes()}
  for ident in adapter.GEOMETRY_IDS:
   writes[ROOT/f'cad/engine/generated/{ident}.step']=(engine.STEP/f'{ident}.step').read_bytes();writes[ROOT/f'models/engine/{ident}.glb']=(engine.OUT/f'{ident}.glb').read_bytes()
  record.update(status='INSTALLED; browser/manufacturing acceptance pending',canonical_modified=True,after_manifest_sha256=sha(path),stage_validation_sha256=sha(out/'validation.json'),canonical_artifact_sha256={str(p.relative_to(ROOT)):hashlib.sha256(d).hexdigest() for p,d in writes.items() if p!=target})
  writes[ROOT/'inventory/engine/iac-electrical-installation.json']=(json.dumps(record,indent=2)+'\n').encode();backups={p:p.read_bytes() if p.exists() else None for p in writes}
  try:
   for p,d in writes.items():tmp=p.with_suffix(p.suffix+'.pending');tmp.write_bytes(d);tmp.replace(p)
  except Exception:
   for p,d in backups.items():
    if d is None:p.unlink(missing_ok=True)
    else:p.write_bytes(d)
   raise
 print(json.dumps(dict(status=record['status'],stage=str(out),definitions=len(m['definitions']),occurrences=len(m['occurrences']),**changed),indent=2))
if __name__=='__main__':main()
