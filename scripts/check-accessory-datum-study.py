"""Test an uninstalled layout hypothesis without modifying shared geometry."""
import hashlib
import itertools
import json
import sys
import tempfile
from pathlib import Path

import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import accessory_datum_study as study
import accessory_belt_profile as profile
import accessory_belt
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
poses = transforms(manifest)
definitions = {entry['id']: entry for entry in manifest['definitions']}
cache = {}
base = {}
fixed = {}
excluded = []
sources = {Path(module.__file__): Path(module.__file__).read_bytes() for module in (study, profile, accessory_belt)}
for occurrence in manifest['occurrences']:
    identifier = occurrence['id']
    if study.dependent(identifier):
        excluded.append(identifier)
        continue
    definition = occurrence['definition']
    if definition not in cache:
        shape = cad.import_step(ROOT / definitions[definition]['step'].lstrip('/'))
        cache[definition] = profile.normalize_definition(definition, shape)
    shape = cache[definition].moved(poses[identifier])
    (base if study.assembly(identifier) else fixed)[identifier] = shape
checks = 0
collisions = []


def check(first_id, first, second_id, second, bounds, angle):
    global checks
    for identifier, shape in ((first_id, first), (second_id, second)):
        if identifier not in bounds:
            bounds[identifier] = shape.bounding_box()
    first_bounds, second_bounds = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_bounds.max, axis), getattr(second_bounds.max, axis)) - max(getattr(first_bounds.min, axis), getattr(second_bounds.min, axis)) <= .01 for axis in 'XYZ'):
        return
    checks += 1
    intersection = first.intersect(second)
    volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
    if volume > .01:
        collisions.append({'angle_degrees': angle, 'a': first_id, 'b': second_id, 'volume_mm3': volume})
        print('Overlap:', collisions[-1], flush=True)


with tempfile.TemporaryDirectory(prefix='accessory-datum-') as directory:
    for angle in (-10, 0, 10):
        candidates = {identifier: study.move(identifier, shape, angle) for identifier, shape in base.items()}
        candidates['candidate-belt'] = study.belt(angle)
        belt = candidates['candidate-belt']
        assert belt.is_valid and len(belt.solids()) == 1
        path = Path(directory) / f'belt-{angle}.step'
        cad.export_step(belt, path)
        restored = cad.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1
        assert abs(restored.volume - belt.volume) < max(.01, belt.volume * 1e-6)
        bounds = {}
        for (first_id, first), (second_id, second) in itertools.combinations(candidates.items(), 2):
            if study.assembly(first_id) == study.assembly(second_id) and study.assembly(first_id) not in (None, 'TENS'):
                continue
            check(first_id, first, second_id, second, bounds, angle)
        for identifier, candidate in candidates.items():
            for fixed_id, shape in fixed.items():
                check(identifier, candidate, fixed_id, shape, bounds, angle)
        print('Completed exploratory angle:', angle, flush=True)
assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
for path, content in sources.items():
    assert path.read_bytes() == content
report = {
    'passed_geometry_only': not collisions,
    'accepted_for_installation': False,
    'verified_nominal_belt_fit': False,
    'manifest_sha256': hashlib.sha256(raw).hexdigest(),
    'source_sha256': {path.name: hashlib.sha256(content).hexdigest() for path, content in sources.items()},
    'targets_yz_mm': study.TARGETS,
    'moved_component_count': len(base),
    'excluded_dependent_brackets': excluded,
    'belt_step_round_trips': 3,
    'narrow_phase_checks': checks,
    'collisions': collisions,
    'numerical_sweep': study.numerical_report(),
    'limits': study.LIMITS
}
(ROOT / 'inventory/engine' / f'accessory-datum-{study.CASE_NAME}-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key: value for key, value in report.items() if key not in ('excluded_dependent_brackets', 'limits')}, indent=2), flush=True)
