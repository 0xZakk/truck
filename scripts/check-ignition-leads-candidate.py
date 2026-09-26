"""Validate insulated lead continuity, firing topology and installed clearances."""
from pathlib import Path
import hashlib
import itertools
import json
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import ignition_leads as leads
from assembly_math import transforms

raw = (ROOT / 'inventory/engine/full-assembly.json').read_bytes()
manifest = json.loads(raw)
locations = transforms(manifest)
definitions = {definition['id']: b.import_step(ROOT / definition['step'].lstrip('/')) for definition in manifest['definitions']}
print('Loaded frozen neighbors', flush=True)
candidates = leads.parts()
candidates['distributor-cap'] = locations['distributor-cap'] * leads.cap_interface(definitions['distributor-cap'])
candidates['cylinder-head'] = locations['cylinder-head'] * leads.head_interface(definitions['cylinder-head'])
invalid = []
with tempfile.TemporaryDirectory(prefix='ignition-leads-') as directory:
    for identifier, shape in candidates.items():
        if not shape.is_valid or len(shape.solids()) != 1:
            invalid.append({'id': identifier, 'valid': shape.is_valid, 'solids': len(shape.solids())})
            continue
        path = Path(directory) / (identifier + '.step')
        b.export_step(shape, path)
        restored = b.import_step(path)
        if not restored.is_valid or len(restored.solids()) != 1:
            invalid.append({'id': identifier, 'step_valid': restored.is_valid, 'step_solids': len(restored.solids())})
print('STEP audit', invalid, flush=True)
neighbors = {occurrence['id']: locations[occurrence['id']] * definitions[occurrence['definition']]
             for occurrence in manifest['occurrences'] if occurrence['id'] not in candidates}
boxes = {identifier: shape.bounding_box() for identifier, shape in (candidates | neighbors).items()}
sections = {}
for cylinder_number in range(1, 7):
    prefix = f'ignition-lead-{cylinder_number}'
    sections[prefix + '-jacket'] = sections[prefix + '-carbon-core'] = [edge.bounding_box() for edge in leads.plug_path(cylinder_number).edges()]
sections['ignition-coil-lead-jacket'] = sections['ignition-coil-lead-carbon-core'] = [edge.bounding_box() for edge in leads.coil_path().edges()]
collisions = []
checks = 0


def overlap_boxes(first, second, padding=0):
    return all(min(getattr(first.max, axis) + padding, getattr(second.max, axis)) -
               max(getattr(first.min, axis) - padding, getattr(second.min, axis)) > .02 for axis in 'XYZ')


def check_pair(first, second, first_shape, second_shape):
    global checks
    if not overlap_boxes(boxes[first], boxes[second]):
        return
    if first in sections and not any(overlap_boxes(section, boxes[second], 3.6) for section in sections[first]):
        return
    if second in sections and not any(overlap_boxes(section, boxes[first], 3.6) for section in sections[second]):
        return
    checks += 1
    overlap = first_shape.intersect(second_shape)
    volume = sum(solid.volume for solid in overlap.solids()) if overlap else 0
    if volume > .1:
        collision = {'first': first, 'second': second, 'volume_mm3': round(volume, 5)}
        collisions.append(collision)
        print('Collision', collision, flush=True)


for (first, first_shape), (second, second_shape) in itertools.combinations(candidates.items(), 2):
    check_pair(first, second, first_shape, second_shape)
for first, first_shape in candidates.items():
    if first in ('distributor-cap', 'cylinder-head'):
        continue
    for second, second_shape in neighbors.items():
        check_pair(first, second, first_shape, second_shape)
additions = candidates['cylinder-head'] - locations['cylinder-head'] * definitions['cylinder-head']
if isinstance(additions, b.ShapeList):
    additions = b.Compound(children=additions)
boxes['coil-mount-head-bosses'] = additions.bounding_box()
for identifier, shape in neighbors.items():
    check_pair('coil-mount-head-bosses', identifier, additions, shape)

inverse_mapping = {tower: cylinder_number for cylinder_number, tower in leads.TOWER_BY_CYLINDER.items()}
clockwise_towers = [1, 6, 5, 4, 3, 2]
assert tuple(inverse_mapping[tower] for tower in clockwise_towers) == leads.FIRING_ORDER
contacts = []
for cylinder_number in range(1, 7):
    prefix = f'ignition-lead-{cylinder_number}'
    path = leads.plug_path(cylinder_number)
    pairs = [(prefix + '-cap-contact', f'distributor-terminal-{leads.TOWER_BY_CYLINDER[cylinder_number]}'),
             (prefix + '-plug-contact', f'spark-plug-{cylinder_number}-terminal')]
    for contact, terminal in pairs:
        distance = candidates[contact].distance_to(neighbors[terminal])
        contacts.append({'contact': contact, 'terminal': terminal, 'distance_mm': distance})
        assert distance < 1e-5, (contact, distance)
    assert b.Vertex(path @ 0).distance_to(candidates[prefix + '-cap-contact']) < 1e-5
    assert b.Vertex(path @ 1).distance_to(candidates[prefix + '-plug-contact']) < 1e-5
for contact, terminal in [('ignition-coil-lead-cap-contact', 'distributor-coil-terminal'),
                          ('ignition-coil-lead-coil-contact', 'ignition-coil-hv-terminal')]:
    distance = candidates[contact].distance_to(neighbors[terminal])
    contacts.append({'contact': contact, 'terminal': terminal, 'distance_mm': distance})
    assert distance < 1e-5, (contact, distance)

assert (ROOT / 'inventory/engine/full-assembly.json').read_bytes() == raw
report = {'installed': False, 'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256((ROOT / 'cad/engine/ignition_leads.py').read_bytes()).hexdigest(),
          'candidate_count': len(candidates), 'invalid': invalid, 'boolean_checks': checks,
          'collisions': collisions, 'terminal_continuity': contacts, 'firing_order': leads.FIRING_ORDER,
          'tower_assignment': leads.TOWER_BY_CYLINDER,
          'cable_lengths_mm': {str(cylinder_number): leads.plug_path(cylinder_number).length for cylinder_number in range(1, 7)},
          'coil_cable_length_mm': leads.coil_path().length,
          'limits': leads.GAPS}
(ROOT / 'inventory/engine/ignition-leads-candidate-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
