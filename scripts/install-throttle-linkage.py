"""Stage a bounded educational linkage upgrade; dry run unless --apply is set."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'cad/engine'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--spring', action='store_true', help='Install illustrative return spring after checked shield')
    parser.add_argument('--shield', action='store_true', help='Install shield after the checked linkage upgrade')
    args = parser.parse_args()
    assert not (args.spring and args.shield), 'Choose one installation stage'
    if not args.apply:
        print('Dry run: add lever, ball stud and pin; replace shaft end and bracket. No writes.')
        return
    import full_engine as engine
    if args.spring:
        import throttle_return_spring_integration as integration
    elif args.shield:
        import throttle_shield_integration as integration
    else:
        import throttle_linkage_integration as integration
    stem = 'throttle-return-spring' if args.spring else 'throttle-shield' if args.shield else 'throttle-linkage'
    report_path = ROOT/f'inventory/engine/{stem}-candidate-validation.json'
    report = json.loads(report_path.read_text())
    assert report['status'] == 'PASS', 'Candidate checks have not passed'
    predecessor = None
    if args.shield or args.spring:
        predecessor_name = 'throttle-shield' if args.spring else 'throttle-linkage'
        predecessor = json.loads((ROOT/f'inventory/engine/{predecessor_name}-installed-validation.json').read_text())
        assert predecessor['status'] == 'PASS'
        assert predecessor['manifest_sha256'] == digest(ROOT/'inventory/engine/full-assembly.json')
    def validate_inputs():
        for name, expected in report['input_hashes'].items():
            if args.shield and name == 'inventory/engine/full-assembly.json':
                expected = predecessor['manifest_sha256']
            elif args.shield and name in ('cad/engine/generated/throttle-shaft.step',
                                         'cad/engine/generated/accelerator-cable-bracket.step'):
                expected = predecessor['artifact_hashes'][name]
            assert digest(ROOT/name) == expected, f'Stale candidate input: {name}'
    validate_inputs()
    path = ROOT/'inventory/engine/full-assembly.json'
    raw = path.read_bytes()
    manifest = json.loads(raw)
    before = copy.deepcopy(manifest)
    engine.defs[:] = manifest['definitions']
    engine.occurrences[:] = manifest['occurrences']
    engine.assemblies[:] = manifest['assemblies']
    with tempfile.TemporaryDirectory(prefix='truck-linkage-') as temporary:
        engine.STEP = Path(temporary)/'step'
        engine.OUT = Path(temporary)/'models'
        engine.STEP.mkdir()
        engine.OUT.mkdir()
        integration.install(engine.define, engine.add, engine.defs,
                            engine.occurrences, engine.shapes)
        for definition in engine.defs:
            if definition['id'] in integration.CHANGED_IDS:
                size = engine.shapes[definition['id']].bounding_box().size
                definition['model_bounds_mm'] = [size.X, size.Y, size.Z]
        manifest.update(definitions=engine.defs, occurrences=engine.occurrences)
        for collection in ('definitions', 'occurrences', 'assemblies'):
            ids = [row['id'] for row in manifest[collection]]
            assert len(ids) == len(set(ids)), f'Duplicate {collection}'
            unchanged = lambda rows: {r['id']: r for r in rows
                                      if r['id'] not in integration.CHANGED_IDS}
            assert unchanged(before[collection]) == unchanged(manifest[collection]), collection
        manifest['sources'].update(integration.sources())
        manifest['coverage'].update(modeled_definitions=len(engine.defs),
                                    modeled_occurrences=len(engine.occurrences))
        assert path.read_bytes() == raw, 'Manifest changed during staging'
        validate_inputs()
        writes = {}
        for ident in integration.CHANGED_IDS:
            writes[ROOT/f'cad/engine/generated/{ident}.step'] = (engine.STEP/f'{ident}.step').read_bytes()
            writes[ROOT/f'models/engine/{ident}.glb'] = (engine.OUT/f'{ident}.glb').read_bytes()
        writes[path] = (json.dumps(manifest, indent=2)+'\n').encode()
        backup = {p: p.read_bytes() if p.exists() else None for p in writes}
        try:
            for destination, content in writes.items():
                pending = destination.with_suffix(destination.suffix+'.pending')
                pending.write_bytes(content)
                pending.replace(destination)
        except Exception:
            for destination, content in backup.items():
                if content is None:
                    destination.unlink(missing_ok=True)
                else:
                    destination.write_bytes(content)
            raise
    result = {'before_manifest_sha256': hashlib.sha256(raw).hexdigest(),
              'after_manifest_sha256': digest(path),
              'candidate_report_sha256': digest(report_path),
              'predecessor_installed_report': predecessor,
              'changed_definitions': sorted(integration.CHANGED_IDS),
              'definitions': len(engine.defs), 'occurrences': len(engine.occurrences),
              'unrelated_inventory_unchanged': True,
              'assembly_frames_sha256': hashlib.sha256(json.dumps(before['assemblies'], sort_keys=True).encode()).hexdigest(),
              'baseline_existing_occurrences': [o for o in before['occurrences']
                  if o['id'] in ('throttle-shaft', 'accelerator-cable-bracket', 'throttle-lever-estimated')],
              'scope': 'Provisional educational linkage; installed checks pending; combined STEP needs regeneration'}
    (ROOT/f'inventory/engine/{stem}-installation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
