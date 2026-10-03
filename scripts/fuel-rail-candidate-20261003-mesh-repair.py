"""Split collinear tessellation T junctions; preserve surface, never cap holes."""
from pathlib import Path
import hashlib,json,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';report={}
for label in ['plus','minus']:
 p=OUT/label/'local-fuel-supply-rail.glb';m=trimesh.load(p,force='mesh');m.merge_vertices(digits_vertex=8)
 u,c=np.unique(m.edges_sorted,axis=0,return_counts=True);boundary=u[c==1];candidates=np.unique(boundary);splits=0;faces=[]
 for face in m.faces:
  replacement=None
  for j in range(3):
   a,d,e=face[j],face[(j+1)%3],face[(j+2)%3]
   if not np.any(np.all(boundary==np.sort([a,d]),axis=1)):continue
   v=m.vertices[d]-m.vertices[a];den=v@v;t=(m.vertices[candidates]-m.vertices[a])@v/den
   dist=np.linalg.norm(m.vertices[candidates]-m.vertices[a]-t[:,None]*v,axis=1)
   good=(t>1e-7)&(t<1-1e-7)&(dist<1e-10)
   inside=candidates[good][np.argsort(t[good])]
   if len(inside):
    chain=[a,*inside,d];replacement=[[chain[k],chain[k+1],e] for k in range(len(chain)-1)];splits+=len(inside);break
  faces.extend(replacement if replacement else [face])
 fixed=trimesh.Trimesh(vertices=m.vertices,faces=faces,process=False);fixed.visual.vertex_colors=[175,185,188,255]
 dest=p.with_name('local-fuel-supply-rail-repaired.glb');dest.write_bytes(trimesh.Scene(fixed).export(file_type='glb'));loaded=trimesh.load(dest,force='mesh');loaded.merge_vertices(digits_vertex=8)
 np.savez_compressed(dest.with_suffix('.npz'),vertices_cad_mm=loaded.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000,faces=loaded.faces)
 report[label]={'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'collinear_tolerance_mm':1e-7,'inserted_vertices_on_edges':splits,'watertight':bool(loaded.is_watertight),'bounds_delta_m':float(abs(m.bounds-loaded.bounds).max()),'volume_delta_m3':float(abs(m.volume-loaded.volume)),'surface_change':'Only triangle subdivision on existing collinear edges; no new spatial vertices/caps.'}
 print(label,report[label])
(OUT/'mesh-repair.json').write_text(json.dumps(report,indent=2)+'\n')
