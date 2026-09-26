"""Check attached heater takeoffs, open passages and installed neighbor clearance."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import cooling_connections as candidate
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
definitions = {definition['id']: definition for definition in manifest['definitions']}
poses = transforms(manifest)
local = candidate.components()
parts = {identifier: b.Pos(*position) * local[definition] for identifier, definition, position in candidate.placements()}
pump = candidate.pump_housing_interface(b.import_step(ROOT / definitions['water-pump-housing']['step'].lstrip('/')))
local['water-pump-housing'] = pump
parts['water-pump-housing'] = pump.moved(poses['water-pump-housing'])
roundtrips = []
with tempfile.TemporaryDirectory(prefix='cooling-connections-') as temporary:
    for identifier, shape in local.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, shape.is_valid, len(shape.solids()))
        path = Path(temporary) / f'{identifier}.step'
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .02, identifier
        roundtrips.append(identifier)
        print('STEP valid', identifier, flush=True)

collisions = []
blocked_passages = []
checks = 0
bounds = {identifier: shape.bounding_box() for identifier, shape in parts.items()}
probes = candidate.flow_probes()
bounds.update({identifier: shape.bounding_box() for identifier, shape in probes.items()})
cache = {}


def overlap(first_id, first, second_id, second, failures):
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
    common = first.intersect(second)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    if volume > .01:
        failures.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})


for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
    overlap(first_id, first, second_id, second, collisions)
for probe_id, probe in probes.items():
    for identifier, shape in parts.items():
        overlap(probe_id, probe, identifier, shape, blocked_passages)
print('Internal', checks, collisions, 'blocked', blocked_passages, flush=True)

if '--internal-only' not in sys.argv:
    for index, occurrence in enumerate(manifest['occurrences']):
        if occurrence['id'] in parts:
            continue
        identifier = occurrence['definition']
        if identifier not in cache:
            cache[identifier] = b.import_step(ROOT / definitions[identifier]['step'].lstrip('/'))
        installed = cache[identifier].moved(poses[occurrence['id']])
        for part_id, shape in parts.items():
            overlap(part_id, shape, occurrence['id'], installed, collisions)
        for probe_id, probe in probes.items():
            overlap(probe_id, probe, occurrence['id'], installed, blocked_passages)
        if index % 200 == 0:
            print('Neighbor progress', index, flush=True)

assert manifest_path.read_bytes() == raw
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'step_roundtrips': roundtrips, 'checks': checks, 'collisions': collisions,
          'flow_probes': list(probes), 'blocked_passages': blocked_passages,
          'internal_only': '--internal-only' in sys.argv, 'installed': False,
          'verified_production_fit': False, 'limits': candidate.GAPS}
filename = 'cooling-connections-internal-validation.json' if '--internal-only' in sys.argv else 'cooling-connections-candidate-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions and not blocked_passages
