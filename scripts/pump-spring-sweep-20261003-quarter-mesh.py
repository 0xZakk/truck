"""Focused faithful absolute-deflection export; no vertex sculpting or hole fill."""
from pathlib import Path
import json,hashlib,time,numpy as np,trimesh
import build123d as b
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopAbs import TopAbs_Orientation
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/pump-spring-sweep-20261003';p=O/'spring-quarter.step';s=b.import_step(p);bb=s.bounding_box()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bound=np.array([tuple(bb.min),tuple(bb.max)])
# Original source clips localX15.5..20; worldX440 plus height correction−48.57.
clip=[440+98.43-147+15.5,440+98.43-147+20]
bound[0,0]=max(bound[0,0],clip[0]);bound[1,0]=min(bound[1,0],clip[1])
planes=[f.center().X for f in s.faces()if f.geom_type==b.GeomType.PLANE and f.bounding_box().size.X<1e-5]
assert all(any(abs(x-q)<1e-5 for q in planes)for x in clip)
# Full solid must remain inside independently declared clipping slab.
slab=b.Pos(sum(clip)/2,-32,170)*b.Box(clip[1]-clip[0],1000,1000)
outside=s.cut(slab)
assert not outside or sum(abs(q.volume)for q in outside.solids())<1e-7
r={'status':'RUNNING','settings':{'absolute_linear_deflection_mm':.01,'angular_rad':.06,'measured_bounds_gate_mm':.025,'no_shape_change':True,'no_hole_filling':True},'ordinary_loose_bounds':[list(bb.min),list(bb.max)],'corrected_conservative_bounds':bound.tolist(),'clip_provenance':'water_pump_mechanical_seal_candidate.py spring clips local15.5..20; world440 +98.43−147. Both actual planar faces verified; full STEP inside slab. Transverse AddOptimal bound retained.','inputs':{str(p.relative_to(R)):sha(p),str(Path(__file__).relative_to(R)):sha(Path(__file__)), 'cad/engine/water_pump_mechanical_seal_candidate.py':sha(R/'cad/engine/water_pump_mechanical_seal_candidate.py')}}
rp=R/'reference/engine/pump-spring-sweep-20261003-quarter-mesh.json'
def save():rp.write_text(json.dumps(r,indent=2)+'\n')
save();BRepTools.Clean_s(s.wrapped);started=time.monotonic();print('ABSOLUTE MESH START',flush=True)
mesher=BRepMesh_IncrementalMesh(s.wrapped,.01,False,.06,True);print('NATIVE MESH COMPLETE',time.monotonic()-started,flush=True)
vertices=[];triangles=[];offset=0
for face in s.faces():
 loc=TopLoc_Location();poly=BRep_Tool.Triangulation_s(face.wrapped,loc);trsf=loc.Transformation();reverse=face.wrapped.Orientation()==TopAbs_Orientation.TopAbs_REVERSED
 for i in range(1,poly.NbNodes()+1):
  v=poly.Node(i).Transformed(trsf);vertices.append((v.X(),v.Y(),v.Z()))
 for tri in poly.Triangles():
  a,z,c=tri.Value(1),tri.Value(2),tri.Value(3)
  triangles.append((a+offset-1,c+offset-1,z+offset-1)if reverse else(a+offset-1,z+offset-1,c+offset-1))
 offset+=poly.NbNodes()

output=R/'cad/engine/generated/pump-spring-sweep-20261003';output.mkdir(exist_ok=True)
v=np.asarray(vertices);f=np.asarray(triangles)
np.savez_compressed(output/'native-quarter.npz',vertices=v,faces=f)
r['precision_trials']=[]
for digits in [8]:
 m=trimesh.Trimesh(v.copy(),f.copy(),process=False);m.merge_vertices(digits_vertex=digits)
 counts=np.bincount(m.edges_unique_inverse)
 row={'digits_vertex':digits,'raw_boundary':int(sum(counts==1)),'raw_nonmanifold':int(sum(counts>2)),'raw_degenerate':int(sum(~m.nondegenerate_faces(height=1e-10)))}
 m.update_faces(m.nondegenerate_faces(height=1e-10));m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();counts=np.bincount(m.edges_unique_inverse)
 row.update({'boundary':int(sum(counts==1)),'nonmanifold':int(sum(counts>2)),'watertight':m.is_watertight,'winding':m.is_winding_consistent,'faces':len(m.faces)})
 if m.is_watertight:
  gp=output/f'quarter-precision-{digits}.glb';trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces,process=False).export(gp)
  g=trimesh.load(gp,force='mesh');row['glb_watertight']=g.is_watertight;row['glb_winding']=g.is_winding_consistent
  gv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;row['bounds_error_mm']=float(np.max(abs(np.array([gv.min(0),gv.max(0)])-bound)))
 r['precision_trials'].append(row);save();print(row,flush=True)
r['status']='DIAGNOSTIC COMPLETE; not installed';r['elapsed_seconds']=time.monotonic()-started;save()
