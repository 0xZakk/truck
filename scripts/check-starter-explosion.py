"""Check new solenoid internals separate visibly at the offline preview settings."""
from pathlib import Path
import sys
import hashlib
import json
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor
import starter_solenoid
import starter_explanations
import starter_engagement
import starter_wiring
import starter_wiring_fit_metadata
import starter_motor_feed
import starter_motor_feed_metadata

shapes, offsets = {}, {}


def define(identifier, shape, *metadata):
    shapes[identifier] = shape


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
    assert tuple(pos) == (0, 0, 0) and tuple(rotation) == (0, 0, 0)
    offsets[identifier] = explode


def group(*arguments, **keywords):
    pass


base = define, add, group
base = starter_wiring.api(starter_wiring_fit_metadata.api(starter_motor_feed_metadata.api(base)))
starter_motor.build(starter_explanations.api(starter_solenoid.api(starter_engagement.api(base))))
starter_solenoid.build(starter_explanations.solenoid_api(base))
starter_wiring.build(starter_explanations.wiring_api(base))
starter_motor_feed_metadata.build(base)
new_parts = set(starter_solenoid.parts()) - starter_solenoid.REPLACED
new_parts.update(set(starter_wiring.parts()) - starter_wiring.REPLACED)
new_parts.update(set(starter_motor_feed.parts()) - starter_motor_feed.REPLACED)
assert len(shapes) == len(offsets) == 132 and len(new_parts) == 25
manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
if '--installed' in sys.argv:
    manifest = json.loads(manifest_bytes)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    installed = {entry['id']: entry for entry in manifest['occurrences'] if entry['id'] in shapes}
    assert len(installed) == 132
    for identifier, occurrence in installed.items():
        assert occurrence['position_cad_mm'] == [0, 0, 0]
        assert occurrence['rotation_cad_deg'] == [0, 0, 0]
        shapes[identifier] = cad.import_step(ROOT / definitions[occurrence['definition']]['step'].lstrip('/'))
        offsets[identifier] = occurrence['explode_cad_mm']
checks = 0
for fraction in (.6, 1):
    posed = {identifier: cad.Pos(*(value * fraction for value in offsets[identifier])) * shape
             for identifier, shape in shapes.items()}
    bounds = {identifier: shape.bounding_box() for identifier, shape in posed.items()}
    for first in new_parts:
        for second in posed:
            if first == second:
                continue
            first_box, second_box = bounds[first], bounds[second]
            if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis))
                   - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
                continue
            common = posed[first].intersect(posed[second])
            volume = sum(solid.volume for solid in common.solids()) if common else 0
            checks += 1
            assert volume < .01, (fraction, first, second, volume)
assert manifest_path.read_bytes() == manifest_bytes
report = {'installed': '--installed' in sys.argv, 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
          'parts': len(shapes), 'target_parts': len(new_parts), 'fractions': [.6, 1], 'exact_checks': checks, 'passed': True}
(ROOT / 'inventory/engine/starter-explosion-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(f'Twenty-five wiring/solenoid additions separate at60/100percent explosion; {checks} exact checks PASS')
