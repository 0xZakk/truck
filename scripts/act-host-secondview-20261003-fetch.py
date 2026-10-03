#!/usr/bin/env python3
"""Reacquire or verify unredistributed public specimen pixels in a caller directory."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', required=True, type=Path)
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    ledger = json.loads((root / 'reference/engine/act-host-secondview-20261003-evidence.json').read_text())
    args.directory.mkdir(parents=True, exist_ok=True)
    for item in ledger['images']:
        target = args.directory / f"act-host-secondview-20261003-view{item['gallery_view']}.webp"
        if args.download:
            request = urllib.request.Request(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != item['sha256']:
                raise SystemExit(f"Source changed: {item['url']}; inspect before rebinding")
            target.write_bytes(data)
        if not target.is_file():
            raise SystemExit(f'Missing {target}; use --download with network access')
        if hashlib.sha256(target.read_bytes()).hexdigest() != item['sha256']:
            raise SystemExit(f'Hash mismatch: {target}')
        print(f"PASS view{item['gallery_view']} {item['sha256']}")


if __name__ == '__main__':
    main()
