"""Isolated switch packaging and contact checks; excludes lever articulation."""
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


def volume(first, second):
    common = first.intersect(second)
    return sum(solid.volume for solid in common.solids()) if common else 0


def near(first, second):
    first_box, second_box = first.bounding_box(), second.bounding_box()
    return all(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
               max(getattr(first_box.min, axis), getattr(second_box.min, axis)) > .001 for axis in 'XYZ')


baseline = starter.parts()
candidate = switch.parts()
failures, samples = [], []
with tempfile.TemporaryDirectory(prefix='starter-switch-') as directory:
    for identifier, shape in candidate.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .002, identifier
print('STEP', len(candidate), 'PASS', flush=True)
assembly = {identifier: shape for identifier, shape in baseline.items() if identifier not in switch.REPLACED}
assembly.update(candidate)
checks = 0
for first, second in itertools.combinations(assembly, 2):
    if first not in candidate and second not in candidate:
        continue
    if not near(assembly[first], assembly[second]):
        continue
    checks += 1
    overlap = volume(assembly[first], assembly[second])
    if overlap > .02:
        failures.append([first, second, overlap])
print('Rest packaging', checks, failures, flush=True)
moving_ids = ['starter-solenoid-contact-rod', 'starter-solenoid-bridge-insulator',
              'starter-solenoid-contact-bridge', 'starter-solenoid-return-spring']
for index in range(17):
    fraction = index / 16
    posed = switch.parts(fraction)
    assert all(shape.is_valid and len(shape.solids()) == 1 for shape in posed.values()), fraction
    assert (13.5 - switch.STROKE * fraction) / 4 > .5, 'Spring turns overlap'
    posed['starter-solenoid-plunger'] = b.Pos(0, 0, -switch.STROKE * fraction) * baseline['starter-solenoid-plunger']
    all_shapes = dict(posed)
    all_shapes['starter-solenoid-shell'] = baseline['starter-solenoid-shell']
    all_shapes['starter-solenoid-front-seat'] = baseline['starter-solenoid-front-seat']
    for first, second in itertools.combinations(all_shapes, 2):
        if first not in moving_ids + ['starter-solenoid-plunger'] and second not in moving_ids + ['starter-solenoid-plunger']:
            continue
        if near(all_shapes[first], all_shapes[second]):
            overlap = volume(all_shapes[first], all_shapes[second])
            if overlap > .02:
                failures.append([fraction, first, second, overlap])
    gaps = [posed['starter-solenoid-contact-bridge'].distance_to(posed[f'starter-solenoid-terminal-{station}']) for station in (1, 2)]
    expected = switch.STROKE * (1 - fraction)
    assert all(abs(gap - expected) < 1e-5 for gap in gaps), (fraction, gaps, expected)
    rod_gap = posed['starter-solenoid-contact-rod'].distance_to(posed['starter-solenoid-contact-bridge'])
    assert rod_gap > .04, 'Uninsulated bridge/rod contact'
    samples.append({'fraction': fraction, 'contact_gaps_mm': gaps, 'rod_bridge_gap_mm': rod_gap,
                    'spring_turn_gap_mm': (13.5 - switch.STROKE * fraction) / 4 - .5})
assert switch.circuit()['physical_wiring_complete'] is False
assert len(switch.circuit()['edges']) == 2 and len(switch.circuit(True)['edges']) == 3
report = {'installed': False, 'parts': len(candidate), 'resulting_starter_parts': len(assembly),
          'rest_boolean_checks': checks, 'failures': failures, 'switch_samples': samples,
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_solenoid.py').read_bytes()).hexdigest(),
          'boundary': 'No lever/clevis/fork articulation, coil lead continuity, electromagnetic or pressure/contact force validation.'}
(ROOT / 'inventory/engine/starter-solenoid-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS switch STEP, rest packaging,17 contact strokes,logical topology', flush=True)
