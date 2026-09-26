"""Check full FS10 flow probes, manifold seats and blind-bolt isolation after the cap correction."""
import hashlib
import json
from pathlib import Path
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor_manifold_passages as candidate
from cad_metrics import step_comparison_shape
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
shapes = candidate.parts()
head_id = 'ac-compressor-rear-head'
expected = shapes[head_id]
head = step_comparison_shape(expected)
assert head.is_valid and len(head.solids()) == 1
artifact_hashes = {}
if '--installed' in sys.argv:
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    occurrences = {entry['id']: entry for entry in manifest['occurrences']}
    path = ROOT / definitions[occurrences[head_id]['definition']]['step'].lstrip('/')
    artifact_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
    head = b.import_step(path).moved(transforms(manifest)[head_id])
    normalized_expected = step_comparison_shape(expected)
    common = head.intersect(normalized_expected)
    assert common and abs(sum(solid.volume for solid in common.solids()) - head.volume) < .02
    assert abs(head.volume - normalized_expected.volume) < .02
shapes[head_id] = head
checks = 0
collisions = []


def overlap(first_id, first, second_id, second):
    global checks
    first_box, second_box = first.bounding_box(), second.bounding_box()
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .001 for axis in 'XYZ'):
        return
    checks += 1
    common = first.intersect(second)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    if volume > .01:
        collisions.append({'first': first_id, 'second': second_id, 'volume_mm3': volume})


networks = {role: step_comparison_shape(shape) for role, shape in candidate.motion.flow_networks().items()}
for role, network in networks.items():
    for identifier, shape in shapes.items():
        overlap(f'{role}-complete-network', network, identifier, shape)
    print('Complete network', role, flush=True)
for role, probe in candidate.manifold.passage_probes().items():
    for identifier, shape in shapes.items():
        overlap(f'{role}-manifold-port', probe, identifier, shape)
    assert probe.distance_to(networks[role]) < 1e-6
overlap('suction-network', networks['suction'], 'discharge-network', networks['discharge'])

bolt_socket = b.Pos(*candidate.POSITION) * b.Rot(0, 90, 0) * candidate.manifold.axial(3.19, 9.99, -91, *candidate.manifold.BOLT_CENTER)
for role, network in networks.items():
    overlap('blind-bolt-socket', bolt_socket, f'{role}-complete-network', network)
    assert bolt_socket.distance_to(network) > 2, role
floor = b.Pos(*candidate.POSITION) * b.Rot(0, 90, 0) * candidate.manifold.axial(3, 1, -85.5, *candidate.manifold.BOLT_CENTER)
common = head.intersect(floor)
assert common and abs(sum(solid.volume for solid in common.solids()) - floor.volume) < .01
for role in candidate.manifold.PORTS:
    seal = shapes[f'ac-compressor-manifold-{role}-seal']
    assert seal.distance_to(head) < 1e-6
    assert seal.distance_to(shapes['ac-compressor-rear-manifold']) < 1e-6
assert head.distance_to(shapes['ac-compressor-rear-manifold']) < 1e-6
for phase in range(0, 360, 45):
    for identifier, shape in candidate.parts(phase).items():
        if identifier != head_id:
            overlap(head_id, head, f'{identifier}@{phase}', shape)

if '--internal-only' not in sys.argv:
    poses = transforms(manifest)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    cache = {}
    for occurrence in manifest['occurrences']:
        if occurrence['id'].startswith('ac-compressor-'):
            continue
        definition = occurrence['definition']
        if definition not in cache:
            path = ROOT / definitions[definition]['step'].lstrip('/')
            artifact_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
            cache[definition] = b.import_step(path)
        overlap(head_id, head, occurrence['id'], cache[definition].moved(poses[occurrence['id']]))
    assert raw == (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
assert all(hashlib.sha256(path.read_bytes()).hexdigest() == digest for path, digest in artifact_hashes.items())
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'candidate_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'exact_checks': checks, 'collisions': collisions, 'full_networks_checked': list(networks),
          'blind_socket_floor_mm': -86, 'nominal_wall_to_physical_cap_drill_mm': 2,
          'installed': '--installed' in sys.argv, 'internal_only': '--internal-only' in sys.argv,
          'production_fit_verified': False}
suffix = '-installed' if '--installed' in sys.argv else '-internal' if '--internal-only' in sys.argv else ''
(ROOT / f'inventory/engine/ac-compressor-manifold-passages{suffix}-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
