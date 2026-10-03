from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';r={}
def volume(s):return sum(abs(t.volume) for t in s.solids()) if s else 0
for label in ['plus','minus']:
 old=b.import_step(OUT/label/'fuel-supply-rail.step');new=b.import_step(OUT/'r4'/label/'fuel-supply-rail.step');rows=[]
 for x in [-250,-40,220]:
  seat=b.Pos(x,-178,367)*b.Box(16,12,6);washer=b.Pos(x,-178,369.95)*b.Cylinder(7,.1);bore=b.Pos(x,-178,367)*b.Cylinder(3.39,6)
  aa=old&seat;cc=new&seat;diff=volume(aa-cc)+volume(cc-aa)
  aw=old&washer;cw=new&washer;wdiff=volume(aw-cw)+volume(cw-aw)
  root=b.Pos(x,-166,367)*b.Box(16,6,4);root_hit=new&root
  rows.append({'x':x,'full_seat_difference_mm3':diff,'washer_contact_difference_mm3':wdiff,'bore_unintended_solid_mm3':volume(new&bore),'root_material_mm3':volume(root_hit),'pass':diff<.1 and wdiff<.1 and volume(new&bore)<.1 and volume(root_hit)>1})
 # Shifted-frame control must reject a displaced full seat.
 mask=b.Pos(-250,-178,367)*b.Box(16,12,6);aa=old&mask;bad=(b.Pos(1,0,0)*new)&mask;negative=volume(aa-bad)+volume(bad-aa)
 r[label]={'rows':rows,'single_valid_fused_rail':new.is_valid and len(new.solids())==1,'shifted_frame_control_difference_mm3':negative,'shifted_frame_detected':negative>.1,'new_step_sha256':hashlib.sha256((OUT/'r4'/label/'fuel-supply-rail.step').read_bytes()).hexdigest()};print(label,r[label],flush=True)
(OUT/'r4/tab-check.json').write_text(json.dumps(r,indent=2)+'\n')
