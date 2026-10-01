#!/usr/bin/env python3
"""Isolated same-path sweep tessellation experiment; preserves failed splice outputs."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
import shifted_oil_pickup_candidate as c
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/shifted-oil-pickup-native-sweep';OUT.mkdir(exist_ok=True)
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());poses=transforms(m);old=poses['oil-pickup-tube']*b.import_step(ROOT/'cad/engine/generated/oil-pickup-tube.step');prior=b.import_step(ROOT/'cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube-world.step');_,data=c.build(old)
path=b.Wire(list(data['path'].edges())+[c.original_path().trim(data['parameter'],1)])
q=b.sweep(b.Plane(origin=data['start'],x_dir=(0,1,0),z_dir=(-1,0,0))*(b.Circle(6)-b.Circle(4.8)),path=path,is_frenet=True)
print('built',q.is_valid,len(q.solids()),flush=True)
vol=lambda s:sum(x.volume for x in s.solids()) if s else 0.
mask=b.Pos(127,0,0)*b.Box(146,2000,2000);a=q.cut(mask);z=old.cut(mask);difference=vol(a.cut(z))+vol(z.cut(a));same=vol(q.cut(prior))+vol(prior.cut(q));print('difference',difference,same,flush=True)
b.export_step(q,OUT/'oil-pickup-tube-world.step');local=poses['oil-pickup-tube'].inverse()*q;b.export_step(local,OUT/'oil-pickup-tube.step')
v,f=local.tessellate(.12,.12);v=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.array(f),process=True);mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();mesh.export(OUT/'oil-pickup-tube.glb');mesh=trimesh.load(OUT/'oil-pickup-tube.glb',force='mesh');mesh.merge_vertices(digits_vertex=8)
r={'status':'EXPERIMENT only','valid':q.is_valid,'solid_count':len(q.solids()),'outside_mask_difference_mm3':difference,'prior_candidate_difference_mm3':same,'mesh':{'watertight':bool(mesh.is_watertight),'winding_consistent':bool(mesh.is_winding_consistent),'positive_volume':bool(mesh.volume>0),'triangles':len(mesh.faces)},'inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['scripts/probe-shifted-oil-pickup-native-sweep.py','cad/engine/shifted_oil_pickup_candidate.py','inventory/engine/full-assembly.json','cad/engine/generated/oil-pickup-tube.step','cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube-world.step']},'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*') if p.is_file()}}
(ROOT/'inventory/engine/shifted-oil-pickup-native-sweep-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(r['mesh'],flush=True)
