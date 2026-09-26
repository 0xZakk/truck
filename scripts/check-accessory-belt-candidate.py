"""Frozen-manifest QC for belt/profile normalization and tensioner attachment."""
import hashlib
import itertools
import json
import math
import sys
import tempfile
from pathlib import Path

import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import accessory_belt
import accessory_belt_profile
import tensioner_engine_support
from assembly_math import transforms

modules = [accessory_belt, accessory_belt_profile, tensioner_engine_support]
sources = {module.__name__: Path(module.__file__).read_bytes() for module in modules}
raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
poses = transforms(manifest)
definitions = {entry['id']: entry for entry in manifest['definitions']}
parts = {**accessory_belt.parts(), **tensioner_engine_support.parts()}
pulley_ids = ['alternator-pulley', 'ps-pump-pulley', 'damper-inertia-ring', 'ac-compressor-clutch-pulley', 'thermactor-pulley']
for identifier in pulley_ids:
    original = cad.import_step(ROOT / definitions[identifier]['step'].lstrip('/'))
    parts[identifier] = accessory_belt_profile.normalize_definition(identifier, original).moved(poses[identifier])
adapted = {}
additions = {}
for identifier, adapter in [('block', tensioner_engine_support.block_interface), ('cylinder-head', tensioner_engine_support.head_interface)]:
    original = cad.import_step(ROOT / definitions[identifier]['step'].lstrip('/'))
    adapted[identifier] = adapter(original).moved(poses[identifier])
    addition = adapted[identifier] - original.moved(poses[identifier])
    if addition:
        additions[identifier + '-new-mount-material'] = cad.Compound(addition.solids())
solution = accessory_belt.solve()
for span in solution['spans']:
    direction = tuple((span['end'][index] - span['start'][index]) / span['length'] for index in range(2))
    assert abs(sum(direction[index] * span['normal'][index] for index in range(2))) < 1e-10
assert abs(sum(-arc['side'] * arc['wrap_degrees'] for arc in solution['arcs']) + 360) < 1e-9
wire = accessory_belt.path(solution)
assert wire.is_closed and wire.is_valid
assert abs(wire.length - solution['length']) < 1e-6
round_trips = []
with tempfile.TemporaryDirectory(prefix='accessory-belt-') as directory:
    for identifier, shape in {**parts, **adapted}.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(directory) / (identifier + '.step')
        cad.export_step(shape, path)
        restored = cad.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) <= max(.01, shape.volume * 1e-6), identifier
        round_trips.append(identifier)
        print('Valid STEP:', identifier, flush=True)
checks = 0
collisions = []
bounds = {}


def check(first_id, first, second_id, second):
    global checks
    for identifier, shape in ((first_id, first), (second_id, second)):
        if identifier not in bounds:
            bounds[identifier] = shape.bounding_box()
    first_bounds, second_bounds = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_bounds.max, axis), getattr(second_bounds.max, axis)) -
           max(getattr(first_bounds.min, axis), getattr(second_bounds.min, axis)) <= .01 for axis in 'XYZ'):
        return
    checks += 1
    intersection = first.intersect(second)
    volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
    if volume > .01:
        collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})
        print('Overlap:', collisions[-1], flush=True)


for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
    check(first_id, first, second_id, second)
for identifier, candidate in parts.items():
    for neighbor_id, shape in adapted.items():
        check(identifier, candidate, neighbor_id, shape)
cache = {}
for occurrence in manifest['occurrences']:
    if occurrence['id'] in parts or occurrence['id'] in adapted:
        continue
    definition = occurrence['definition']
    if definition not in cache:
        cache[definition] = cad.import_step(ROOT / definitions[definition]['step'].lstrip('/'))
    shape = cache[definition].moved(poses[occurrence['id']])
    for identifier, candidate in {**parts, **additions}.items():
        check(identifier, candidate, occurrence['id'], shape)
assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
for module in modules:
    assert Path(module.__file__).read_bytes() == sources[module.__name__]
report = {
    'passed': not collisions,
    'verified_production_fit': False,
    'verified_nominal_belt_fit': False,
    'manifest_sha256': hashlib.sha256(raw).hexdigest(),
    'source_sha256': {name: hashlib.sha256(content).hexdigest() for name, content in sources.items()},
    'step_round_trips': len(round_trips),
    'analytic_tangency_closed_wire_and_winding': True,
    'narrow_phase_checks': checks,
    'collisions': collisions,
    'routing': accessory_belt.routing_report(),
    'support_limits': tensioner_engine_support.GAPS
}
(ROOT / 'inventory/engine/accessory-belt-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key: value for key, value in report.items() if key not in ('routing', 'support_limits')}, indent=2), flush=True)
assert not collisions
