"""Check nominal radial support interfaces and composed compressor geometry."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor_shaft_support as candidate
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
changed = candidate.changed_parts()
checks = 0
collisions = []
dependencies = [Path(candidate.__file__), Path(candidate.accepted.__file__),
                Path(candidate.accepted.accepted.__file__), Path(candidate.accepted.accepted.accepted.__file__)]
dependency_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in dependencies}
artifact_hashes = {}


def overlap(first_id, first, second_id, second, phase=0):
    global checks
    first_box, second_box = first.bounding_box(), second.bounding_box()
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .001 for axis in 'XYZ'):
        return
    checks += 1
    common = first.intersect(second)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    if volume > .01:
        collisions.append({'first': first_id, 'second': second_id, 'phase': phase, 'volume_mm3': volume})


if '--installed' in sys.argv:
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    occurrences = {entry['id']: entry for entry in manifest['occurrences']}
    poses = transforms(manifest)
    for identifier, expected in list(changed.items()):
        occurrence = occurrences[identifier]
        path = ROOT / definitions[occurrence['definition']]['step'].lstrip('/')
        artifact_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        actual = b.import_step(path).moved(poses[identifier])
        common = actual.intersect(expected)
        assert common and abs(sum(solid.volume for solid in common.solids()) - expected.volume) < .02
        assert abs(actual.volume - expected.volume) < .02
        changed[identifier] = actual

roundtrips = []
with tempfile.TemporaryDirectory(prefix='fs10-shaft-support-') as temporary:
    for identifier, shape in changed.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(temporary) / f'{identifier}.step'
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1
        assert abs(restored.volume - shape.volume) < .02
        roundtrips.append(identifier)
        print('STEP', identifier, flush=True)

contacts = []
for phase in range(0, 360, 45):
    shapes = {**candidate.parts(phase), **changed}
    for (first_id, first), (second_id, second) in itertools.combinations(shapes.items(), 2):
        if first_id in changed or second_id in changed:
            overlap(first_id, first, second_id, second, phase)
    for label in ('front', 'rear'):
        bearing = shapes[f'ac-compressor-{label}-shaft-bearing']
        for target_id in ('ac-compressor-swashplate-shaft', f'ac-compressor-{label}-cylinder'):
            distance = bearing.distance_to(shapes[target_id])
            assert distance < 1e-6, (label, target_id, phase, distance)
            contacts.append({'bearing': label, 'target': target_id, 'phase': phase, 'distance_mm': distance})
    print('Phase', phase, flush=True)

for role, probe in candidate.accepted.accepted.accepted.flow_networks().items():
    for identifier, shape in changed.items():
        overlap(f'{role}-network', probe, identifier, shape)

api_shapes = {}
api_occurrences = []
api_groups = []


def define(identifier, shape, *metadata):
    api_shapes[identifier] = shape


def add(identifier, definition, parent, position=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), **metadata):
    api_occurrences.append({'id': identifier, 'definition': definition, 'parent': parent, 'position_cad_mm': position, 'rotation_cad_deg': rotation})


def group(identifier, name, parent='engine', motion=None, position=(0, 0, 0), rotation=(0, 0, 0)):
    api_groups.append({'id': identifier, 'parent': parent, 'position_cad_mm': position, 'rotation_cad_deg': rotation, 'motion': motion})


candidate.build((define, add, group))
assert len(api_occurrences) == len(api_shapes) == 67
api_manifest = {'mechanism': manifest['mechanism'], 'assemblies': [{'id': 'engine', 'parent': None}, {'id': 'accessory-drive', 'parent': 'engine'}] + api_groups, 'occurrences': api_occurrences}
api_checks = 0
for phase, engaged in ((0, True), (90, True), (173, False)):
    poses = transforms(api_manifest, compressor_degrees=phase, compressor_engaged=engaged)
    expected = candidate.parts(phase, engaged)
    for occurrence in api_occurrences:
        identifier = occurrence['id']
        actual = api_shapes[identifier].moved(poses[identifier])
        common = actual.intersect(expected[identifier])
        assert common and abs(sum(solid.volume for solid in common.solids()) - expected[identifier].volume) < .02, (identifier, phase)
        api_checks += 1

if '--internal-only' not in sys.argv:
    poses = transforms(manifest)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    cache = {}
    for occurrence in manifest['occurrences']:
        if occurrence['id'].startswith('ac-compressor-'):
            continue
        definition = occurrence['definition']
        if definition not in cache:
            path = ROOT / definitions[definition]['step'].lstrip('/')
            artifact_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
            cache[definition] = b.import_step(path)
        installed = cache[definition].moved(poses[occurrence['id']])
        for identifier, shape in changed.items():
            overlap(identifier, shape, occurrence['id'], installed)
    assert manifest_path.read_bytes() == raw
assert all(hashlib.sha256(path.read_bytes()).hexdigest() == digest for path, digest in artifact_hashes.items())
assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest for path, digest in dependency_hashes.items())
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'dependency_sha256': dependency_hashes,
          'step_roundtrips': roundtrips, 'exact_checks': checks, 'collisions': collisions,
          'nominal_contacts': contacts, 'api_shape_pose_checks': api_checks,
          'internal_only': '--internal-only' in sys.argv, 'installed_shapes': '--installed' in sys.argv,
          'production_dimensions_verified': False, 'bearing_internals_complete': False}
suffix = '-installed' if '--installed' in sys.argv else '-internal' if '--internal-only' in sys.argv else ''
(ROOT / f'inventory/engine/ac-compressor-shaft-support{suffix}-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
