from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_front_block_expanded_seat_v3_candidate as c
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate';paths=[OUT/'block.step',c.FROZEN];q,old=[b.import_step(p)for p in paths];rows=[]
for name,shape in [('added',q.cut(old)),('removed',old.cut(q))]:
 for i,s in enumerate(shape.solids()):
  bb=s.bounding_box();measurements=[]
  for eps in [1e-9,1e-11,1e-13]:
   props=GProp_GProps();err=BRepGProp.VolumeProperties_s(s.wrapped,props,eps,True,False);measurements.append({'requested':eps,'reported_error':err,'diagnostic_mass_not_accepted_if_unconverged':props.Mass()})
   if err<=1e-7:break
  row={'delta':name,'solid':i,'valid':s.is_valid,'bounds_mm':[list(bb.min),list(bb.max)],'conservative_box_volume_mm3':math.prod(bb.size),'measurements':measurements,'strict_converged':err<=1e-7};rows.append(row)
  if err>1e-7:b.export_step(s,OUT/f'{name}-unconverged-{i}.step')
r={'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(__file__)]},'solids':rows,'status':'Diagnostic only; no threshold relaxation or geometric healing'}
(ROOT/'inventory/engine/timing-front-v3-material-integration-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows,indent=2))
