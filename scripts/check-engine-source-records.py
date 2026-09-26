"""Check saved reference integrity without claiming the references prove CAD accuracy."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
sources = manifest['sources']
errors = []
checked = 0
for identifier, source in sources.items():
    path, digest = source.get('path'), source.get('sha256')
    if not path or not digest:
        errors.append({'source': identifier, 'error': 'Missing local capture path or SHA256'})
        continue
    capture = ROOT / path.lstrip("/")
    if not capture.is_file():
        errors.append({'source': identifier, 'error': 'Missing capture', 'path': path})
        continue
    actual = hashlib.sha256(capture.read_bytes()).hexdigest()
    checked += 1
    if actual != digest:
        errors.append({'source': identifier, 'error': 'Capture hash mismatch', 'expected': digest, 'actual': actual})
for definition in manifest['definitions']:
    for identifier in definition.get('sources', []):
        if identifier not in sources:
            errors.append({'definition': definition['id'], 'source': identifier, 'error': 'Unregistered source'})
assert manifest_path.read_bytes() == manifest_bytes, 'Manifest changed during source audit'
report = {
    'passed': not errors,
    'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
    'source_records': len(sources),
    'captures_checked': checked,
    'errors': errors,
    'scope': 'Local capture integrity and definition-reference registration only; not claim accuracy, applicability or completion.'
}
(ROOT / 'inventory/engine/source-record-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))
