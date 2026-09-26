"""Check exported fan placements and parallel alternator candidate clearance."""
import hashlib
import json
from pathlib import Path
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import fan_clutch
import alternator
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
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


fan_clutch.build((define, add, group))
manifest['occurrences'] = occurrences
poses = transforms(manifest)
expected = {identifier: b.Pos(*fan_clutch.POSITION) * b.Pos(*position) * b.Rot(*rotation) * definitions[definition]
            for identifier, definition, position, rotation in fan_clutch.placements()}
for occurrence in occurrences:
    actual = definitions[occurrence['definition']].moved(poses[occurrence['id']])
    target = expected[occurrence['id']]
    common = actual.intersect(target)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    assert abs(volume - target.volume) < .02, occurrence['id']

neighbors = alternator.parts()
bounds = {identifier: shape.bounding_box() for identifier, shape in {**expected, **neighbors}.items()}
collisions = []
exact_checks = 0
for identifier, shape in expected.items():
    for neighbor_id, neighbor in neighbors.items():
        first, second = bounds[identifier], bounds[neighbor_id]
        if any(min(getattr(first.max, axis), getattr(second.max, axis)) -
               max(getattr(first.min, axis), getattr(second.min, axis)) <= .01 for axis in 'XYZ'):
            continue
        exact_checks += 1
        common = shape.intersect(neighbor)
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        if volume > .01:
            collisions.append({'a': identifier, 'b': neighbor_id, 'volume_mm3': volume})

assert raw == manifest_path.read_bytes()
axial_gap = min(bounds[identifier].min.X for identifier in expected) - max(bounds[identifier].max.X for identifier in neighbors)
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': {module.__name__: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
                            for module in (fan_clutch, alternator)},
          'api_transform_checks': len(occurrences), 'cross_candidate_pairs': len(expected) * len(neighbors),
          'exact_checks_after_aabb': exact_checks, 'collisions': collisions,
          'alternator_position': alternator.POSITION, 'verified_production_fit': False,
          'minimum_axial_gap_mm': axial_gap,
          'rotation_clearance_from_axial_separation': axial_gap > .01,
          'scope': 'Positive X-axis separation also excludes alternator contact throughout fan rotation about X. This is not a production or radiator/shroud-clearance certificate.'}
(ROOT / 'inventory/engine/fan-clutch-interface-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
