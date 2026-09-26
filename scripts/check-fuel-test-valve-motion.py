import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile

import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import fuel_test_valve_motion as valve
import fuel_test_valve
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
poses = transforms(manifest)
definitions = {entry['id']: entry for entry in manifest['definitions']}
sources = {Path(module.__file__): Path(module.__file__).read_bytes() for module in (valve, fuel_test_valve)}
cache = {}
neighbors = {}
for occurrence in manifest['occurrences']:
    if occurrence['id'].startswith('fuel-test-'):
        continue
    definition = occurrence['definition']
    if definition not in cache:
        cache[definition] = cad.import_step(ROOT / definitions[definition]['step'].lstrip('/'))
    neighbors[occurrence['id']] = cache[definition].moved(poses[occurrence['id']])


def volume(shape):
    return sum(solid.volume for solid in shape.solids()) if shape else 0


def overlap(first, second):
    first_bounds, second_bounds = first.bounding_box(), second.bounding_box()
    return all(min(getattr(first_bounds.max, axis), getattr(second_bounds.max, axis)) - max(getattr(first_bounds.min, axis), getattr(second_bounds.min, axis)) > 1e-6 for axis in 'XYZ')


collisions = []
states = []
checks = 0
round_trips = 0
with tempfile.TemporaryDirectory(prefix='fuel-valve-motion-') as directory:
    for travel, cap_removed in [(0, False), (0, True), (.03, True), (.06, True), (.09, True), (.12, True)]:
        local = valve.components(travel, cap_removed)
        candidates = valve.parts(travel, cap_removed)
        for identifier, shape in candidates.items():
            assert shape.is_valid and len(shape.solids()) == 1
            path = Path(directory) / f'{travel}-{cap_removed}-{identifier}.step'
            cad.export_step(shape, path)
            restored = cad.import_step(path)
            assert restored.is_valid and len(restored.solids()) == 1
            assert abs(restored.volume - shape.volume) < .001
            round_trips += 1
        pairs = list(itertools.combinations(candidates.items(), 2)) + list(itertools.product(candidates.items(), neighbors.items()))
        for (first_id, first), (second_id, second) in pairs:
            if not overlap(first, second):
                continue
            checks += 1
            common = volume(first.intersect(second))
            if common > .0001:
                collisions.append({'travel_mm': travel, 'cap_removed': cap_removed, 'a': first_id, 'b': second_id, 'volume_mm3': common})
        blocked = 0
        closed_control_blocked = 0
        if travel:
            probe_segments = valve.passage_probe(travel)
            blocked = sum(volume(shape.intersect(probe)) for shape in local.values() for probe in probe_segments)
            closed_control_blocked = sum(volume(shape.intersect(probe)) for shape in valve.components(0, True).values() for probe in probe_segments)
            assert blocked < 1e-8, (travel, blocked)
            assert closed_control_blocked > 1e-6, (travel, closed_control_blocked)
        rail_probe = cad.Pos(*valve.POSITION) * cad.Pos(0, 0, -4.5) * cad.Cylinder(.5, 9)
        assert volume(neighbors['fuel-supply-rail'].intersect(rail_probe)) < 1e-6
        states.append({'travel_mm': travel, 'cap_removed': cap_removed, 'spring_pitch_mm': (1.62 - travel) / 4, 'wire_diameter_mm': .36, 'open_path_blockage_mm3': blocked if travel else None, 'closed_control_blockage_mm3': closed_control_blocked if travel else None})
        print('Completed state', states[-1], flush=True)
assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
for path, content in sources.items():
    assert path.read_bytes() == content
report = {'passed': not collisions, 'verified_production_fit': False, 'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'sources_sha256': {path.name: hashlib.sha256(content).hexdigest() for path, content in sources.items()}, 'step_round_trips': round_trips, 'narrow_phase_checks': checks, 'collisions': collisions, 'states': states, 'unresolved_static_seal_radial_gap_mm': .01, 'limits': valve.GAPS}
(ROOT / 'inventory/engine/fuel-test-valve-motion-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert report['passed']
