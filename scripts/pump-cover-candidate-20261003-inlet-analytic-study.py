"""Independent analytical own-flow-axis experiment, no neighbor masks."""
from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_cover_candidate_20261003 as c
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):
 try:return sum(abs(solid_volume(q,'adaptive')) for q in c.norm(s).solids()) if s else 0
 except Exception as e:return {'status':'INCONCLUSIVE','error':str(e)}
p=c.O/'water-pump-housing.step';h=b.import_step(p);l=c.T*c.inlet(True);probe=c.T*c.inlet(probe=True);frame=c.T*b.Pos(0,-32,170)*b.Rot(-130,0,0)
a=np.array([397,35*c.G,6*c.G]);z=np.array([403,60*c.G,6*c.G]);v=z-a;L=np.linalg.norm(v)
def tube(radius):return frame*b.Solid.make_cylinder(radius,L,b.Plane(origin=a,z_dir=v))
t=tube(5);q=c.norm(h.cut(t));out=c.O/'housing-inlet-analytic-diagnostic.step';b.export_step(q,out)
r={'scope':'Frozen candidate, analytical first-span axis; radius5 is a diagnostic, not source-specified passage','input_sha256':sha(p),'script_sha256':sha(Path(__file__)),'source_module_sha256':sha(Path(c.__file__)),'tube_outside_declared_lumen':vol(t.cut(l)),'original_axis_R1_obstruction':vol(h.intersect(tube(1))),'original_axis_R5_obstruction':vol(h.intersect(t)),'after_axis_R1_obstruction':vol(q.intersect(tube(1))),'after_loft_probe_obstruction':vol(q.intersect(probe)),'valid':q.is_valid,'solids':len(q.solids()),'removed_stock':vol(h.cut(q)),'added_stock':vol(q.cut(h)),'path':str(out.relative_to(R)),'sha256':sha(out)}
(R/'reference/engine/pump-cover-candidate-20261003-inlet-analytic-study.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
