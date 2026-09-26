"""Validate candidate drive geometry without mutating the installed engine."""
from pathlib import Path
import hashlib
import itertools
import json
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import oil_drive_layout as layout
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
definitions = {}
for definition in manifest['definitions']:
    definitions[definition['id']] = b.import_step(ROOT / definition['step'].lstrip('/'))
print('Loaded frozen geometry', flush=True)
candidates = layout.candidate_parts(manifest, definitions)
print('Built candidate', flush=True)
invalid = []
with tempfile.TemporaryDirectory(prefix='oil-drive-layout-') as directory:
    for identifier, shape in candidates.items():
        if not shape.is_valid or len(shape.solids()) != 1:
            invalid.append({'id': identifier, 'valid': shape.is_valid, 'solids': len(shape.solids())})
            continue
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        if not restored.is_valid or len(restored.solids()) != 1:
            invalid.append({'id': identifier, 'step_valid': restored.is_valid, 'step_solids': len(restored.solids())})
print('STEP audit', invalid, flush=True)
locations = transforms(manifest)
neighbors = {occurrence['id']: locations[occurrence['id']] * definitions[occurrence['definition']]
             for occurrence in manifest['occurrences'] if occurrence['id'] not in candidates}
boxes = {identifier: shape.bounding_box() for identifier, shape in (candidates | neighbors).items()}
collisions = []
checks = 0


def check_pair(first, second, first_shape, second_shape):
    global checks
    first_box, second_box = boxes[first], boxes[second]
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .02 for axis in 'XYZ'):
        return
    checks += 1
    overlap = first_shape.intersect(second_shape)
    volume = sum(solid.volume for solid in overlap.solids()) if overlap else 0
    if volume > .1:
        collision = {'first': first, 'second': second, 'volume_mm3': round(volume, 5)}
        collisions.append(collision)
        print('Collision', collision, flush=True)


for (first, first_shape), (second, second_shape) in itertools.combinations(candidates.items(), 2):
    check_pair(first, second, first_shape, second_shape)
for first, first_shape in candidates.items():
    if first == 'block':
        continue
    for second, second_shape in neighbors.items():
        check_pair(first, second, first_shape, second_shape)

additions = candidates['block'] - definitions['block']
if isinstance(additions, b.ShapeList):
    additions = b.Compound(children=additions)
boxes['block-added-material'] = additions.bounding_box()
for identifier, shape in neighbors.items():
    check_pair('block-added-material', identifier, additions, shape)

motion_collisions = []
for crank_angle in range(0, 360, 30):
    crank = b.Rot(crank_angle, 0, 0) * definitions['crankshaft']
    identifier = f'crankshaft-at-{crank_angle}'
    boxes[identifier] = crank.bounding_box()
    previous_count = len(collisions)
    for candidate, shape in candidates.items():
        if candidate.startswith(('oil-pump-', 'oil-pickup-')):
            check_pair(candidate, identifier, shape, crank)
    motion_collisions += collisions[previous_count:]
    del collisions[previous_count:]

gear_samples = []
cam_gear = layout.helical_gear(12, 2.5)
distributor_gear = layout.helical_gear(12, 11.25)
for sample in range(17):
    shaft_angle = sample * 22.5 / 16
    cam_shape = b.Pos(layout.DRIVE_X, 90, 72) * b.Rot(-shaft_angle, 0, 0) * b.Rot(0, 90, 0) * cam_gear
    distributor_shape = layout.GEAR_FRAME * b.Rot(0, 0, -shaft_angle) * distributor_gear
    overlap = cam_shape.intersect(distributor_shape)
    volume = sum(solid.volume for solid in overlap.solids()) if overlap else 0
    gear_samples.append({'shaft_degrees': shaft_angle, 'overlap_mm3': round(volume, 6),
                         'minimum_distance_mm': cam_shape.distance_to(distributor_shape)})
    print('Gear sample', gear_samples[-1], flush=True)

assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
report = {'installed': False, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/oil_drive_layout.py').read_bytes()).hexdigest(),
          'candidate_count': len(candidates), 'invalid': invalid, 'checks': checks, 'collisions': collisions,
          'crank_motion_collisions': motion_collisions, 'gear_mesh_samples': gear_samples,
          'gear_origin_mm': [layout.DRIVE_X, layout.GEAR_Y, layout.GEAR_Z],
          'tilt_degrees': layout.TILT, 'shaft_length_mm': layout.LENGTH,
          'limits': layout.GAPS + ['Static neighbor audit plus twelve crank angles and seventeen points across one gear-tooth period. Unchanged block-to-neighbor intersections are not re-audited.']}
(ROOT / 'inventory/engine/oil-drive-layout-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
