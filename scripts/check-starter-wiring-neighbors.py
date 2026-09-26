"""Frozen-manifest neighbor audit for the isolated coil attachment study."""
from pathlib import Path
import hashlib
import json
import math
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_wiring as wiring
from assembly_math import transforms

path = ROOT / 'inventory/engine/full-assembly.json'
raw = path.read_bytes()
manifest = json.loads(raw)
installed = '--installed' in sys.argv
definitions = {item['id']: b.import_step(ROOT / item['step'].lstrip('/')) for item in manifest['definitions']}
locations = transforms(manifest)
neighbors = {item['id']: locations[item['id']] * definitions[item['definition']] for item in manifest['occurrences'] if installed or item['definition'] not in wiring.REPLACED}
candidate = {identifier: starter.FRAME * shape for identifier, shape in wiring.parts().items()}
shape_checks = []
if installed:
    for identifier, expected in candidate.items():
        actual = neighbors[identifier]
        assert actual.is_valid and len(actual.solids()) == 1, identifier
        common = actual.intersect(expected)
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        volume_error = abs(actual.volume - expected.volume)
        difference = expected.volume + actual.volume - 2 * volume
        assert volume_error < .002 and abs(difference) < .002, (identifier, volume_error, difference)
        shape_checks.append({'id': identifier, 'volume_error_mm3': volume_error, 'symmetric_difference_mm3': difference})
    candidate = {identifier: neighbors[identifier] for identifier in candidate}
neighbors.update(candidate)
boxes = {identifier: shape.bounding_box() for identifier, shape in (neighbors | candidate).items()}
allowed = {frozenset(('starter-solenoid-lead-' + role, target)) for role, targets in wiring.CONTACTS.items() for target in targets}
shared = {frozenset(('starter-solenoid-lead-pull-s', 'starter-solenoid-lead-hold-s')),
          frozenset(('starter-solenoid-lead-insulation-pull-s', 'starter-solenoid-lead-insulation-hold-s'))}
insulating = {'starter-solenoid-' + role for role in ('winding-bobbin', 'bridge-insulator', 's-terminal-insulator', 'end-cap')}
insulating.update('starter-solenoid-lead-insulation-' + role for role in wiring.ROUTES)
conductors = {'starter-solenoid-lead-' + role for role in wiring.ROUTES}
clearances, clearance_checks = [], 0
checks, failures, contacts = 0, [], []
for first, shape in candidate.items():
    minimum_clearance, nearest_neighbor = math.inf, None
    for second, neighbor in neighbors.items():
        if first == second:
            continue
        first_box, second_box = boxes[first], boxes[second]
        pair = frozenset((first, second))
        if pair in shared:
            continue
        if first in conductors and second not in insulating and pair not in allowed:
            lower_bound = math.sqrt(sum(max(getattr(second_box.min, axis) - getattr(first_box.max, axis), getattr(first_box.min, axis) - getattr(second_box.max, axis), 0) ** 2 for axis in 'XYZ'))
            if lower_bound < minimum_clearance:
                clearance_checks += 1
                distance = shape.distance_to(neighbor)
                if distance < minimum_clearance:
                    minimum_clearance, nearest_neighbor = distance, second
                if distance < .01:
                    failures.append([first, second, 'unintended conductor clearance', distance])
        if any(min(getattr(first_box.max, axis), getattr(second_box.max, axis)) - max(getattr(first_box.min, axis), getattr(second_box.min, axis)) <= .0001 for axis in 'XYZ'):
            continue
        checks += 1
        common = shape.intersect(neighbor)
        volume = sum(solid.volume for solid in common.solids()) if common else 0
        if pair in allowed:
            contacts.append([first, second, volume])
        elif volume > .001:
            failures.append([first, second, volume])
    if first in conductors:
        assert nearest_neighbor is not None
        clearances.append({'lead': first, 'nearest_unintended_neighbor': nearest_neighbor, 'clearance_mm': minimum_clearance})
    print(first, checks, len(failures), flush=True)
assert path.read_bytes() == raw, 'Frozen manifest changed'
assert len(contacts) == 8 and all(item[2] > .001 for item in contacts), contacts
report = {'installed': installed, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/starter_wiring.py').read_bytes()).hexdigest(),
          'candidate_parts': len(candidate), 'checks': checks, 'contacts': contacts, 'failures': failures,
          'installed_shape_checks': shape_checks, 'clearance_checks': clearance_checks, 'conductor_clearances': clearances,
          'clearance_scope': 'Each coil-end conductor versus every installed neighbor except its declared winding/terminal/frame attachments, the shared S junction, and known solenoid dielectric parts. Other material-unknown neighbors are conservatively treated as conductive. AABB lower bounds prune exact distances without excluding a closer neighbor.',
          'boundary': 'Static full-engine neighbors; separate isolated validator samples seventeen solenoid/linkage poses. Production routing and complete motor electrical continuity remain unresolved.'}
filename = 'starter-wiring-installed-validation.json' if installed else 'starter-wiring-neighbors-validation.json'
(ROOT / 'inventory/engine' / filename).write_text(json.dumps(report, indent=2) + '\n')
assert not failures, failures
print('PASS frozen starter coil-lead neighbors', flush=True)
