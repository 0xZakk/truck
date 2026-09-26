"""Validate alternator construction and frozen installed-neighbor fit."""
import hashlib
import itertools
import json
import sys
import tempfile
from pathlib import Path

import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import alternator
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
source = (ROOT / 'cad/engine/alternator.py').read_bytes()
manifest = json.loads(raw)
poses = transforms(manifest)
definitions = {entry['id']: entry for entry in manifest['definitions']}
parts = alternator.parts()
with tempfile.TemporaryDirectory(prefix='alternator-candidate-') as directory:
    for identifier, shape in parts.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        destination = Path(directory) / (identifier + '.step')
        cad.export_step(shape, destination)
        restored = cad.import_step(destination)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < 0.01, identifier
        print('Valid STEP round trip:', identifier, flush=True)

checks = 0
collisions = []
bounds = {}


def check(first_id, first, second_id, second):
    global checks
    if first_id not in bounds:
        bounds[first_id] = first.bounding_box()
    if second_id not in bounds:
        bounds[second_id] = second.bounding_box()
    first_bounds, second_bounds = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_bounds.max, axis), getattr(second_bounds.max, axis)) -
           max(getattr(first_bounds.min, axis), getattr(second_bounds.min, axis)) <= 0.01
           for axis in 'XYZ'):
        return
    checks += 1
    intersection = first.intersect(second)
    volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
    if volume > 0.01:
        collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})
        print('Overlap:', collisions[-1], flush=True)


for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
    check(first_id, first, second_id, second)
cache = {}
for occurrence in manifest['occurrences']:
    if occurrence['id'] in parts:
        continue
    definition = occurrence['definition']
    if definition not in cache:
        cache[definition] = cad.import_step(ROOT / definitions[definition]['step'].lstrip('/'))
    installed = cache[definition].moved(poses[occurrence['id']])
    for identifier, candidate in parts.items():
        check(identifier, candidate, occurrence['id'], installed)

assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
assert (ROOT / 'cad/engine/alternator.py').read_bytes() == source
report = {
    'passed': not collisions,
    'installed': False,
    'verified_production_fit': False,
    'manifest_sha256': hashlib.sha256(raw).hexdigest(),
    'source_sha256': hashlib.sha256(source).hexdigest(),
    'solid_step_round_trips': len(parts),
    'narrow_phase_checks': checks,
    'collisions': collisions,
    'limits': alternator.GAPS,
}
(ROOT / 'inventory/engine/alternator-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
