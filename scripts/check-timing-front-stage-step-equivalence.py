"""Strict material comparison of staged STEP restored through declared frames."""
from pathlib import Path
import json,sys,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from assembly_math import transforms
import timing_cover_seven_fastener_candidate as c
rp=R/'inventory/engine/timing-front-coordinated-stage-validation.json';r=json.loads(rp.read_text());mp=R/'inventory/engine/full-assembly.json';poses=transforms(json.loads(mp.read_text()));rows=[];errors={};paths=[rp,mp,Path(__file__)]
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(q)for q in s)
 total=0.
 for q in s.solids():
  for eps in[1e-9,1e-11,1e-13]:
   p=GProp_GProps();e=BRepGProp.VolumeProperties_s(q.wrapped,p,eps,True,False)
   if e<=1e-7:total+=abs(p.Mass());break
  else:raise ValueError(e)
 return total
for part in r['parts']:
 p=R/part['step'];sp=R/part['source_step'];paths.extend([p,sp]);s=b.import_step(sp);local=b.import_step(p);ident=part['id'];frame=poses[ident]if ident in ['block','timing-cover','oil-pan','oil-pan-molded-gasket']else(c.frame(*c.AXES[0])if ident=='timing-cover-mounting-screw'else b.Location());q=frame*local;row={'id':ident}
 for label,shape in [('added',q.cut(s)),('missing',s.cut(q))]:
  try:row[label+'_mm3']=vol(shape)
  except Exception as e:row[label+'_mm3']=None;errors[ident+label]=repr(e)
 rows.append(row);print(row,flush=True)
r={'rows':rows,'measurement_errors':errors,'status':'PASS strict restoredSTEP equivalence'if not errors and all(row['added_mm3']+row['missing_mm3']<1e-5 for row in rows)else'FAIL or NOT VERIFIED','input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'note':'Default whole-volume differences in stage report are serialization diagnostics; this independent Boolean material comparison retains strict1e-7integration/1e-5mm3difference gates.'};(R/'inventory/engine/timing-front-stage-step-equivalence.json').write_text(json.dumps(r,indent=2)+'\n')
