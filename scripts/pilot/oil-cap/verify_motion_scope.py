"""Capture/check the exact motion inputs when unrelated assembly entries change.

Capture only immediately after a successful motion audit. Verification does not
extend sampled coverage or validate newly added moving hardware.
"""
from pathlib import Path
import hashlib
import json
import sys
from copy import deepcopy
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'inventory/engine/pilot/oil-cap'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def scope(manifest):
    rockers = [o for o in manifest['occurrences'] if o.get('valvetrain', {}).get('role') == 'rocker']
    assemblies = {a['id']: a for a in manifest['assemblies']}
    ancestry = {}
    for o in rockers:
        parent = o['parent']
        while parent in assemblies:
            a = assemblies[parent]
            ancestry[parent] = a
            parent = a.get('parent')
    return {'mechanism': manifest['mechanism'], 'rockers': sorted(rockers, key=lambda o:o['id']),
            'assemblies': [a for a in manifest['assemblies'] if a['id'] in ancestry],
            'definitions': [d for d in manifest['definitions'] if d['id'] in {o['definition'] for o in rockers}],
            'valvetrain_models': sorted({o['valvetrain'].get('model', '') for o in manifest['occurrences'] if o.get('valvetrain')})}

manifest_path = ROOT/'inventory/engine/full-assembly.json'
report_path = OUT/'motion-validation.json'
snapshot_path = OUT/'motion-input-scope.json'
manifest = json.loads(manifest_path.read_text())
report = json.loads(report_path.read_text())
assert report['status'] == 'PASS_SAMPLED_CLEARANCE', 'Successful motion report required'
current = scope(manifest)
# Sensitivity: a changed rocker position must invalidate the scope snapshot.
bad = deepcopy(manifest)
next(o for o in bad['occurrences'] if o.get('valvetrain', {}).get('role') == 'rocker')['position_cad_mm'][0] += 1
assert scope(bad) != current
if '--capture' in sys.argv:
    assert all(sha(ROOT/p) == h for p,h in report['hashes'].items()), 'Audit inputs changed before capture'
    snapshot = {'scope': current, 'report_sha256': sha(report_path),
                'baseline_manifest_sha256': sha(manifest_path)}
    snapshot_path.write_text(json.dumps(snapshot, indent=2)+'\n')
else:
    snapshot = json.loads(snapshot_path.read_text())
    assert snapshot['report_sha256'] == sha(report_path), 'Motion report changed; capture again after rerun'
    assert snapshot['scope'] == current, 'Relevant transforms/motion metadata changed; rerun full audit'
    assert all(sha(ROOT/p) == h for p,h in report['hashes'].items()
               if p != 'inventory/engine/full-assembly.json'), 'Motion geometry/code changed; rerun full audit'
print(json.dumps({'status':'PASS_UNCHANGED_SCOPE','baseline_manifest_sha256':snapshot['baseline_manifest_sha256'],
    'current_manifest_sha256':sha(manifest_path),'report_sha256':sha(report_path),
    'scope_sha256':sha(snapshot_path),'verifier_sha256':sha(Path(__file__)),
    'negative_control':'1mm rocker location change correctly invalidates scope',
    'limit':'Existing cap-vs-rocker samples only; newly added hardware requires separate integration checks.'},indent=2))
