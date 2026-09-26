"""Audit isolated rectangular front ports, connected passages and saved neighbors."""
from pathlib import Path
import hashlib
import itertools
import json
import sys
import tempfile
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import exhaust_front_profile as profile
import manifold_lifting_eye
import exhaust_rear_entries
from assembly_math import transforms
from cad_metrics import solid_volume, step_comparison_shape

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
installed = '--installed' in sys.argv
rear_entries = '--rear-entries' in sys.argv
casting_id = 'exhaust-rear' if rear_entries else 'exhaust-front'
port_stations = exhaust_rear_entries.PORTS if rear_entries else profile.PORTS
locations = transforms(manifest)
dependencies = [Path(profile.__file__), Path(manifold_lifting_eye.__file__)]
if rear_entries:
    dependencies.append(Path(exhaust_rear_entries.__file__))
    dependencies.append(Path(exhaust_rear_entries.egr_tube.__file__))
source_hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in dependencies}
step_hashes = {}
definitions = {}
for definition in manifest['definitions']:
    path = ROOT / definition['step'].lstrip('/')
    step_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    definitions[definition['id']] = cad.import_step(path)
shapes = {entry['id']: locations[entry['id']] * definitions[entry['definition']] for entry in manifest['occurrences']}
originals = {identifier: shapes[identifier] for identifier in (casting_id, 'cylinder-head')}
if rear_entries:
    candidates = {casting_id: exhaust_rear_entries.rear_interface(originals[casting_id]),
                  'cylinder-head': locations['cylinder-head'] * exhaust_rear_entries.head_interface(definitions['cylinder-head']),
                  'egr-tube-manifold-fitting': exhaust_rear_entries.fitting_interface(shapes['egr-tube-manifold-fitting'])}
else:
    candidates = {casting_id: profile.front_casting(),
                  'cylinder-head': locations['cylinder-head'] * profile.head_interface(definitions['cylinder-head'])}
installed_matches = []
if installed:
    for identifier, expected in list(candidates.items()):
        actual = shapes[identifier]
        normalized = step_comparison_shape(expected)
        common = actual.intersect(normalized)
        volume = sum(solid_volume(solid, 'adaptive') for solid in common.solids()) if common else 0
        difference = solid_volume(actual, 'adaptive') + solid_volume(normalized, 'adaptive') - 2 * volume
        assert abs(difference) < .01, (identifier, difference)
        installed_matches.append({'part': identifier, 'symmetric_difference_mm3': difference})
        candidates[identifier] = actual
roundtrips = []
with tempfile.TemporaryDirectory(prefix='exhaust-profile-') as directory:
    for identifier, shape in candidates.items():
        assert shape.is_valid and len(shape.solids()) == 1, identifier
        path = Path(directory) / (identifier + '.step')
        cad.export_step(shape, path)
        restored = cad.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        volume_difference = solid_volume(restored, 'adaptive') - solid_volume(shape, 'adaptive')
        print('STEP roundtrip', identifier, volume_difference, flush=True)
        assert abs(volume_difference) < .01, (identifier, volume_difference)
        candidates[identifier] = restored
        roundtrips.append(identifier)
shapes.update(candidates)
boxes = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
failures = []
checks = 0


def intersects_boxes(first, second):
    return all(min(getattr(first.max, axis), getattr(second.max, axis))
               - max(getattr(first.min, axis), getattr(second.min, axis)) > 1e-6 for axis in 'XYZ')


def overlap(first, second):
    common = first.intersect(second)
    return sum(solid_volume(solid, 'adaptive') for solid in common.solids()) if common else 0


for first, second in itertools.combinations(shapes, 2):
    if first not in candidates and second not in candidates:
        continue
    if not intersects_boxes(boxes[first], boxes[second]):
        continue
    volume = overlap(shapes[first], shapes[second])
    checks += 1
    if volume > .01:
        failures.append({'first': first, 'second': second, 'overlap_mm3': volume})
print('Candidate neighbor checks', checks, 'failures', failures, flush=True)
flow_checks = 0
probes = []
for horizontal in port_stations:
    for role, probe in [('runner', profile.runner_void(horizontal, shrink=.05)),
                        ('head-entry', profile.head_void(horizontal, shrink=.05))]:
        probes.append((str(horizontal), role, probe))
if rear_entries:
    network = cad.Pos(port_stations[1], -180, 230) * cad.extrude(cad.RectangleRounded(267.9, 35.9, 7.95), amount=17.95, both=True)
    network += cad.Pos(-286.688, -180, 230) * cad.Rot(0, 90, 0) * cad.Cylinder(7.9, 17, align=(cad.Align.CENTER, cad.Align.CENTER, cad.Align.MIN))
else:
    network = profile.capsule(17.95)
network += cad.Pos(port_stations[1], -180, 175) * cad.Cylinder(19.95, 86)
for horizontal in port_stations:
    network += profile.runner_void(horizontal, shrink=.05)
probes.append(('all', 'connected-collector-and-outlet', network))
for station, role, probe in probes:
    assert probe.is_valid and len(probe.solids()) == 1, (station, role)
    bounds = probe.bounding_box()
    for identifier, shape in shapes.items():
        if not intersects_boxes(bounds, boxes[identifier]):
            continue
        volume = overlap(probe, shape)
        flow_checks += 1
        if volume > .01:
            failures.append({'port_x': station, 'probe': role, 'part': identifier, 'obstruction_mm3': volume})
rim_checks = []
for horizontal in port_stations:
    for identifier, depth in [(casting_id, -133.1), ('cylinder-head', -131.1)]:
        rim = cad.extrude(profile.section(horizontal, depth, 31, 4.5), amount=1)
        rim -= cad.extrude(profile.section(horizontal, depth + .1, 29, 3.5), amount=1.2)
        material = overlap(candidates[identifier], rim)
        error = abs(material - solid_volume(rim, 'adaptive'))
        rim_checks.append({'port_x': horizontal, 'part': identifier, 'missing_material_mm3': error})
        if error > .001:
            failures.append({'port_x': horizontal, 'part': identifier, 'missing_rim_mm3': error})
corner_checks = []
for horizontal in port_stations:
    for identifier, depth in [(casting_id, -133.5), ('cylinder-head', -132.5)]:
        for offset_x, offset_z in itertools.product((-11.5, 11.5), repeat=2):
            probe = cad.Pos(horizontal + offset_x, depth, profile.PORT_Z + offset_z) * cad.Sphere(.15)
            obstruction = overlap(candidates[identifier], probe)
            control = originals[identifier]
            if installed:
                control = cad.Pos(horizontal, depth, profile.PORT_Z) * cad.Rot(90, 0, 0) * (cad.Cylinder(18, 2) - cad.Cylinder(15, 3))
            old_obstruction = overlap(control, probe)
            corner_checks.append({'port_x': horizontal, 'part': identifier, 'offset': [offset_x, offset_z],
                                  'candidate_obstruction_mm3': obstruction, 'old_circular_obstruction_mm3': old_obstruction})
            if obstruction > 1e-5 or old_obstruction < probe.volume * .99:
                failures.append({'port_x': horizontal, 'part': identifier, 'corner_test': [obstruction, old_obstruction]})
contacts = []
contact_pairs = [(casting_id, 'cylinder-head')]
if not rear_entries:
    contact_pairs.append(('front-manifold-lifting-eye', casting_id))
for first, second in contact_pairs:
    distance = shapes[first].distance_to(shapes[second])
    contacts.append({'first': first, 'second': second, 'distance_mm': distance})
    if distance > 1e-6:
        failures.append({'missing_contact': [first, second], 'gap_mm': distance})
assert manifest_path.read_bytes() == manifest_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in {**step_hashes, **source_hashes}.items())
report = {'passed': not failures, 'installed': installed, 'installed_matches': installed_matches,
          'corner_control': 'Analytic historical15mm circular envelope' if installed else 'Actual previous circular-port STEP',
          'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
          'source_sha256': source_hashes, 'step_sha256': step_hashes, 'step_roundtrips': roundtrips,
          'neighbor_checks': checks, 'flow_checks': flow_checks, 'corner_checks': corner_checks,
          'rim_checks': rim_checks, 'connected_flow_network': True,
          'contacts': contacts, 'failures': failures, 'limits': exhaust_rear_entries.GAPS if rear_entries else profile.GAPS,
          'scope': 'Isolated two-definition candidate versus all saved neighbors. Shape-class corner controls, open entry/runner probes and nominal contacts; not production dimensions, pressure performance or finished casting detail.'}
filename = 'exhaust-front-profile-installed-validation.json' if installed else 'exhaust-front-profile-validation.json'
if rear_entries:
    filename = 'exhaust-rear-entries-installed-validation.json' if installed else 'exhaust-rear-entries-validation.json'
    report['scope'] = 'Three-definition rear entry/head/fitting correction against saved neighbors, with retained provisional collector/EGR flow regression. Not the finished rear casting or verified EGR routing.'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key: value for key, value in report.items() if key not in ('step_sha256', 'corner_checks')}, indent=2), flush=True)
assert not failures
