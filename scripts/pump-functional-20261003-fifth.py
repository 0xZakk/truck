from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import pump_functional_20261003 as c
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.norm(s).solids())if s else 0.
h=b.import_step(c.O/'water-pump-housing.step')
y,z=c.EXTRA
start=np.array([386.,y-32,z+170]);end=np.array([386.,y*.78-32,z*.78+170])
probe=c.segment(.5,start,end)
r={'scope':'Existing unidentified fifth aperture to declared cavity, finite centerline witness; no production function assigned','obstruction_mm3':vol(probe.intersect(h)),'plug_control_mm3':vol(probe.intersect(b.Pos(*((start+end)/2))*b.Sphere(1))),'inputs':{}}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in[Path(__file__),Path(c.__file__),c.O/'water-pump-housing.step']:r['inputs'][str(p.relative_to(R))]=sha(p)
p=c.O/'region-fifth-connection-probe.step';b.export_step(probe,p);r['probe']={'path':str(p.relative_to(R)),'sha256':sha(p)}
(R/'reference/engine/pump-functional-20261003-fifth.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
