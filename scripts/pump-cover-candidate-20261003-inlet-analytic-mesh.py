"""Exact same candidate mesh gates on the isolated analytical-channel diagnostic."""
from pathlib import Path
import json,hashlib,numpy as np
import build123d as b,trimesh
from OCP.BRepTools import BRepTools
R=Path(__file__).resolve().parents[1];P='pump-cover-candidate-20261003';jp=R/f'reference/engine/{P}-inlet-analytic-study.json';j=json.loads(jp.read_text());p=R/j['path'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(p)==j['sha256'];s=b.import_step(p);bounds=np.array([list(s.bounding_box().min),list(s.bounding_box().max)])
BRepTools.Clean_s(s.wrapped);vs,fs=s.tessellate(.003,.025);m=trimesh.Trimesh(np.array([tuple(v)for v in vs]),np.array(fs),process=True);m.merge_vertices(digits_vertex=5);gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp);g=trimesh.load(gp,force='mesh');v=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
r={'scope':'Isolated own-axis inlet diagnostic; candidate datums remain failed','path':str(gp.relative_to(R)),'sha256':sha(gp),'watertight':g.is_watertight,'winding':g.is_winding_consistent,'components':len(g.split()),'finite':bool(np.isfinite(v).all()),'cad_bounds_error_mm':float(np.max(abs(np.array([v.min(0),v.max(0)])-bounds))),'bounds_gate_mm':.025,'settings':{'linear_mm':.003,'angular_rad':.025,'merge_digits_mm':5},'inputs':{str(q.relative_to(R)):sha(q)for q in[p,jp,Path(__file__)]}}
np.savez_compressed(R/f'reference/engine/{P}-inlet-analytic-mesh.npz',vertices=v,faces=g.faces)
(R/f'reference/engine/{P}-inlet-analytic-mesh.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
