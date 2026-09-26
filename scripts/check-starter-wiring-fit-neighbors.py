"""Bidirectional full-engine overlap audit for corrected starter coil interfaces."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_wiring_fit as wiring
from assembly_math import transforms


def overlap(first, second):
    common = first.intersect(second)
    return sum(solid.volume for solid in common.solids()) if common else 0


path = ROOT / 'inventory/engine/full-assembly.json'
raw = path.read_bytes()
manifest = json.loads(raw)
installed = '--installed' in sys.argv
definitions = {item['id']: b.import_step(ROOT / item['step'].lstrip('/')) for item in manifest['definitions']}
locations = transforms(manifest)
shapes = {item['id']: locations[item['id']] * definitions[item['definition']] for item in manifest['occurrences']}
candidate = {}
with tempfile.TemporaryDirectory(prefix='starter-wiring-fit-expected-') as directory:
    for identifier, shape in wiring.parts().items():
        expected_path = Path(directory) / (identifier + '.step')
        b.export_step(shape, expected_path)
        restored = b.import_step(expected_path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .002, identifier
        candidate[identifier] = starter.FRAME * restored
shape_checks = []
if installed:
    for identifier, expected in candidate.items():
        actual = shapes[identifier]
        assert actual.is_valid and len(actual.solids()) == 1, identifier
        difference = actual.volume + expected.volume - 2 * overlap(actual, expected)
        assert abs(difference) < .002 and abs(actual.volume - expected.volume) < .002, (identifier, difference)
        shape_checks.append({'id': identifier, 'symmetric_difference_mm3': difference})
    candidate = {identifier: shapes[identifier] for identifier in candidate}
shapes.update(candidate)
boxes = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
contacts, allowed = [], set()
for role, targets in wiring.CONTACTS.items():
    identifier = 'starter-solenoid-lead-' + role
    for target in targets:
        distance = shapes[identifier].distance_to(shapes[target])
        forward, reverse = overlap(shapes[identifier], shapes[target]), overlap(shapes[target], shapes[identifier])
        assert distance < 1e-6 and max(forward, reverse) < .001, (identifier, target, distance, forward, reverse)
        contacts.append({'lead': identifier, 'target': target, 'distance_mm': distance, 'forward_overlap_mm3': forward, 'reverse_overlap_mm3': reverse})
        allowed.add(frozenset((identifier, target)))
checks, failures = 0, []
for first, second in itertools.combinations(shapes, 2):
    if first not in candidate and second not in candidate:
        continue
    first_box, second_box = boxes[first], boxes[second]
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .0001 for axis in 'XYZ'):
        continue
    for left, right in ((first, second), (second, first)):
        checks += 1
        volume = overlap(shapes[left], shapes[right])
        if volume > .001:
            failures.append([left, right, volume])
print('Bidirectional overlaps', checks, failures, flush=True)
insulating = {'starter-solenoid-' + role for role in ('winding-bobbin', 'bridge-insulator', 's-terminal-insulator', 'end-cap')}
insulating.update('starter-solenoid-lead-insulation-' + role for role in wiring.ROUTES)
clearances, clearance_checks = [], 0
for role in wiring.ROUTES:
    first = 'starter-solenoid-lead-' + role
    minimum, nearest = math.inf, None
    for second, neighbor in shapes.items():
        if first == second or second in insulating or frozenset((first, second)) in allowed:
            continue
        first_box, second_box = boxes[first], boxes[second]
        lower_bound = math.sqrt(sum(max(getattr(second_box.min, axis) - getattr(first_box.max, axis), getattr(first_box.min, axis) - getattr(second_box.max, axis), 0) ** 2 for axis in 'XYZ'))
        if lower_bound >= minimum:
            continue
        clearance_checks += 1
        distance = shapes[first].distance_to(neighbor)
        if distance < minimum:
            minimum, nearest = distance, second
        if distance < .01:
            failures.append([first, second, 'unintended clearance', distance])
    clearances.append({'lead': first, 'nearest': nearest, 'distance_mm': minimum})
assert path.read_bytes() == raw, 'Frozen manifest changed'
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_wiring_fit.py').read_bytes()).hexdigest(),
          'candidate_parts': len(candidate), 'canonical_step_expected': True, 'shape_checks': shape_checks, 'directed_boolean_checks': checks, 'contacts': contacts,
          'clearance_checks': clearance_checks, 'clearances': clearances, 'failures': failures,
          'boundary': 'No volume-overlap exemptions, including intended attachments and the two separate S paths. Known dielectric parts excluded only from conductor-to-conductor clearance; all physical overlap pairs checked in both Boolean operand orders.'}
filename = 'starter-wiring-fit-installed-validation.json' if installed else 'starter-wiring-fit-neighbors-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS corrected starter wiring frozen neighbors', flush=True)
