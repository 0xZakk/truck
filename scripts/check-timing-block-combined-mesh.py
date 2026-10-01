"""Native composition export check, separate from frozen locality evidence."""
from pathlib import Path
import sys, json, hashlib
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import numpy as np
import trimesh
import timing_block_combined_candidate as c
OUT = ROOT / 'cad/engine/generated/timing-block-combined-candidate'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
proof = ROOT / 'inventory/engine/timing-block-combined-validation.json'
r = json.loads(proof.read_text())
inputs = dict(r['inputs'])
inputs[str(proof.relative_to(ROOT))] = sha(proof)
inputs[str(Path(__file__).relative_to(ROOT))] = sha(Path(__file__))
assert all(sha(ROOT / p) == h for p, h in inputs.items())
assert sha(OUT / 'block.step') == r['step_sha256']
q, _ = c.build()
vertices, faces = q.tessellate(.12, .15)
v = np.array([tuple(p) for p in vertices])
mesh = trimesh.Trimesh(v[:, [0, 2, 1]] * [1, 1, -1] / 1000, np.asarray(faces))
mesh.update_faces(mesh.nondegenerate_faces())
mesh.update_faces(mesh.unique_faces())
mesh.remove_unreferenced_vertices()
mesh.export(OUT / 'block.glb')
rt = trimesh.load(OUT / 'block.glb', force='mesh')
rt.merge_vertices(digits_vertex=8)
v = np.asarray(rt.vertices)[:, [0, 2, 1]] * [1, -1, 1] * 1000
bb = q.bounding_box()
error = float(np.max(abs(np.array([v.min(0), v.max(0)]) - np.array([list(bb.min), list(bb.max)]))))
gates = {'native_valid_single': q.is_valid and len(q.solids()) == 1,
         'watertight': bool(rt.is_watertight), 'bounds': error < .15}
assert all(sha(ROOT / p) == h for p, h in inputs.items())
report = {'status': 'PASS' if all(gates.values()) else 'FAIL', 'gates': gates,
          'input_sha256': inputs, 'mesh_origin': 'native composed CAD, no STEP healing',
          'bounds_error_mm': error, 'triangles': len(rt.faces),
          'mesh_sha256': sha(OUT / 'block.glb'),
          'remaining': ['Actual mesh visual review pending', 'Front block/cover conflict', 'Not installed', 'Browser NOT RUN']}
(ROOT / 'inventory/engine/timing-block-combined-mesh-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
assert all(gates.values())
