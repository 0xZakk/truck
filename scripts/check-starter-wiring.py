"""Isolated starter lead contacts and static/dynamic neighbor audit."""
from pathlib import Path
import hashlib
import itertools
import json
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
import starter_engagement as linkage
import starter_wiring as wiring


def overlap(first, second):
    common = first.intersect(second)
    return sum(solid.volume for solid in common.solids()) if common else 0


def near(first, second):
    first_box, second_box = first.bounding_box(), second.bounding_box()
    return all(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) > .0001 for axis in 'XYZ')


baseline = starter.parts()
assembly = {identifier: shape for identifier, shape in baseline.items() if identifier not in switch.REPLACED}
assembly.update(switch.parts())
assembly.update(linkage.parts(baseline=baseline))
candidate = wiring.parts()
assembly.update(candidate)
contacts = []
allowed = set()
for role, endpoints in wiring.CONTACTS.items():
    identifier = 'starter-solenoid-lead-' + role
    for endpoint in endpoints:
        volume = overlap(candidate[identifier], assembly[endpoint])
        assert volume > .001, (identifier, endpoint, volume)
        contacts.append([identifier, endpoint, volume])
        allowed.add(frozenset((identifier, endpoint)))
allowed.add(frozenset(('starter-solenoid-lead-pull-s', 'starter-solenoid-lead-hold-s')))
allowed.add(frozenset(('starter-solenoid-lead-insulation-pull-s', 'starter-solenoid-lead-insulation-hold-s')))
failures, checks = [], 0
minimum_clearance = None
conductive_targets = ['starter-solenoid-' + role for role in ('shell', 'fixed-pole', 'plunger', 'contact-rod', 'contact-bridge', 'terminal-1', 'terminal-2', 's-terminal', 'pull-winding', 'hold-winding')]
with tempfile.TemporaryDirectory(prefix='starter-wiring-') as directory:
    for identifier, shape in candidate.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, len(shape.solids()))
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(shape.volume - restored.volume) < .002, identifier
for index in range(17):
    shapes = dict(assembly)
    shapes.update(switch.parts(index / 16))
    shapes.update(linkage.parts(index / 16, baseline))
    shapes.update(candidate)
    for role in wiring.ROUTES:
        identifier = 'starter-solenoid-lead-' + role
        for target in conductive_targets:
            if frozenset((identifier, target)) in allowed:
                continue
            distance = shapes[identifier].distance_to(shapes[target])
            minimum_clearance = distance if minimum_clearance is None else min(minimum_clearance, distance)
            if distance < .01:
                failures.append([index / 16, identifier, target, 'conductive clearance', distance])
    for first, second in itertools.combinations(shapes, 2):
        if first not in candidate and second not in candidate:
            continue
        if frozenset((first, second)) in allowed or not near(shapes[first], shapes[second]):
            continue
        checks += 1
        volume = overlap(shapes[first], shapes[second])
        if volume > .001:
            failures.append([index / 16, first, second, volume])
    print('Pose', index / 16, 'checks', checks, 'failures', failures[-8:], flush=True)
report = {'installed': False, 'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_wiring.py').read_bytes()).hexdigest(),
          'candidate_parts': len(candidate), 'boolean_checks': checks, 'minimum_unintended_conductor_clearance_mm': minimum_clearance, 'contacts': contacts, 'failures': failures,
          'boundary': 'Four provisional aggregate coil attachments. Complete starter electrical continuity, winding turn geometry, electrical/thermal ratings and OEM routing are not claimed.'}
(ROOT / 'inventory/engine/starter-wiring-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS isolated starter coil-lead study', flush=True)
