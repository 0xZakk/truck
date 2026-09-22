#!/usr/bin/env python3
"""Restore public manufacturer PDFs recorded by the engine evidence ledger."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen, Request

root = Path(__file__).resolve().parents[1]
data = json.loads((root/'inventory/engine/dimensions.json').read_text())
extra=root/'inventory/engine/comparison-sources.json'
if extra.exists():data['sources'].update(json.loads(extra.read_text()))
for source in data['sources'].values():
    if not source['path'].endswith(('.pdf','.jpg','.png')):
        continue
    target = root/source['path']
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == source['sha256']:
        print(f'Already verified: {target.name}')
        continue
    with urlopen(Request(source['url'], headers={'User-Agent':'TruckResearch/1.0'}), timeout=90) as response:
        content = response.read()
    if hashlib.sha256(content).hexdigest() != source['sha256']:
        raise SystemExit(f'{target.name}: upstream content changed; review before replacing the recorded reference')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    print(f'Restored and verified: {target.name}')
