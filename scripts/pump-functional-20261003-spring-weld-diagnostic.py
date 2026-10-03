from pathlib import Path
import json,numpy as np,trimesh
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[1];p=R/'cad/engine/generated/pump-functional-20261003/spring-absolute-raw.glb';m=trimesh.load(p,force='mesh');m.vertices=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
rows=[]
for tol in [1e-5,3e-5,1e-4,3e-4]:
 pairs=cKDTree(m.vertices).query_pairs(tol,output_type='ndarray')
 parent=np.arange(len(m.vertices))
 def root(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for a,z in pairs:
  a,z=root(a),root(z)
  if a!=z:parent[max(a,z)]=min(a,z)
 mapping=np.array([root(i)for i in range(len(parent))])
 q=trimesh.Trimesh(m.vertices.copy(),mapping[m.faces],process=False)
 q.update_faces(q.nondegenerate_faces(height=1e-8));q.update_faces(q.unique_faces());q.remove_unreferenced_vertices()
 counts=np.bincount(q.edges_unique_inverse);row={'weld_radius_mm':tol,'pairs':len(pairs),'collapsed_vertices':int(sum(mapping!=np.arange(len(mapping)))),'max_representative_displacement_mm':float(np.max(np.linalg.norm(m.vertices-m.vertices[mapping],axis=1))),'watertight':q.is_watertight,'winding':q.is_winding_consistent,'boundary_edges':int(sum(counts==1)),'nonmanifold_edges':int(sum(counts>2)),'faces':len(q.faces)}
 rows.append(row);print(row,flush=True)
(R/'reference/engine/pump-functional-20261003-spring-weld-diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n')
