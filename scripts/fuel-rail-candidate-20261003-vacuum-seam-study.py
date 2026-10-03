"""Same approved centerline; diagnose joined-wire versus separate sweep/lead."""
from pathlib import Path
import build123d as b,numpy as np,trimesh,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/vacuum-seam-study';OUT.mkdir(exist_ok=True);r={}
for label,sign in [('plus',1),('minus',-1)]:
 gx=174.136;gy=-163+24*sign;curve=b.Bezier((gx,gy,420),(gx,gy,444),(145,(-120 if sign==1 else -170),460),(80,-90,460),(0,-95,460),(0,-75,460));plane=b.Plane(origin=curve@0,z_dir=curve%0)
 def pipe(radius):
  swept=b.sweep(plane*b.Circle(radius),path=curve,is_frenet=True);lead=b.Pos(0,-65,460)*b.Rot(90,0,0)*b.Cylinder(radius,20)
  return swept.fuse(lead)
 hose=pipe(6)-pipe(4.1);hose-=b.Pos(gx,gy,424.5)*b.Cylinder(4.15,11)
 b.export_step(hose,OUT/(label+'.step'));loaded=b.import_step(OUT/(label+'.step'));v,f=loaded.tessellate(.07,.08);vv=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(vertices=(vv[:,[0,2,1]]*np.array([1,1,-1])/1000).astype(np.float32),faces=f);mesh.update_faces(mesh.area_faces>0);mesh.remove_unreferenced_vertices();dest=OUT/(label+'.glb');dest.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));m=trimesh.load(dest,force='mesh');m.merge_vertices(digits_vertex=8)
 r[label]={'valid':hose.is_valid,'solids':len(hose.solids()),'roundtrip_valid':loaded.is_valid,'watertight':bool(m.is_watertight),'volume_mm3':hose.volume,'roundtrip_volume_delta_mm3':abs(hose.volume-loaded.volume),'triangles':len(m.faces)};print(label,r[label],flush=True)
(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
