"""Bind new runtime spring CAD to previously checked rest and peak assets."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import occurrence_shape,REVISION
from valve_spring_seating_candidate import INSTALLED
import cam_clockwise_candidate as cam
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[];inputs={}
for kind,peak in [('intake',468),('exhaust',246)]:
 for event,name in [(0,'rest'),(peak,'peak')]:
  path=R/'cad/engine/generated'/((kind+'-spring.step')if name=='rest' else ('timing-rocker-crest-candidate/'+kind+'-spring-peak.step'))
  old=b.import_step(path);o={'valvetrain':{'model':REVISION,'role':'spring','kind':kind,'cylinder':1}}
  new=occurrence_shape(o,old,event);bb=new.bounding_box();height=INSTALLED[kind]-max(0,cam.state(event,1,kind)['valve_lift'])
  assert new.is_valid and len(new.solids())==1
  volume_error=abs(new.volume-old.volume);bounds_error=max(abs(a-z)for a,z in zip([*bb.min,*bb.max],[*old.bounding_box().min,*old.bounding_box().max]))
  assert volume_error<.01 and bounds_error<1e-5 and abs(bb.min.Z)<1e-6 and abs(bb.max.Z-height)<1e-6
  rows.append({'kind':kind,'state':name,'height_mm':height,'frozen_asset_volume_difference_mm3':volume_error,'frozen_bounds_difference_mm':bounds_error,'faces':len(new.faces()),'frozen_faces':len(old.faces())});inputs[str(path.relative_to(R))]=sha(path)
for f in ['scripts/check-clockwise-spring-shapes.py','cad/engine/assembly_clockwise_candidate.py','cad/engine/valve_spring_seating_candidate.py','cad/engine/cam_clockwise_candidate.py']:inputs[f]=sha(R/f)
out={'status':'PASS actual runtime rest/peak CAD against frozen qualified springs','rows':rows,'bindings':inputs,'limits':['Bounds/volume and unchanged construction; not new full assembly collision proof','Estimated coil geometry, no factory rate or strength claim']}
(R/'inventory/engine/clockwise-spring-shape-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
