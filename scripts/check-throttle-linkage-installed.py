"""Bind the checked candidate geometry and motion contract to installed parts."""
from pathlib import Path
import hashlib
import argparse
import json
import sys
import build123d as b
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'cad/engine'))
from cad_metrics import solid_volume


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def difference(left, right):
    def vol(shape):
        return sum(solid_volume(s, 'adaptive') for s in shape.solids()) if shape else 0.
    return vol(left-right)+vol(right-left)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--spring', action='store_true')
parser.add_argument('--shield', action='store_true')
args = parser.parse_args()
assert not (args.spring and args.shield)
stem = 'throttle-return-spring' if args.spring else 'throttle-shield' if args.shield else 'throttle-linkage'
mp = ROOT/'inventory/engine/full-assembly.json'
raw = mp.read_bytes()
m = json.loads(raw)
defs = {d['id']: d for d in m['definitions']}
occs = {o['id']: o for o in m['occurrences']}
cp = ROOT/f'inventory/engine/{stem}-candidate-validation.json'
candidate = json.loads(cp.read_text())
installation = json.loads((ROOT/f'inventory/engine/{stem}-installation.json').read_text())
assert candidate['status'] == 'PASS'
assert installation['candidate_report_sha256'] == sha(cp)
if args.shield or args.spring:
    predecessor = installation['predecessor_installed_report']
    assert predecessor['status'] == 'PASS'
    assert predecessor['manifest_sha256'] == installation['before_manifest_sha256']
else:
    assert installation['before_manifest_sha256'] == candidate['input_hashes']['inventory/engine/full-assembly.json']
assert installation['after_manifest_sha256'] == sha(mp)
assert installation['assembly_frames_sha256'] == hashlib.sha256(json.dumps(m['assemblies'], sort_keys=True).encode()).hexdigest()
for old in installation['baseline_existing_occurrences']:
    for key in ('parent', 'position_cad_mm', 'rotation_cad_deg'):
        assert old.get(key) == occs[old['id']].get(key), (old['id'], key)
mapping = ({'accelerator-cable-bracket': 'accelerator-bracket-shield-hole-estimated'} if args.shield else
           {'throttle-shaft': 'throttle-shaft-keyed-estimated',
            'accelerator-cable-bracket': 'accelerator-bracket-offset-estimated'})
new_ids = (('throttle-linkage-shield-estimated', 'throttle-shield-pushpin-estimated') if args.shield else
           ('throttle-lever-estimated', 'throttle-cable-ball-stud-estimated', 'throttle-lever-retaining-pin-estimated'))
for key in new_ids:
    mapping[key] = key
    assert occs[key]['parent'] == ('throttle-assembly' if args.shield else 'throttle-moving')
    assert occs[key]['position_cad_mm'] == [0, 0, 0]
    assert occs[key].get('rotation_cad_deg', [0, 0, 0]) == [0, 0, 0]
if args.spring:
    mapping={'accelerator-cable-bracket':'bracket-spring-seat','throttle-lever-estimated':'lever-spring-seat','throttle-return-spring-illustrative':'spring-0'}
    occurrence=occs['throttle-return-spring-illustrative']
    assert occurrence['parent']=='throttle-assembly' and occurrence['position_cad_mm']==[0,0,0]
    assert occurrence['throttle_spring']['model']=='illustrative-single-v1'
checked = []
hashes = {}
for installed, study in mapping.items():
    expected = ROOT/f'cad/engine/generated/{stem}-candidate/{study}.step'
    assert sha(expected) == candidate['output_hashes'][str(expected.relative_to(ROOT))]
    actual = ROOT/defs[installed]['step'].lstrip('/')
    mesh_path = ROOT/defs[installed]['glb'].lstrip('/')
    for path in (expected, actual, mesh_path):
        hashes[str(path.relative_to(ROOT))] = sha(path)
    reference, shape = b.import_step(expected), b.import_step(actual)
    delta = difference(shape, reference)
    assert delta < .001, (installed, delta)
    fault = difference(shape.moved(b.Pos(1, 0, 0)), reference)
    assert fault > 1, (installed, 'shift control missed')
    mesh = trimesh.load(mesh_path, force='mesh')
    bounds = shape.bounding_box().size
    error = float(np.max(np.abs(mesh.extents*1000-np.array([bounds.X, bounds.Z, bounds.Y]))))
    assert error < .2, (installed, error)
    checked.append({'id': installed, 'symmetric_difference_mm3': delta,
                    'shifted_negative_control_mm3': fault, 'mesh_bounds_error_mm': error})
assert mp.read_bytes() == raw
assert all(sha(ROOT/p) == h for p, h in hashes.items())
result = {'status': 'PASS', 'manifest_sha256': sha(mp),
          'candidate_report_sha256': sha(cp), 'parts': checked, 'artifact_hashes': hashes,
          'scope': ('Installed geometry/frames match illustrative spring candidate checked at 11 travel poses.' if args.spring else 'Installed geometry/frames match the candidate checked across 46 local motion poses.')+' Whole-engine static, browser and production-fidelity acceptance remain separate.'}
(ROOT/f'inventory/engine/{stem}-installed-validation.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result['parts'], indent=2))
