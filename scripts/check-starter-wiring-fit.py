"""Nonpenetrating starter coil interfaces and sampled clearance validation."""
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
import starter_wiring_fit as wiring


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
contacts, allowed = [], set()
for role, endpoints in wiring.CONTACTS.items():
    identifier = 'starter-solenoid-lead-' + role
    for index, endpoint in enumerate(endpoints):
        shape, target = candidate[identifier], assembly[endpoint]
        distance = shape.distance_to(target)
        volume = overlap(shape, target)
        direction = b.Vector(wiring.ROUTES[role][0]) - b.Vector(wiring.ROUTES[role][1]) if index == 0 else b.Vector(wiring.ROUTES[role][-1]) - b.Vector(wiring.ROUTES[role][-2])
        direction = direction.normalized()
        witness = b.Pos(*(direction * .001)) * shape
        projected_area = overlap(witness, target) / .001
        assert distance < 1e-6 and volume < 1e-5 and projected_area > .02, (identifier, endpoint, distance, volume, projected_area)
        contacts.append({'lead': identifier, 'target': endpoint, 'distance_mm': distance, 'overlap_mm3': volume, 'projected_contact_area_mm2': projected_area})
        allowed.add(frozenset((identifier, endpoint)))
print('Eight nonpenetrating face attachments PASS', contacts, flush=True)
with tempfile.TemporaryDirectory(prefix='starter-wiring-fit-') as directory:
    for identifier, shape in candidate.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, len(shape.solids()))
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(shape.volume - restored.volume) < .002, identifier
failures, checks, minimum_clearance = [], 0, None
conductive_targets = ['starter-solenoid-' + role for role in ('shell', 'fixed-pole', 'plunger', 'contact-rod', 'contact-bridge', 'terminal-1', 'terminal-2', 's-terminal', 'pull-winding', 'hold-winding')]
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
        if first not in candidate and second not in candidate or not near(shapes[first], shapes[second]):
            continue
        checks += 1
        volume = overlap(shapes[first], shapes[second])
        if volume > .001:
            failures.append([index / 16, first, second, volume])
    print('Pose', index / 16, 'checks', checks, 'failures', failures[-8:], flush=True)
s_lead_gap = candidate['starter-solenoid-lead-pull-s'].distance_to(candidate['starter-solenoid-lead-hold-s'])
s_sleeve_gap = candidate['starter-solenoid-lead-insulation-pull-s'].distance_to(candidate['starter-solenoid-lead-insulation-hold-s'])
assert s_lead_gap > .1 and s_sleeve_gap > .1, (s_lead_gap, s_sleeve_gap)
report = {'installed': False, 'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_wiring_fit.py').read_bytes()).hexdigest(),
          'candidate_parts': len(candidate), 'boolean_checks': checks, 'contacts': contacts, 'failures': failures,
          'minimum_unintended_conductor_clearance_mm': minimum_clearance, 'separate_s_lead_gap_mm': s_lead_gap, 'separate_s_sleeve_gap_mm': s_sleeve_gap,
          'contact_area_method': 'A 0.001 mm witness translation along each attachment direction estimates projected contact area from common volume divided by travel. Nominal solids themselves have zero-distance interfaces and no positive-volume overlap.',
          'boundary': 'Provisional four coil-end attachment geometry only; no production routing, joint process, ampacity, dielectric strength or complete starter circuit is established.'}
(ROOT / 'inventory/engine/starter-wiring-fit-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS separate nonpenetrating starter leads', flush=True)
