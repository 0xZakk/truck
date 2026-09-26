"""Export the isolated lifting-eye interfaces for offline visual inspection."""
from pathlib import Path
import hashlib
import json
import sys

import build123d as cad
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import manifold_lifting_eye as candidate
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
source_path = Path(candidate.__file__)
source_bytes = source_path.read_bytes()
definitions = {entry['id']: entry for entry in manifest['definitions']}
locations = transforms(manifest)
shapes = candidate.parts()
colors = ['#bc955b', '#8796a6', '#8796a6']
adapters = {'cylinder-head': candidate.head_interface, 'efi-lower-intake': candidate.lower_interface,
            'efi-head-intake-gasket': candidate.gasket_interface, 'exhaust-front': candidate.front_interface}
step_hashes = {}
for occurrence in manifest['occurrences']:
    identifier = occurrence['id']
    if identifier not in adapters:
        continue
    definition = definitions[occurrence['definition']]
    path = ROOT / definition['step'].lstrip('/')
    step_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    shape = adapters[identifier](cad.import_step(path))
    if not isinstance(shape, cad.Shape):
        shape = cad.Compound(children=list(shape))
    shapes[identifier] = locations[identifier] * shape
    colors.append(definition['color'])
arrays = {}
for index, (identifier, shape) in enumerate(shapes.items()):
    assert shape.is_valid and len(shape.solids()) == 1, identifier
    vertices, faces = shape.tessellate(.15, .15)
    arrays[f'vertices_{index}'] = np.array([tuple(vertex) for vertex in vertices])
    arrays[f'faces_{index}'] = np.array(faces)
    offset = (0, -100, 0) if identifier.startswith('front-manifold') else (0, 0, 0)
    if identifier in ('efi-lower-intake', 'efi-head-intake-gasket'):
        offset = (0, -200, 0)
    arrays[f'explode_{index}'] = np.array(offset)
assert manifest_path.read_bytes() == manifest_bytes
assert source_path.read_bytes() == source_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in step_hashes.items())
arrays['metadata'] = np.array(json.dumps({
    'assembly': 'Isolated manifold lifting-eye candidate', 'parts': len(shapes),
    'colors': colors, 'identifiers': list(shapes), 'installed': False,
    'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
    'source_sha256': hashlib.sha256(source_bytes).hexdigest(), 'step_sha256': step_hashes
}))
np.savez_compressed(sys.argv[1], **arrays)
print(sys.argv[1], flush=True)
