"""Apply the bounded ignition proposal to a new v3; frozen v2 is immutable."""
from pathlib import Path
import copy, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def compose(manifest, patch, manifest_sha):
    if patch['manifest_sha256'] != manifest_sha:
        raise ValueError('Stale ignition proposal baseline')
    result = copy.deepcopy(manifest)
    bindings = {}
    counts = {}
    for group in ('definitions', 'assemblies', 'occurrences'):
        rows = {row['id']: row for row in result[group]}
        seen = set()
        counts[group] = 0
        for update in patch.get(group, []):
            key = update['id']
            if key in seen or key not in rows or rows[key] != update['before']:
                raise ValueError(f'Duplicate, absent or stale {group}: {key}')
            seen.add(key)
            after = copy.deepcopy(update['after'])
            if after is None or after['id'] != key:
                raise ValueError('Ignition proposal must preserve identities')
            for kind, asset in update.get('copy_assets', {}).items():
                if kind not in ('step', 'glb'):
                    raise ValueError('Unknown asset kind')
                path = (ROOT / asset['from']).resolve()
                if not path.is_relative_to(ROOT / 'cad/engine/generated'):
                    raise ValueError('Candidate asset outside generated tree')
                if sha(path) != asset['sha256']:
                    raise ValueError(f'Stale asset: {key}')
                bindings[str(path.relative_to(ROOT))] = asset['sha256']
                after[kind] = '/' + str(path.relative_to(ROOT))
            rows[key].clear()
            rows[key].update(after)
            counts[group] += 1
    if result['assemblies'] != manifest['assemblies']:
        raise ValueError('Ignition correction must not relocate assemblies')
    if result['occurrences'] != manifest['occurrences']:
        raise ValueError('World-frame ignition shapes must not be translated twice')
    result['integration_stage']['patches'].append('shifted-ignition-lead-integration-proposal')
    result['integration_stage']['open'].append('Ignition v3 candidate requires root replay; unrelated v2 gasket/cover/block failures remain')
    return result, bindings, counts


def main():
    baseline = ROOT / 'inventory/engine/corrected-engine-stage-v2.json'
    proposal = ROOT / 'inventory/engine/shifted-ignition-lead-integration-proposal.json'
    m = json.loads(baseline.read_text())
    p = json.loads(proposal.read_text())
    inputs = {str(f.relative_to(ROOT)): sha(f) for f in (baseline, proposal, Path(__file__))}
    result, assets, counts = compose(m, p, sha(baseline))
    inputs.update(assets)
    assert all(sha(ROOT / f) == h for f, h in inputs.items())
    target = ROOT / 'inventory/engine/corrected-engine-stage-v3.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    report = {'status': 'PASS guarded composition only; installation not accepted',
              'stage_sha256': sha(target), 'bindings': inputs, 'applied_rows': counts,
              'definitions': len(result['definitions']), 'occurrences': len(result['occurrences']),
              'canonical_modified': False, 'v2_unchanged': sha(baseline) == inputs[str(baseline.relative_to(ROOT))]}
    (ROOT / 'inventory/engine/corrected-engine-stage-v3-composition.json').write_text(json.dumps(report, indent=2) + '\n')
    print({k: v for k, v in report.items() if k != 'bindings'})


if __name__ == '__main__':
    main()
