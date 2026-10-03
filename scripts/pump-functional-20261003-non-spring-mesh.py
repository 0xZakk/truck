from pathlib import Path
import json,hashlib,numpy as np
import build123d as b,trimesh
from OCP.BRepTools import BRepTools
R=Path(__file__).resolve().parents[1];rp=R/'reference/engine/pump-functional-20261003-build.json';r=json.loads(rp.read_text());rows={};meshes={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,v in r['parts'].items():
 if n=='water-pump-seal-spring':continue
 p=R/v['path'];assert sha(p)==v['sha256'];s=b.import_step(p)
 BRepTools.Clean_s(s.wrapped)
 vs,fs=s.tessellate(.003,.025)
 m=trimesh.Trimesh(np.array([tuple(v)for v in vs]),np.array(fs),process=True)
 m.merge_vertices(digits_vertex=5)
 gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp)
 g=trimesh.load(gp,force='mesh');vv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-v['bounds'])))
 rows[n]={'path':str(gp.relative_to(R)),'sha256':sha(gp),'watertight':g.is_watertight,'winding':g.is_winding_consistent,'cad_bounds_error_mm':err,'vertices':len(g.vertices),'faces':len(g.faces),'step_sha256':sha(p)};meshes[n]=m
 print(n,rows[n]['watertight'],err,flush=True)
 (R/'reference/engine/pump-functional-20261003-non-spring-mesh.json').write_text(json.dumps({'settings':{'linear_mm':.003,'angular_rad':.025,'vertex_merge_digits_mm':5,'bounds_gate_mm':.025},'parts':rows,'inputs':{str(p.relative_to(R)):sha(p)for p in[rp,Path(__file__)]}},indent=2)+'\n')
np.savez_compressed(R/'reference/engine/pump-functional-20261003-non-spring-meshes.npz',**{n+'__'+k:a for n,m in meshes.items()for k,a in [('vertices',m.vertices),('faces',m.faces)]})
