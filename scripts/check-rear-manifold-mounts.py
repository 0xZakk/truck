"""Audit rear fastener candidate, supporting material and saved-assembly neighbors."""
from pathlib import Path
import hashlib
import itertools
import json
import sys
import tempfile
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import rear_manifold_mounts as mounts
from assembly_math import transforms
from cad_metrics import solid_volume

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
locations = transforms(manifest)
hashes = {str(Path(module.__file__)): hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
          for module in (mounts, mounts.hardware, mounts.profile)}
definitions = {}
for definition in manifest['definitions']:
    path = ROOT / definition['step'].lstrip('/')
    hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    definitions[definition['id']] = cad.import_step(path)
shapes = {entry['id']: locations[entry['id']] * definitions[entry['definition']] for entry in manifest['occurrences']}
candidates = mounts.parts()
for identifier, adapter in mounts.ADAPTERS.items():
    candidates[identifier] = locations[identifier] * adapter(definitions[identifier])
roundtrips = []
with tempfile.TemporaryDirectory(prefix='rear-mounts-') as directory:
    for identifier, shape in candidates.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(directory) / (identifier + '.step')
        cad.export_step(shape, path)
        restored = cad.import_step(path)
        difference = solid_volume(restored, 'adaptive') - solid_volume(shape, 'adaptive')
        assert restored.is_valid and len(restored.solids()) == 1 and abs(difference) < .01, (identifier, difference)
        candidates[identifier] = restored
        roundtrips.append({'part': identifier, 'volume_difference_mm3': difference})
        print('STEP', identifier, difference, flush=True)
shapes.update(candidates)
boxes = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
failures = []


def boxes_overlap(first, second):
    return all(min(getattr(first.max, axis), getattr(second.max, axis))
               - max(getattr(first.min, axis), getattr(second.min, axis)) > 1e-6 for axis in 'XYZ')


def overlap(first, second):
    common = first.intersect(second)
    return sum(solid_volume(solid, 'adaptive') for solid in common.solids()) if common else 0


neighbor_checks = 0
for first, second in itertools.combinations(shapes, 2):
    if first not in candidates and second not in candidates:
        continue
    if not boxes_overlap(boxes[first], boxes[second]):
        continue
    volume = overlap(shapes[first], shapes[second])
    neighbor_checks += 1
    if volume > .01:
        failures.append({'first': first, 'second': second, 'overlap_mm3': volume})
print('Neighbors', neighbor_checks, failures, flush=True)
material_checks = []
contacts = []
for identifier, (horizontal, vertical) in mounts.STATIONS.items():
    bolt_id = 'rear-manifold-' + identifier
    distance = shapes[bolt_id].distance_to(shapes['exhaust-rear'])
    contacts.append({'parts': [bolt_id, 'exhaust-rear'], 'distance_mm': distance})
    if distance > 1e-6:
        failures.append({'missing_seat_contact': bolt_id, 'distance_mm': distance})
    wall = mounts.hardware.axis_y(6, -130, -110, horizontal, vertical)
    wall -= mounts.hardware.axis_y(5.1, -131, -109, horizontal, vertical)
    floor = mounts.hardware.axis_y(4.6, -107.3, -105.5, horizontal, vertical)
    seat = mounts.hardware.axis_y(7.5, -142.9, -141.9, horizontal, vertical)
    seat -= mounts.hardware.axis_y(5.3, -143, -141.8, horizontal, vertical)
    for role, target, probe in [('socket-wall', 'cylinder-head', wall),
                                ('socket-floor', 'cylinder-head', floor),
                                ('bolt-seat', 'exhaust-rear', seat)]:
        missing = abs(solid_volume(probe, 'adaptive') - overlap(shapes[target], probe))
        material_checks.append({'station': identifier, 'role': role, 'missing_material_mm3': missing})
        if missing > .001:
            failures.append(material_checks[-1])
flow_checks = 0
for horizontal in (*mounts.profile.PORTS, -31.896, -145.688, -259.48):
    for role, probe in [('runner', mounts.profile.runner_void(horizontal, shrink=.05)),
                        ('head-entry', mounts.profile.head_void(horizontal, shrink=.05))]:
        assert probe.is_valid and len(probe.solids()) == 1
        bounds = probe.bounding_box()
        for identifier, shape in shapes.items():
            if not boxes_overlap(bounds, boxes[identifier]):
                continue
            volume = overlap(shape, probe)
            flow_checks += 1
            if volume > .01:
                failures.append({'port_x': horizontal, 'role': role, 'part': identifier, 'obstruction_mm3': volume})
assert manifest_path.read_bytes() == manifest_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in hashes.items())
report = {'passed': not failures, 'installed': False, 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
          'dependency_sha256': hashes, 'step_roundtrips': roundtrips, 'neighbor_checks': neighbor_checks,
          'flow_checks': flow_checks, 'material_checks': material_checks, 'contacts': contacts,
          'failures': failures, 'limits': mounts.GAPS,
          'scope': 'Six-definition candidate against all saved neighbors. Nominal bolt seats and positive socket wall/floor material; no production threads, clamp load, gallery compatibility or finished manifold claim.'}
(ROOT / 'inventory/engine/rear-manifold-mounts-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key: value for key, value in report.items() if key != 'dependency_sha256'}, indent=2), flush=True)
assert not failures
