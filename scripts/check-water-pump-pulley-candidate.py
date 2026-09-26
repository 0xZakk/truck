"""Check pulley candidate solids and neighbors against an unchanged manifest."""
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import water_pump_pulley as candidate
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
manifest_raw = manifest_path.read_bytes()
manifest = json.loads(manifest_raw)
poses = transforms(manifest)
definitions = {definition['id']: definition for definition in manifest['definitions']}
parts = candidate.parts()
checks = 0
collisions = []
roundtrips = []
cache = {}


def overlap(first_id, first, second_id, second):
    global checks
    first_box, second_box = first.bounding_box(), second.bounding_box()
    if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) -
           max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
        return
    checks += 1
    intersection = first.intersect(second)
    volume = sum(solid.volume for solid in intersection.solids()) if intersection else 0
    if volume > .01:
        collisions.append({'a': first_id, 'b': second_id, 'volume_mm3': volume})


with tempfile.TemporaryDirectory(prefix='water-pump-pulley-') as temporary:
    for part_id, shape in parts.items():
        assert shape.is_valid and len(shape.solids()) == 1, part_id
        destination = Path(temporary) / f'{part_id}.step'
        b.export_step(shape, destination)
        imported = b.import_step(destination)
        assert imported.is_valid and len(imported.solids()) == 1, part_id
        assert abs(imported.volume - shape.volume) < .01, part_id
        roundtrips.append(part_id)
        print('STEP valid', part_id, flush=True)

for occurrence in manifest['occurrences']:
    if occurrence['id'] in parts:
        continue
    definition_id = occurrence['definition']
    if definition_id not in cache:
        cache[definition_id] = b.import_step(ROOT / definitions[definition_id]['step'].lstrip('/'))
    installed = cache[definition_id].moved(poses[occurrence['id']])
    for part_id, shape in parts.items():
        overlap(part_id, shape, occurrence['id'], installed)

for (first_id, first), (second_id, second) in itertools.combinations(parts.items(), 2):
    overlap(first_id, first, second_id, second)

assert manifest_path.read_bytes() == manifest_raw, 'Installed manifest changed during candidate checks'
report = {
    'installed': False,
    'verified_production_fit': False,
    'manifest_sha256': hashlib.sha256(manifest_raw).hexdigest(),
    'source_sha256': hashlib.sha256((ROOT / 'cad/engine/water_pump_pulley.py').read_bytes()).hexdigest(),
    'step_roundtrips': roundtrips,
    'checks': checks,
    'collisions': collisions,
    'belt_plane': {'candidate_mm': candidate.BELT_CENTER_X, 'existing_groove_mean_mm': 473.56,
                   'axial_delta_mm': candidate.BELT_CENTER_X - 473.56,
                   'status': 'Assumed dish offset, not a measured alignment'},
    'limits': candidate.GAPS
}
(ROOT / 'inventory/engine/water-pump-pulley-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
assert not collisions, 'Candidate contains solid overlaps'
