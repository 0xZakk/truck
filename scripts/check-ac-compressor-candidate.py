"""Validate FS10 study solids, discrete internal motion and frozen neighbors."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ac_compressor as candidate
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
local = candidate.components()
roundtrips = []
with tempfile.TemporaryDirectory(prefix='ac-compressor-') as temporary:
    for identifier, shape in local.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, shape.is_valid, len(shape.solids()))
        path = Path(temporary) / f'{identifier}.step'
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .02, identifier
        roundtrips.append(identifier)
        print('STEP valid', identifier, flush=True)

collisions = []
checks = 0
bounds = {}


def overlap(first_id, first, second_id, second, phase):
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
    common = first.intersect(second)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    if volume > .01:
        collisions.append({'a': first_id, 'b': second_id, 'phase': phase, 'volume_mm3': volume})


phases = [0] if '--static-only' in sys.argv else [0, 45, 90, 135, 180, 225, 270, 315]
for phase in phases:
    parts = {identifier: b.Pos(*candidate.POSITION) * shape for identifier, shape in local.items()} if phase == 0 else candidate.parts(phase)
    bounds.clear()
    for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
        if phase and not any('piston' in name or 'shoe' in name or 'swashplate' in name for name in (first_id, second_id)):
            continue
        overlap(first_id, first, second_id, second, phase)
    print('Phase', phase, 'checks', checks, 'collisions', collisions, flush=True)

if '--internal-only' not in sys.argv:
    parts = {identifier: b.Pos(*candidate.POSITION) * shape for identifier, shape in local.items()}
    bounds.clear()
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
            overlap(part_id, shape, occurrence['id'], installed, 0)
        if index % 200 == 0:
            print('Neighbor progress', index, flush=True)
    assert manifest_path.read_bytes() == raw

report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'step_roundtrips': roundtrips, 'checks': checks, 'collisions': collisions,
          'phases_degrees': phases, 'internal_only': '--internal-only' in sys.argv,
          'verified_production_fit': False, 'limits': candidate.GAPS}
filename = 'ac-compressor-internal-validation.json' if '--internal-only' in sys.argv else 'ac-compressor-candidate-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions
