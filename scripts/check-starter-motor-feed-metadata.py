"""Motor-feed adapter, learning links and exploded separation composition check."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
import starter_explanations as explanations
import starter_engagement as linkage
import starter_wiring as coil
import starter_wiring_fit_metadata as coil_fit
import starter_motor_feed as feed
import starter_motor_feed_metadata as overlay

definitions, occurrences = {}, {}


def define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs):
    assert identifier not in definitions, identifier
    definitions[identifier] = {'shape': shape, 'function': function, 'gaps': gaps}


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
    assert identifier not in occurrences and tuple(pos) == tuple(rotation) == (0, 0, 0), identifier
    occurrences[identifier] = {'definition': definition, 'parent': parent, 'explode': explode}


def group(*args, **kwargs):
    return None


wrapped = coil.api(coil_fit.api(overlay.api((define, add, group))))
starter.build(explanations.api(switch.api(linkage.api(wrapped))))
switch.build(explanations.solenoid_api(wrapped))
coil.build(explanations.wiring_api(wrapped))
overlay.build(wrapped)
assert len(definitions) == len(occurrences) == 132
expected = feed.parts()
for identifier, shape in expected.items():
    actual = definitions[identifier]['shape']
    assert abs(actual.volume - shape.volume) < 1e-7, identifier
    common = actual.intersect(shape)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    assert abs(actual.volume + shape.volume - 2 * volume) < .002, identifier
for identifier, metadata in definitions.items():
    assert coil.GAPS[2] not in metadata['gaps'], identifier
new_parts = set(expected) - feed.REPLACED
assert len(new_parts) == 8
assert all(occurrences[identifier]['parent'] == 'starter-motor-assembly' for identifier in new_parts)
lessons = json.loads((ROOT / 'inventory/engine/starter-motor-feed-learning.json').read_text())
for lesson in lessons.values():
    for step in lesson['steps'] + lesson['troubleshooting']:
        assert step['part'] in definitions or step['part'].endswith('-assembly'), step
checks = 0
for fraction in (.6, 1):
    posed = {identifier: b.Pos(*(value * fraction for value in occurrences[identifier]['explode'])) * metadata['shape'] for identifier, metadata in definitions.items()}
    boxes = {identifier: shape.bounding_box() for identifier, shape in posed.items()}
    for first in new_parts:
        for second in posed:
            if first == second:
                continue
            first_box, second_box = boxes[first], boxes[second]
            if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
                continue
            checks += 1
            common = posed[first].intersect(posed[second])
            volume = sum(solid.volume for solid in common.solids()) if common else 0
            assert volume < .01, (fraction, first, second, volume)
report = {'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_motor_feed.py').read_bytes()).hexdigest(), 'adapter_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_motor_feed_metadata.py').read_bytes()).hexdigest(), 'parts': 132, 'new_parts': 8, 'shape_overrides': 14, 'learning_targets_valid': True, 'stale_motor_feed_absence_removed': True, 'explosion_fractions': [.6, 1], 'explosion_exact_checks': checks, 'passed': True}
(ROOT / 'inventory/engine/starter-motor-feed-metadata-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
