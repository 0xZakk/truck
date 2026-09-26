"""Compare emitted FS10 groups with actual shared CAD transforms and analytic poses."""
import hashlib
import json
import math
from pathlib import Path
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor_motion as candidate
import ac_compressor_bearing as bearing
import ac_compressor_manifold as manifold_geometry
import ac_compressor_shaft_support as shaft_support
import ac_compressor_manifold_passages as manifold_passages
import assembly_math

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
installed = '--installed' in sys.argv
geometry = manifold_passages if '--passages' in sys.argv else shaft_support if '--shaft-support' in sys.argv else manifold_geometry if '--manifold' in sys.argv else bearing if '--bearing' in sys.argv else candidate
expected_count = 67 if '--passages' in sys.argv or '--shaft-support' in sys.argv else 65 if '--manifold' in sys.argv else 61
descendants = {'ac-compressor'}
while True:
    expanded = descendants | {entry['id'] for entry in manifest['assemblies'] if entry['parent'] in descendants}
    if expanded == descendants:
        break
    descendants = expanded
if not installed:
    manifest['assemblies'] = [entry for entry in manifest['assemblies'] if entry['id'] not in descendants]
definitions = {}
occurrences = []


def define(identifier, shape, *metadata):
    definitions[identifier] = shape


def group(identifier, name, parent='engine', motion=None, position=(0, 0, 0), rotation=(0, 0, 0)):
    manifest['assemblies'].append({'id': identifier, 'name': name, 'parent': parent, 'motion': motion,
                                   'position_cad_mm': position, 'rotation_cad_deg': rotation})


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0)):
    occurrences.append({'id': identifier, 'definition': definition, 'parent': parent,
                        'position_cad_mm': pos, 'rotation_cad_deg': rotation, 'explode_cad_mm': explode})


if installed:
    occurrences = [entry for entry in manifest['occurrences'] if entry['parent'] in descendants]
    used = {entry['definition'] for entry in occurrences}
    definitions = {entry['id']: b.import_step(ROOT / entry['step'].lstrip('/'))
                   for entry in manifest['definitions'] if entry['id'] in used}
    assert sum((entry.get('motion') or {}).get('type') == 'fs10'
               for entry in manifest['assemblies'] if entry['id'] in descendants) == 17
else:
    geometry.build((define, add, group))
    manifest['occurrences'] = occurrences
assert len(occurrences) == len(definitions) == expected_count
checked = 0
analytic_checks = 0
for engaged in (True, False):
    for phase in (0, 37, 90, 173, 271, 360):
        poses = assembly_math.transforms(manifest, degrees=123, compressor_degrees=phase, compressor_engaged=engaged)
        targets = geometry.parts(phase, engaged)
        for occurrence in occurrences:
            identifier = occurrence['id']
            if phase and candidate.descriptor(identifier) is None:
                continue
            actual = definitions[occurrence['definition']].moved(poses[identifier])
            target = targets[identifier]
            common = actual.intersect(target)
            volume = sum(solid.volume for solid in common.solids()) if common else 0
            assert abs(volume - target.volume) < .02, (identifier, phase, engaged, volume, target.volume)
            assert abs(actual.volume - geometry.home_components()[identifier].volume) < .02, identifier
            checked += 1
        effective_phase = phase if engaged else 0
        for index in range(5):
            displacement = candidate.base.displacement(index, effective_phase)
            horizontal, vertical = candidate.base.axis_position(index)
            normal = (math.cos(math.radians(candidate.TILT)),
                      math.sin(math.radians(candidate.TILT)) * math.sin(math.radians(effective_phase)),
                      -math.sin(math.radians(candidate.TILT)) * math.cos(math.radians(effective_phase)))
            for direction in (-1, 1):
                center = (displacement + direction * candidate.BALL_HEIGHT, vertical, -horizontal)
                plane_distance = sum(first * second for first, second in zip(normal, center))
                assert abs(plane_distance - direction * 3.2) < 1e-10
                analytic_checks += 1
        print('API', phase, engaged, checked, flush=True)

assert manifest_path.read_bytes() == raw
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'candidate_sha256': hashlib.sha256(Path(geometry.__file__).read_bytes()).hexdigest(),
          'assembly_math_sha256': hashlib.sha256(Path(assembly_math.__file__).read_bytes()).hexdigest(),
          'definition_count': len(definitions), 'occurrence_count': len(occurrences),
          'api_shape_pose_checks': checked, 'analytic_shoe_plane_checks': analytic_checks,
          'phases_degrees': [0, 37, 90, 173, 271, 360], 'engagement_states': [True, False],
          'crank_degrees_deliberately_unrelated': 123, 'passed': True,
          'limits': 'Disengagement resets the reference pose; no physical run-down, armature flexure or speed ratio is claimed.'}
filename = 'ac-compressor-motion-installed-validation.json' if installed else 'ac-compressor-motion-api-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
