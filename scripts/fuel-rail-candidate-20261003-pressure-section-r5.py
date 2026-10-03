from pathlib import Path
import json,build123d as b,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r5';gx=174.136;gy=-139
ids=['fuel-supply-rail','fuel-return-tube','regulator-lower-housing','regulator-upper-housing','regulator-diaphragm','regulator-gasket','regulator-inlet-screen','regulator-valve-seat','regulator-valve'];r={}
plane=b.Plane(origin=(gx,gy,385),x_dir=(1,0,0),z_dir=(0,-1,0))
for ident in ids:
 p=OUT/'plus'/(ident+'.step');shape=b.import_step(p);section=b.section(shape,section_by=plane)
 r[ident]={'step_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'polylines_r_z_mm':[[[v.X-gx,v.Z] for v in [edge.position_at(i/48) for i in range(49)]] for edge in section.edges()]}
(OUT/'pressure-section.json').write_text(json.dumps(r,indent=2)+'\n');print('Actual plus STEP section saved; minus identical relative internal frame')
