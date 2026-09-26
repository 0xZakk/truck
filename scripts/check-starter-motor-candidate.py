"""Frozen installed-neighbor audit of the disengaged manual PMGR candidate."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
from assembly_math import transforms
from cad_metrics import step_comparison_shape

target = ROOT / 'inventory/engine/full-assembly.json'
raw = target.read_bytes()
manifest = json.loads(raw)
definitions = {definition['id']: b.import_step(ROOT / definition['step'].lstrip('/')) for definition in manifest['definitions']}
locations = transforms(manifest)
neighbors = {occurrence['id']: locations[occurrence['id']] * definitions[occurrence['definition']] for occurrence in manifest['occurrences']}
candidate = {identifier: starter.FRAME * shape for identifier, shape in starter.parts().items()}
installed = '--installed' in sys.argv
if installed and 'starter-solenoid-s-terminal' in neighbors:
    import starter_solenoid as switch
    candidate = {identifier: shape for identifier, shape in candidate.items() if identifier not in switch.REPLACED}
    candidate.update({identifier: starter.FRAME * shape for identifier, shape in switch.parts().items()})
    assert len(candidate) == 116
if '--engagement' in sys.argv:
    import starter_engagement as engagement
    candidate.update({identifier: starter.FRAME * shape for identifier, shape in engagement.parts(baseline=starter.parts()).items()})
if '--wiring' in sys.argv:
    import starter_wiring as wiring
    candidate.update({identifier: starter.FRAME * shape for identifier, shape in wiring.parts().items()})
if '--wiring-fit' in sys.argv:
    import starter_wiring_fit as wiring_fit
    candidate.update({identifier: starter.FRAME * shape for identifier, shape in wiring_fit.parts().items()})
if '--motor-feed' in sys.argv:
    import starter_motor_feed as motor_feed
    candidate.update({identifier: starter.FRAME * shape for identifier, shape in motor_feed.parts().items()})
source_modules = [starter]
if installed and 'starter-solenoid-s-terminal' in neighbors:
    source_modules.append(switch)
if '--engagement' in sys.argv:
    source_modules.append(engagement)
if '--wiring' in sys.argv:
    source_modules.append(wiring)
if '--wiring-fit' in sys.argv:
    source_modules.extend([wiring_fit, wiring_fit.accepted])
if '--motor-feed' in sys.argv:
    source_modules.append(motor_feed)
source_hashes = {str(Path(module.__file__).relative_to(ROOT)): hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() for module in source_modules}
if installed:
    for identifier, expected in candidate.items():
        actual = neighbors[identifier]
        expected = starter.FRAME * step_comparison_shape(starter.FRAME.inverse() * expected)
        common = actual.intersect(expected)
        common_volume = sum(solid.volume for solid in common.solids()) if common else 0
        assert abs(actual.volume - expected.volume) < .02, identifier
        assert abs(common_volume - expected.volume) < .02, (identifier, 'installed pose mismatch')
    candidate = {identifier: neighbors[identifier] for identifier in candidate}
boxes = {identifier: shape.bounding_box() for identifier, shape in (neighbors | candidate).items()}
checks, collisions = 0, []
for first, shape in candidate.items():
    assert shape.is_valid and len(shape.solids()) == 1, first
    for second, neighbor in neighbors.items():
        if first == second:
            continue
        first_box, second_box = boxes[first], boxes[second]
        if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .02 for axis in 'XYZ'):
            continue
        checks += 1
        common = shape.intersect(neighbor)
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        if volume > .1:
            collisions.append({'first': first, 'second': second, 'volume_mm3': volume})
    print('Neighbor part', first, 'checks', checks, 'collisions', len(collisions), flush=True)
assert target.read_bytes() == raw, 'Frozen manifest changed'
assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest for path, digest in source_hashes.items()), 'Generator changed during audit'
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'comparison_method': 'Expected geometry independently STEP-roundtripped before intersection; original volume tolerance remains0.02mm3.',
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_motor.py').read_bytes()).hexdigest(),
          'composed_source_sha256': source_hashes,
          'candidate_parts': len(candidate), 'boolean_checks': checks, 'collisions': collisions,
          'boundary': 'Default disengaged stationary candidate. Bellhousing/index-plate support unresolved. Isolated checker separately samples reducer and engaged flywheel mesh.'}
filename = 'starter-motor-installed-validation.json' if installed else 'starter-motor-candidate-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
assert not collisions, collisions
print('PASS starter frozen-neighbor audit', flush=True)
