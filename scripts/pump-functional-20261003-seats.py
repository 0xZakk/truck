from pathlib import Path
import sys,json,hashlib,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from cad_metrics import solid_volume
import pump_functional_20261003 as c
from water_pump_joint_candidate import MOUNTING,EXTRA
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.core.norm(s).solids())if s else 0.
inputs={};parts={}
for n in ['water-pump-housing','water-pump-drive-hub','water-pump-pulley']:
 p=c.O/(n+'.step');parts[n]=b.import_step(p);inputs[str(p.relative_to(R))]=sha(p)
h=parts['water-pump-housing'];old=b.import_step(c.core.REAR);window=b.Pos(189,-32,170)*b.Box(400,600,600);rearnew=h.intersect(window);rearold=old.intersect(window);foot=c.core.cx(66,375,389)
for y,z in [*MOUNTING,EXTRA]:foot=foot.fuse(b.Pos(0,y,z)*c.core.cx(11.5,375,389))
face=473.43;thin=c.core.cx(35,face,face+.001).cut(c.core.cx(15.05,face-1,face+1))
for a in range(0,360,90):thin=thin.cut(b.Pos(0,25*math.cos(math.radians(a)),25*math.sin(math.radians(a)))*c.core.cx(3.5,face-1,face+1))
f=b.Compound([x for x in thin.faces()if x.geom_type==b.GeomType.PLANE and abs(x.center().X-face)<1e-5]);seats={}
for n in ['water-pump-drive-hub','water-pump-pulley']:
 op=BRepAlgoAPI_Cut(f.wrapped,b.Compound(list(parts[n].faces())).wrapped);op.Build();seats[n]={'area_mm2':f.area,'missing_mm2':b.Compound(op.Shape()).area,'done':op.IsDone()}
r={'hub_pulley_named_seat':seats,'entire_rear_slice_added_mm3':vol(rearnew.cut(rearold)),'entire_rear_slice_removed_mm3':vol(rearold.cut(rearnew)),'protected_joint_footprint_added_mm3':vol(c.core.norm(rearnew.cut(rearold)).intersect(foot)),'protected_joint_footprint_removed_mm3':vol(c.core.norm(rearold.cut(rearnew)).intersect(foot)),'limitation':'Initial contract said exact fullrearX<=389. Port additions are assessed explicitly; jointfootprint result does not erase broader failure. Inherited bearing outerR23.9 vsboreR24 andshaftR8 vsbearingbore8.05 leave estimated radialgaps; no pressed-fit support PASS.','inputs':{**inputs,str(c.core.REAR.relative_to(R)):sha(c.core.REAR),str(Path(__file__).relative_to(R)):sha(Path(__file__))}}
(R/'reference/engine/pump-functional-20261003-seats.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
