#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut,BRepAlgoAPI_Common
from OCP.BRepCheck import BRepCheck_Analyzer
OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r4'
manifest=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in manifest['definitions']};old=b.import_step(ROOT/defs['fuel-supply-rail']['step'].lstrip('/'))
def boolean(a,c,kind):
 op=kind(a.wrapped,c.wrapped);op.Build()
 if not op.IsDone() or op.Shape().IsNull() or not BRepCheck_Analyzer(op.Shape()).IsValid():raise RuntimeError('Boolean error/invalid result')
 result=b.Compound(op.Shape())
 if any(s.volume< -1e-6 for s in result.solids()):raise RuntimeError('Negative oriented solid')
 return result
reports={}
for label in ['plus','minus']:
 folder=OUT/label;build=json.loads((folder/'build.json').read_text());r={'protected_interfaces':{},'exports':{},'export_step':{}}
 rail=b.import_step(folder/'fuel-supply-rail.step')
 masks={}
 for i,x in enumerate([259.48-113.792*k for k in range(6)],1):masks[f'injector_cup_{i}']=b.Pos(x,-163,356.5)*b.Box(19,19,12.8)
 for i,x in enumerate([-250,-40,220],1):masks[f'mount_bottom_{i}']=b.Pos(x,-178,364.05)*b.Box(16,12,.1)
 for name,mask in masks.items():
  try:
   aa=boolean(old,mask,BRepAlgoAPI_Common);cc=boolean(rail,mask,BRepAlgoAPI_Common);ab=boolean(aa,cc,BRepAlgoAPI_Cut);ba=boolean(cc,aa,BRepAlgoAPI_Cut)
   diff=sum(s.volume for s in ab.solids())+sum(s.volume for s in ba.solids());r['protected_interfaces'][name]={'status':'PASS' if diff<.1 else 'FAIL','symmetric_difference_mm3':diff}
  except Exception as e:r['protected_interfaces'][name]={'status':'ERROR','error':str(e)}
 for ident,row in build['definitions'].items():
  step=folder/('local-'+ident+'.step');shape=b.import_step(step)
  r['export_step'][ident]={'valid':row['valid'] and row['roundtrip_valid'],'single_solid':row['solids']==row['roundtrip_solids']==1,'relative_volume_delta':row['volume_delta_mm3']/row['volume_mm3'],'bounds_max_error_mm':row['bounds_max_error_mm']}
  vertices,faces=shape.tessellate(.07,.08);v=np.array([tuple(x) for x in vertices]);xyz=v[:,[0,2,1]]*np.array([1,1,-1])/1000
  mesh=trimesh.Trimesh(vertices=xyz.astype(np.float32),faces=faces);mesh.update_faces(mesh.area_faces>0);mesh.remove_unreferenced_vertices();mesh.visual.vertex_colors=[175,185,188,255]
  dest=folder/('local-'+ident+'.glb');dest.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));loaded=trimesh.load(dest,force='mesh');loaded.merge_vertices(digits_vertex=8)
  vv=np.array(loaded.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;bb=shape.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
  r['exports'][ident]={'watertight':bool(loaded.is_watertight),'bounds_error_mm':err,'triangles':len(loaded.faces),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
  np.savez_compressed(folder/('local-'+ident+'-mesh.npz'),vertices_cad_mm=vv,faces=loaded.faces)
 # World component meshes for source-review rendering, excluding inherited complex springs.
 for ident in ['regulator-upper-housing','regulator-lower-housing','regulator-gasket','regulator-valve-seat','regulator-valve','regulator-diaphragm','regulator-inlet-screen','fuel-supply-coupling-male','fuel-return-coupling-male']:
  shape=b.import_step(folder/(ident+'.step'));v,f=shape.tessellate(.12,.12);np.savez_compressed(folder/(ident+'-mesh.npz'),vertices_cad_mm=np.array([tuple(x) for x in v]),faces=f)
 reports[label]=r;(OUT/'checks.json').write_text(json.dumps(reports,indent=2)+'\n');print(label,r,flush=True)
