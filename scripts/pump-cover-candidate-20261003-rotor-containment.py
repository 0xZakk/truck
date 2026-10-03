from pathlib import Path
import sys,json,hashlib,math,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import pump_cover_candidate_20261003 as c
p=c.O/'water-pump-impeller.step';s=b.import_step(p);rotor=c.T*(c.cx(51,369,373).fuse(c.cx(math.hypot(48.5,1.5),372,384)).cut(c.cx(8.05,368,385)));print('ACTUAL CONTAINMENT START',flush=True);q=c.norm(s.cut(rotor));v=sum(abs(solid_volume(z,'adaptive'))for z in q.solids())if q else 0.
center=(c.T*b.Vertex(0,-32,170)).center();wrong=(c.T*b.Vertex(*tuple(center))).center();error=float(np.linalg.norm(np.array(tuple(center))[1:]-[c.Y,c.Z]));wrongerr=float(np.linalg.norm(np.array(tuple(wrong))[1:]-[c.Y,c.Z]));r={'actual_impeller_outside_exact_swept_envelope_mm3':v,'fresh_actual_STEP':True,'single_transform_axis_error_mm':error,'wrong_double_transform_control_error_mm':wrongerr,'control_status':'PASS'if error<1e-8 and wrongerr>1 else'FAIL','inputs':{str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest()for x in [p,Path(__file__),Path(c.__file__)]}};(R/'reference/engine/pump-cover-candidate-20261003-rotor-containment.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
