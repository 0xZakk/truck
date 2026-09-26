"""Frozen installed-neighbor audit across the prescribed starter engagement stroke."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
import starter_engagement as linkage
from assembly_math import transforms

path = ROOT / 'inventory/engine/full-assembly.json'
raw = path.read_bytes()
manifest = json.loads(raw)
baseline = starter.parts()
replaced = set(switch.parts()) | linkage.REPLACED | switch.REPLACED
definitions = {item['id']: b.import_step(ROOT / item['step'].lstrip('/')) for item in manifest['definitions']}
locations = transforms(manifest)
neighbors = {item['id']: locations[item['id']] * definitions[item['definition']] for item in manifest['occurrences'] if item['definition'] not in replaced}
boxes = {identifier: shape.bounding_box() for identifier, shape in neighbors.items()}
checks, failures = 0, []
for index in range(17):
    fraction = index / 16
    candidate = switch.parts(fraction)
    candidate.update(linkage.parts(fraction, baseline))
    for first, local in candidate.items():
        shape = starter.FRAME * local
        first_box = shape.bounding_box()
        for second, neighbor in neighbors.items():
            second_box = boxes[second]
            if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
                continue
            checks += 1
            common = shape.intersect(neighbor)
            overlap = sum(solid.volume for solid in common.solids()) if common else 0
            if overlap > .05:
                failures.append([fraction, first, second, overlap])
    print(fraction, checks, failures[-4:], flush=True)
assert path.read_bytes() == raw, 'Frozen manifest changed'
report = {'installed': False, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_engagement.py').read_bytes()).hexdigest(),
          'stroke_samples': 17, 'checks': checks, 'failures': failures,
          'boundary': 'Prescribed stroke and indexed flywheel phase only; no tooth-blocking or loaded performance simulation.'}
(ROOT / 'inventory/engine/starter-engagement-neighbors-validation.json').write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS frozen full-stroke starter neighbors', flush=True)
