"""Validate CII pump internals and optionally the frozen installed assembly."""
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
import power_steering_pump as pump
from assembly_math import transforms

parser = argparse.ArgumentParser()
parser.add_argument('--internal-only', action='store_true')
options = parser.parse_args()
source = (ROOT / 'cad/engine/power_steering_pump.py').read_bytes()
raw = None if options.internal_only else (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
parts = pump.parts()
candidate_sources = {'power_steering_pump.py': source}
if not options.internal_only:
    import tensioner_arm
    import tensioner_pulley
    parts.update(tensioner_arm.parts())
    parts.update(tensioner_pulley.parts())
    for name in ('tensioner_arm.py', 'tensioner_pulley.py'):
        candidate_sources[name] = (ROOT / 'cad/engine' / name).read_bytes()
step_volume_deltas = []
with tempfile.TemporaryDirectory(prefix='ps-pump-candidate-') as directory:
    for identifier, shape in parts.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        destination = Path(directory) / (identifier + '.step')
        cad.export_step(shape, destination)
        restored = cad.import_step(destination)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        difference = abs(restored.volume - shape.volume)
        assert difference <= max(0.01, shape.volume * 1e-6), identifier
        step_volume_deltas.append((difference, difference / shape.volume))
        print('Valid STEP:', identifier, flush=True)

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
if raw is not None:
    manifest = json.loads(raw)
    poses = transforms(manifest)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
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
for name, content in candidate_sources.items():
    assert (ROOT / 'cad/engine' / name).read_bytes() == content
report = {
    'passed': not collisions,
    'installed': False,
    'verified_production_fit': False,
    'scope': 'internal-only' if options.internal_only else 'internal-and-installed-neighbors',
    'manifest_sha256': hashlib.sha256(raw).hexdigest() if raw is not None else None,
    'source_sha256': hashlib.sha256(source).hexdigest(),
    'replacement_source_sha256': {name: hashlib.sha256(content).hexdigest() for name, content in candidate_sources.items()},
    'solid_step_round_trips': len(parts),
    'step_volume_tolerance': '0.01 mm3 or 1 ppm of volume, whichever is larger',
    'maximum_step_volume_delta_mm3': max(delta[0] for delta in step_volume_deltas),
    'maximum_step_relative_volume_delta': max(delta[1] for delta in step_volume_deltas),
    'narrow_phase_checks': checks,
    'collisions': collisions,
    'limits': pump.GAPS,
}
name = 'power-steering-pump-internal-validation.json' if options.internal_only else 'power-steering-pump-candidate-validation.json'
(ROOT / 'inventory/engine' / name).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
