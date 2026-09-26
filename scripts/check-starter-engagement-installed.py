"""Pose saved starter solids through the prescribed linkage stroke and check neighbors."""
from pathlib import Path
import hashlib
import json
import math
import sys
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
import starter_engagement as linkage
from assembly_math import transforms
from cad_metrics import step_comparison_shape

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
source_paths = [Path(module.__file__) for module in (starter, switch, linkage)]
source_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
paths = {entry['id']: ROOT / entry['step'].lstrip('/') for entry in manifest['definitions']}
hashes = {identifier: hashlib.sha256(path.read_bytes()).hexdigest() for identifier, path in paths.items()}
definitions = {identifier: cad.import_step(path) for identifier, path in paths.items()}
occurrences = {entry['id']: entry for entry in manifest['occurrences']}
locations = transforms(manifest)
rest = {identifier: locations[identifier] * definitions[entry['definition']] for identifier, entry in occurrences.items()}
moving = {'starter-drive-lever', 'starter-solenoid-clevis-pin', 'starter-solenoid-plunger',
          'starter-drive-clutch', 'starter-drive-pinion', 'starter-solenoid-contact-rod',
          'starter-solenoid-bridge-insulator', 'starter-solenoid-contact-bridge', 'starter-solenoid-return-spring'}
checks, pose_checks, failures = 0, 0, []
baseline = starter.parts()
sampled_gaps = []


def volume(shape):
    return sum(solid.volume for solid in shape.solids()) if shape else 0


for index in range(17):
    fraction = index / 16
    drive = starter.TRAVEL * fraction
    plunger = linkage.UPPER_ARM / linkage.LOWER_ARM * drive
    lever = cad.Pos(*linkage.PIVOT) * cad.Rot(math.degrees(math.asin(drive / linkage.LOWER_ARM)), 0, 0) * cad.Pos(*(-value for value in linkage.PIVOT))
    posed = dict(rest)
    targets = switch.parts(fraction)
    targets.update(linkage.parts(fraction, baseline))
    for identifier in moving:
        if identifier == 'starter-solenoid-return-spring':
            shape = targets[identifier]
            assert shape.is_valid and len(shape.solids()) == 1
            posed[identifier] = locations[identifier] * shape
        else:
            if identifier in ('starter-drive-lever', 'starter-solenoid-clevis-pin'):
                motion = lever
            elif identifier in ('starter-drive-clutch', 'starter-drive-pinion'):
                motion = cad.Pos(0, 0, drive)
            else:
                motion = cad.Pos(0, 0, -plunger)
            posed[identifier] = locations[identifier] * motion * definitions[occurrences[identifier]['definition']]
        target = starter.FRAME * step_comparison_shape(targets[identifier])
        assert abs(posed[identifier].volume - target.volume) < .02, identifier
        assert abs(volume(posed[identifier].intersect(target)) - target.volume) < .02, (fraction, identifier, 'pose mismatch')
        pose_checks += 1
    bounds = {identifier: shape.bounding_box() for identifier, shape in posed.items()}
    checked_pairs = set()
    for first in moving:
        for second in posed:
            pair = tuple(sorted((first, second)))
            if first == second or pair in checked_pairs:
                continue
            checked_pairs.add(pair)
            first_box, second_box = bounds[first], bounds[second]
            if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis))
                   - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
                continue
            overlap = volume(posed[first].intersect(posed[second]))
            checks += 1
            if overlap > .05:
                failures.append({'fraction': fraction, 'first': first, 'second': second, 'volume_mm3': overlap})
    gaps = [posed['starter-solenoid-contact-bridge'].distance_to(posed[f'starter-solenoid-terminal-{terminal}']) for terminal in (1, 2)]
    assert all(abs(gap - switch.STROKE * (1 - fraction)) < 1e-5 for gap in gaps)
    sampled_gaps.append(gaps)
    print('Installed starter stroke', fraction, checks, 'checks', len(failures), 'overlaps', flush=True)

assert manifest_path.read_bytes() == manifest_bytes, 'Manifest changed during audit'
assert all(hashlib.sha256(paths[identifier].read_bytes()).hexdigest() == digest for identifier, digest in hashes.items()), 'Saved STEP changed during audit'
assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest for path, digest in source_hashes.items()), 'Generator changed during audit'
report = {'installed': True, 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
          'source_sha256': source_hashes,
          'comparison_method': 'Expected geometry independently STEP-roundtripped before intersection; original volume tolerance remains0.02mm3.',
          'stroke_samples': 17, 'pose_comparisons': pose_checks, 'exact_checks': checks,
          'contact_gaps_mm': sampled_gaps, 'failures': failures,
          'scope': 'Eight rigid saved-STEP components move through the prescribed stroke against all saved neighbors; return spring is regenerated at each sample as an explicit deformation exception. Viewer remains static; no loaded starting, continuous collision or production fit claim.'}
(ROOT / 'inventory/engine/starter-engagement-installed-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS installed starter stroke', flush=True)
