"""Validate isolated rear-manifold solids, nominal interfaces and installed neighbors."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor_manifold as candidate
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
parts = candidate.changed_parts()
checks = 0
collisions = []
dependencies = [Path(candidate.__file__), Path(candidate.accepted.__file__),
                Path(candidate.accepted.accepted.__file__), Path(candidate.accepted.accepted.base.__file__)]
dependency_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in dependencies}
installed_hashes = {}
if '--installed' in sys.argv:
    installed_poses = transforms(manifest)
    installed_definitions = {entry['id']: entry for entry in manifest['definitions']}
    installed_occurrences = {entry['id']: entry for entry in manifest['occurrences']}
    for identifier, expected in list(parts.items()):
        occurrence = installed_occurrences[identifier]
        path = ROOT / installed_definitions[occurrence['definition']]['step'].lstrip('/')
        installed_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        actual = b.import_step(path).moved(installed_poses[identifier])
        common = actual.intersect(expected)
        assert common and abs(sum(solid.volume for solid in common.solids()) - expected.volume) < .02, identifier
        assert abs(actual.volume - expected.volume) < .02, identifier
        parts[identifier] = actual


def overlap(first_id, first, second_id, second):
    global checks
    first_box, second_box = first.bounding_box(), second.bounding_box()
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .001 for axis in 'XYZ'):
        return
    checks += 1
    common = first.intersect(second)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    if volume > .01:
        collisions.append({'first': first_id, 'second': second_id, 'volume_mm3': volume})


roundtrips = []
with tempfile.TemporaryDirectory(prefix='fs10-manifold-') as temporary:
    for identifier, shape in parts.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, len(shape.solids()))
        path = Path(temporary) / f'{identifier}.step'
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1
        assert abs(restored.volume - shape.volume) < .02
        roundtrips.append(identifier)
        print('STEP', identifier, flush=True)

for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
    overlap(first_id, first, second_id, second)
for phase in range(0, 360, 45):
    for identifier, shape in candidate.accepted.parts(phase).items():
        if identifier in parts:
            continue
        for added_id, added in parts.items():
            overlap(added_id, added, identifier, shape)
    print('Phase', phase, flush=True)

contacts = []
rear = parts['ac-compressor-rear-head']
manifold = parts['ac-compressor-rear-manifold']
for role in candidate.PORTS:
    seal = parts[f'ac-compressor-manifold-{role}-seal']
    for target_id, target in [('head', rear), ('manifold', manifold)]:
        distance = seal.distance_to(target)
        assert distance < 1e-6, (role, target_id, distance)
        contacts.append({'seal': role, 'target': target_id, 'distance_mm': distance})
bolt = parts['ac-compressor-manifold-bolt']
assert bolt.distance_to(manifold) < 1e-6
assert rear.distance_to(manifold) < 1e-6
probes = candidate.passage_probes()
for role, probe in probes.items():
    assert len(probe.solids()) == 1
    for identifier, shape in parts.items():
        overlap(f'{role}-passage', probe, identifier, shape)
    base_probe = candidate.accepted.accepted.flow_networks()[role]
    assert probe.distance_to(base_probe) < 1e-6, role
overlap('suction-probe', probes['suction'], 'discharge-probe', probes['discharge'])

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
assert len(api_occurrences) == 65
api_manifest = {'mechanism': manifest['mechanism'], 'assemblies': [{'id': 'engine', 'parent': None}, {'id': 'accessory-drive', 'parent': 'engine'}] + api_groups, 'occurrences': api_occurrences}
api_poses = transforms(api_manifest)
for occurrence in api_occurrences:
    identifier = occurrence['id']
    if identifier in parts:
        actual = api_shapes[identifier].moved(api_poses[identifier])
        target = parts[identifier]
        common = actual.intersect(target)
        assert common and abs(sum(solid.volume for solid in common.solids()) - target.volume) < .02, identifier

if '--internal-only' not in sys.argv:
    poses = transforms(manifest)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    cache = {}
    for occurrence in manifest['occurrences']:
        if occurrence['id'] in parts or occurrence['id'].startswith('ac-compressor-'):
            continue
        definition = occurrence['definition']
        if definition not in cache:
            path = ROOT / definitions[definition]['step'].lstrip('/')
            installed_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
            cache[definition] = b.import_step(path)
        installed = cache[definition].moved(poses[occurrence['id']])
        for identifier, shape in parts.items():
            overlap(identifier, shape, occurrence['id'], installed)
    assert raw == (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
    assert all(hashlib.sha256(path.read_bytes()).hexdigest() == digest for path, digest in installed_hashes.items())

assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest for path, digest in dependency_hashes.items())

report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'candidate_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'step_roundtrips': roundtrips, 'exact_checks': checks, 'collisions': collisions,
          'contacts': contacts, 'api_occurrences': len(api_occurrences),
          'dependency_sha256': dependency_hashes,
          'installed_definition_sha256': {str(path.relative_to(ROOT)): digest for path, digest in installed_hashes.items()},
          'internal_only': '--internal-only' in sys.argv, 'installed_shapes': '--installed' in sys.argv, 'production_fit_verified': False}
filename = 'ac-compressor-manifold-internal-validation.json' if '--internal-only' in sys.argv else 'ac-compressor-manifold-validation.json'
if '--installed' in sys.argv:
    filename = 'ac-compressor-manifold-installed-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
