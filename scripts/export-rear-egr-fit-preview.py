"""Export a labeled half-section of the provisional rear EGR connection."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as cad
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import exhaust_rear_entries as rear
from assembly_math import transforms

dependencies = [Path(rear.__file__), Path(rear.front.__file__),
                Path(rear.front.lifting_eye.__file__), Path(rear.egr_tube.__file__)]
hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in dependencies}
manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
installed = '--installed' in sys.argv
crop = cad.Pos(-284, -195, 230) * cad.Box(65, 30, 44)
if installed:
    manifest = json.loads(manifest_bytes)
    locations = transforms(manifest)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    shapes = {}
    for identifier in ('exhaust-rear', 'egr-tube-manifold-fitting'):
        occurrence = next(entry for entry in manifest['occurrences'] if entry['id'] == identifier)
        source_path = ROOT / definitions[occurrence['definition']]['step'].lstrip('/')
        hashes[str(source_path)] = hashlib.sha256(source_path.read_bytes()).hexdigest()
        shapes[identifier] = locations[identifier] * cad.import_step(source_path)
else:
    shapes = {'exhaust-rear': rear.rear_casting(),
              'egr-tube-manifold-fitting': rear.fitting_interface(None)}
arrays = {}
for index, (identifier, shape) in enumerate(shapes.items()):
    shape = shape.intersect(crop)
    assert shape and shape.is_valid and len(shape.solids()) > 0, identifier
    vertices, faces = shape.tessellate(.04, .1)
    arrays[f'vertices_{index}'] = np.array([tuple(vertex) for vertex in vertices])
    arrays[f'faces_{index}'] = np.array(faces)
    arrays[f'explode_{index}'] = np.array((-15 * index, 0, 0))
assert manifest_path.read_bytes() == manifest_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in hashes.items())
arrays['metadata'] = np.array(json.dumps({
    'assembly': 'Provisional EGR fitting insertion — cropped half-section, not factory routing',
    'parts': len(shapes), 'colors': ['#7c6e63', '#aeb8bf'], 'identifiers': list(shapes),
    'installed': installed, 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
    'source_sha256': hashes, 'limits': rear.GAPS,
    'crop': 'X[-316.5,-251.5], Y[-210,-180], Z[208,252] mm; display-only removal'
}))
np.savez_compressed(sys.argv[1], **arrays)
print(sys.argv[1], flush=True)
