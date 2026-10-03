from pathlib import Path
import build123d as b,numpy as np,trimesh,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';r={}
for label in ['plus','minus']:
 shape=b.import_step(OUT/'r4'/label/'local-regulator-vacuum-hose.step');v,f=shape.tessellate(.02,.05);v=np.array([tuple(x) for x in v]);m=trimesh.Trimesh(vertices=(v[:,[0,2,1]]*np.array([1,1,-1])/1000).astype(np.float32),faces=f);m.update_faces(m.area_faces>0);m.remove_unreferenced_vertices();dest=OUT/'r4'/label/'local-regulator-vacuum-hose-refined.glb';dest.write_bytes(trimesh.Scene(m).export(file_type='glb'));ml=trimesh.load(dest,force='mesh');ml.merge_vertices(digits_vertex=8);u,c=np.unique(ml.edges_sorted,axis=0,return_counts=True)
 r[label]={'watertight':bool(ml.is_watertight),'triangles':len(ml.faces),'edge_counts':{str(n):int(sum(c==n)) for n in np.unique(c)},'linear_deflection_mm':.02,'angular_deflection_rad':.05};print(label,r[label],flush=True)
(OUT/'r4/vacuum-mesh-refine.json').write_text(json.dumps(r,indent=2)+'\n')
