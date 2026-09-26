"""Verify candidate API transforms and independently modeled accessory clearance."""
import hashlib
import json
from pathlib import Path
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import water_pump_pulley
import tensioner_arm
import tensioner_pulley
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_raw = manifest_path.read_bytes()
manifest = json.loads(manifest_raw)
manifest['assemblies'] = [entry for entry in manifest['assemblies']
                          if entry['id'] != 'water-pump-pulley-assembly']
definitions = {}
occurrences = []


def define(identifier, shape, *metadata):
    definitions[identifier] = shape


def group(identifier, name, parent='engine', motion=None, position=(0, 0, 0)):
    manifest['assemblies'].append({'id': identifier, 'name': name, 'parent': parent,
                                   'position_cad_mm': position, 'motion': motion})


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0)):
    occurrences.append({'id': identifier, 'definition': definition, 'parent': parent,
                        'position_cad_mm': pos, 'rotation_cad_deg': rotation})


water_pump_pulley.build((define, add, group))
manifest['occurrences'] = occurrences
poses = transforms(manifest)
candidate = water_pump_pulley.parts()
transform_checks = []
for occurrence in occurrences:
    actual = definitions[occurrence['definition']].moved(poses[occurrence['id']])
    expected = candidate[occurrence['id']]
    intersection = actual.intersect(expected)
    common_volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
    assert abs(common_volume - expected.volume) < .01, occurrence['id']
    assert abs(actual.volume - expected.volume) < .01, occurrence['id']
    transform_checks.append(occurrence['id'])

neighbors = {**tensioner_arm.parts(), **tensioner_pulley.parts()}
collisions = []
for part_id, shape in candidate.items():
    for neighbor_id, neighbor in neighbors.items():
        intersection = shape.intersect(neighbor)
        volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
        if volume > .01:
            collisions.append({'a': part_id, 'b': neighbor_id, 'volume_mm3': volume})

assert manifest_path.read_bytes() == manifest_raw
report = {
    'manifest_sha256': hashlib.sha256(manifest_raw).hexdigest(),
    'source_sha256': {module.__name__: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
                      for module in (water_pump_pulley, tensioner_arm, tensioner_pulley)},
    'api_world_transform_checks': transform_checks,
    'cross_candidate_pairs': len(candidate) * len(neighbors),
    'collisions': collisions,
    'verified_production_fit': False,
    'unresolved_belt_alignment': {
        'water_pump_belt_center_x': water_pump_pulley.BELT_CENTER_X,
        'tensioner_envelope_center_x': tensioner_pulley.POSITION[0],
        'center_delta_mm': water_pump_pulley.BELT_CENTER_X - tensioner_pulley.POSITION[0],
        'meaning': 'Illustrative axial centers are reconciled; actual belt tracking, usable pulley face width and production datums remain unverified.'
    }
}
(ROOT / 'inventory/engine/water-pump-pulley-interface-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
