#!/usr/bin/env python3
"""Exercise rear promotion guards on a disposable stage, never canonical writes."""
from pathlib import Path
import copy,importlib.util,json,shutil,tempfile
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'scripts/install-exhaust-rear-collector.py';spec=importlib.util.spec_from_file_location('rear_install_controls',p);installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
if __name__=='__main__':
 stage=installer.STAGE;record=installer.read(stage/'installation.json');good=installer.read(stage/'validation.json');assert good['status']=='PASS staged rear collector';assert good['installation_sha256']==installer.sha(stage/'installation.json')
 canonical=installer.sha(ROOT/'inventory/engine/full-assembly.json');trials=[]
 with tempfile.TemporaryDirectory(prefix='guard-controls-',dir=stage.parent) as tmp:
  installer.STAGE=Path(tmp)/'stage';shutil.copytree(stage,installer.STAGE)
  mutations=[('candidate_proof',lambda r:r.update(candidate_proof_sha256='0'*64),'Changed candidate proof'),('source_dependency',lambda r:r['input_sha256'].update({'cad/engine/full_engine.py':'0'*64}),'Changed stage dependency'),('staged_mesh',lambda r:r['staged_artifact_sha256'].update({'models/exhaust-rear.glb':'0'*64}),'Changed staged export'),('neighbor',lambda r:r['context']['artifact_sha256'].update({next(iter(r['context']['artifact_sha256'])):'0'*64}),'Changed neighbor')]
  for name,mutate,expected in mutations:
   bad=copy.deepcopy(record);mutate(bad)
   try:installer.guard(bad)
   except AssertionError as e:assert expected in str(e);trials.append(name)
   else:raise AssertionError('Failed to reject '+name)
  # Simulate byte mutations in a disposable mirror of canonical rear paths.
  # The production guard uses this same helper with ROOT, never this mirror.
  mirror=Path(tmp)/'canonical-mirror'
  for rel,digest in record['before_artifact_sha256'].items():
   dest=mirror/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((ROOT/rel).read_bytes())
  installer.check_artifacts(record['before_artifact_sha256'],mirror)
  for rel in record['before_artifact_sha256']:
   dest=mirror/rel;raw=dest.read_bytes();dest.write_bytes(raw+b'changed')
   try:installer.check_artifacts(record['before_artifact_sha256'],mirror)
   except AssertionError as e:assert 'Canonical rear artifact changed' in str(e);trials.append('canonical_'+dest.suffix[1:]+'_mutation')
   else:raise AssertionError('Canonical artifact mutation accepted')
   dest.write_bytes(raw)
  original=installer.read(installer.STAGE/'full-assembly.json');bad_manifest=copy.deepcopy(original)
  next(d for d in bad_manifest['definitions'] if d['id']=='exhaust-rear').pop('model_bounds_mm')
  installer.dump(installer.STAGE/'full-assembly.json',bad_manifest);bad=copy.deepcopy(record);bad['staged_manifest_sha256']=installer.sha(installer.STAGE/'full-assembly.json')
  try:installer.guard(bad)
  except AssertionError as e:assert 'Rear definition metadata dropped' in str(e);trials.append('dropped_model_bounds_metadata')
  else:raise AssertionError('Dropped bounds metadata accepted')
  installer.dump(installer.STAGE/'full-assembly.json',original)
  bad_manifest=copy.deepcopy(original);next(d for d in bad_manifest['definitions'] if d['id']=='exhaust-rear')['unresolved'].append('This incremental entry correction retains the old collector and EGR end connection. Both remain unsupported form/routing studies pending joint reconstruction; this is not a completed rear manifold.')
  installer.dump(installer.STAGE/'full-assembly.json',bad_manifest);bad=copy.deepcopy(record);bad['staged_manifest_sha256']=installer.sha(installer.STAGE/'full-assembly.json')
  try:installer.guard(bad)
  except AssertionError as e:assert 'Obsolete collector limitation retained' in str(e);trials.append('obsolete_collector_gap_rejected')
  else:raise AssertionError('Obsolete collector gap accepted')
  installer.dump(installer.STAGE/'full-assembly.json',original)
  m=installer.read(installer.STAGE/'full-assembly.json');next(o for o in m['occurrences'] if o['id']=='exhaust-rear')['position_cad_mm'][0]+=.5;installer.dump(installer.STAGE/'full-assembly.json',m)
  bad=copy.deepcopy(record);bad['staged_manifest_sha256']=installer.sha(installer.STAGE/'full-assembly.json')
  try:installer.guard(bad)
  except ValueError as e:assert 'Unreviewed rear local frame' in str(e);trials.append('shifted_frame_even_with_updated_manifest_hash')
  else:raise AssertionError('Frame mutation accepted')
  bad=copy.deepcopy(record);bad['isolated_export_test_only']=True;installer.dump(installer.STAGE/'installation.json',bad)
  try:installer.apply()
  except AssertionError as e:assert 'Isolated exporter shim cannot be promoted' in str(e);trials.append('isolated_export_promotion_blocked')
  else:raise AssertionError('Isolated exporter promoted')
 assert installer.sha(ROOT/'inventory/engine/full-assembly.json')==canonical
 report=dict(status='PASS',script_sha256=installer.sha(Path(__file__)),installer_sha256=installer.sha(p),stage_record_sha256=installer.sha(stage/'installation.json'),validation_sha256=installer.sha(stage/'validation.json'),canonical_manifest_sha256=canonical,controls=trials,canonical_unchanged=True)
 installer.dump(stage/'promotion-controls.json',report);print(json.dumps(report,indent=2))
