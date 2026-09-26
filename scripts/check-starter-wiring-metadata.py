"""Verify wiring integration composition, metadata and unchanged geometry code."""
from pathlib import Path
import ast
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_motor as starter
import starter_solenoid as switch
import starter_explanations as explanations
import starter_wiring as wiring

source = ROOT / 'cad/engine/starter_wiring.py'
tree = ast.parse(source.read_text())
nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ('route', 'parts') or isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in ('ROUTES', 'CONTACTS', 'REPLACED') for target in node.targets)]
geometry_hash = hashlib.sha256(ast.dump(ast.Module(body=nodes, type_ignores=[])).encode()).hexdigest()
assert geometry_hash == '169a2bbf99c58a1dc086c45a8a62a9ed150538bc3dfa6b9acfb2a46e3c51e0ab'
definitions, occurrences = {}, {}


def define(identifier, shape, name, function, system, color, sources, gaps, *args, **kwargs):
    assert identifier not in definitions, identifier
    definitions[identifier] = {'shape': shape, 'function': function, 'gaps': gaps, 'sources': sources}


def add(identifier, definition, parent, *args, **kwargs):
    assert identifier not in occurrences, identifier
    occurrences[identifier] = definition


def group(*args, **kwargs):
    return None


wrapped = wiring.api((define, add, group))
starter.build(explanations.api(switch.api(wrapped)))
switch.build(explanations.solenoid_api(wrapped))
wiring.build(wrapped)
assert len(definitions) == len(occurrences) == 124, (len(definitions), len(occurrences))
expected = wiring.parts()
for identifier in wiring.REPLACED:
    assert abs(definitions[identifier]['shape'].volume - expected[identifier].volume) < 1e-7, identifier
for identifier, metadata in definitions.items():
    if identifier.startswith('starter-solenoid-'):
        assert switch.GAPS[2] not in metadata['gaps'], identifier
        assert wiring.GAPS[2] in metadata['gaps'], identifier
        role = identifier.removeprefix('starter-solenoid-')
        if role in wiring.FUNCTIONS:
            assert metadata['function'] == wiring.FUNCTIONS[role], identifier
for closed in (False, True):
    circuit = wiring.circuit(closed)
    assert circuit['edges'] == switch.circuit(closed)['edges']
    assert not circuit['physical_wiring_complete']
    assert 'coil end leads' not in circuit['open_boundaries']
    assert 'motor brush feed at M' in circuit['open_boundaries']
    assert len(circuit['modeled_coil_interfaces']) == 4
lesson = json.loads((ROOT / 'inventory/engine/starter-wiring-learning.json').read_text())['starter-solenoid-assembly']
for step in lesson['steps'] + lesson['troubleshooting']:
    assert step['part'] in definitions, step
report = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'geometry_ast_sha256': geometry_hash,
          'geometry_validation_source_sha256': '0484e7556d098b869afe46bd698c74357dcf6fa01249a2dc0f5057259c43a3ca',
          'definitions': len(definitions), 'occurrences': len(occurrences), 'geometry_code_unchanged': True,
          'stale_coil_absence_removed': True, 'motor_feed_still_open': True, 'learning_part_targets_valid': True}
(ROOT / 'inventory/engine/starter-wiring-metadata-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
