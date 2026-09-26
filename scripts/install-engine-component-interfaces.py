"""Export bounded provisional interface upgrades without rebuilding other parts.

Uses the shared engine exporter. Does not claim production acceptance or update
the old combined STEP; that derivative must be regenerated separately if needed.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if not args.apply:
        print('Dry run: replace one seal envelope with six teaching parts; add bracket and estimated mounting studs. No writes.')
        return
    import full_engine as engine
    import component_interface_integration as integration
    path = ROOT / 'inventory/engine/full-assembly.json'
    raw = path.read_bytes()
    manifest = json.loads(raw)
    original = copy.deepcopy(manifest)
    engine.defs[:] = manifest['definitions']
    engine.occurrences[:] = manifest['occurrences']
    engine.assemblies[:] = manifest['assemblies']
    integration.install(engine.define, engine.add, engine.group,
                        engine.defs, engine.occurrences, engine.assemblies)
    manifest.update(definitions=engine.defs, occurrences=engine.occurrences, assemblies=engine.assemblies)
    for definition in engine.defs:
        if definition['id'] in integration.NEW_IDS:
            shape = engine.shapes[definition['id']]
            size = (engine.support_bounds(shape) if definition['id'] == 'water-pump-seal-spring' else shape.bounding_box()).size
            definition['model_bounds_mm'] = [size.X, size.Y, size.Z]
    for collection in ('definitions', 'occurrences', 'assemblies'):
        ids = [item['id'] for item in manifest[collection]]
        assert len(ids) == len(set(ids)), f'Duplicate {collection}'
    # Check that a narrowly scoped installation did not mutate unrelated rows.
    mutable = integration.NEW_IDS | {'water-pump-seal', 'water-pump-mechanical-seal-assembly',
        'throttle-stud-3', 'throttle-stud-4', 'throttle-nut-3', 'throttle-nut-4'}
    for collection in ('definitions', 'occurrences', 'assemblies'):
        before = {v['id']: v for v in original[collection] if v['id'] not in mutable}
        after = {v['id']: v for v in manifest[collection] if v['id'] not in mutable}
        assert before == after, f'Unexpected change in {collection}'
    manifest['sources'].update(integration.sources())
    manifest['coverage'].update(modeled_definitions=len(engine.defs), modeled_occurrences=len(engine.occurrences))
    assert path.read_bytes() == raw, 'Manifest changed during export; refusing overwrite'
    output = (json.dumps(manifest, indent=2) + '\n').encode()
    temporary = path.with_suffix('.json.pending')
    temporary.write_bytes(output)
    temporary.replace(path)
    report = {'before_manifest_sha256': hashlib.sha256(raw).hexdigest(),
              'after_manifest_sha256': hashlib.sha256(output).hexdigest(),
              'definitions': len(engine.defs), 'occurrences': len(engine.occurrences),
              'new_definitions': sorted(integration.NEW_IDS),
              'unrelated_inventory_unchanged': True,
              'readiness': 'Provisional educational integration; acceptance checks pending',
              'combined_step': 'NOT REGENERATED; old full-assembly.step is a historical derivative'}
    (ROOT / 'inventory/engine/component-interface-installation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
