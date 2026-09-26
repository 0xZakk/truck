"""Smoke real generators through both layout and motion callback adapters."""
from pathlib import Path
import json
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import distributor
import oil_pump
import oil_drive_layout as layout
import oil_pump_motion as motion
from assembly_math import transforms

shapes, occurrences = {}, []
assemblies = [{'id': 'engine', 'parent': None}]


def define(identifier, shape, *args):
    assert identifier not in shapes
    assert shape.is_valid and len(shape.solids()) == 1, identifier
    shapes[identifier] = shape


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
    occurrences.append({'id': identifier, 'definition': definition, 'parent': parent,
                        'position_cad_mm': pos, 'rotation_cad_deg': rotation})


def group(identifier, name, parent='engine', motion=None, position=(0, 0, 0), rotation=(0, 0, 0)):
    assert identifier not in {assembly['id'] for assembly in assemblies}
    assert parent in {assembly['id'] for assembly in assemblies}
    assemblies.append({'id': identifier, 'parent': parent, 'motion': motion,
                       'position_cad_mm': position, 'rotation_cad_deg': rotation})


def cylinder_x(radius, width):
    return b.Rot(0, 90, 0) * b.Cylinder(radius, width)


def spring(radius, wire, height, turns):
    path = b.Helix(height / turns, height, radius)
    return b.sweep(b.Plane(origin=path @ 0, z_dir=path % 0) * b.Circle(wire), path=path)


distributor.build(layout.distributor_api((define, add, group)))
oil_pump.build(layout.pump_api(motion.pump_api((define, add, group, cylinder_x, spring))))
layout.build(motion.drive_api((define, add, group)))
assert len({occurrence['id'] for occurrence in occurrences}) == len(occurrences)
assert all(occurrence['parent'] in {assembly['id'] for assembly in assemblies} for occurrence in occurrences)
manifest = {'assemblies': assemblies, 'occurrences': occurrences, 'mechanism': {'stroke_mm': 98, 'rod_length_mm': 170}}
for crank_angle in range(0, 721, 15):
    locations = transforms(manifest, crank_angle)
    inner_pose, outer_pose = motion.rotor_poses(crank_angle)
    expected = {
        'oil-pump-inner-rotor': layout.PUMP_FRAME * inner_pose,
        'oil-pump-outer-rotor': layout.PUMP_FRAME * outer_pose,
        'oil-pump-rotor-shaft': layout.PUMP_FRAME * b.Pos(3.5, 0, 5) * b.Rot(0, 0, -crank_angle / 2),
        'oil-pump-intermediate-shaft': layout.GEAR_FRAME * b.Rot(0, 0, -crank_angle / 2) * b.Pos(0, 0, layout.INTERMEDIATE_BOTTOM),
        'oil-pump-drive-retainer': layout.GEAR_FRAME * b.Rot(0, 0, -crank_angle / 2) * b.Pos(0, 0, layout.INTERMEDIATE_BOTTOM),
    }
    for identifier, frame in expected.items():
        for point in [(0, 0, 0), (5, 0, 0), (0, 5, 0), (0, 0, 5)]:
            assert ((locations[identifier] * b.Vertex(*point)).center() - (frame * b.Vertex(*point)).center()).length < 1e-7, (identifier, crank_angle)
report = {'status': 'pass', 'definitions': len(shapes), 'occurrences': len(occurrences), 'assemblies': len(assemblies),
          'transform_poses': 49, 'unique_ids': True, 'valid_single_solids': True,
          'scope': 'Real callback builds and shared CAD rotary transforms; no installed manifest or assets changed.'}
(ROOT / 'inventory/engine/oil-pump-motion-adapter-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
