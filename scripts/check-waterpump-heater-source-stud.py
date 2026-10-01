"""Resolve report-container error without discarding original neighbor audit."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import waterpump_heater_source_candidate as c
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());poses=transforms(m,0,0);o=next(x for x in m['occurrences']if x['id']=='front-manifold-stud13');d=next(x for x in m['definitions']if x['id']==o['definition']);p=R/d['step'].lstrip('/');q=c.O/'tube.step';hit=c.rear.norm(b.import_step(q).intersect(poses[o['id']]*occurrence_shape(o,b.import_step(p),0,0)));v=sum(abs(solid_volume(s,'adaptive'))for s in hit.solids());box=hit.bounding_box();wp=c.O/'tube__front-manifold-stud13.step';b.export_step(hit,wp)
r={'status':'FAIL actual tube neighbor'if v>.1 else'PASS original gate','neighbor':o['id'],'overlap_mm3':v,'bounds_mm':[list(box.min),list(box.max)],'solids':len(hit.solids()),'prior_report_error':'ShapeList bounding_box method unavailable; normalized to Compound. Original report retained.','inputs':{str(x.relative_to(R)):c.rear.sha(x)for x in [Path(__file__),mp,p,q]},'witness':str(wp.relative_to(R)),'witness_sha256':c.rear.sha(wp)};(R/'inventory/engine/waterpump-heater-source-stud.json').write_text(json.dumps(r,indent=2)+'\n');print(r,flush=True)
