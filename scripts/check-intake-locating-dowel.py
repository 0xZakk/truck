import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile

import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import intake_locating_dowel as dowel
from assembly_math import transforms
from cad_metrics import solid_volume, step_comparison_shape

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
source_path = ROOT / 'cad/engine/intake_locating_dowel.py'
source_raw = source_path.read_bytes()
manifest = json.loads(raw)
verify_installed = '--installed' in sys.argv
poses = transforms(manifest)
definitions = {entry['id']: entry for entry in manifest['definitions']}
adapters = {'cylinder-head': dowel.head_interface, 'efi-lower-intake': dowel.lower_interface, 'efi-head-intake-gasket': dowel.gasket_interface}
cache = {}
step_hashes = {}
installed = {}
adapted = {}
added = {}
bounds = {}
for occurrence in manifest['occurrences']:
    identifier = occurrence['id']
    definition = occurrence['definition']
    if definition not in cache:
        step_path = ROOT / definitions[definition]['step'].lstrip('/')
        step_hashes[str(step_path)] = hashlib.sha256(step_path.read_bytes()).hexdigest()
        cache[definition] = cad.import_step(step_path)
    original = cache[definition]
    world = original.moved(poses[identifier])
    if definition in adapters:
        changed = adapters[definition](original)
        adapted[identifier] = changed.moved(poses[identifier])
        delta = changed - original
        if not hasattr(delta, 'volume'):
            delta = cad.Compound(children=list(delta))
        if delta.volume > 1e-7:
            added[identifier + '-added-material'] = delta.moved(poses[identifier])
    installed[identifier] = world
    bounds[identifier] = world.bounding_box()


def volume(shape):
    return sum(solid.volume for solid in shape.solids()) if shape else 0


collisions = []
checks = 0
def check(first_id, first, second_id, second):
    global checks
    first_box = bounds.setdefault(first_id, first.bounding_box())
    second_box = bounds.get(second_id)
    if second_box is None:
        second_box = second.bounding_box()
        bounds[second_id] = second_box
    if not all(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) > 1e-6 for axis in 'XYZ'):
        return
    checks += 1
    common = volume(first.intersect(second))
    if common > 1e-5:
        collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': common})


candidates = {**dowel.parts(), **adapted}
installed_matches = []
if verify_installed:
    for identifier, expected in list(candidates.items()):
        actual = installed[identifier]
        normalized = step_comparison_shape(expected)
        common = actual.intersect(normalized)
        common_volume = sum(solid_volume(solid, 'adaptive') for solid in common.solids()) if common else 0
        difference = solid_volume(actual, 'adaptive') + solid_volume(normalized, 'adaptive') - 2 * common_volume
        assert abs(difference) < .01, (identifier, difference)
        installed_matches.append({'part': identifier, 'symmetric_difference_mm3': difference})
        candidates[identifier] = actual
        if identifier in adapted:
            adapted[identifier] = actual
with tempfile.TemporaryDirectory(prefix='intake-dowel-') as directory:
    for identifier, shape in candidates.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(directory) / f'{identifier}.step'
        cad.export_step(shape, path)
        restored = cad.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1
        assert abs(restored.volume - shape.volume) < max(.001, shape.volume * 1e-8)
    for (first_id, first), (second_id, second) in itertools.combinations(candidates.items(), 2):
        check('candidate-' + first_id, first, 'candidate-' + second_id, second)
    new_pin = {identifier: candidates[identifier] for identifier in dowel.parts()}
    for first_id, first in {**new_pin, **added}.items():
        for second_id, second in installed.items():
            if second_id in candidates:
                continue
            check(first_id, first, second_id, second)
    assert adapted['cylinder-head'].is_inside((0, -117.9, 298))
    assert adapted['efi-lower-intake'].is_inside((0, -146.15, 298))
    pin_probe = dowel.along_y(dowel.RADIUS - .01, dowel.PIN_FIRST, dowel.PIN_LAST)
    assert all(volume(shape.intersect(pin_probe)) < 1e-7 for shape in adapted.values())
    for identifier, first, last in [('cylinder-head', -132.99, -118.01), ('efi-lower-intake', -145.89, -135.51)]:
        wall = dowel.along_y(4.6, first, last) - dowel.along_y(4.1, first - 1, last + 1)
        assert abs(volume(adapted[identifier].intersect(wall)) - wall.volume) < .001, identifier
    for identifier, first, last in [('cylinder-head', -117.99, -117.5), ('efi-lower-intake', -146.39, -145.91)]:
        floor = dowel.along_y(3.9, first, last)
        assert abs(volume(adapted[identifier].intersect(floor)) - floor.volume) < .001, identifier
    for cylinder in [284.48, 170.688, 56.896, -56.896, -170.688, -284.48]:
        for offset in (-25, 25):
            passage = dowel.along_y(14.9, -146, -119, cylinder + offset, 277.5)
            assert all(volume(shape.intersect(passage)) < 1e-7 for shape in added.values())
assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
assert source_path.read_bytes() == source_raw
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in step_hashes.items())
report = {'passed': not collisions, 'verified_production_fit': False, 'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'source_sha256': hashlib.sha256(source_raw).hexdigest(), 'step_sha256': step_hashes, 'socket_wall_probes': 2, 'blind_floor_probes': 2, 'nominal_pin_mm': [7.9375, 25.4], 'installed': False, 'new_parts': 1, 'adapted_definitions': list(adapters), 'step_round_trips': len(candidates), 'narrow_phase_checks': checks, 'collisions': collisions, 'head_engagement_mm': 13, 'intake_engagement_mm': 9.9, 'head_bottom_clearance_mm': 2, 'intake_bottom_clearance_mm': .5, 'added_material_blocks_existing_port_probes': False, 'limits': dowel.GAPS}
report['installed'] = verify_installed
report['installed_matches'] = installed_matches
filename = 'intake-locating-dowel-installed-validation.json' if verify_installed else 'intake-locating-dowel-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert report['passed']
