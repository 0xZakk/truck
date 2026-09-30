#!/usr/bin/env python3
"""Plan by default; isolated --stage; explicit --apply after independent check."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import evr_mechanism_integration as adapter
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def scoped(m,ids):
 D={r['id']:r for r in m['definitions']};O={r['id']:r for r in m['occurrences']};A={r['id']:r for r in m['assemblies']};anc=set()
 for key in ids:
  p=O[key]['parent']
  while p in A:anc.add(p);p=A[p]['parent']
 return dict(definitions={O[k]['definition']:D[O[k]['definition']] for k in ids},occurrences={k:O[k] for k in ids},assemblies={k:A[k] for k in sorted(anc)})
def evidence():
 p=ROOT/'inventory/engine/evr-mechanism-candidate-validation.json';r=json.loads(p.read_text());assert r['status']=='PASS' and r['inputs_stable']
 for key,h in r['input_sha256'].items():assert sha(ROOT/key)==h,key
 for row in json.loads((ROOT/'reference/engine/evr-detail-mechanism-review.json').read_text())['sources']:assert sha(ROOT/row['path'])==row['sha256']
 for ident,e in r['exports'].items():
  for ext in ['step','glb']:assert sha(ROOT/f'cad/engine/generated/evr-mechanism-candidate/{ident}.{ext}')==e[ext+'_sha256']
 return dict(candidate_report_sha256=sha(p),source_review_sha256=sha(ROOT/'reference/engine/evr-detail-mechanism-review.json'))
def assert_scope(before,after):
 for kind,allowed in [('definitions',adapter.CHANGED_IDS),('occurrences',adapter.CHANGED_IDS),('assemblies',set())]:
  assert {r['id']:r for r in before[kind] if r['id'] not in allowed}=={r['id']:r for r in after[kind] if r['id'] not in allowed},kind
  assert len(after[kind])==len({r['id'] for r in after[kind]})
 O={r['id']:r for r in after['occurrences']}
 for o in before['occurrences']:
  if o['id'] in adapter.NEW_IDS:continue
  for k in ['definition','parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:assert o.get(k)==O[o['id']].get(k),(o['id'],k)
def main():
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group();g.add_argument('--stage',action='store_true');g.add_argument('--apply',action='store_true');p.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/evr-mechanism-integration-stage');args=p.parse_args()
 if not(args.stage or args.apply):print('Plan only: replace4originalEVR definitions, add7illustrativeparts and5discrete spring poses. No writes.');return
 deps=['scripts/install-evr-mechanism.py','scripts/check-evr-mechanism-installed.py','scripts/prepare-evr-motion.py','cad/engine/evr_mechanism_integration.py','cad/engine/full_engine.py','cad/engine/cad_metrics.py','inventory/engine/evr-mechanism-learning.json','viewer/evr-discrete-motion.js']
 initial_inputs={p:sha(ROOT/p) for p in deps}
 import full_engine as engine
 target=ROOT/'inventory/engine/full-assembly.json';raw=target.read_bytes();before=json.loads(raw);m=copy.deepcopy(before);ev=evidence();already=adapter.SOURCE_IDS[0] in m['sources'];near=adapter.neighbor_ids(m)
 if already:
  rec=json.loads((ROOT/'inventory/engine/evr-mechanism-installation.json').read_text());assert rec['candidate_evidence']==ev and near==rec['neighbor_ids'];assert scoped(m,rec['guard_occurrences'])==rec['installed_scope']
  for path,h in rec['canonical_artifact_sha256'].items():assert sha(ROOT/path)==h,path
 out=args.stage_dir.resolve();assert ROOT in out.parents and 'generated' in out.parts;out.mkdir(parents=True,exist_ok=True)
 (out/'baseline').mkdir(exist_ok=True)
 olddefs={d['id']:d for d in before['definitions']};original_hashes={}
 for ident in adapter.REPLACED:
  q=ROOT/olddefs[ident]['step'].lstrip('/');original_hashes[str(q.relative_to(ROOT))]=sha(q);(out/'baseline'/(ident+'.step')).write_bytes(q.read_bytes())
 engine.STEP=out/'step';engine.OUT=out/'models';engine.STEP.mkdir(exist_ok=True);engine.OUT.mkdir(exist_ok=True);engine.defs[:]=m['definitions'];engine.occurrences[:]=m['occurrences'];engine.assemblies[:]=m['assemblies'];engine.shapes.clear()
 changed=adapter.install(engine.define,engine.add,engine.group,engine.defs,engine.occurrences,engine.assemblies,engine.shapes);m.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies);m['sources'].update(adapter.sources());assert_scope(before,m)
 spec=importlib.util.spec_from_file_location('evr_motion',ROOT/'scripts/prepare-evr-motion.py');motion=importlib.util.module_from_spec(spec);spec.loader.exec_module(motion);motion.prepare(out/'motion')
 guard=sorted(adapter.CHANGED_IDS|set(near));path=out/'full-assembly.json';path.write_text(json.dumps(m,indent=2)+'\n');baseline=out/'before.json';baseline.write_text(json.dumps(before,indent=2)+'\n')
 record=dict(status='STAGED illustrative EVR; no installed acceptance',candidate_evidence=ev,**changed,neighbor_ids=near,guard_occurrences=guard,before_manifest_sha256=hashlib.sha256(raw).hexdigest(),staged_manifest_sha256=sha(path),baseline_snapshot_sha256=sha(baseline),input_scope=scoped(before,sorted(adapter.REPLACED|set(near))),installed_scope=scoped(m,guard),input_sha256=initial_inputs,neighbor_artifact_sha256={},canonical_modified=False,original_artifact_sha256=original_hashes)
 D={d['id']:d for d in before['definitions']};O={o['id']:o for o in before['occurrences']}
 for k in near:
  for key in ['step','glb']:
   q=ROOT/D[O[k]['definition']][key].lstrip('/');record['neighbor_artifact_sha256'][str(q.relative_to(ROOT))]=sha(q)
 record['staged_artifact_sha256']={str(q.relative_to(out)):sha(q) for folder in ['step','models','motion','baseline'] for q in (out/folder).iterdir() if q.is_file()}
 (out/'installation.json').write_text(json.dumps(record,indent=2)+'\n');assert target.read_bytes()==raw;assert evidence()==ev
 for q,h in original_hashes.items():assert sha(ROOT/q)==h,q
 for q,h in initial_inputs.items():assert sha(ROOT/q)==h,q
 if args.apply:
  subprocess.run([sys.executable,str(ROOT/'scripts/check-evr-mechanism-installed.py'),'--stage-dir',str(out)],check=True);assert target.read_bytes()==raw;assert evidence()==ev
  for q,h in record['input_sha256'].items():assert sha(ROOT/q)==h,q
  writes={target:path.read_bytes()}
  for ident in adapter.GEOMETRY_IDS:
   for directory,ext,destination in [('step','step','cad/engine/generated'),('models','glb','models/engine')]:writes[ROOT/destination/(ident+'.'+ext)]=(out/directory/(ident+'.'+ext)).read_bytes()
  for q in (out/'motion').iterdir():
   dest=ROOT/('models/engine/evr-motion' if q.suffix in ['.glb','.json'] else 'cad/engine/generated/evr-motion')/q.name;writes[dest]=q.read_bytes()
  record.update(status='INSTALLED illustrativeEVR; browser/factory acceptance pending',canonical_modified=True,stage_validation_sha256=sha(out/'validation.json'),canonical_artifact_sha256={str(q.relative_to(ROOT)):hashlib.sha256(v).hexdigest() for q,v in writes.items() if q!=target})
  writes[ROOT/'inventory/engine/evr-mechanism-installation.json']=(json.dumps(record,indent=2)+'\n').encode();backups={q:q.read_bytes() if q.exists() else None for q in writes}
  try:
   for q,v in writes.items():q.parent.mkdir(parents=True,exist_ok=True);tmp=q.with_suffix(q.suffix+'.pending');tmp.write_bytes(v);tmp.replace(q)
  except Exception:
   for q,v in backups.items():
    if v is None:q.unlink(missing_ok=True)
    else:q.write_bytes(v)
   raise
 print(json.dumps(dict(status=record['status'],stage=str(out),definitions=len(m['definitions']),occurrences=len(m['occurrences']),neighbors=near),indent=2))
if __name__=='__main__':main()
