"""Frozen installed-neighbor audit for the proposed coordinated pump drive."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import oil_pump_motion as motion
import oil_drive_layout as layout
from assembly_math import transforms

target = ROOT / 'inventory/engine/full-assembly.json'
raw = target.read_bytes()
manifest = json.loads(raw)
installed = '--installed' in sys.argv
artifact_paths = [ROOT / definition['step'].lstrip('/') for definition in manifest['definitions']]
artifact_hashes = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in artifact_paths}
definitions = {definition['id']: b.import_step(ROOT / definition['step'].lstrip('/')) for definition in manifest['definitions']}
if not installed:
    definitions['oil-pump-inner-rotor'] = motion.inner_rotor()
    definitions['oil-pump-outer-rotor'] = motion.outer_rotor()
    definitions['oil-pump-rotor-shaft'] = motion.shaft_interface(definitions['oil-pump-rotor-shaft'])
affected = {'oil-pump-inner-rotor', 'oil-pump-outer-rotor', 'oil-pump-rotor-shaft',
            'oil-pump-intermediate-shaft', 'oil-pump-drive-retainer'}
checks, collisions = 0, []
for crank_angle in range(0, 721, 30):
    locations = transforms(manifest, crank_angle)
    if not installed:
        inner_pose, outer_pose = motion.rotor_poses(crank_angle)
        spin = b.Rot(0, 0, -crank_angle / 2)
        locations['oil-pump-inner-rotor'] = layout.PUMP_FRAME * inner_pose
        locations['oil-pump-outer-rotor'] = layout.PUMP_FRAME * outer_pose
        locations['oil-pump-rotor-shaft'] = layout.PUMP_FRAME * b.Pos(3.5, 0, 5) * spin
        for identifier in ('oil-pump-intermediate-shaft', 'oil-pump-drive-retainer'):
            locations[identifier] = layout.GEAR_FRAME * spin * b.Pos(0, 0, layout.INTERMEDIATE_BOTTOM)
    shapes = {occurrence['id']: locations[occurrence['id']] * definitions[occurrence['definition']] for occurrence in manifest['occurrences']}
    boxes = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
    for first in sorted(affected):
        for second in shapes:
            if second == first or second in affected and second < first:
                continue
            first_box, second_box = boxes[first], boxes[second]
            if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .02 for axis in 'XYZ'):
                continue
            checks += 1
            overlap = shapes[first].intersect(shapes[second])
            volume = sum(solid.volume for solid in overlap.solids()) if overlap else 0
            if volume > .1:
                collisions.append({'crank_degrees': crank_angle, 'first': first, 'second': second, 'volume_mm3': volume})
    print('Installed-neighbor pose', crank_angle, 'checks', checks, 'collisions', len(collisions), flush=True)
assert target.read_bytes() == raw, 'Frozen manifest changed'
assert all(hashlib.sha256(path.read_bytes()).hexdigest() == digest for path, digest in artifact_hashes.items()), 'Frozen STEP artifacts changed'
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/oil_pump_motion.py').read_bytes()).hexdigest(),
          'poses': 25, 'boolean_checks': checks, 'collisions': collisions}
filename = 'oil-pump-motion-installed-validation.json' if installed else 'oil-pump-motion-neighbor-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
assert not collisions, collisions
print('PASS frozen installed-neighbor audit', flush=True)
