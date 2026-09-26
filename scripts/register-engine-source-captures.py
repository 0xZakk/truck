"""Bind existing source citations to saved captures; no geometry changes."""
from pathlib import Path
import argparse
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'inventory/engine/full-assembly.json'
    raw = target.read_bytes()
    original = json.loads(raw)
    updated = copy.deepcopy(original)
    overrides = json.loads((ROOT / 'inventory/engine/source-capture-overrides.json').read_text())
    for identifier, fields in overrides.items():
        assert identifier in updated['sources'], identifier
        capture = ROOT / fields['path'].lstrip('/')
        assert digest(capture.read_bytes()) == fields['sha256'], capture
        updated['sources'][identifier].update(fields)
    assert {k: v for k, v in updated.items() if k != 'sources'} == {
        k: v for k, v in original.items() if k != 'sources'
    }
    encoded = (json.dumps(updated, indent=2) + '\n').encode()
    report = {
        'status': 'APPLIED' if args.apply else 'DRY RUN',
        'before_manifest_sha256': digest(raw),
        'after_manifest_sha256': digest(encoded),
        'updated_sources': list(overrides),
        'geometry_placements_learning_unchanged': True,
        'scope': 'Capture registration only; does not strengthen source applicability or certify geometry.',
    }
    if args.apply:
        assert target.read_bytes() == raw, 'Manifest changed during registration'
        pending = target.with_suffix('.pending.json')
        pending.write_bytes(encoded)
        pending.replace(target)
        (ROOT / 'inventory/engine/source-capture-registration.json').write_text(
            json.dumps(report, indent=2) + '\n'
        )
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
