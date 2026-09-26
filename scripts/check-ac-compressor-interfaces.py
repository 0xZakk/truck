"""Check compressor build placements and the provisional support candidate."""
import hashlib
import json
from pathlib import Path
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor as candidate
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


candidate.build((define, add, group))
manifest['occurrences'] = occurrences
poses = transforms(manifest)
parts = {}
for occurrence in occurrences:
    actual = definitions[occurrence['definition']].moved(poses[occurrence['id']])
    expected = b.Pos(*candidate.POSITION) * definitions[occurrence['definition']]
    common = actual.intersect(expected)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    assert abs(volume - expected.volume) < .02, occurrence['id']
    parts[occurrence['id']] = actual

bounds = {identifier: shape.bounding_box() for identifier, shape in parts.items()}
collisions = []
checks = 0
bracket_hash = None
if '--brackets' in sys.argv:
    import accessory_brackets
    bracket_hash = hashlib.sha256(Path(accessory_brackets.__file__).read_bytes()).hexdigest()
    for neighbor_id, neighbor in accessory_brackets.parts().items():
        neighbor_box = neighbor.bounding_box()
        for identifier, shape in parts.items():
            box = bounds[identifier]
            if any(min(getattr(box.max, axis), getattr(neighbor_box.max, axis)) -
                   max(getattr(box.min, axis), getattr(neighbor_box.min, axis)) <= .01 for axis in 'XYZ'):
                continue
            checks += 1
            common = shape.intersect(neighbor)
            volume = sum(solid.volume for solid in common.solids()) if common else 0
            if volume > .01:
                collisions.append({'a': identifier, 'b': neighbor_id, 'volume_mm3': volume})

assert raw == manifest_path.read_bytes()
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'bracket_source_sha256': bracket_hash, 'bracket_exact_checks': checks,
          'api_transform_checks': len(occurrences), 'collisions': collisions,
          'clutch_gap_mm': .6, 'verified_production_fit': False}
(ROOT / 'inventory/engine/ac-compressor-interface-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
