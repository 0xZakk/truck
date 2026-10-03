from pathlib import Path
import json,numpy as np,trimesh
r=Path.cwd();a=np.load(r/'cad/engine/generated/pump-spring-manifold-20261003/native-delabella.npz');m=trimesh.Trimesh(a['vertices'],a['faces'],process=False);m.merge_vertices(digits_vertex=8);m.update_faces(m.nondegenerate_faces(height=1e-10));m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();counts=np.bincount(m.edges_unique_inverse);bad=np.where(counts!=2)[0];out=[]
for i in bad:
 edge=m.edges_unique[i];faces=np.unique(np.flatnonzero(m.edges_unique_inverse==i)//3);out.append({'edge':edge.tolist(),'count':int(counts[i]),'xyz':m.vertices[edge].tolist(),'face_ids':faces.tolist(),'triangles':m.triangles[faces].tolist(),'areas':m.area_faces[faces].tolist()})
p=r/'reference/engine/pump-spring-manifold-20261003-edge-diagnostic.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2)[:6500])
