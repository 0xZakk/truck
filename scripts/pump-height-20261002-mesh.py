from pathlib import Path
import json,hashlib,numpy as np
import build123d as b,trimesh
R=Path(__file__).resolve().parents[1];rp=R/'reference/engine/pump-height-20261002-ports-trial3.json';r=json.loads(rp.read_text());rows={};meshes={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,v in r['variants']['nominal']['parts'].items():
 p=R/v['path'];s=b.import_step(p);vs,fs=s.tessellate(.05,.12);m=trimesh.Trimesh(np.array([tuple(v)for v in vs]),np.array(fs));m.merge_vertices(digits_vertex=6);gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp);g=trimesh.load(gp,force='mesh');vv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-v['bounds'])));rows[n]={'path':str(gp.relative_to(R)),'sha256':sha(gp),'watertight':g.is_watertight,'winding':g.is_winding_consistent,'cad_bounds_error_mm':err};meshes[n]=m

np.savez_compressed(R/'reference/engine/pump-height-20261002-meshes.npz',**{n+'__'+k:a for n,m in meshes.items()for k,a in [('vertices',m.vertices),('faces',m.faces)]})
(R/'reference/engine/pump-height-20261002-mesh.json').write_text(json.dumps(rows,indent=2)+'\n')
