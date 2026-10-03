from pathlib import Path
import json,time,hashlib
import build123d as b
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/pump-spring-sweep-20261003';O.mkdir(exist_ok=True)
t=time.monotonic();segments=[]
for i in range(16):
 path=b.Rot(0,0,90*i)*b.Helix(1.4,.35,15.5,center=(0,0,.35*i))
 profile=b.Plane(origin=path@0,z_dir=path%0)*b.Circle(.4)
 segments.append(b.sweep(profile,path=path,is_frenet=True))
 print('segment',i,flush=True)
s=segments[0].fuse(*segments[1:]);print('fused',len(s.solids()),flush=True)
s=b.Pos(14.95,0,0)*b.Rot(0,90,0)*s
s=s&(b.Pos(17.75,0,0)*b.Box(4.5,50,50));s=b.Pos(391.43,-32,170)*s
p=O/'spring-quarter.step';b.export_step(s,p);q=b.import_step(p)
r={'scope':'Illustrative spring; Quarter-turn Frenet sweep construction trial','parameters':{'pitch':1.4,'height':5.6,'radius':15.5,'wire_radius':.4,'clip_local_X':[15.5,20]},'valid':s.is_valid,'solids':len(s.solids()),'volume_mm3':s.volume,'area_mm2':s.area,'bounds':[list(s.bounding_box().min),list(s.bounding_box().max)],'roundtrip_valid':q.is_valid,'roundtrip_solids':len(q.solids()),'roundtrip_volume_mm3':q.volume,'step_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'elapsed_seconds':time.monotonic()-t,'installed':False}
(R/'reference/engine/pump-spring-sweep-20261003-quarter-build.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
