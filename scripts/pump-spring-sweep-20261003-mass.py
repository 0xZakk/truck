"""Adaptive B-spline mass integration; default values retained for comparison."""
import json,time,hashlib
from pathlib import Path
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
R=Path(__file__).resolve().parents[1];rows=[]
for name in ['cad/engine/generated/pump-functional-20261003/water-pump-seal-spring.step','cad/engine/generated/pump-spring-sweep-20261003/spring.step']:
 p=R/name;s=b.import_step(p);g=GProp_GProps();t=time.monotonic();error=BRepGProp.VolumePropertiesGK_s(s.wrapped,g,1e-8,True,True)
 rows.append({'step':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'default_volume':s.volume,'adaptive_volume':g.Mass(),'requested_relative_error':1e-8,'estimated_relative_error':error,'elapsed_seconds':time.monotonic()-t})
(R/'reference/engine/pump-spring-sweep-20261003-mass.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
