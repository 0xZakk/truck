"""Audit the unpublished shaft study; report installation blockers without hiding collisions."""
from pathlib import Path
import hashlib
import json
import math
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import oil_pump_drive as drive
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
locations = transforms(manifest)
definitions = {definition['id']: definition for definition in manifest['definitions']}
parts = drive.parts()
roundtrips = []
with tempfile.TemporaryDirectory(prefix='oil-pump-drive-') as directory:
    for identifier, shape in parts.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        output = Path(directory) / (identifier + '.step')
        b.export_step(shape, output)
        restored = b.import_step(output)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .001, identifier
        roundtrips.append({'id': identifier, 'valid': True, 'solids': 1, 'volume_mm3': shape.volume})

shaft_box = parts['oil-pump-intermediate-shaft'].bounding_box()
assert abs(shaft_box.size.Z - drive.LENGTH) < 1e-5
assert abs(shaft_box.size.Y - drive.ACROSS_FLATS) < 1e-5
internal = parts['oil-pump-intermediate-shaft'].intersect(parts['oil-pump-drive-retainer'])
assert not internal or sum(solid.volume for solid in internal.solids()) < .001
placed = {identifier: shape.moved(b.Pos(*drive.POSITION)) for identifier, shape in parts.items()}
bounds = {identifier: shape.bounding_box() for identifier, shape in placed.items()}
cache = {}
collisions = []
checks = 0
for occurrence in manifest['occurrences']:
    definition = occurrence['definition']
    if definition not in cache:
        cache[definition] = b.import_step(ROOT / definitions[definition]['step'].lstrip('/'))
    neighbor = cache[definition].moved(locations[occurrence['id']])
    neighbor_box = neighbor.bounding_box()
    for identifier, shape in placed.items():
        candidate_box = bounds[identifier]
        if any(min(getattr(candidate_box.max, axis), getattr(neighbor_box.max, axis)) -
               max(getattr(candidate_box.min, axis), getattr(neighbor_box.min, axis)) <= .01 for axis in 'XYZ'):
            continue
        checks += 1
        intersection = shape.intersect(neighbor)
        volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
        if volume > .01:
            collisions.append({'candidate': identifier, 'neighbor': occurrence['id'], 'volume_mm3': round(volume, 6)})

pump_center = b.Vertex(0, 0, 0).moved(locations['oil-pump-rotor-shaft']).center()
distributor_center = b.Vertex(0, 0, 0).moved(locations['distributor-shaft']).center()
lateral_error = math.hypot(pump_center.X - distributor_center.X, pump_center.Y - distributor_center.Y)
assert lateral_error > 100
assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
report = {
    'installed': False, 'release_status': 'blocked-installation', 'component_geometry_status': 'pass',
    'manifest_sha256': hashlib.sha256(raw).hexdigest(),
    'source_sha256': hashlib.sha256((ROOT / 'cad/engine/oil_pump_drive.py').read_bytes()).hexdigest(),
    'step_roundtrips': roundtrips, 'candidate_origin_mm': drive.POSITION,
    'neighbor_boolean_checks': checks, 'collisions': collisions,
    'axis_lateral_error_mm': lateral_error,
    'pump_socket_across_flats_mm': 3 * math.sqrt(3),
    'shaft_across_flats_mm': drive.ACROSS_FLATS,
    'shaft_length_mm': drive.LENGTH,
    'candidate_top_z_mm': drive.POSITION[2] + drive.LENGTH,
    'distributor_bottom_z_mm': distributor_center.Z - 103,
    'required_changes': [
        'Resolve block, cam, distributor and pump axis stations together from reference measurements.',
        'Rebuild the provisional pump socket for the manufacturer hex dimension plus a justified fit allowance.',
        'Add the distributor lower hex socket after reconciling shaft length and engagement depths.',
        'Resolve block passage and retainer stop before claiming retained installation.'
    ],
    'limits': drive.GAPS + ['Neighbor audit is static at zero crank angle; it intentionally diagnoses the proposed pump-side placement.']
}
(ROOT / 'inventory/engine/oil-pump-drive-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
