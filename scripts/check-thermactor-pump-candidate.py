"""Check Thermactor exterior/interfaces without claiming a resolved pumping cartridge."""
import argparse
import hashlib
import itertools
import json
import sys
import tempfile
from pathlib import Path

import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import accessory_brackets
import thermactor_pump
from assembly_math import transforms

parser = argparse.ArgumentParser()
parser.add_argument('--internal-only', action='store_true')
options = parser.parse_args()
modules = [accessory_brackets, thermactor_pump]
sources = {module.__name__: Path(module.__file__).read_bytes() for module in modules}
parts = thermactor_pump.parts()
neighbors = accessory_brackets.parts()
raw = None if options.internal_only else (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
adapted = {}
additions = {}
if raw is not None:
    manifest = json.loads(raw)
    poses = transforms(manifest)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    for identifier, adapter in [('block', lambda shape: thermactor_pump.block_interface(accessory_brackets.block_interface(shape)))]:
        original = cad.import_step(ROOT / definitions[identifier]['step'].lstrip('/'))
        adapted[identifier] = adapter(original).moved(poses[identifier])
        neighbors[identifier] = adapted[identifier]
        addition = adapted[identifier] - original.moved(poses[identifier])
        if addition:
            additions[identifier + '-new-boss-material'] = cad.Compound(addition.solids())
checks = 0
collisions = []
round_trips = []
bounds = {}


def check(first_id, first, second_id, second):
    global checks
    for identifier, shape in ((first_id, first), (second_id, second)):
        if identifier not in bounds:
            bounds[identifier] = shape.bounding_box()
    first_bounds, second_bounds = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_bounds.max, axis), getattr(second_bounds.max, axis)) -
           max(getattr(first_bounds.min, axis), getattr(second_bounds.min, axis)) <= 0.01 for axis in 'XYZ'):
        return
    checks += 1
    intersection = first.intersect(second)
    volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
    if volume > 0.01:
        collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})
        print('Overlap:', collisions[-1], flush=True)


with tempfile.TemporaryDirectory(prefix='thermactor-pump-') as directory:
    for identifier, shape in {**parts, **adapted}.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(directory) / (identifier + '.step')
        cad.export_step(shape, path)
        restored = cad.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) <= max(.01, shape.volume * 1e-6), identifier
        round_trips.append(identifier)
        print('Valid STEP:', identifier, flush=True)
for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
    check(first_id, first, second_id, second)
for identifier, candidate in parts.items():
    for neighbor_id, neighbor in neighbors.items():
        check(identifier, candidate, neighbor_id, neighbor)
if raw is not None:
    manifest = json.loads(raw)
    poses = transforms(manifest)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    cache = {}
    for occurrence in manifest['occurrences']:
        if occurrence['id'] in parts or occurrence['id'] in neighbors:
            continue
        definition = occurrence['definition']
        if definition not in cache:
            cache[definition] = cad.import_step(ROOT / definitions[definition]['step'].lstrip('/'))
        shape = cache[definition].moved(poses[occurrence['id']])
        for identifier, candidate in parts.items():
            check(identifier, candidate, occurrence['id'], shape)
        for identifier, candidate in additions.items():
            check(identifier, candidate, occurrence['id'], shape)
    assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
for module in modules:
    assert Path(module.__file__).read_bytes() == sources[module.__name__]
report = {
    'passed': not collisions,
    'verified_production_fit': False,
    'scope': 'internal-and-accessory-bracket-candidates' if options.internal_only else 'internal-candidates-and-installed',
    'manifest_sha256': hashlib.sha256(raw).hexdigest() if raw else None,
    'source_sha256': {name: hashlib.sha256(content).hexdigest() for name, content in sources.items()},
    'step_round_trips': len(round_trips),
    'narrow_phase_checks': checks,
    'collisions': collisions,
    'limits': thermactor_pump.GAPS
}
destination = 'thermactor-pump-internal-validation.json' if options.internal_only else 'thermactor-pump-candidate-validation.json'
(ROOT / 'inventory/engine' / destination).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
