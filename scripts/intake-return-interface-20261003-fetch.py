#!/usr/bin/env python3
"""Re-fetch excluded public comparison originals to an external review folder."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('destination', type=Path)
a = p.parse_args()
destination = a.destination.resolve()
if destination == ROOT or ROOT in destination.parents:
    p.error('Original photographs must remain outside the repository.')
destination.mkdir(parents=True, exist_ok=True)
ledger = json.loads((ROOT / 'reference/engine/intake-return-interface-20261003-evidence.json').read_text())
for entry in ledger['public_photos']:
    data = urlopen(entry['url'], timeout=30).read()
    actual = hashlib.sha256(data).hexdigest()
    if actual != entry['sha256']:
        raise RuntimeError(f"Source bytes changed: {entry['id']}: {actual}")
    target = destination / (entry['id'] + '.webp')
    target.write_bytes(data)
    print(target)
