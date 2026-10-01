"""Compose a guarded private accessory stage; never modify the installed viewer."""
from pathlib import Path
import copy, hashlib, json, sys
import numpy as np
import trimesh
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'cad/engine'))
import build123d as cad
from cad_metrics import solid_volume
from assembly_clockwise_candidate import transforms
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
cp = R / 'inventory/engine/accessory-coordinated-stage-contract.json'
c = json.loads(cp.read_text())
for name, digest in c['input_sha256'].items():
    assert sha(R / name) == digest, name
mp = R / 'inventory/engine/corrected-engine-stage-v3.json'
assert sha(mp) == c['manifest_sha256']
base = json.loads(mp.read_text())
stage = copy.deepcopy(base)
tables = {k: {x['id']: x for x in stage[k]} for k in ['assemblies', 'occurrences', 'definitions']}
for k in tables:
    assert len(tables[k]) == len(stage[k]), k
for edit in c['pose_edits']:
    row = tables[edit['table']][edit['id']]
    assert row == edit['before'], edit['id']
    row.clear(); row.update(copy.deepcopy(edit['after']))
exports = []
for item in c['carrier_replacements']:
    name = item['id']; d = tables['definitions'][name]
    assert d == item['before_definition']
    assert tables['occurrences'][name] == item['before_occurrence']
    for asset in item['replacement_assets'].values():
        assert sha(R / asset['path']) == asset['sha256']
    sp = R / item['replacement_assets']['step']['path']
    gp = R / item['replacement_assets']['glb']['path']
    solid = cad.import_step(sp); mesh = trimesh.load(gp, force='mesh')
    mesh.merge_vertices(digits_vertex=8)
    vertices = np.asarray(mesh.vertices)[:, [0, 2, 1]] * [1, -1, 1] * 1000
    bb = solid.bounding_box()
    actual = np.array([tuple(bb.min), tuple(bb.max)])
    error = float(abs(np.array([vertices.min(0), vertices.max(0)]) - actual).max())
    assert solid.is_valid and len(solid.solids()) == 1
    assert mesh.is_watertight and mesh.is_winding_consistent and error < .1
    wording = 'Estimated accessory support prototype at inferred layout positions; factory casting shape and installed acceptance remain unresolved.'
    d.update(step='/' + str(sp.relative_to(R)), glb='/' + str(gp.relative_to(R)),
             function=wording, geometry_status='provisional',
             volume_mm3=solid_volume(solid), volume_method='default', solid_count=1,
             triangle_count=len(mesh.faces), model_bounds_mm=(actual[1]-actual[0]).tolist(),
             unresolved=copy.deepcopy(c['retained_failures']))
    tables['occurrences'][name]['function'] = wording
    exports.append({'id': name, 'step_sha256': sha(sp), 'glb_sha256': sha(gp),
                    'bounds_mm': actual.tolist(), 'bounds_error_mm': error,
                    'volume_mm3': d['volume_mm3'], 'triangle_count': len(mesh.faces)})
owner = {}
for group, ids in c['moving_occurrence_ownership'].items():
    for oid in ids:
        assert oid not in owner; owner[oid] = group

def matrix(location):
    tr = location.wrapped.Transformation()
    return np.array([[tr.Value(i,j) for j in range(1,5)] for i in range(1,4)])

def errors(candidate, state):
    before = transforms(base, **state); after = transforms(candidate, **state)
    result = {}
    for oid in before:
        wanted = matrix(before[oid])
        if oid in owner: wanted[:,3] += c['delta_world_mm'][owner[oid]]
        error = float(abs(matrix(after[oid]) - wanted).max())
        if error > 1e-8: result[oid] = error
    return result
states = c['verification']['states']
for state in states: assert not errors(stage, state)
bad = copy.deepcopy(stage)
for row in bad['occurrences']:
    if row['id'] == c['carrier_replacements'][0]['id']:
        row['position_cad_mm'] = c['delta_world_mm']['ALT']
control = errors(bad, states[0]); assert c['carrier_replacements'][0]['id'] in control
out = R / 'inventory/engine/corrected-engine-stage-v4.json'
report = R / 'inventory/engine/accessory-stage-v4-composition.json'
# Add explicit noninstallation metadata without modifying existing kinematics.
stage['accessory_candidate'] = {'contract': str(cp.relative_to(R)), 'status': 'PRIVATE CANDIDATE; not accepted or installed', 'retained_failures': c['retained_failures']}
out.write_text(json.dumps(stage, indent=2) + '\n')
report.write_text(json.dumps({'status': 'PASS guarded composition/export/frame checks only',
    'input_sha256': {str(cp.relative_to(R)): sha(cp), str(mp.relative_to(R)): sha(mp),
                     str(Path(__file__).relative_to(R)): sha(Path(__file__))},
    'stage_sha256': sha(out), 'exports': exports, 'guarded_pose_edits': len(c['pose_edits']),
    'frame_comparisons': len(base['occurrences'])*len(states), 'world_carrier_double_translation_control': control,
    'limits': ['Combined solid/contact/tool checks pending', 'No browser or factory fidelity acceptance', 'Canonical manifest unchanged']}, indent=2) + '\n')
print('WROTE PRIVATE V4', sha(out), exports, flush=True)
