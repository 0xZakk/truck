"""Frozen installed-neighbor audit for the open solenoid candidate."""
from pathlib import Path
import hashlib
import json
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
from assembly_math import transforms

path = ROOT / 'inventory/engine/full-assembly.json'
raw = path.read_bytes()
manifest = json.loads(raw)
installed = '--installed' in sys.argv
definitions = {item['id']: b.import_step(ROOT / item['step'].lstrip('/')) for item in manifest['definitions']}
locations = transforms(manifest)
neighbors = {item['id']: locations[item['id']] * definitions[item['definition']] for item in manifest['occurrences'] if installed or item['definition'] not in switch.REPLACED}
candidate = {identifier: starter.FRAME * shape for identifier, shape in switch.parts().items()}
if installed:
    assert 'starter-solenoid-coil-envelope' not in neighbors
    for identifier, expected in candidate.items():
        actual = neighbors[identifier]
        assert actual.is_valid and len(actual.solids()) == 1, identifier
        common = actual.intersect(expected)
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        assert abs(volume - expected.volume) < .02, (identifier, 'installed pose mismatch')
        assert abs(actual.volume - expected.volume) < .02, identifier
    candidate = {identifier: neighbors[identifier] for identifier in candidate}
boxes = {identifier: shape.bounding_box() for identifier, shape in (neighbors | candidate).items()}
checks, failures = 0, []
for first, shape in candidate.items():
    for second, neighbor in neighbors.items():
        if first == second:
            continue
        first_box, second_box = boxes[first], boxes[second]
        if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .01 for axis in 'XYZ'):
            continue
        checks += 1
        common = shape.intersect(neighbor)
        overlap = sum(solid.volume for solid in common.solids()) if common else 0
        if overlap > .05:
            failures.append([first, second, overlap])
    print(first, checks, len(failures), flush=True)
assert path.read_bytes() == raw, 'Frozen manifest changed'
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_solenoid.py').read_bytes()).hexdigest(),
          'candidate_parts': len(candidate), 'checks': checks, 'failures': failures,
          'boundary': 'Open static pose only. Isolated checker audits internal contacts through stroke, not complete engagement linkage.'}
filename = 'starter-solenoid-installed-validation.json' if installed else 'starter-solenoid-neighbors-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS frozen solenoid neighbors', flush=True)
