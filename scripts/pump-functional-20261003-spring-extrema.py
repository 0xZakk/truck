from pathlib import Path
import json,numpy as np,trimesh,build123d as b
R=Path(__file__).resolve().parents[1];p=R/'cad/engine/generated/pump-height-20261002-ports-trial3/nominal-water-pump-seal-spring.glb';m=trimesh.load(p,force='mesh');v=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;s=b.import_step(R/'cad/engine/generated/pump-functional-20261003/water-pump-seal-spring.step')
r={}
for axis in range(3):
 for side,fun in [('min',np.argmin),('max',np.argmax)]:
  point=v[fun(v[:,axis])];r[str(axis)+side]={'point':point.tolist(),'distance_to_actual_step_mm':s.distance_to(b.Vertex(*point))};print(str(axis)+side,r[str(axis)+side],flush=True)
(R/'reference/engine/pump-functional-20261003-spring-extrema.json').write_text(json.dumps(r,indent=2)+'\n')
