"""Bind the v2 delta to the frozen v1 failures without promoting either stage."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
load = lambda p: json.loads((ROOT / p).read_text())
a = 'inventory/engine/corrected-stage-changed-neighbors.json'
b = 'inventory/engine/corrected-stage-v2-sealing-neighbors.json'
old, result = load(a), load(b)
assert result['status'].startswith(('PASS', 'FAIL', 'INCONCLUSIVE'))
assert len(result['exact_checks']) == result['broadphase_candidates']
for report in (old, result):
    for path, digest in report['input_sha256'].items():
        assert sha(path) == digest, path
before = {o['id']: o for o in load('inventory/engine/corrected-engine-stage.json')['occurrences']}
for occurrence in load('inventory/engine/corrected-engine-stage-v2.json')['occurrences']:
    if occurrence.get('valvetrain'):
        assert occurrence['valvetrain'] == before[occurrence['id']]['valvetrain']
changed = set(result['changed_occurrences']) | set(result['removed_occurrences'])
retained = [{'a': row['a'], 'b': row['b'], 'overlap_mm3': row['adaptive_overlap_mm3']}
            for row in old['conflicts'] if not {row['a'], row['b']} & changed]
report = {
    'status': 'FAIL v2 composed static stage',
    'fresh_pairs': len(result['exact_checks']),
    'fresh_conflicts': len(result['conflicts']),
    'metric_errors': len(result['metric_errors']),
    'retained_v1_conflicts': retained,
    'combined_known_conflict_pairs': len(retained) + len(result['conflicts']),
    'resolved_scope': 'Old front seal deleted; all affected case/elastomer/spring/hub broadphase neighbor pairs clear at q0. Dynamic proof not implied.',
    'new_failure_scope': 'Main-cover gasket against water-pump gasket and six compressor parts.',
    'bindings': {p: sha(p) for p in (a, b, 'scripts/check-corrected-stage-v2-sealing-neighbors.py',
                                    'scripts/summarize-corrected-stage-v2-sealing.py')},
    'canonicalModified': False,
}
# These statements describe this frozen delivery, not a general future verdict.
assert len(result['conflicts']) == 7 and len(retained) == 75
assert not result['metric_errors']
assert all(row['b'] == 'timing-cover-main-gasket' or row['a'] == 'timing-cover-main-gasket'
           for row in result['conflicts'])
(ROOT / 'inventory/engine/corrected-stage-v2-sealing-summary.json').write_text(json.dumps(report, indent=2) + '\n')
print({k: report[k] for k in ('status', 'fresh_pairs', 'fresh_conflicts', 'combined_known_conflict_pairs')})
