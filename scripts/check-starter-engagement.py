"""Candidate full-stroke rigid linkage and casing-clearance validation."""
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


def overlap(first, second):
    common = first.intersect(second)
    return sum(solid.volume for solid in common.solids()) if common else 0


def near(first, second):
    first_box, second_box = first.bounding_box(), second.bounding_box()
    return all(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
               max(getattr(first_box.min, axis), getattr(second_box.min, axis)) > .001 for axis in 'XYZ')


baseline = starter.parts()
assembly = {identifier: shape for identifier, shape in baseline.items() if identifier not in switch.REPLACED}
assembly.update(switch.parts())
candidate = linkage.parts(baseline=baseline)
with tempfile.TemporaryDirectory(prefix='starter-linkage-') as directory:
    for identifier, shape in candidate.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, len(shape.solids()))
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .002, identifier
print('STEP8 PASS', flush=True)
failures, samples = [], []
static = dict(assembly)
static.update(candidate)
moving = {'starter-drive-lever', 'starter-solenoid-plunger', 'starter-solenoid-clevis-pin',
          'starter-drive-clutch', 'starter-drive-pinion', 'starter-solenoid-contact-rod',
          'starter-solenoid-bridge-insulator', 'starter-solenoid-contact-bridge', 'starter-solenoid-return-spring'}
checks = 0
for index in range(17):
    fraction = index / 16
    shapes = dict(static)
    shapes.update(switch.parts(fraction))
    shapes.update(linkage.parts(fraction, baseline))
    for first, second in itertools.combinations(shapes, 2):
        relevant = moving if index else moving | linkage.REPLACED
        if first not in relevant and second not in relevant:
            continue
        if not near(shapes[first], shapes[second]):
            continue
        checks += 1
        volume = overlap(shapes[first], shapes[second])
        if volume > .02:
            failures.append([fraction, first, second, volume])
    coordinates = linkage.pose(fraction)
    pin_center = b.Vertex(0, -62, -16).moved(linkage.lever_location(fraction)).center()
    pad_center = b.Vertex(18.5, 0, -16).moved(linkage.lever_location(fraction)).center()
    assert abs(pin_center.Z - (-16 - coordinates['plunger_mm'])) < 1e-8
    assert abs(pin_center.Y - (-62 + coordinates['upper_pin_slide_mm'])) < 1e-8
    assert abs(pad_center.Z - (-16 + coordinates['drive_mm'])) < 1e-8
    gap = shapes['starter-drive-lever'].distance_to(shapes['starter-drive-clutch'])
    assert gap < 1e-5, (fraction, gap)
    samples.append(dict(coordinates, fraction=fraction, fork_clutch_gap_mm=gap))
    print('Pose', fraction, 'checks', checks, 'failures', failures[-5:], flush=True)
reset = linkage.parts(0, baseline)
for identifier, expected in candidate.items():
    assert abs(reset[identifier].volume - expected.volume) < 1e-7
    assert abs(overlap(reset[identifier], expected) - expected.volume) < .002, identifier
report = {'installed': False, 'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_engagement.py').read_bytes()).hexdigest(),
          'boolean_checks': checks, 'failures': failures, 'samples': samples,
          'boundary': 'Reversible prescribed geometry, not dynamics or tooth-blocking simulation. All new linkage dimensions and sliding-joint construction are provisional.'}
(ROOT / 'inventory/engine/starter-engagement-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS full-stroke starter linkage', flush=True)
