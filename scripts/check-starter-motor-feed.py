"""Isolated motor-feed attachments and all-pair geometry study."""
from pathlib import Path
import itertools
import hashlib
import json
import math
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
import starter_engagement as linkage
import starter_wiring_fit as coil_wiring
import starter_motor_feed as feed


def overlap(first, second):
    common = first.intersect(second)
    return sum(solid.volume for solid in common.solids()) if common else 0


def near(first, second):
    first_box, second_box = first.bounding_box(), second.bounding_box()
    return all(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) > .0001 for axis in 'XYZ')


baseline = starter.parts()
shapes = {identifier: shape for identifier, shape in baseline.items() if identifier not in switch.REPLACED}
shapes.update(switch.parts())
shapes.update(linkage.parts(baseline=baseline))
coil_candidate = coil_wiring.parts()
shapes.update(coil_candidate)
candidate = feed.parts()
shapes.update(candidate)
for identifier, shape in candidate.items():
    assert shape.is_valid and len(shape.solids()) == 1, (identifier, len(shape.solids()))
with tempfile.TemporaryDirectory(prefix='starter-motor-feed-') as directory:
    for identifier, shape in candidate.items():
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(shape.volume - restored.volume) < .002, identifier
contacts = [('starter-motor-positive-feed', 'starter-solenoid-terminal-2'),
            ('starter-motor-positive-feed', 'starter-solenoid-terminal-nut-2'),
            ('starter-motor-ground-bridge', 'starter-brush-end-plate'),
            ('starter-motor-ground-bridge', 'starter-brush-plate-screw-1'),
            ('starter-motor-ground-bridge', 'starter-brush-plate-screw-2')]
for role in feed.PIGTAILS:
    identifier = 'starter-brush-pigtail-' + role
    target = 'starter-motor-positive-feed' if role.startswith('positive') else 'starter-motor-ground-bridge'
    contacts.extend([(identifier, target), (identifier, 'starter-brush-' + role[-1])])
contact_rows, contact_areas = [], []
for first, second in contacts:
    distance = shapes[first].distance_to(shapes[second])
    volume = overlap(shapes[first], shapes[second])
    contact_rows.append([first, second, distance, volume])
    assert distance < 1e-6 and volume < .001, contact_rows[-1]
    if first.startswith('starter-brush-pigtail-'):
        role = first.removeprefix('starter-brush-pigtail-')
        points = feed.PIGTAILS[role]
        direction = b.Vector(points[-1]) - b.Vector(points[-2]) if second.startswith('starter-brush-') else b.Vector(points[0]) - b.Vector(points[1])
        direction = direction.normalized()
    elif second == 'starter-solenoid-terminal-2':
        direction = b.Vector(1, 0, 0)
    else:
        direction = b.Vector(0, 0, -1 if second == 'starter-brush-end-plate' else 1)
    witness_area = overlap(b.Pos(*(direction * .001)) * shapes[first], shapes[second]) / .001
    assert witness_area > .02, (first, second, witness_area)
    contact_areas.append([first, second, witness_area])
print('CONTACTS', contact_rows, flush=True)
checks, failures = 0, []
for first, second in itertools.combinations(shapes, 2):
    if first not in candidate and second not in candidate or not near(shapes[first], shapes[second]):
        continue
    for left, right in ((first, second), (second, first)):
        checks += 1
        volume = overlap(shapes[left], shapes[right])
        if volume > .001:
            failures.append([left, right, volume])
print('CHECKS', checks, 'FAILURES', failures, flush=True)
moving = {'starter-drive-lever', 'starter-solenoid-plunger', 'starter-solenoid-clevis-pin', 'starter-drive-clutch', 'starter-drive-pinion', 'starter-solenoid-contact-rod', 'starter-solenoid-bridge-insulator', 'starter-solenoid-contact-bridge', 'starter-solenoid-return-spring'}
for index in range(1, 17):
    pose = dict(shapes)
    pose.update(switch.parts(index / 16))
    pose.update(linkage.parts(index / 16, baseline))
    pose.update(coil_candidate)
    pose.update(candidate)
    for first in candidate:
        for second in moving:
            if not near(pose[first], pose[second]):
                continue
            for left, right in ((first, second), (second, first)):
                checks += 1
                volume = overlap(pose[left], pose[right])
                if volume > .001:
                    failures.append([index / 16, left, right, volume])
    print('POSE', index / 16, 'CHECKS', checks, 'FAILURES', failures[-5:], flush=True)
dielectric = {'starter-brush-carrier', 'starter-commutator-insulator', 'starter-motor-feed-jacket', 'starter-motor-feed-grommet', 'starter-solenoid-winding-bobbin', 'starter-solenoid-bridge-insulator', 'starter-solenoid-s-terminal-insulator', 'starter-solenoid-end-cap'}
dielectric.update(identifier for identifier in shapes if identifier.startswith(('starter-brush-holder-', 'starter-solenoid-lead-insulation-')))
conductors = {'starter-motor-positive-feed', 'starter-motor-ground-bridge'} | {'starter-brush-pigtail-' + role for role in feed.PIGTAILS}
allowed = {frozenset(pair) for pair in contacts}
boxes = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
clearances = []
for first in conductors:
    minimum, nearest = math.inf, None
    for second in shapes:
        if first == second or second in dielectric or frozenset((first, second)) in allowed:
            continue
        first_box, second_box = boxes[first], boxes[second]
        lower_bound = math.sqrt(sum(max(getattr(second_box.min, axis) - getattr(first_box.max, axis), getattr(first_box.min, axis) - getattr(second_box.max, axis), 0) ** 2 for axis in 'XYZ'))
        if lower_bound >= minimum:
            continue
        distance = shapes[first].distance_to(shapes[second])
        if distance < minimum:
            minimum, nearest = distance, second
    clearances.append([first, nearest, minimum])
    assert minimum > .01, clearances[-1]
report = {'installed': False, 'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_motor_feed.py').read_bytes()).hexdigest(), 'parts': len(candidate), 'contacts': contact_rows, 'projected_contact_areas_mm2': contact_areas, 'directed_checks': checks, 'failures': failures, 'stroke_poses': 17, 'conductor_clearances': clearances,
          'boundary': 'Source-backed two-feed/two-ground comparison topology, provisional routing and brush clocking. STEP round trips and geometric attachment/clearance only; no brush-wear, winding topology, current, temperature or dielectric simulation.'}
(ROOT / 'inventory/engine/starter-motor-feed-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
