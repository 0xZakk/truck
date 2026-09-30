"""Transfer the stop proof only across array-order-only manifest changes."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
stage = ROOT/'cad/engine/generated/throttle-stop-integration-stage'
manifest = ROOT/'inventory/engine/full-assembly.json'
original = json.loads((stage/'full-assembly.json').read_text())
current = json.loads(manifest.read_text())
order = {}
for key in ('definitions', 'occurrences', 'assemblies'):
    order[key] = [r['id'] for r in original[key]] != [r['id'] for r in current[key]]
    for data in (original, current):
        indexed = {r['id']: r for r in data[key]}
        assert len(indexed) == len(data[key]), 'Duplicate IDs'
        data[key] = indexed
assert original == current, 'Changed geometry/metadata requires scoped revalidation'
report_path = ROOT/'inventory/engine/throttle-stop-installed-validation.json'
report = json.loads(report_path.read_text())
record = json.loads((stage/'installation.json').read_text())
assert report['status'] == 'PASS installed throttle stops; browser pending'
assert report['installation_sha256'] == sha(stage/'installation.json')
assert report['manifest_sha256'] == sha(stage/'full-assembly.json')
for path, digest in {**record['input_sha256'], **report['context']['artifact_sha256']}.items():
    assert sha(ROOT/path) == digest, path
for path, digest in record['staged_artifact_sha256'].items():
    folder = {'step': 'cad/engine/generated', 'models': 'models/engine'}[Path(path).parts[0]]
    assert sha(ROOT/folder/Path(path).name) == digest, path
result = dict(
    status='PASS unchanged geometry and metadata; definition/occurrence array order only',
    checker_sha256=sha(Path(__file__)), current_manifest_sha256=sha(manifest),
    original_report_sha256=sha(report_path), stage_manifest_sha256=sha(stage/'full-assembly.json'),
    changed_array_order=order, source_dependencies_verified=record['input_sha256'],
    context_artifact_count=len(report['context']['artifact_sha256']),
    scope='All manifest fields identical after indexing unique IDs; installed stop exports and every recorded context artifact/source dependency retain original hashes. Prior installed scope transfers without repeating unchanged CAD sweeps. Browser remains NOT RUN.',
)
(ROOT/'inventory/engine/throttle-stop-checkpoint-binding.json').write_text(json.dumps(result, indent=2)+'\n')
print(result['status'])
