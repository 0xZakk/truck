from pathlib import Path
import json,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';report={}
for label in ['plus','minus']:
 p=OUT/label/'local-fuel-supply-rail.glb';m=trimesh.load(p,force='mesh');m.merge_vertices(digits_vertex=8)
 u,c=np.unique(m.edges_sorted,axis=0,return_counts=True);edges=u[c!=2];v=m.vertices[edges].reshape(-1,3)[:,[0,2,1]]*np.array([1,-1,1])*1000
 report[label]={'non_two_face_edges':len(edges),'counts':{str(n):int(sum(c==n)) for n in np.unique(c)},'bounds_cad_mm':[v.min(0).tolist(),v.max(0).tolist()],'edge_midpoints_cad_mm':v.reshape(-1,2,3).mean(1).tolist()}
 print(label,report[label]['non_two_face_edges'],report[label]['bounds_cad_mm'])
(OUT/'mesh-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
