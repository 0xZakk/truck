from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
p=R/'cad/engine/generated/pump-functional-20261003/water-pump-seal-spring.step';s=b.import_step(p);bb=s.bounding_box();lo=np.array(tuple(bb.min));hi=np.array(tuple(bb.max));center=(lo+hi)/2
r={'method':'BRep minimum distance to six remote planar1000mm square faces; all body bounds project inside each square. Exact CAD support extrema, no meshing, no tolerance change.','ordinary_optimal_bounds':[lo.tolist(),hi.tolist()],'support_bounds':[[],[]]}
for axis in range(3):
 for side in [0,1]:
  origin=center.copy();origin[axis]=(lo[axis]-100)if side==0 else(hi[axis]+100)
  direction=np.zeros(3);direction[axis]=1
  plane=b.Plane(origin=tuple(origin),z_dir=tuple(direction))*b.Rectangle(1000,1000)
  distance=s.distance_to(plane)
  coord=origin[axis]+distance if side==0 else origin[axis]-distance
  r['support_bounds'][side].append(float(coord));print(axis,side,coord,flush=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r['inputs']={str(p.relative_to(R)):sha(p),str(Path(__file__).relative_to(R)):sha(Path(__file__))}
(R/'reference/engine/pump-functional-20261003-spring-bounds.json').write_text(json.dumps(r,indent=2)+'\n')
