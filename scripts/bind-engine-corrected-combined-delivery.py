#!/usr/bin/env python3
"""Bind diagnostic delivery integrity without converting its mechanical FAIL to PASS."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
names=['engine-corrected-combined-motion','engine-corrected-combined-snapshot','engine-corrected-rod-bolt-conflict','engine-corrected-combined-render']
reports={f'inventory/engine/{n}-validation.json':json.loads((ROOT/f'inventory/engine/{n}-validation.json').read_text()) for n in names}
checks={}
for path,d in reports.items():
 for p,h in d['inputs'].items():
  assert sha(p)==h,(path,p,'changed input')
  checks[p]=h
 checks[path]=sha(path)
folder='cad/engine/generated/engine-corrected-combined-candidate/'
snap=reports['inventory/engine/engine-corrected-combined-snapshot-validation.json']
render=reports['inventory/engine/engine-corrected-combined-render-validation.json']
for p,h in [(folder+'combined-q55-named.step',snap['snapshot_sha256']),(render['render'],render['render_sha256']),(snap['initial_shared_topology_export']['path'],snap['initial_shared_topology_export']['sha256'])]:
 assert sha(p)==h,p
 checks[p]=h
assert reports['inventory/engine/engine-corrected-combined-motion-validation.json']['status'].startswith('FAIL')
for p in ['docs/components/engine-corrected-combined-motion.md','scripts/bind-engine-corrected-combined-delivery.py','inventory/engine/engine-corrected-combined-initial-support-diagnostic.json']:
 checks[p]=sha(p)
out={'status':'PASS delivery integrity; mechanical FAIL preserved; uninstalled diagnostic only','inputs':checks,'visual_review':'Worker inspected actual mesh overview and strict-witness bolt/block section 2026-10-01','mechanical_status':reports['inventory/engine/engine-corrected-combined-motion-validation.json']['status'],'scope':'328-occurrence selected snapshot; continuous conservative supports and finite actual samples only; missing coverage retained in source reports'}
p=ROOT/'inventory/engine/engine-corrected-combined-delivery-validation.json';p.write_text(json.dumps(out,indent=2)+'\n');print(p.relative_to(ROOT),sha(str(p.relative_to(ROOT))))
