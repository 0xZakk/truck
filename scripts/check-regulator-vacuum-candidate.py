"""Check an open regulator vacuum path and fit against the frozen assembly."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile

import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import regulator_vacuum
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
definitions = {entry['id']: entry for entry in manifest['definitions']}
poses = transforms(manifest)
parts = regulator_vacuum.parts()
intake = cad.import_step(ROOT / definitions['efi-upper-intake']['step'].lstrip('/'))
parts['efi-upper-intake'] = regulator_vacuum.intake_interface(intake)
with tempfile.TemporaryDirectory(prefix='regulator-vacuum-') as directory:
    for identifier, shape in parts.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(directory) / (identifier + '.step')
        cad.export_step(shape, path)
        restored = cad.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < max(.01, shape.volume * 1e-5), identifier
        print('STEP valid', identifier, flush=True)

collisions = []
checks = 0
bounds = {}


def check(first_id, first, second_id, second):
    global checks
    if first_id not in bounds:
        bounds[first_id] = first.bounding_box()
    if second_id not in bounds:
        bounds[second_id] = second.bounding_box()
    first_bounds, second_bounds = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_bounds.max, axis), getattr(second_bounds.max, axis)) -
           max(getattr(first_bounds.min, axis), getattr(second_bounds.min, axis)) <= .01
           for axis in 'XYZ'):
        return
    checks += 1
    overlap = first.intersect(second)
    volume = sum(solid.volume for solid in overlap.solids()) if overlap else 0
    if volume > .01:
        collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})


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

probe = regulator_vacuum.cylinder(1, (0, -74, 460), (0, -39, 460))
for identifier in ('regulator-vacuum-fitting', 'efi-upper-intake'):
    overlap = parts[identifier].intersect(probe)
    assert not overlap or sum(solid.volume for solid in overlap.solids()) < .01, identifier
assert manifest_path.read_bytes() == raw
report = {
    'passed': not collisions,
    'manifest_sha256': hashlib.sha256(raw).hexdigest(),
    'source_sha256': hashlib.sha256(Path(regulator_vacuum.__file__).read_bytes()).hexdigest(),
    'checks': checks, 'collisions': collisions, 'plenum_port_probe': 'open',
    'verified_production_fit': False, 'limits': regulator_vacuum.GAPS
}
(ROOT / 'inventory/engine/regulator-vacuum-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
