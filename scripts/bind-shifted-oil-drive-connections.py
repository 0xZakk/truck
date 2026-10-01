#!/usr/bin/env python3
"""Bind limited reconnection delivery, retaining native mesh and fluid-system gaps."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
reports=['shifted-oil-drive-connection-audit','shifted-oil-drive-inlet-probes','shifted-oil-drive-mount-validation','shifted-oil-pickup-candidate-validation','shifted-oil-pickup-contact-validation','shifted-oil-pickup-native-sweep-diagnostic','shifted-oil-pickup-parametric-mesh-validation','shifted-oil-pickup-render-validation','shifted-oil-pickup-parametric-render-validation']
inputs={};data={}
for n in reports:
 p=f'inventory/engine/{n}.json';d=json.loads((R/p).read_text());data[n]=d
 for f,h in d.get('inputs',{}).items():assert sha(f)==h,(p,f);inputs[f]=h
 for f,h in d.get('artifacts',{}).items():assert sha(f)==h,(p,f);inputs[f]=h
 if 'artifact' in d:assert sha(d['artifact'])==d['sha256'];inputs[d['artifact']]=d['sha256']
 if 'render' in d:assert sha(d['render'])==d['sha256'];inputs[d['render']]=d['sha256']
 inputs[p]=sha(p)
d=data['shifted-oil-pickup-candidate-validation'];assert d['valid'] and d['solid_count']==1 and d['outside_mask_difference_mm3']<1e-5 and d['roundtrip_volume_error_mm3']<1e-5
assert all(x['overlap_mm3']<.1 for x in d['neighbors'])
assert not d['mesh']['watertight'] # Failure remains recorded, not silently overwritten.
assert data['shifted-oil-pickup-parametric-mesh-validation']['mesh']['watertight']
for p in ['scripts/bind-shifted-oil-drive-connections.py','docs/components/shifted-oil-drive-connections.md','reference/engine/shifted-oil-drive-connection-sources.json','inventory/engine/shifted-oil-pickup-initial-bend-diagnostic.json']:inputs[p]=sha(p)
r={'status':'PASS bounded uninstalled pickup reconnection delivery; oil-system acceptance remains incomplete','inputs':inputs,'selected_definition':'oil-pickup-tube','selected_local_step':'cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube.step','selected_local_glb':'cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube-parametric.glb','visual_review':'Worker inspected actual parametric mesh and inserted actual STEP section; source schematic qualitative only','preserved_failures':['Initial immediate-bend housing overlap0.154512896mm3','Native spliced and full-sweep GLBs not watertight','Canonical pickup native mesh also not watertight'],'open_interfaces':['Pump discharge port and block gallery','Source-supported mounting gasket and sealing face','Inherited bell clearance and retention','Production geometry and complete oil-system/browser acceptance']}
p=R/'inventory/engine/shifted-oil-drive-connection-delivery.json';p.write_text(json.dumps(r,indent=2)+'\n');print(str(p.relative_to(R)),sha(str(p.relative_to(R))))
