from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frozen=R/'reference/engine/pump-functional-20261003-delivery.json'
assert sha(frozen)=='5003936ae17bc0aba6b4adcc3e3d360bc10050a420b614b229b47cec3228771f'
old=json.loads(frozen.read_text())
for group in ['authored_files','generated_assets']:
 for path,h in old[group].items():assert sha(R/path)==h,('frozen changed',path)
measure=R/'reference/engine/pump-source-registration-20261003-measurements.json';m=json.loads(measure.read_text());guard={};excluded={}
for p,h in m['inputs'].items():
 assert sha(R/p)==h,p
 (excluded if p.endswith('.jpg')else guard)[p]=h
clash=R/'reference/engine/pump-source-registration-20261003-clash-ownership.json';c=json.loads(clash.read_text())
for p,h in c['inputs'].items():assert sha(R/p)==h,p;guard[p]=h
for p in [frozen,R/'docs/components/timing-pump-rear-flange-contract.md',R/'docs/components/timing-pump-rear-flange-candidate.md',R/'reference/engine/water-pump-mounting-topology-reviewed.json',R/'inventory/engine/full-assembly.json',R/'inventory/engine/corrected-engine-stage-v4.json']:
 guard[str(p.relative_to(R))]=sha(p)
gallery=R/'reference/engine/pump-junction-online-20261002-full-captures.json';guard[str(gallery.relative_to(R))]=sha(gallery)
for entry in json.loads(gallery.read_text())['images']:
 if any('_'+label+'_'in entry['path']for label in ['BOT','TOP','FRO','BAC','LEF','RIT']):
  assert sha(R/entry['path'])==entry['sha256'];excluded[entry['path']]=entry['sha256']
artifacts={}
for directory in ['scripts','docs/components','reference/engine']:
 for p in (R/directory).glob('pump-source-registration-20261003*'):
  if p.is_file()and p.name!='pump-source-registration-20261003-delivery.json':artifacts[str(p.relative_to(R))]=sha(p)
r={'status':'bounded research and coordinated correction proposal; no CAD changes','authored_files':artifacts,'guarded_inputs':guard,'excluded_source_originals':excluded,'source_pixels_redistributed':False,'frozen_functional_delivery_unchanged':True,'no_running_process':True,'new_geometry_or_installer':False,'open_work':'Carter-only side/profile registration and joint pump/cover/carrier interface contract; source dimensions/3D shape remain unresolved','usage_model_effort':'unavailable'}
(R/'reference/engine/pump-source-registration-20261003-delivery.json').write_text(json.dumps(r,indent=2)+'\n')
print('authored',len(artifacts),'guarded',len(guard),'excluded originals',len(excluded),'bytes',sum((R/p).stat().st_size for p in artifacts),flush=True)
