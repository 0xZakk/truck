"""Isolated conjugate rotor and continuous drive-interface checks."""
from pathlib import Path
import hashlib
import json
import math
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import oil_pump_motion as motion
import oil_drive_layout as layout
import oil_pump_drive as drive

inner, outer = motion.inner_rotor(), motion.outer_rotor()
original_shaft = b.Cylinder(4.75, 42) - b.Pos(0, 0, 20) * b.extrude(b.RegularPolygon(3, 6), amount=9, both=True)
pump_shaft = motion.shaft_interface(layout.rotor_shaft_interface(original_shaft))
original_distributor = b.Pos(0, 0, -11.5) * b.Cylinder(5.9, 183) + b.Pos(0, 0, 59.5) * b.Cylinder(12, 1)
distributor = layout.distributor_shaft_interface(original_distributor)
intermediate, retainer = drive.shaft(), drive.retainer()
shapes = {'inner': inner, 'outer': outer, 'pump-shaft': pump_shaft,
          'distributor-shaft': distributor, 'intermediate': intermediate, 'retainer': retainer}
with tempfile.TemporaryDirectory(prefix='oil-pump-motion-') as directory:
    for identifier, shape in shapes.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        target = Path(directory) / (identifier + '.step')
        b.export_step(shape, target)
        restored = b.import_step(target)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .001, identifier


def overlap_volume(first, second):
    overlap = first.intersect(second)
    return sum(solid.volume for solid in overlap.solids()) if overlap else 0


samples = []
for crank_angle in range(0, 721, 10):
    inner_pose, outer_pose = motion.rotor_poses(crank_angle)
    inner_world, outer_world = inner_pose * inner, outer_pose * outer
    spin = b.Rot(0, 0, -crank_angle / 2)
    shaft_world = b.Pos(3.5, 0, 5) * spin * pump_shaft
    intermediate_world = b.Pos(3.5, 0, 17) * spin * intermediate
    ring_world = b.Pos(3.5, 0, 17) * spin * retainer
    distributor_world = b.Pos(3.5, 0, 17 - layout.INTERMEDIATE_BOTTOM + 85) * spin * distributor
    checks = {
        'rotors': overlap_volume(inner_world, outer_world),
        'inner-shaft': overlap_volume(inner_world, shaft_world),
        'lower-socket': overlap_volume(intermediate_world, shaft_world),
        'upper-socket': overlap_volume(intermediate_world, distributor_world),
        'retainer': overlap_volume(intermediate_world, ring_world),
    }
    assert max(checks.values()) < .001, (crank_angle, checks)
    clearance = inner_world.distance_to(outer_world)
    assert .024 < clearance < .026, (crank_angle, clearance)
    upper_engagement = (intermediate_world & b.Pos(3.5, 0, 17 + drive.LENGTH - 5) * b.Cylinder(6, 10)).volume
    lower_engagement = (intermediate_world & b.Pos(3.5, 0, 21.5) * b.Cylinder(6, 9)).volume
    assert upper_engagement > 500 and lower_engagement > 450
    samples.append({'crank_degrees': crank_angle, 'overlaps_mm3': checks,
                    'rotor_clearance_mm': clearance, 'upper_insert_volume_mm3': upper_engagement,
                    'lower_insert_volume_mm3': lower_engagement})
    print('Motion sample', crank_angle, 'PASS', flush=True)

cam, gear = layout.helical_gear(12, 2.5), layout.helical_gear(12, 11.25)
gear_samples = []
for index in range(17):
    angle = index * 22.5 / 16
    cam_world = b.Pos(layout.DRIVE_X, 90, 72) * b.Rot(-angle, 0, 0) * b.Rot(0, 90, 0) * cam
    gear_world = layout.GEAR_FRAME * b.Rot(0, 0, -angle) * gear
    overlap = overlap_volume(cam_world, gear_world)
    assert overlap < .001
    gear_samples.append({'shaft_degrees': angle, 'overlap_mm3': overlap, 'clearance_mm': cam_world.distance_to(gear_world)})

report = {'installed': False, 'source_sha256': hashlib.sha256((ROOT / 'cad/engine/oil_pump_motion.py').read_bytes()).hexdigest(),
          'valid_step_solids': list(shapes), 'motion_samples': samples, 'gear_samples': gear_samples,
          'continuous_socket_reason': 'Every socket and its engaged hex rotate by the same angle about the same axis. Their relative rigid transform and axial insertion are invariant for all crank angles; sampled Boolean checks additionally verify the modeled pose.',
          'shaft_length_mm': drive.LENGTH, 'shaft_across_flats_mm': drive.ACROSS_FLATS,
          'scope': 'Isolated rotor/drive geometry only. No installed neighbor or hydraulic validation.'}
(ROOT / 'inventory/engine/oil-pump-motion-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS isolated motion, sockets, gerotor, gears, STEP', flush=True)
