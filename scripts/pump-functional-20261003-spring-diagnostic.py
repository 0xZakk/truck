from pathlib import Path
import json,hashlib,numpy as np,trimesh
R=Path(__file__).resolve().parents[1];p=R/'cad/engine/generated/pump-height-20261002-ports-trial3/nominal-water-pump-seal-spring.glb';m=trimesh.load(p,force='mesh');m.vertices=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
support=json.loads((R/'reference/engine/pump-functional-20261003-spring-bounds.json').read_text())['support_bounds']
r={'scope':'Historical original GLB diagnostics only; no accepted new spring asset','historical_vertices':len(m.vertices),'historical_faces':len(m.faces),'support_bounds_error_mm':float(np.max(abs(m.bounds-support))),'trials':[]}
for digits in [6,5,4]:
 q=m.copy();q.merge_vertices(digits_vertex=digits);counts=np.bincount(q.edges_unique_inverse)
 r['trials'].append({'merge_digits_mm':digits,'vertices':len(q.vertices),'watertight':q.is_watertight,'winding':q.is_winding_consistent,'boundary_edges':int(sum(counts==1)),'nonmanifold_edges':int(sum(counts>2)),'degenerate_faces':int(sum(~q.nondegenerate_faces()))})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r['inputs']={str(p.relative_to(R)):sha(p),str(Path(__file__).relative_to(R)):sha(Path(__file__))}
(R/'reference/engine/pump-functional-20261003-spring-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
