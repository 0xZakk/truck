"""Frozen filter attachment, separated gallery and neighbor candidate audit."""
from pathlib import Path
import hashlib
import json
import math
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import oil_filter_adapter as adapter
from assembly_math import transforms

target = ROOT / 'inventory/engine/full-assembly.json'
raw = target.read_bytes()
manifest = json.loads(raw)
definitions = {definition['id']: b.import_step(ROOT / definition['step'].lstrip('/')) for definition in manifest['definitions']}
locations = transforms(manifest)
neighbors = {occurrence['id']: locations[occurrence['id']] * definitions[occurrence['definition']] for occurrence in manifest['occurrences']}
installed = '--installed' in sys.argv
block = neighbors['block'] if installed else adapter.block_interface(definitions['block'])
insert = neighbors['oil-filter-mounting-insert'] if installed else adapter.FRAME * adapter.insert()
with tempfile.TemporaryDirectory(prefix='filter-adapter-') as directory:
    for identifier, shape in {'block': block, 'insert': insert}.items():
        assert shape.is_valid and len(shape.solids()) == 1, (identifier, shape.is_valid, len(shape.solids()))
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        assert restored.is_valid and len(restored.solids()) == 1, identifier
        assert abs(restored.volume - shape.volume) < .02, identifier
print('Single-solid STEP validation PASS', flush=True)


def volume(shape):
    return sum(solid.volume for solid in shape.solids()) if shape else 0


inlet, outlet = adapter.FRAME * adapter.inlet_void(), adapter.FRAME * adapter.outlet_void()
assert len(inlet.solids()) == len(outlet.solids()) == 1
assert inlet.distance_to(outlet) > 15
assert volume(inlet & block) < .001
assert volume(outlet & block) < .001
assert volume(inlet & insert) < .001
assert volume(outlet & insert) < .001
assert insert.distance_to(neighbors['oil-filter-baseplate']) < .00001
assert block.distance_to(neighbors['oil-filter-gasket']) < .00001
land = adapter.FRAME * (adapter.cylinder(36, -.1, 0) - adapter.cylinder(31.5, -.2, .1))
assert abs(volume(land & block) - land.volume) < .001
for index in range(8):
    angle = math.tau * index / 8
    probe = adapter.FRAME * b.Pos(27 * math.cos(angle), 27 * math.sin(angle), 0) * adapter.cylinder(2.9, -3, 6)
    assert volume(probe & block) < .001
    assert volume(probe & neighbors['oil-filter-baseplate']) < .001
for boundary in adapter.gallery_boundaries().values():
    center = b.Vector(*boundary['center_cad_mm'])
    assert volume(b.Pos(center) * b.Sphere(.1) & block) < .001
print('Separated open galleries, all8inlets, insert/gasket contacts PASS', flush=True)

additions = block if installed else block - definitions['block']
if isinstance(additions, b.ShapeList):
    additions = b.Compound(children=additions)
checks, collisions = 0, []
block_identifier = 'block' if installed else 'filter-boss-added-material'
for first, shape in {block_identifier: additions, 'oil-filter-mounting-insert': insert}.items():
    first_box = shape.bounding_box()
    for second, neighbor in neighbors.items():
        if first == second:
            continue
        if second == 'block':
            neighbor = block
            if first == 'filter-boss-added-material':
                continue
        second_box = neighbor.bounding_box()
        if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .02 for axis in 'XYZ'):
            continue
        checks += 1
        overlap = volume(shape & neighbor)
        if overlap > .1:
            collisions.append({'first': first, 'second': second, 'volume_mm3': overlap})
assert target.read_bytes() == raw, 'Frozen manifest changed'
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/oil_filter_adapter.py').read_bytes()).hexdigest(),
          'valid_step_solids': ['modified-block', 'oil-filter-mounting-insert'],
          'inlet_outlet_separation_mm': inlet.distance_to(outlet), 'open_gallery_boundaries': adapter.gallery_boundaries(),
          'all_eight_filter_inlets_open': True, 'full_gasket_land_supported': True,
          'boolean_checks': checks, 'collisions': collisions,
          'scope': 'Static attachment and bounded galleries only; no full oil circuit or service-insert anti-drainback performance.'}
report_name = 'oil-filter-adapter-installed-validation.json' if installed else 'oil-filter-adapter-candidate-validation.json'
(ROOT / 'inventory/engine' / report_name).write_text(json.dumps(report, indent=2) + '\n')
assert not collisions, collisions
print('PASS filter adapter ' + ('installed' if installed else 'candidate'), flush=True)
