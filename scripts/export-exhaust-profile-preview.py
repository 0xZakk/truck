"""Export the isolated front casting and eye for a head-facing offline view."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as cad
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import exhaust_front_profile as profile
import manifold_lifting_eye as eye
import exhaust_rear_entries as rear
import rear_manifold_mounts as rear_mounts

dependencies = [Path(profile.__file__), Path(eye.__file__)]
mounting_candidate = '--rear-mounts' in sys.argv
rear_entries = '--rear-entries' in sys.argv or mounting_candidate
if rear_entries:
    dependencies.append(Path(rear.__file__))
    dependencies.append(Path(rear.egr_tube.__file__))
if mounting_candidate:
    dependencies.append(Path(rear_mounts.__file__))
hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in dependencies}
manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
if rear_entries:
    manifest = json.loads(manifest_bytes)
    definition = next(entry for entry in manifest['definitions'] if entry['id'] == 'exhaust-rear')
    source_path = ROOT / definition['step'].lstrip('/')
    hashes[str(source_path)] = hashlib.sha256(source_path.read_bytes()).hexdigest()
    shapes = {'exhaust-rear': rear.rear_interface(cad.import_step(source_path))}
    if mounting_candidate:
        shapes['exhaust-rear'] = rear_mounts.rear_interface(shapes['exhaust-rear'])
        shapes.update(rear_mounts.parts())
else:
    shapes = {'exhaust-front': profile.front_casting(), **eye.parts()}
arrays = {}
colors = ['#7c6e63'] if rear_entries else ['#7c6e63', '#858a8e', '#858a8e', '#858a8e']
if mounting_candidate:
    colors += ['#858a8e'] * len(rear_mounts.STATIONS)
for index, (identifier, shape) in enumerate(shapes.items()):
    assert shape.is_valid and len(shape.solids()) == 1, identifier
    vertices, faces = shape.tessellate(.1, .15)
    arrays[f'vertices_{index}'] = np.array([tuple(vertex) for vertex in vertices])
    arrays[f'faces_{index}'] = np.array(faces)
    arrays[f'explode_{index}'] = np.array((0, -60 * index, 0))
assert manifest_path.read_bytes() == manifest_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in hashes.items())
arrays['metadata'] = np.array(json.dumps({
    'assembly': 'Rear bolt15/16 candidate — provisional stations and casting' if mounting_candidate else 'Rear entry candidate — unfinished collector/EGR interface' if rear_entries else 'Front rectangular-port candidate — head omitted for inspection',
    'parts': len(shapes), 'colors': colors, 'identifiers': list(shapes), 'installed': False,
    'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(), 'source_sha256': hashes,
    'limits': rear.GAPS + rear_mounts.GAPS if mounting_candidate else rear.GAPS if rear_entries else profile.GAPS
}))
np.savez_compressed(sys.argv[1], **arrays)
print(sys.argv[1], flush=True)
