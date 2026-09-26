"""Restore public research captures from a dated acquisition ledger.

Retains original bytes and SHA-256. Existing known hashes must match; changes
are reported without silently replacing prior evidence. No paid content fetched.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('ledger', nargs='?', default='inventory/engine/research-2026-09-23.json')
args = parser.parse_args()
ledger_path = ROOT / args.ledger
ledger = json.loads(ledger_path.read_text())

def capture(source):
    row = dict(source)
    path = (ROOT / row['local_path']).resolve()
    if not path.is_relative_to(ROOT / 'reference'):
        raise ValueError('Capture must stay under reference/')
    try:
        if path.exists():
            raw = path.read_bytes()
            final_url = row.get('retrieved_url', row['url'])
        elif row.get('capture_method') == 'browser-reviewed transcription':
            raise ValueError('Dynamic source: reapply saved browser filters; do not substitute the portal homepage')
        else:
            request = urllib.request.Request(row['url'], headers={'User-Agent': 'TruckReferenceResearch/1.0'})
            with urllib.request.urlopen(request, timeout=45) as response:
                raw = response.read(50_000_001)
                final_url = response.url
            if len(raw) > 50_000_000:
                raise ValueError('Capture exceeds 50 MB limit')
        if row['format'] == 'pdf' and not raw.startswith(b'%PDF-'):
            raise ValueError('Response is not PDF bytes')
        digest = hashlib.sha256(raw).hexdigest()
        if row.get('sha256') and row['sha256'] != digest:
            raise ValueError('Source hash changed; review before replacing')
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(raw)
        row.update(status='captured', sha256=digest, bytes=len(raw), retrieved_url=final_url)
        row.pop('error', None)
    except Exception as error:
        row.update(status='capture-failed', error=str(error))
    print(row['id'], row['status'], flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    ledger['sources'] = list(pool.map(capture, ledger['sources']))
ledger_path.write_text(json.dumps(ledger, indent=2) + '\n')
