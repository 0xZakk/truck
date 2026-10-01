"""Independent conservative bound for the preserved failed adaptive pair."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import waterpump_source_offset_inlet_candidate as c
from assembly_clockwise_candidate import transforms,occurrence_shape
mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());poses=transforms(m,0,0);o=next(x for x in m['occurrences']if x['id']=='alternator-thermactor-common-carrier');d=next(x for x in m['definitions']if x['id']==o['definition']);p=R/d['step'].lstrip('/');q=c.O/'low-offset-housing.step';h=b.import_step(q).intersect(poses[o['id']]*occurrence_shape(o,b.import_step(p),0,0));box=h.bounding_box();v=box.size.X*box.size.Y*box.size.Z;w=c.O/'low-offset__carrier-residual.step';b.export_step(h,w)
r={'status':'PASS conservative original0.1mm3 gate'if v<.1 else'NOT VERIFIED original0.1mm3 gate','adaptive_failure_preserved':'waterpump-source-offset-inlet-neighbors.json','bounds_mm':[list(box.min),list(box.max)],'conservative_bbox_volume_bound_mm3':v,'diagnostic_default_volume_mm3':sum(abs(s.volume)for s in h.solids()),'claim':'Bounding box product is an upper bound, not measured overlap volume. Default volume is diagnostic only.','inputs':{str(x.relative_to(R)):c.rear.sha(x)for x in [Path(__file__),mp,p,q]},'witness':str(w.relative_to(R)),'witness_sha256':c.rear.sha(w)}
# Seek an independent finite interior cube; positive volume exceeds unchanged gate.
import numpy as np
rng=np.random.default_rng(44009);interior=None
for point in rng.uniform(tuple(box.min),tuple(box.max),(1000,3)):
 if h.is_inside(tuple(point),tolerance=1e-7):
  cube=b.Pos(*point)*b.Box(.6,.6,.6);missing=sum(abs(z.volume)for z in cube.cut(h).solids())
  if missing<1e-8:
   interior={'center_mm':point.tolist(),'cube_edge_mm':.6,'cube_volume_mm3':.216,'missing_from_intersection_mm3':missing};break
r['strict_interior_cube']=interior
if interior:r['status']='FAIL finite interior witness exceeds original0.1mm3 gate'
(R/'inventory/engine/waterpump-source-offset-residual.json').write_text(json.dumps(r,indent=2)+'\n');print(r,flush=True)
