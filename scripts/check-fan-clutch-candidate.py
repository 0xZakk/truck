"""Validate fan construction and explicit replacement interfaces without publishing."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import fan_clutch as candidate
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
poses = transforms(manifest)
definitions = {definition['id']: definition for definition in manifest['definitions']}
local_shapes = candidate.components()
parts = {identifier: b.Pos(*candidate.POSITION) * b.Pos(*position) * b.Rot(*rotation) * local_shapes[definition]
         for identifier, definition, position, rotation in candidate.placements()}
interfaces = {'water-pump-drive-hub': candidate.hub_interface,
              'water-pump-pulley': candidate.pulley_interface}
for identifier, adapt in interfaces.items():
    shape = adapt(b.import_step(ROOT / definitions[identifier]['step'].lstrip('/')))
    local_shapes[identifier] = shape
    parts[identifier] = shape.moved(poses[identifier])

roundtrips = []
with tempfile.TemporaryDirectory(prefix='fan-clutch-') as temporary:
    for identifier, shape in local_shapes.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, shape.is_valid, len(shape.solids()))
        path = Path(temporary) / f'{identifier}.step'
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .02, identifier
        roundtrips.append(identifier)
        print('STEP valid', identifier, flush=True)

checks = 0
collisions = []
cache = {}
bounds = {identifier: shape.bounding_box() for identifier, shape in parts.items()}


def compare(first_id, first, second_id, second):
    global checks
    if first_id not in bounds:
        bounds[first_id] = first.bounding_box()
    if second_id not in bounds:
        bounds[second_id] = second.bounding_box()
    first_box, second_box = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
        return
    checks += 1
    intersection = first.intersect(second)
    volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
    if volume > .01:
        collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})


for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
    compare(first_id, first, second_id, second)
print('Internal checks', checks, 'collisions', collisions, flush=True)
if '--internal-only' not in sys.argv:
    for occurrence in manifest['occurrences']:
        if occurrence['id'] in parts:
            continue
        identifier = occurrence['definition']
        if identifier not in cache:
            cache[identifier] = b.import_step(ROOT / definitions[identifier]['step'].lstrip('/'))
        installed = cache[identifier].moved(poses[occurrence['id']])
        for part_id, shape in parts.items():
            compare(part_id, shape, occurrence['id'], installed)

assert raw == manifest_path.read_bytes(), 'Installed manifest changed during audit'
report = {'installed': False, 'verified_production_fit': False,
          'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'step_roundtrips': roundtrips, 'candidate_occurrences': len(parts),
          'checks': checks, 'collisions': collisions, 'internal_only': '--internal-only' in sys.argv,
          'replaced_definitions': list(interfaces), 'limits': candidate.GAPS}
report_path = ROOT / ('inventory/engine/fan-clutch-internal-validation.json' if '--internal-only' in sys.argv
                      else 'inventory/engine/fan-clutch-candidate-validation.json')
report_path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
