#!/usr/bin/env python3
"""Bind only local proofs carried through independently verified geometry identity."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['cam-composed-drive-build-review','cam-composed-drive-section-review','cam-composed-drive-pair-review','cam-composed-drive-render-review','cam-clockwise-candidate-delivery-validation','crossed-oil-drive-corrected-pair-review','crossed-oil-drive-endplay-review']
reports={};checked={}
for name in names:
 p=R/'inventory/engine'/(name+'.json');r=json.loads(p.read_text());reports[str(p.relative_to(R))]=sha(p)
 for key in ['input_sha256','output_sha256','sha256','reports','artifacts','transitive_source_sha256']:
  for path,h in r.get(key,{}).items():
   assert sha(R/path)==h,(name,path);checked[path]=h
base=json.loads((R/'inventory/engine/cam-composed-drive-build-review.json').read_text());assert base['outside_exact_mask_difference_mm3']==0 and base['actual_gear_window_difference_mm3']==0
sections=json.loads((R/'inventory/engine/cam-composed-drive-section-review.json').read_text());assert len(sections['lobes'])==12
# Previous120-contact checker clipped each lobe to station±7.500005.
assert all(abs(x['x_mm']-227.584)>6+7.500005 for x in sections['lobes'])
r={'status':'PASS scoped composed-cam proof binding; not installed','reports_sha256':reports,'verified_dependencies':checked,'reused_claims':[
 '120 earlier localized lobe/lifter witnesses and their phase/normal controls: every clipped lobe lies outside the changed mask; exact protected material and independent lobe sections unchanged',
 'Earlier linkage solver/frame consistency: source API and profile hashes unchanged; no new whole-assembly clearance inference',
 '17 corrected drive-pair poses plus nine endplay poses and their controls: actual composed gear-window equals frozen corrected gear, and pose APIs remain unchanged',
 'Actual fullcam/distributor two new interstitial snapshots supplement local gear-window reuse'],
 'not_rebound':['Any whole-engine collision clearance','Continuous actual tooth contact, force/backlash production values','Browser/explode/disassembly acceptance','Factory cam or gear calibration'],
 'checker_sha256':sha(Path(__file__))}
(R/'inventory/engine/cam-composed-drive-proof-binding.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
