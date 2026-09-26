#!/usr/bin/env python3
"""Isolated installed mirror, artifact/frame faults and rollback controls."""
from pathlib import Path
import hashlib,json,importlib.util
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 installer=load(ROOT/'scripts/install-distributor-center-contact.py','rotor_promotion_installer');record=installer.preflight();stage=installer.STAGE
 mirror=ROOT/'cad/engine/generated/distributor-center-contact-promotion-mirror';mirror.mkdir(exist_ok=True)
 def put(rel,data):
  p=mirror/rel;p.parent.mkdir(parents=True,exist_ok=True)
  if p.is_symlink():p.unlink()
  p.write_bytes(data);return p
 for rel in set(record['source_sha256'])|set(record['neighbor_sha256']):
  p=mirror/rel;p.parent.mkdir(parents=True,exist_ok=True)
  if p.exists() or p.is_symlink():p.unlink()
  p.symlink_to(ROOT/rel)
 for rel,p in installer.artifacts().items():put(rel,p.read_bytes())
 put('inventory/engine/full-assembly.json',(stage/'full-assembly.json').read_bytes());put('inventory/engine/distributor-center-contact-installation.json',(stage/'installation.json').read_bytes())
 # Include every distributor STEP needed by the actual installed checker.
 for d in record['installed_scope']['definitions'].values():
  rel=d['step'].lstrip('/');p=mirror/rel
  if not p.exists():p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(ROOT/rel)
 checker=load(installer.CHECKER,'rotor_promotion_checker');checker.ROOT=mirror
 result=checker.validate(True,stage)
 target=mirror/'models/engine/distributor-rotor-center-leaf.glb';old=target.read_bytes();artifact_rejected=False
 try:
  target.write_bytes(old+b'corruption-control')
  try:checker.validate(True,stage)
  except AssertionError:artifact_rejected=True
 finally:target.write_bytes(old)
 assert artifact_rejected
 mp=mirror/'inventory/engine/full-assembly.json';raw=mp.read_bytes();frame_rejected=False
 try:
  m=json.loads(raw);next(o for o in m['occurrences'] if o['id']=='distributor-rotor-center-leaf')['position_cad_mm'][0]+=.25;mp.write_text(json.dumps(m))
  try:checker.validate(True,stage)
  except AssertionError as e:frame_rejected='scope' in str(e)
 finally:mp.write_bytes(raw)
 assert frame_rejected
 scene_rejected=False
 try:
  m=json.loads(raw);next(o for o in m['occurrences'] if o['parent'] not in ('distributor-assembly','distributor-rotation'))['position_cad_mm'][0]+=1;mp.write_text(json.dumps(m))
  try:checker.validate(True,stage)
  except AssertionError as e:scene_rejected='scene frames' in str(e)
 finally:mp.write_bytes(raw)
 assert scene_rejected
 helper=load(installer.HELPER,'rotor_transaction');folder=mirror/'transaction-controls';folder.mkdir(exist_ok=True);rollback=[]
 for fail in (1,3,9,'postcheck'):
  paths=[folder/f'file{i}.bin' for i in range(9)]
  for i,p in enumerate(paths):
   p.unlink(missing_ok=True)
   if i%2==0:p.write_bytes(b'baseline')
  baseline={p:p.read_bytes() if p.exists() else None for p in paths}
  def post():
   if fail=='postcheck':raise RuntimeError('Injected postcheck failure')
  try:helper.promote({p:b'candidate' for p in paths},post,fail_after=fail if isinstance(fail,int) else None)
  except RuntimeError:pass
  else:raise AssertionError('Injected failure not raised')
  assert all((p.read_bytes() if p.exists() else None)==v for p,v in baseline.items())
  assert not list(folder.glob('*.pending'));rollback.append(str(fail))
 assert sha(stage/'installation.json')==result['installation_record_sha256']
 report=dict(status='PASS isolated installed mirror and promotion controls',stage_validation_sha256=sha(stage/'validation.json'),stage_installation_sha256=sha(stage/'installation.json'),source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'scripts/install-distributor-center-contact.py',installer.CHECKER,installer.HELPER]},installed_mirror_status=result['status'],corrupt_glb_rejected=artifact_rejected,shifted_leaf_frame_rejected=frame_rejected,changed_external_scene_frame_rejected=scene_rejected,rollback_failures_restored=rollback,canonical_writes=False)
 (ROOT/'inventory/engine/distributor-center-contact-promotion-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
