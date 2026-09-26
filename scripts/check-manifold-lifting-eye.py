"""Validate the unfinished two-point lifting-eye candidate before integration."""
from pathlib import Path
import hashlib
import itertools
import json
import sys
import tempfile
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import manifold_lifting_eye as candidate
import exhaust_front_profile
from assembly_math import transforms
from cad_metrics import solid_volume, step_comparison_shape

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_bytes = manifest_path.read_bytes()
source_path = Path(candidate.__file__)
source_bytes = source_path.read_bytes()
rectangular = '--rectangular' in sys.argv
profile_path = Path(exhaust_front_profile.__file__)
profile_bytes = profile_path.read_bytes()
manifest = json.loads(manifest_bytes)
definitions = {entry['id']: entry for entry in manifest['definitions']}
locations = transforms(manifest)
adapters = {'cylinder-head': candidate.head_interface, 'efi-lower-intake': candidate.lower_interface,
            'efi-head-intake-gasket': candidate.gasket_interface, 'exhaust-front': candidate.front_interface}
if rectangular:
    adapters['exhaust-front'] = exhaust_front_profile.front_interface
shapes = candidate.parts()
whole_engine = '--whole-engine' in sys.argv
installed = '--installed' in sys.argv
step_hashes = {}
originals = {}
failures = []
roundtrips = []
for occurrence in manifest['occurrences']:
    identifier = occurrence['id']
    if identifier not in adapters:
        continue
    step_path = ROOT / definitions[occurrence['definition']]['step'].lstrip('/')
    step_hashes[str(step_path)] = hashlib.sha256(step_path.read_bytes()).hexdigest()
    original = cad.import_step(step_path)
    originals[identifier] = locations[identifier] * original
    changed = adapters[identifier](original)
    if not isinstance(changed, cad.Shape):
        changed = cad.Compound(children=list(changed))
    shapes[identifier] = locations[identifier] * changed
assert len(shapes) == 7
candidate_ids = set(shapes)
installed_matches = []
if installed:
    occurrences = {entry['id']: entry for entry in manifest['occurrences']}
    for identifier, expected in list(shapes.items()):
        occurrence = occurrences[identifier]
        step_path = ROOT / definitions[occurrence['definition']]['step'].lstrip('/')
        step_hashes[str(step_path)] = hashlib.sha256(step_path.read_bytes()).hexdigest()
        actual = locations[identifier] * cad.import_step(step_path)
        normalized = step_comparison_shape(expected)
        common = actual.intersect(normalized)
        volume = sum(solid_volume(solid, 'adaptive') for solid in common.solids()) if common else 0
        difference = solid_volume(actual, 'adaptive') + solid_volume(normalized, 'adaptive') - 2 * volume
        installed_matches.append({'part': identifier, 'symmetric_difference_mm3': difference})
        if abs(difference) > .01:
            failures.append({'part': identifier, 'installed_difference_mm3': difference})
        shapes[identifier] = actual
with tempfile.TemporaryDirectory(prefix='manifold-eye-') as directory:
    for identifier, shape in shapes.items():
        if not shape.is_valid or len(shape.solids()) != 1:
            failures.append({'part': identifier, 'error': 'Invalid or disconnected solid', 'solids': len(shape.solids())})
            continue
        path = Path(directory) / f'{identifier}.step'
        cad.export_step(shape, path)
        restored = cad.import_step(path)
        if not restored.is_valid or len(restored.solids()) != 1 or abs(restored.volume - shape.volume) > max(.001, shape.volume * 1e-8):
            failures.append({'part': identifier, 'error': 'STEP round-trip mismatch'})
        else:
            roundtrips.append(identifier)
if whole_engine:
    cached = {}
    for occurrence in manifest['occurrences']:
        identifier = occurrence['id']
        if identifier in shapes:
            continue
        definition = occurrence['definition']
        if definition not in cached:
            step_path = ROOT / definitions[definition]['step'].lstrip('/')
            step_hashes[str(step_path)] = hashlib.sha256(step_path.read_bytes()).hexdigest()
            cached[definition] = cad.import_step(step_path)
        shapes[identifier] = locations[identifier] * cached[definition]
bounds = {identifier: shape.bounding_box() for identifier, shape in shapes.items()}
checks = 0
for (first_id, first), (second_id, second) in itertools.combinations(shapes.items(), 2):
    if first_id not in candidate_ids and second_id not in candidate_ids:
        continue
    first_box, second_box = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= 1e-6 for axis in 'XYZ'):
        continue
    common = first.intersect(second)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    checks += 1
    if volume > .01:
        failures.append({'first': first_id, 'second': second_id, 'overlap_mm3': volume})
contacts = []
for first_id, second_id in [('front-manifold-lifting-eye', 'exhaust-front'),
                            ('front-manifold-lifting-eye', 'front-manifold-stud13'),
                            ('front-manifold-lifting-eye', 'front-manifold-bolt14')]:
    distance = shapes[first_id].distance_to(shapes[second_id])
    contacts.append({'first': first_id, 'second': second_id, 'distance_mm': distance})
    if distance > 1e-6:
        failures.append({'first': first_id, 'second': second_id, 'missing_contact_mm': distance})
port_checks = []
for horizontal in [309.48, 195.688, 81.896]:
    path = cad.Bezier((horizontal, -138, 277.5), (horizontal, -188, 277.5),
                      (horizontal, -180, 258), (horizontal, -180, 235))
    bore = cad.Wire([cad.Line((horizontal, -125, 277.5), path @ 0), path,
                     cad.Line(path @ 1, (horizontal, -180, 225))])
    probe = cad.sweep(cad.Plane(origin=bore @ 0, z_dir=bore % 0) * cad.Circle(14.99), path=bore)
    if rectangular:
        probe = exhaust_front_profile.runner_void(horizontal, shrink=.05)
    common = shapes['exhaust-front'].intersect(probe)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    port_checks.append({'port_x_mm': horizontal, 'obstruction_mm3': volume})
    if volume > .01:
        failures.append({'port_x_mm': horizontal, 'obstruction_mm3': volume})
interface_checks = []
for station, (horizontal, vertical) in candidate.STATIONS.items():
    def cylinder(radius, first, last):
        return candidate.axis_y(radius, first, last, horizontal, vertical)

    def annulus(outer, inner, first, last):
        return cylinder(outer, first, last) - cylinder(inner, first - 1, last + 1)

    foot = shapes['front-manifold-lifting-eye'].intersect(cylinder(8, -148, -142))
    pad = shapes['exhaust-front'].intersect(cylinder(8, -144, -132))
    for role, first, second in [
            ('individual-foot-pad', foot, shapes['exhaust-front']),
            ('individual-foot-shoulder', foot, shapes['front-manifold-' + station]),
            ('individual-pad-head', pad, shapes['cylinder-head'])]:
        if not first or first.volume <= 0:
            failures.append({'station': station, 'role': role, 'missing_local_solid': True})
            continue
        distance = first.distance_to(second)
        interface_checks.append({'station': station, 'role': role, 'distance_mm': distance})
        if distance > 1e-6:
            failures.append({'station': station, 'role': role, 'gap_mm': distance})
    probes = [
        ('eye-foot', 'front-manifold-lifting-eye', annulus(6.5, 6, -146.99, -143.01), True),
        ('casting-pad', 'exhaust-front', annulus(6.5, 6, -142.99, -133.01), True),
        ('fastener-shoulder', 'front-manifold-' + station, annulus(6.5, 6, -152.99, -147.01), True),
        ('socket-wall', 'cylinder-head', annulus(5.4, 4.9, -132.99, -111.01), True),
        ('blind-floor', 'cylinder-head', cylinder(4.7, -110.99, -110.49), True),
        ('clear-socket', 'cylinder-head', cylinder(4.8, -132.99, -111.01), False)
    ]
    for role, identifier, probe, occupied in probes:
        common = shapes[identifier].intersect(probe)
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        error = abs(volume - (probe.volume if occupied else 0))
        interface_checks.append({'station': station, 'role': role, 'occupied': occupied,
                                 'probe_mm3': probe.volume, 'material_mm3': volume})
        if error > .001:
            failures.append({'station': station, 'role': role, 'material_error_mm3': error})
    control = cylinder(4.8, -132.99, -111.01)
    common = originals['cylinder-head'].intersect(control)
    control_volume = sum(solid.volume for solid in common.solids()) if common else 0
    interface_checks.append({'station': station, 'role': 'original-head-material-before-boss',
                             'probe_mm3': control.volume, 'material_mm3': control_volume})
assert manifest_path.read_bytes() == manifest_bytes
assert source_path.read_bytes() == source_bytes
assert profile_path.read_bytes() == profile_bytes
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest for path, digest in step_hashes.items())
report = {'passed': not failures, 'installed': installed, 'installed_matches': installed_matches, 'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
          'source_sha256': hashlib.sha256(source_bytes).hexdigest(), 'step_roundtrips': roundtrips,
          'rectangular_ports': rectangular, 'profile_sha256': hashlib.sha256(profile_bytes).hexdigest() if rectangular else None,
          'exact_checks': checks, 'failures': failures, 'contacts': contacts, 'exhaust_port_probes': port_checks,
          'mounting_interface_probes': interface_checks,
          'whole_engine_neighbors': whole_engine, 'step_hashes': step_hashes,
          'scope': 'Candidate validity, STEP roundtrip, interference, nominal shoulder/foot contact and front exhaust bore preservation. No production fit, threaded retention, preload or lifting strength certification.'}
filename = 'manifold-lifting-eye-neighbors-validation.json' if whole_engine else 'manifold-lifting-eye-initial-validation.json'
if installed:
    filename = 'manifold-lifting-eye-installed-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not failures
