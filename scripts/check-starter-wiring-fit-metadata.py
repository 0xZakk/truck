"""Check the fitted wiring adapter through the accepted starter build pipeline."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
import starter_explanations as explanations
import starter_wiring as accepted
import starter_wiring_fit as fitted
import starter_wiring_fit_metadata as overlay

definitions, occurrences = {}, {}


def define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs):
    assert identifier not in definitions, identifier
    definitions[identifier] = {'shape': shape, 'function': function, 'gaps': gaps}


def add(identifier, definition, parent, *args, **kwargs):
    assert identifier not in occurrences, identifier
    occurrences[identifier] = definition


def group(*args, **kwargs):
    return None


wrapped = accepted.api(overlay.api((define, add, group)))
starter.build(explanations.api(switch.api(wrapped)))
switch.build(explanations.solenoid_api(wrapped))
accepted.build(wrapped)
assert len(definitions) == len(occurrences) == 124
expected = fitted.parts()
for identifier, shape in expected.items():
    actual = definitions[identifier]['shape']
    assert abs(actual.volume - shape.volume) < 1e-7, identifier
    common = actual.intersect(shape)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    assert abs(actual.volume + shape.volume - 2 * volume) < .002, identifier
    assert overlay.GAPS[0] in definitions[identifier]['gaps'], identifier
lesson = json.loads((ROOT / 'inventory/engine/starter-wiring-fit-learning.json').read_text())['starter-solenoid-assembly']
for step in lesson['steps'] + lesson['troubleshooting']:
    assert step['part'] in definitions, step
report = {'geometry_source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_wiring_fit.py').read_bytes()).hexdigest(),
          'adapter_source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_wiring_fit_metadata.py').read_bytes()).hexdigest(),
          'definitions': len(definitions), 'occurrences': len(occurrences), 'all_ten_shape_overrides_match': True, 'learning_targets_valid': True}
(ROOT / 'inventory/engine/starter-wiring-fit-metadata-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
