"""Isolated PMGR decomposition, reducer, and manual-flywheel engagement study."""
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
import flywheel

parts = starter.parts()
invalid, collisions = [], []
checks = 0
with tempfile.TemporaryDirectory(prefix='starter-internal-') as directory:
    for identifier, shape in parts.items():
        if not hasattr(shape, 'is_valid') or not shape.is_valid or len(shape.solids()) != 1:
            invalid.append(identifier)
            continue
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        if not restored.is_valid or len(restored.solids()) != 1 or abs(restored.volume - shape.volume) > .002:
            invalid.append(identifier)
print('STEP', len(parts), 'invalid', invalid, flush=True)
assert not invalid, invalid
boxes = {identifier: shape.bounding_box() for identifier, shape in parts.items()}


def overlap(first, second):
    common = first.intersect(second)
    return sum(solid.volume for solid in common.solids()) if common else 0


for first, second in itertools.combinations(parts, 2):
    first_box, second_box = boxes[first], boxes[second]
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
        continue
    checks += 1
    volume = overlap(parts[first], parts[second])
    if volume > .05:
        collisions.append({'first': first, 'second': second, 'volume_mm3': volume})
print('Internal', checks, 'collisions', collisions, flush=True)

reducer_samples = []
sun, fixed_ring = starter.gear(12, 1, -46, -34, 2.05), parts['starter-stationary-gear']
planet = starter.gear(18, 1, -46, -34, 3.05, phase=10)
for motor_angle in range(0, 91, 3):
    rotating_sun = b.Rot(0, 0, motor_angle) * sun
    overlaps = []
    for index in range(3):
        moving_planet = b.Rot(0, 0, index * 120 + motor_angle / 5) * b.Pos(15, 0, 0) * b.Rot(0, 0, -8 * motor_angle / 15) * planet
        overlaps += [overlap(rotating_sun, moving_planet), overlap(fixed_ring, moving_planet)]
    reducer_samples.append({'motor_degrees': motor_angle, 'max_overlap_mm3': max(overlaps)})
    assert max(overlaps) < .05, reducer_samples[-1]
print('Reducer31poses PASS', flush=True)

flywheel_ring = flywheel.ring_gear()
engaged_pinion = starter.pinion(True)
mesh_samples = []
for index in range(17):
    crank_angle = index * 360 / 164 / 16
    ring_world = b.Rot(crank_angle, 0, 0) * flywheel.MOUNT * flywheel_ring
    pinion_world = starter.FRAME * b.Rot(0, 0, crank_angle * 16.4) * engaged_pinion
    volume = overlap(ring_world, pinion_world)
    mesh_samples.append({'crank_degrees': crank_angle, 'overlap_mm3': volume,
                         'clearance_mm': ring_world.distance_to(pinion_world)})
    assert volume < .05, mesh_samples[-1]
print('Manual-flywheel17meshposes PASS', flush=True)

engaged = starter.parts(True)
for identifier in ('starter-drive-clutch', 'starter-drive-pinion'):
    for second in parts:
        if second in ('starter-drive-clutch', 'starter-drive-pinion'):
            continue
        volume = overlap(engaged[identifier], parts[second])
        if volume > .05:
            collisions.append({'state': 'engaged-drive-only', 'first': identifier, 'second': second, 'volume_mm3': volume})
report = {'installed': False, 'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_motor.py').read_bytes()).hexdigest(),
          'parts': len(parts), 'invalid': invalid, 'static_boolean_checks': checks, 'collisions': collisions,
          'reducer_samples': reducer_samples, 'flywheel_mesh_samples': mesh_samples,
          'pinion_teeth': starter.PINION_TEETH, 'pinion_catalog_od_mm': starter.PINION_OD,
          'rest_axial_gap_to_ring_mm': 3.525, 'engaged_axial_overlap_mm': 8.475,
          'boundary': 'Manual fit-study datums only; bellhousing/index plate not modeled. No claim of production mounting, electrical operation or validated lever articulation.'}
(ROOT / 'inventory/engine/starter-motor-internal-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not collisions, collisions
print('PASS starter isolated audit', flush=True)
