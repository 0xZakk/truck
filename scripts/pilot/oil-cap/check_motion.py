"""Audit candidate cap against all installed rockers through the shared motion API.

Read-only on assembly inputs. Requires restored generated STEP baseline. Exit 1
means a detected clearance failure; retention is explicitly a separate open gate.
"""
from pathlib import Path
import hashlib
import json
import math
import platform
import sys
import importlib.metadata
import build123d as b

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT/'cad/engine'), str(ROOT/'cad/engine/pilot/oil-cap')]
from assembly_math import transforms
from oil_cap import POSITION

OUT = ROOT/'inventory/engine/pilot/oil-cap/motion-validation.json'
manifest_path = ROOT/'inventory/engine/full-assembly.json'
m = json.loads(manifest_path.read_text())
defs = {d['id']: d for d in m['definitions']}
rockers = [o for o in m['occurrences'] if o.get('valvetrain', {}).get('role') == 'rocker']
assert len(rockers) == 12, 'Expected all twelve installed rocker motion records'
paths = {ROOT/'cad/engine/pilot/oil-cap/oil-filler-cap.step', manifest_path, Path(__file__)}
# Include transitive motion implementation: changes invalidate this report.
paths.update(ROOT/'cad/engine'/name for name in [
    'assembly_math.py', 'valvetrain_dispatch.py', 'valve_source_integration.py',
    'valve_source_layout.py', 'valve_layout_integration.py', 'valve_layout_candidate.py',
    'valve_motion_candidate.py', 'valve_dimensions_candidate.py',
    'valve_spring_seating_candidate.py'])
paths.add(ROOT/'cad/engine/pilot/oil-cap/oil_cap.py')
cap = b.Pos(*POSITION)*b.import_step(ROOT/'cad/engine/pilot/oil-cap/oil-filler-cap.step')
shapes = {}
for o in rockers:
    p = ROOT/defs[o['definition']]['step'].lstrip('/')
    paths.add(p)
    if o['definition'] not in shapes:
        shapes[o['definition']] = b.import_step(p)

input_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}

# Shared motion uses firing order [1,5,3,6,2,4], support +/-135deg,
# intake peak468deg / exhaust246deg; include exact extrema and boundaries.
angles = set(range(0, 721, 5))
for phase in range(0, 720, 120):
    for center in (246, 468):
        for delta in (-135, 0, 135):
            angles.add((phase+center+delta) % 720)
angles = sorted(angles)
rocker_manifest = dict(m, occurrences=rockers)
for angle in (0, 246, 468, 720):
    full, focused = transforms(m, angle), transforms(rocker_manifest, angle)
    for o in rockers:
        assert full[o['id']].to_tuple() == focused[o['id']].to_tuple(), 'Focused transform mismatch'


def volume(shape):
    return sum(s.volume for s in shape.solids()) if shape else 0.

def bound_distance(a, c):
    aa, cc = a.bounding_box(), c.bounding_box()
    return math.sqrt(sum(max(0., tuple(aa.min)[i]-tuple(cc.max)[i],
                                  tuple(cc.min)[i]-tuple(aa.max)[i])**2 for i in range(3)))

failures = []
checks = []
broad = 0
for angle in angles:
    poses = transforms(rocker_manifest, angle)
    for o in rockers:
        s = poses[o['id']]*shapes[o['definition']]
        bound = bound_distance(cap, s)
        if bound > 15:
            broad += 1
            continue
        distance = cap.distance_to(s)
        overlap = volume(cap & s) if distance < .002 else 0.
        result = {'crank_deg': angle, 'rocker': o['id'], 'distance_mm': distance,
                  'overlap_mm3': overlap}
        checks.append(result)
        if overlap > .1 or distance < .002:
            failures.append(result)
    print(f'Checked crank {angle} degrees', flush=True)
assert checks, 'No nearby rocker checks executed'
closest = min(checks, key=lambda v: v['distance_mm'])
o = next(o for o in rockers if o['id'] == closest['rocker'])
s = transforms(m, closest['crank_deg'])[o['id']]*shapes[o['definition']]
# Lower the installed cap 10mm into its closest rocker. A fixed, relevant bad
# installation should trigger the same geometric overlap/contact criterion.
bad = b.Pos(0, 0, -10)*cap
negative_overlap = volume(bad & s)
negative_distance = bad.distance_to(s)
negative = {'cap_offset_cad_mm': [0,0,-10], 'rocker': o['id'],
            'crank_deg': closest['crank_deg'], 'overlap_mm3': negative_overlap,
            'distance_mm': negative_distance, 'detected': negative_overlap > .1}
assert negative['detected'], 'Collision checker failed its negative control'
assert input_hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}, 'Inputs changed during audit; rerun against a frozen revision'
report = {
    'status': 'FAIL' if failures else 'PASS_SAMPLED_CLEARANCE',
    'retention_status': 'FAIL: smooth cover bore cannot retain male screw cap',
    'environment': {'python': platform.python_version(), 'platform': platform.platform(),
                    'build123d': importlib.metadata.version('build123d')},
    'thresholds': {'overlap_mm3': .1, 'clearance_numerical_floor_mm': .002,
                   'broadphase_distance_mm': 15, 'maximum_crank_step_deg': 5},
    'crank_degrees': angles, 'rocker_count': len(rockers),
    'exact_pairs': len(checks), 'aabb_separated_pairs': broad,
    'closest': closest, 'negative_control': negative, 'failures': failures,
    'limits': ['Sampled sweep only; not a continuous clearance proof or production tolerance stack.',
               'Reuses installed educational motion law, not a measured factory cam curve.',
               'Cap kept fixed; retention, seal compression and threaded disassembly remain unvalidated.',
               'Tests cap body vs all rockers; other moving hardware and whole assembly require integration review.'],
    'hashes': input_hashes,
    'samples': checks,
}
OUT.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k: report[k] for k in ['status','exact_pairs','aabb_separated_pairs','closest','negative_control']}, indent=2))
sys.exit(1 if failures else 0)
