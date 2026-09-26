"""Export an explicitly cropped dowel joint and check repeat-adapter behavior."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as cad
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import intake_locating_dowel as candidate
from assembly_math import transforms
from cad_metrics import solid_volume

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
source_path = Path(candidate.__file__)
source_bytes = source_path.read_bytes()
manifest = json.loads(manifest_bytes)
definitions = {entry['id']: entry for entry in manifest['definitions']}
locations = transforms(manifest)
adapters = {'cylinder-head': candidate.head_interface, 'efi-lower-intake': candidate.lower_interface,
            'efi-head-intake-gasket': candidate.gasket_interface}
shapes = candidate.parts()
installed = '--installed' in sys.argv
colors = ['#b88749']
crop = cad.Pos(-10, -132, 298) * cad.Box(20, 45, 28)
step_hashes = {}
repeat_checks = []
if installed:
    occurrence = next(entry for entry in manifest['occurrences'] if entry['id'] == 'intake-head-locating-dowel')
    path = ROOT / definitions[occurrence['definition']]['step'].lstrip('/')
    step_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    shapes[occurrence['id']] = locations[occurrence['id']] * cad.import_step(path)
for occurrence in manifest['occurrences']:
    identifier = occurrence['id']
    if identifier not in adapters:
        continue
    definition = definitions[occurrence['definition']]
    path = ROOT / definition['step'].lstrip('/')
    step_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    original = cad.import_step(path)
    first = adapters[identifier](original)
    second = adapters[identifier](first)
    assert first.is_valid and second.is_valid and len(first.solids()) == len(second.solids()) == 1
    difference = abs(solid_volume(first, 'adaptive') - solid_volume(second, 'adaptive'))
    assert difference < .001, (identifier, difference)
    for left, right in [(first, second), (second, first)]:
        remaining = left.cut(right)
        assert sum(solid_volume(solid, 'adaptive') for solid in remaining.solids()) < .001
    repeat_checks.append(identifier)
    shapes[identifier] = (locations[identifier] * (original if installed else first)).intersect(crop)
    colors.append(definition['color'])
offsets = {'intake-head-locating-dowel': (0, -20, 0), 'cylinder-head': (0, 0, 0),
           'efi-head-intake-gasket': (0, -45, 0), 'efi-lower-intake': (0, -75, 0)}
arrays = {}
for index, (identifier, shape) in enumerate(shapes.items()):
    assert shape.is_valid and shape.volume > 0, identifier
    vertices, faces = shape.tessellate(.06, .12)
    arrays[f'vertices_{index}'] = np.array([tuple(vertex) for vertex in vertices])
    arrays[f'faces_{index}'] = np.array(faces)
    arrays[f'explode_{index}'] = np.array(offsets[identifier])
assert manifest_path.read_bytes() == manifest_bytes
assert source_path.read_bytes() == source_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in step_hashes.items())
metadata = {'assembly': ('Installed' if installed else 'Isolated') + ' dowel joint — cropped half-section, full pin', 'parts': len(shapes),
            'colors': colors, 'identifiers': list(shapes), 'installed': installed,
            'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
            'source_sha256': hashlib.sha256(source_bytes).hexdigest(), 'step_sha256': step_hashes,
            'repeat_adapter_checks': repeat_checks,
            'limits': 'Crop and display offsets expose the joint; these are not complete component silhouettes or removal paths.'}
arrays['metadata'] = np.array(json.dumps(metadata))
np.savez_compressed(sys.argv[1], **arrays)
print(json.dumps(metadata, indent=2), flush=True)
