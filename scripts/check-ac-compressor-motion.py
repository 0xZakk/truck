"""Check revised FS10 geometry, separated routes and rigid-motion descriptors."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor_motion as candidate
import ac_compressor_bearing as bearing
import ac_compressor_manifold as manifold_geometry
import ac_compressor_shaft_support as shaft_support
import ac_compressor_manifold_passages as manifold_passages
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
installed_mode = '--installed' in sys.argv
geometry = manifold_passages if '--passages' in sys.argv else shaft_support if '--shaft-support' in sys.argv else manifold_geometry if '--manifold' in sys.argv else bearing if '--bearing' in sys.argv else candidate
expected_count = 67 if '--passages' in sys.argv or '--shaft-support' in sys.argv else 65 if '--manifold' in sys.argv else 61
local_parts = geometry.home_components()
installed_occurrences = []
if installed_mode:
    identifiers = set(local_parts)
    installed_occurrences = [entry for entry in manifest['occurrences'] if entry['id'] in identifiers]
    used = {entry['definition'] for entry in installed_occurrences}
    local_parts = {entry['id']: b.import_step(ROOT / entry['step'].lstrip('/'))
                   for entry in manifest['definitions'] if entry['id'] in used}
    assert len(installed_occurrences) == len(local_parts) == expected_count


def posed_parts(phase=0):
    if not installed_mode:
        return geometry.parts(phase)
    poses = transforms(manifest, compressor_degrees=phase)
    return {entry['id']: local_parts[entry['definition']].moved(poses[entry['id']])
            for entry in installed_occurrences}


parts = posed_parts()
roundtrips = []
with tempfile.TemporaryDirectory(prefix='fs10-motion-') as temporary:
    for identifier, shape in local_parts.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, shape.is_valid, len(shape.solids()))
        path = Path(temporary) / f'{identifier}.step'
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .02, identifier
        roundtrips.append(identifier)
        print('STEP', identifier, flush=True)

bounds = {}
checks = 0
collisions = []


def common_volume(first, second):
    common = first.intersect(second)
    return sum(solid.volume for solid in common.solids()) if common else 0


def overlap(first_id, first, second_id, second, category):
    global checks
    if first_id not in bounds:
        bounds[first_id] = first.bounding_box()
    if second_id not in bounds:
        bounds[second_id] = second.bounding_box()
    first_box, second_box = bounds[first_id], bounds[second_id]
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
        return
    checks += 1
    volume = common_volume(first, second)
    if volume > .01:
        collisions.append({'a': first_id, 'b': second_id, 'category': category, 'volume_mm3': volume})


phases = [0] if '--static-only' in sys.argv else list(range(0, 360, 45))
for phase in phases:
    moving = posed_parts(phase)
    bounds.clear()
    for (first_id, first), (second_id, second) in itertools.combinations(moving.items(), 2):
        if phase and not any(candidate.descriptor(identifier) for identifier in (first_id, second_id)):
            continue
        overlap(first_id, first, second_id, second, f'phase-{phase}')
    print('Phase', phase, 'checks', checks, 'collisions', collisions, flush=True)

bounds.clear()
networks = candidate.flow_networks()
for label, network in networks.items():
    assert network.is_valid and len(network.solids()) == 1, (label, len(network.solids()))
    for identifier, shape in parts.items():
        overlap(label, network, identifier, shape, 'open-passage')
overlap('suction', networks['suction'], 'discharge', networks['discharge'], 'short-circuit')
reed_tests = []
for label, (reed_id, probe) in candidate.valve_probes().items():
    blocked_volume = common_volume(probe, parts[reed_id])
    assert blocked_volume > .5, (label, blocked_volume)
    for identifier, shape in parts.items():
        if identifier != reed_id:
            overlap(label, probe, identifier, shape, 'reed-window-cleared')
    reed_tests.append({'probe': label, 'seated_reed_mm3': blocked_volume})
print('Flow checks', checks, 'collisions', collisions, flush=True)

if '--internal-only' not in sys.argv:
    definitions = {definition['id']: definition for definition in manifest['definitions']}
    poses = transforms(manifest)
    cache = {}
    for index, occurrence in enumerate(manifest['occurrences']):
        if occurrence['id'] in parts:
            continue
        identifier = occurrence['definition']
        if identifier not in cache:
            cache[identifier] = b.import_step(ROOT / definitions[identifier]['step'].lstrip('/'))
        installed = cache[identifier].moved(poses[occurrence['id']])
        for part_id, shape in parts.items():
            overlap(part_id, shape, occurrence['id'], installed, 'installed')
        if index % 200 == 0:
            print('Neighbor', index, flush=True)
    assert manifest_path.read_bytes() == raw

report = {'installed': installed_mode, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256(Path(geometry.__file__).read_bytes()).hexdigest(),
          'base_sha256': hashlib.sha256(Path(candidate.base.__file__).read_bytes()).hexdigest(),
          'step_roundtrips': roundtrips, 'phases': phases, 'checks': checks, 'collisions': collisions,
          'connected_probe_networks': list(networks), 'seated_reed_tests': reed_tests,
          'internal_only': '--internal-only' in sys.argv, 'production_fit': False, 'limits': list(dict.fromkeys(candidate.GAPS + geometry.GAPS))}
filename = 'ac-compressor-motion-internal-validation.json' if '--internal-only' in sys.argv else 'ac-compressor-motion-validation.json'
if installed_mode:
    filename = 'ac-compressor-motion-installed-clearance-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
