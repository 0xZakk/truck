"""Rebuild only the combined STEP from the manifest and current part STEP files."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
from assembly_math import transforms
from valvetrain_dispatch import occurrence_shape

path = ROOT / 'inventory/engine/full-assembly.json'
raw = path.read_bytes()
manifest = json.loads(raw)
locations = transforms(manifest)
shapes, hashes = {}, {}
for definition in manifest['definitions']:
    source = ROOT / definition['step'].lstrip('/')
    hashes[str(source.relative_to(ROOT))] = hashlib.sha256(source.read_bytes()).hexdigest()
    shapes[definition['id']] = b.import_step(source)
placed = []
for occurrence in manifest['occurrences']:
    shape = occurrence_shape(occurrence, shapes[occurrence['definition']], 0).moved(locations[occurrence['id']])
    shape.label = occurrence['id']
    placed.append(shape)
output = ROOT / 'cad/engine/generated/full-assembly.step'
temporary = output.with_name('full-assembly.pending.step')
b.export_step(b.Compound(children=placed), temporary, unit=b.Unit.MM)
assert path.read_bytes() == raw, 'Manifest changed during combined export'
assert all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest for name, digest in hashes.items())
temporary.replace(output)
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'part_step_hashes': hashes,
          'assembly_step_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
          'occurrences': len(placed), 'scope': 'Combined STEP regenerated from current part definitions and zero-angle poses'}
(ROOT / 'inventory/engine/combined-step-export.json').write_text(json.dumps(report, indent=2)+'\n')
print(f'Exported combined STEP: {len(placed)} occurrences', flush=True)
