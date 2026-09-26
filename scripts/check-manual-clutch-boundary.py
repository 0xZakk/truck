import hashlib
import itertools
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import build123d as cad
import flywheel
import manual_clutch_boundary as clutch
import manual_clutch_load_path as load_path

source = ROOT / 'cad/engine/manual_clutch_boundary.py'
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
report = {'accepted_for_installation': False, 'installed_variant_verified': False, 'source_sha256': source_hash, 'scope': 'Isolated local flywheel body and crank fasteners; no frozen-manifest neighbor audit.', 'variants': {}}
with tempfile.TemporaryDirectory(prefix='clutch-boundary-') as directory:
    for variant in clutch.VARIANTS:
        assert not load_path.acceptance(variant)['ready_for_installed_assembly']
        try:
            clutch.build((None, None, None), variant)
        except ValueError as error:
            assert str(error).startswith('Incomplete clutch load path:')
        else:
            raise AssertionError('Incomplete clutch must not enter installed assembly')
        parts = clutch.components(variant)
        fixture = {'flywheel-body': flywheel.body()}
        for index, (horizontal, vertical) in enumerate(flywheel.HOLES):
            fixture[f'flywheel-bolt-{index}'] = cad.Pos(horizontal, vertical, 0) * flywheel.bolt()
        for identifier, shape in parts.items():
            assert shape.is_valid and len(shape.solids()) == 1, identifier
            path = pathlib.Path(directory) / f'{variant}-{identifier}.step'
            cad.export_step(shape, path)
            restored = cad.import_step(path)
            assert restored.is_valid and len(restored.solids()) == 1
            assert abs(restored.volume - shape.volume) < 1e-3
        collisions = []
        checks = 0
        pairs = list(itertools.combinations(parts.items(), 2)) + list(itertools.product(parts.items(), fixture.items()))
        for (first_id, first), (second_id, second) in pairs:
            checks += 1
            intersection = first.intersect(second)
            volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
            if volume > 1e-5:
                collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})
        report['variants'][variant] = {'part_count': len(parts), 'step_round_trips': len(parts), 'intersection_checks': checks, 'collisions': collisions}
        print(variant, report['variants'][variant], flush=True)
assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
report['passed_isolated_geometry'] = all(not entry['collisions'] for entry in report['variants'].values())
(ROOT / 'inventory/engine/manual-clutch-boundary-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert report['passed_isolated_geometry']
