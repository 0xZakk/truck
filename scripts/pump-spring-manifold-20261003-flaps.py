"""Diagnose native redundant flaps; no vertex edits or hole filling."""
from pathlib import Path
import json,hashlib,time,numpy as np,trimesh,build123d as b
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/pump-spring-manifold-20261003';a=np.load(O/'native-delabella.npz');m=trimesh.Trimesh(a['vertices'],a['faces'],process=False);m.merge_vertices(digits_vertex=8);m.update_faces(m.nondegenerate_faces(height=1e-10));m.update_faces(m.unique_faces());m.remove_unreferenced_vertices()
counts=np.bincount(m.edges_unique_inverse);fc=counts[m.faces_unique_edges];remove=np.where((np.sum(fc==1,axis=1)==2)&(np.sum(fc==3,axis=1)==1))[0];assert len(remove)==2
removed=m.triangles[remove].copy();badvertices=np.unique(m.edges_unique[np.where(counts!=2)[0]]);affected=np.flatnonzero(np.isin(m.faces,badvertices).any(axis=1));affectedpoints=m.triangles_center[affected].copy();beforebounds=m.bounds.copy();beforevolume=float(m.volume);beforearea=float(m.area)
m.update_faces(~np.isin(np.arange(len(m.faces)),remove));m.remove_unreferenced_vertices();gp=O/'spring-no-native-flaps.glb';trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces,process=False).export(gp);g=trimesh.load(gp,force='mesh');gv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;gm=trimesh.Trimesh(gv,g.faces,process=False)
step=R/'cad/engine/generated/pump-functional-20261003/water-pump-seal-spring.step';s=b.import_step(step);shell=s.shells()[0];rng=np.random.default_rng(20261003);ids=rng.choice(len(gm.faces),min(200,len(gm.faces)),replace=False);points=np.vstack([gm.triangles_center[ids],affectedpoints,removed.reshape(-1,3)])
report={'removed_face_count':len(remove),'removed_face_ids':remove.tolist(),'removed_area_mm2':float(beforearea-m.area),'bounds_change_mm':float(abs(m.bounds-beforebounds).max()),'before_volume_mm3':beforevolume,'after_volume_mm3':float(m.volume),'cad_volume_mm3':float(s.volume),'cad_area_mm2':float(s.area),'mesh_area_mm2':float(m.area),'native_watertight':m.is_watertight,'native_winding':m.is_winding_consistent,'glb_watertight':g.is_watertight,'glb_winding':g.is_winding_consistent,'glb_components':len(g.split()),'inputs':{str(step.relative_to(R)):hashlib.sha256(step.read_bytes()).hexdigest()},'surface_sample_count':len(points),'surface_distances_mm':[],'status':'RUNNING distance samples'}
p=R/'reference/engine/pump-spring-manifold-20261003-flaps.json'
def save():p.write_text(json.dumps(report,indent=2)+'\n')
save()
for i,point in enumerate(points):
 dist=b.Vertex(*point).distance_to(shell);report['surface_distances_mm'].append(float(dist))
 if i%25==0:save();print('sample',i,'distance',dist,flush=True)
report['sample_max_distance_mm']=max(report['surface_distances_mm']);report['status']='PASS finite mesh checks; independent review required' if g.is_watertight and g.is_winding_consistent and len(g.split())==1 and m.volume>0 and report['sample_max_distance_mm']<=.025 else 'FAIL mesh or sampled surface distance';save();print(report['status'],report['sample_max_distance_mm'],flush=True)
