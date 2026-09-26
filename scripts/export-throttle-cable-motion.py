#!/usr/bin/env python3
"""Export integer-angle exact CAD meshes; preserve ground ends and core nipple."""
from pathlib import Path
import sys,json,hashlib,base64,zlib
import numpy as np
import build123d as b
import trimesh
from OCP.BRepTools import BRepTools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import throttle_cable_candidate as c
from cad_metrics import support_bounds

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def delta(now,zero):
 loc=now.location*zero.location.inverse();origin=np.array(tuple(b.Vertex(0,0,0).moved(loc).center()));R=np.column_stack([np.array(tuple(b.Vertex(*v).moved(loc).center()))-origin for v in [(1,0,0),(0,1,0),(0,0,1)]])
 C=np.array([[1,0,0],[0,0,1],[0,-1,0]]);matrix=np.eye(4);matrix[:3,:3]=C@R@C.T;q=trimesh.transformations.quaternion_from_matrix(matrix)
 return dict(translation_cad_mm=origin.tolist(),quaternion_viewer_xyzw=q[[1,2,3,0]].tolist(),rotation_cad_matrix=R.tolist())
inputs={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(c.__file__),ROOT/'inventory/engine/throttle-cable-candidate-validation.json']};frames=[];rows=[];_,_,zero,zfixed,_=c.state(0)
for angle in range(91):
 parts,meta=c.moving(angle);ball,u,frame,fixed,L=c.state(angle);meshes={};checks={}
 for kind,key in [('core','throttle-cable-core-illustrative'),('compression-spring','throttle-cable-compression-spring-illustrative')]:
  q=parts[key];BRepTools.Clean_s(q.wrapped);v,f=q.tessellate(.025,.5);mesh=trimesh.Trimesh(np.array([tuple(x) for x in v]),np.asarray(f));mesh.merge_vertices(digits_vertex=4);mesh.update_faces(mesh.nondegenerate_faces());mesh.remove_unreferenced_vertices()
  vertices=np.rint(np.asarray(mesh.vertices)*10000).astype('<i4');faces=np.asarray(mesh.faces,dtype='<u4');packed=vertices.tobytes()+faces.tobytes();payload=zlib.compress(packed,9);decoded=vertices.astype(float)/10000
  actual=q.bounding_box();bounds=np.array([tuple(actual.min),tuple(actual.max)]);error=float(np.max(np.abs(np.array([decoded.min(0),decoded.max(0)])-bounds)))
  if error>=.2:
   actual=support_bounds(q);bounds=np.array([tuple(actual.min),tuple(actual.max)]);error=float(np.max(np.abs(np.array([decoded.min(0),decoded.max(0)])-bounds)))
  check=dict(cad_valid=q.is_valid,cad_solids=len(q.solids()),watertight=mesh.is_watertight,winding_consistent=mesh.is_winding_consistent,vertices=len(vertices),triangles=len(faces),bounds_error_mm=error,quantization_error_mm=float(np.max(np.linalg.norm(decoded-np.asarray(mesh.vertices),axis=1))),cad_bounds_mm=bounds.tolist())
  assert check['cad_valid'] and check['cad_solids']==1 and check['watertight'] and check['winding_consistent'] and error<.2 and check['quantization_error_mm']<.0001,check
  meshes[kind]=dict(vertex_count=len(vertices),triangle_count=len(faces),packed_sha256=hashlib.sha256(packed).hexdigest(),deflate_base64=base64.b64encode(payload).decode());checks[kind]=check
 frames.append(dict(angle_deg=angle,ball_center_cad_mm=ball.tolist(),fixed_pivot_cad_mm=c.PIVOT.tolist(),rigid=dict(socket=delta(frame,zero),seat=delta(fixed,zfixed),guide=delta(fixed,zfixed)),meshes=meshes,cad_metrics=meta));rows.append(dict(angle_deg=angle,meshes=checks));print(angle,flush=True)
data=dict(schema='illustrative-throttle-cable-motion-v1',scope='Exact CAD integer poses; estimated educational engine-end mechanism, not production cable/force validation.',coordinate_frame='throttle-assembly parent-local CAD millimeters; no ancestor shift baked in',encoding='zlib-base64; int32 little-endian XYZ vertices in 0.0001 mm, then uint32 little-endian triangle indices',tessellation=dict(linear_deflection_mm=.025,angular_deflection_rad=.5),frames=frames,input_hashes=inputs)
out=ROOT/'viewer/throttle-cable-motion.json';out.write_text(json.dumps(data,separators=(',',':'))+'\n')
assert all(sha(ROOT/p)==h for p,h in inputs.items()),'Motion input changed'
r=dict(status='PASS',scope=data['scope'],input_hashes=inputs,output_sha256=sha(out),output_bytes=out.stat().st_size,frames=rows,maximum_bounds_error_mm=max(v['bounds_error_mm'] for row in rows for v in row['meshes'].values()),maximum_vertex_quantization_error_mm=max(v['quantization_error_mm'] for row in rows for v in row['meshes'].values()),cad_spring_length_variation_mm=max(f['cad_metrics']['spring_cad_centerline_length_mm'] for f in frames)-min(f['cad_metrics']['spring_cad_centerline_length_mm'] for f in frames))
(ROOT/'inventory/engine/throttle-cable-motion-validation.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS',out.stat().st_size,flush=True)
