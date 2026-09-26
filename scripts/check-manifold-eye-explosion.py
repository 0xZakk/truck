"""Check installed lifting-eye exploded poses against every saved engine part."""
from pathlib import Path
import hashlib
import itertools
import json
import sys
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
locations = transforms(manifest)
definitions = {}
hashes = {}
for definition in manifest['definitions']:
    path = ROOT / definition['step'].lstrip('/')
    hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    definitions[definition['id']] = cad.import_step(path)
targets = {'front-manifold-lifting-eye', 'front-manifold-stud13', 'front-manifold-bolt14'}
if '--include-dowel' in sys.argv:
    targets.add('intake-head-locating-dowel')
candidate_offsets = {
    'front-manifold-lifting-eye': (0, -350, -100),
    'front-manifold-stud13': (0, -440, -100),
    'front-manifold-bolt14': (0, -500, -100)
} if '--candidate-offsets' in sys.argv else {}
assert targets <= {entry['id'] for entry in manifest['occurrences']}
checks = 0
failures = []
for fraction in (.6, 1):
    shapes = {}
    for occurrence in manifest['occurrences']:
        identifier = occurrence['id']
        location = locations[identifier]
        parent = location * cad.Rot(*occurrence.get('rotation_cad_deg', [0, 0, 0])).inverse()
        matrix = parent.wrapped.Transformation()
        offset = candidate_offsets.get(identifier, occurrence['explode_cad_mm'])
        displacement = [fraction * sum(matrix.Value(row, column) * offset[column - 1]
                                       for column in range(1, 4)) for row in range(1, 4)]
        shapes[identifier] = cad.Pos(*displacement) * location * definitions[occurrence['definition']]
    boxes = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
    for first, second in itertools.combinations(shapes, 2):
        if first not in targets and second not in targets:
            continue
        first_box, second_box = boxes[first], boxes[second]
        if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis))
               - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= 1e-6 for axis in 'XYZ'):
            continue
        common = shapes[first].intersect(shapes[second])
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        checks += 1
        if volume > .01:
            failures.append({'fraction': fraction, 'first': first, 'second': second, 'overlap_mm3': volume})
assert manifest_path.read_bytes() == manifest_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in hashes.items())
report = {'passed': not failures, 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
          'parts': len(shapes), 'targets': sorted(targets), 'fractions': [.6, 1],
          'exact_checks': checks, 'failures': failures, 'step_sha256': hashes,
          'candidate_offsets': candidate_offsets,
          'scope': 'Two sampled exploded display states, not an assembly-removal trajectory or production fit proof.'}
filename = 'manifold-eye-explosion-candidate-validation.json' if candidate_offsets else 'manifold-eye-explosion-validation.json'
if '--include-dowel' in sys.argv:
    filename = 'manifold-joint-explosion-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key: value for key, value in report.items() if key != 'step_sha256'}, indent=2), flush=True)
assert not failures
