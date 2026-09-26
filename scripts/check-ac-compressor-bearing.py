"""Check dimensioned bearing revision against moving compressor and frozen neighbors."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor_bearing as candidate
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
roundtrips = []
with tempfile.TemporaryDirectory(prefix='fs10-bearing-') as temporary:
    for identifier, shape in candidate.replacements().items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, len(shape.solids()))
        path = Path(temporary) / f'{identifier}.step'
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1
        assert abs(restored.volume - shape.volume) < .02
        roundtrips.append(identifier)
        print('STEP', identifier, flush=True)

bounds = {}
checks = 0
collisions = []


def overlap(first_id, first, second_id, second, phase):
    global checks
    for identifier, shape in ((first_id, first), (second_id, second)):
        if identifier not in bounds:
            bounds[identifier] = shape.bounding_box()
    first_box, second_box = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
        return
    checks += 1
    common = first.intersect(second)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    if volume > .01:
        collisions.append({'a': first_id, 'b': second_id, 'phase': phase, 'volume_mm3': volume})


phases = [0] if '--static-only' in sys.argv else list(range(0, 360, 45))
for phase in phases:
    parts = candidate.parts(phase)
    bounds.clear()
    for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
        if first_id in candidate.replacements() or second_id in candidate.replacements():
            overlap(first_id, first, second_id, second, phase)
    print('Phase', phase, checks, collisions, flush=True)

parts = candidate.parts()
bounds.clear()
for probe_id, probe in candidate.accepted.flow_networks().items():
    for identifier, shape in parts.items():
        overlap(probe_id, probe, identifier, shape, 'open-passage')

api_definitions = {}
api_occurrences = []
api_manifest = json.loads(raw)
descendants = {'ac-compressor'}
while True:
    expanded = descendants | {entry['id'] for entry in api_manifest['assemblies'] if entry['parent'] in descendants}
    if expanded == descendants:
        break
    descendants = expanded
api_manifest['assemblies'] = [entry for entry in api_manifest['assemblies'] if entry['id'] not in descendants]


def define(identifier, shape, *metadata):
    api_definitions[identifier] = shape


def group(identifier, name, parent='engine', motion=None, position=(0, 0, 0), rotation=(0, 0, 0)):
    api_manifest['assemblies'].append({'id': identifier, 'name': name, 'parent': parent, 'motion': motion,
                                       'position_cad_mm': position, 'rotation_cad_deg': rotation})


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0)):
    api_occurrences.append({'id': identifier, 'definition': definition, 'parent': parent,
                            'position_cad_mm': pos, 'rotation_cad_deg': rotation})


candidate.build((define, add, group))
api_manifest['occurrences'] = api_occurrences
assert len(api_occurrences) == len(api_definitions) == 61
api_checks = 0
for phase, engaged in ((0, True), (137, True), (137, False)):
    poses = transforms(api_manifest, compressor_degrees=phase, compressor_engaged=engaged)
    targets = candidate.parts(phase, engaged)
    for occurrence in api_occurrences:
        actual = api_definitions[occurrence['definition']].moved(poses[occurrence['id']])
        target = targets[occurrence['id']]
        common = actual.intersect(target)
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        assert abs(volume - target.volume) < .02, (occurrence['id'], phase, engaged)
        api_checks += 1
print('API', api_checks, flush=True)

if '--internal-only' not in sys.argv:
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    poses = transforms(manifest)
    cache = {}
    for index, occurrence in enumerate(manifest['occurrences']):
        if occurrence['id'] in parts:
            continue
        definition = occurrence['definition']
        if definition not in cache:
            cache[definition] = b.import_step(ROOT / definitions[definition]['step'].lstrip('/'))
        installed = cache[definition].moved(poses[occurrence['id']])
        for identifier in candidate.replacements():
            overlap(identifier, parts[identifier], occurrence['id'], installed, 'installed')
        if index % 300 == 0:
            print('Neighbor', index, flush=True)
    assert raw == (ROOT / 'inventory/engine/full-assembly.json').read_bytes()

bearing_box = candidate.replacements()['ac-compressor-pulley-bearing'].bounding_box()
assert abs(bearing_box.size.X - 23) < 1e-6
assert abs(bearing_box.size.Y - 55) < 1e-6
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'candidate_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'accepted_motion_sha256': hashlib.sha256(Path(candidate.accepted.__file__).read_bytes()).hexdigest(),
          'step_roundtrips': roundtrips, 'checks': checks, 'collisions': collisions,
          'api_shape_pose_checks': api_checks,
          'phases': phases, 'bearing_dimensions_mm': [30, 55, 23],
          'bearing_internals_complete': False, 'internal_only': '--internal-only' in sys.argv}
filename = 'ac-compressor-bearing-internal-validation.json' if '--internal-only' in sys.argv else 'ac-compressor-bearing-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
