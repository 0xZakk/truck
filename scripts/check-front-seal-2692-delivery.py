#!/usr/bin/env python3
"""Freeze input/report/artifact binding after all seal candidate validation passes."""
from pathlib import Path
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();OUT=ROOT/'cad/engine/generated/front-seal-2692-candidate'
names=['candidate','contact-bands','internal-clearance','render','exploded'];r={'status':'RUNNING','reports':{},'inputs':{},'artifacts':{},'scope':'Uninstalled estimated-internal2692 nominal-fitted candidate. No final expanded-seat pair, browser, production or installation acceptance.'}
for n in names:
 p=ROOT/f'inventory/engine/front-seal-2692-{n}-validation.json';v=json.loads(p.read_text());assert v['status'].startswith('PASS'),(n,v['status']);r['reports'][str(p.relative_to(ROOT))]=sha(p)
 for path,h in v['inputs'].items():assert sha(ROOT/path)==h,(n,path);r['inputs'][path]=h
 if 'render'in v:
  assert sha(ROOT/v['render']['path'])==v['render']['sha256']
 if n=='candidate':
  for key,row in v['exports'].items():assert sha(OUT/(key+'.step'))==row['sha256']
 if n=='render':
  for key,row in v['meshes'].items():assert row['watertight'] and sha(OUT/(key+'.glb'))==row['sha256']
 if n=='exploded':
  for row in v['meshes'].values():assert row['watertight'] and row['winding_consistent'] and row['positive_signed_volume_mm3']>0
for rel in ['docs/components/front-seal-2692-datum-contract.md','inventory/engine/front-seal-2692-spring-construction-diagnostics.json','reference/engine/front-crank-seal-envelope-review.json','cad/engine/front_crank_seal_envelope_candidate.py','cad/engine/cad_metrics.py','cad/requirements-engine-lock.txt',str(Path(__file__).relative_to(ROOT))]:r['inputs'][rel]=sha(ROOT/rel)
for p in OUT.iterdir():
 if p.suffix in ['.step','.glb','.png']:r['artifacts'][str(p.relative_to(ROOT))]=sha(p)
r['status']='PASS bound scoped candidate reports, transitive inputs and delivered artifacts';r['review_limits']=['Root reviewed actual section; exploded GLB view produced for final root review.','Type76 architecture qualitative; seatX420/boss/internalwall/lip/96-turnspring estimates.','Final expanded-seat pair and browser checks remain outside this delivery.','Garter sweep failures preserved; selected winding is ruled48-section approximation.'];(ROOT/'inventory/engine/front-seal-2692-delivery-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
