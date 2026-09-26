"""Exercise the real build callbacks without publishing geometry or a manifest."""
from pathlib import Path
import json
import hashlib
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import distributor
import oil_pump
import oil_drive_layout as layout
from assembly_math import transforms

shapes = {}
assemblies = [{'id': 'engine', 'parent': None, 'position_cad_mm': [0, 0, 0]}]
occurrences = []


def define(identifier, shape, name, function, system, color, sources, gaps, claims=()):
    assert identifier not in shapes, identifier
    assert shape.is_valid and len(shape.solids()) == 1, identifier
    shapes[identifier] = shape


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
    occurrences.append({'id': identifier, 'definition': definition, 'parent': parent,
                        'position_cad_mm': pos, 'rotation_cad_deg': rotation})


def group(identifier, name, parent='engine', motion=None, position=(0, 0, 0), rotation=(0, 0, 0)):
    assemblies.append({'id': identifier, 'parent': parent, 'motion': motion,
                       'position_cad_mm': position, 'rotation_cad_deg': rotation})


def cylinder_x(radius, width):
    return b.Rot(0, 90, 0) * b.Cylinder(radius, width)


def spring(radius, wire, height, turns):
    path = b.Helix(height / turns, height, radius)
    return b.sweep(b.Plane(origin=path @ 0, z_dir=path % 0) * b.Circle(wire), path=path)


distributor.build(layout.distributor_api((define, add, group)))
oil_pump.build(layout.pump_api((define, add, group, cylinder_x, spring)))
layout.build((define, add, group))
assert len({assembly['id'] for assembly in assemblies}) == len(assemblies)
assert len({occurrence['id'] for occurrence in occurrences}) == len(occurrences)
groups = {assembly['id'] for assembly in assemblies}
assert all(occurrence['parent'] in groups and occurrence['definition'] in shapes for occurrence in occurrences)
manifest = {'assemblies': assemblies, 'occurrences': occurrences,
            'mechanism': {'stroke_mm': 98, 'rod_length_mm': 170}}
positions = transforms(manifest)
shaft = positions['oil-pump-intermediate-shaft'] * shapes['oil-pump-intermediate-shaft']
expected = layout.GEAR_FRAME * b.Pos(0, 0, layout.INTERMEDIATE_BOTTOM) * layout.intermediate_shaft()
assert (shaft.center() - expected.center()).length < 1e-6
report = {'status': 'pass', 'definitions': len(shapes), 'occurrences': len(occurrences),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/oil_drive_layout.py').read_bytes()).hexdigest(),
          'assemblies': len(assemblies), 'real_generator_callbacks': ['distributor.build', 'oil_pump.build', 'oil_drive_layout.build'],
          'group_rotations': 'pass', 'unique_ids': 'pass', 'valid_single_solids': 'pass',
          'scope': 'Read-only callback and hierarchy smoke test. No generated assets or shared manifest written.'}
(ROOT / 'inventory/engine/oil-drive-adapter-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
