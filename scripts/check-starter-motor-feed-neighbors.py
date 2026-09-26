"""Canonical-STEP motor-feed candidate or installed full-engine neighbor audit."""
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
import starter_motor_feed as feed
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
with tempfile.TemporaryDirectory(prefix='starter-feed-expected-') as directory:
    for identifier, shape in feed.parts().items():
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
contact_pairs = [('starter-motor-positive-feed', 'starter-solenoid-terminal-2'), ('starter-motor-positive-feed', 'starter-solenoid-terminal-nut-2'), ('starter-motor-ground-bridge', 'starter-brush-end-plate'), ('starter-motor-ground-bridge', 'starter-brush-plate-screw-1'), ('starter-motor-ground-bridge', 'starter-brush-plate-screw-2')]
for role in feed.PIGTAILS:
    identifier = 'starter-brush-pigtail-' + role
    target = 'starter-motor-positive-feed' if role.startswith('positive') else 'starter-motor-ground-bridge'
    contact_pairs.extend([(identifier, target), (identifier, 'starter-brush-' + role[-1])])
contacts = []
for first, second in contact_pairs:
    distance = shapes[first].distance_to(shapes[second])
    volumes = [overlap(shapes[first], shapes[second]), overlap(shapes[second], shapes[first])]
    assert distance < 1e-6 and max(volumes) < .001, (first, second, distance, volumes)
    contacts.append([first, second, distance, volumes])
boxes = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
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
print('Directed checks', checks, 'failures', failures, flush=True)
dielectric = {'starter-brush-carrier', 'starter-commutator-insulator', 'starter-motor-feed-jacket', 'starter-motor-feed-grommet', 'starter-solenoid-winding-bobbin', 'starter-solenoid-bridge-insulator', 'starter-solenoid-s-terminal-insulator', 'starter-solenoid-end-cap'}
dielectric.update(identifier for identifier in shapes if identifier.startswith(('starter-brush-holder-', 'starter-solenoid-lead-insulation-')))
conductors = {'starter-motor-positive-feed', 'starter-motor-ground-bridge'} | {'starter-brush-pigtail-' + role for role in feed.PIGTAILS}
allowed = {frozenset(pair) for pair in contact_pairs}
clearances, clearance_checks = [], 0
for first in conductors:
    minimum, nearest = math.inf, None
    for second in shapes:
        if first == second or second in dielectric or frozenset((first, second)) in allowed:
            continue
        first_box, second_box = boxes[first], boxes[second]
        lower_bound = math.sqrt(sum(max(getattr(second_box.min, axis) - getattr(first_box.max, axis), getattr(first_box.min, axis) - getattr(second_box.max, axis), 0) ** 2 for axis in 'XYZ'))
        if lower_bound >= minimum:
            continue
        clearance_checks += 1
        distance = shapes[first].distance_to(shapes[second])
        if distance < minimum:
            minimum, nearest = distance, second
        if distance < .01:
            failures.append([first, second, 'unintended conductive clearance', distance])
    clearances.append([first, nearest, minimum])
assert path.read_bytes() == raw, 'Frozen manifest changed'
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_motor_feed.py').read_bytes()).hexdigest(), 'parts': len(candidate), 'canonical_step_expected': True, 'shape_checks': shape_checks, 'directed_boolean_checks': checks, 'contacts': contacts, 'clearance_checks': clearance_checks, 'clearances': clearances, 'failures': failures,
          'boundary': 'No volume-overlap exemptions. Known dielectrics excluded only from conductive clearance; material-unknown neighbors conservatively treated as conductors. Production brush clocking and routing, electrical performance and armature winding continuity remain unverified.'}
filename = 'starter-motor-feed-installed-validation.json' if installed else 'starter-motor-feed-neighbors-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS motor-feed full-engine neighbors', flush=True)
