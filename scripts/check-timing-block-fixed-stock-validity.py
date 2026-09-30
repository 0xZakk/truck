#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepCheck import BRepCheck_Analyzer
import trimesh,numpy as np
OUT=ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate';rows=[];inputs={}
for p in sorted(OUT.glob('*.step')):
 if p.stem in ['added','removed']:continue
 q=b.import_step(p);an=BRepCheck_Analyzer(q.wrapped);bad=[]
 for kind,items in [('face',q.faces()),('edge',q.edges())]:
  for i,item in enumerate(items):
   result=an.Result(item.wrapped)
   if result is None:continue
   statuses=[str(s) for s in result.Status()]
   if any('NoError' not in s for s in statuses):
    bb=item.bounding_box();bad.append({'kind':kind,'index':i,'status':statuses,'bounds_mm':[list(bb.min),list(bb.max)]})
 rows.append({'path':str(p.relative_to(ROOT)),'valid_after_step_readback':q.is_valid,'solid_count':len(q.solids()),'invalid_subshapes':bad});inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();print(rows[-1],flush=True)
p=OUT/'block.glb';mesh=trimesh.load(p,force='mesh');mesh.merge_vertices(digits_vertex=8);edges=np.sort(mesh.edges,axis=1);unique,count=np.unique(edges,axis=0,return_counts=True);boundary=unique[count!=2];points=np.asarray(mesh.vertices)[boundary].reshape(-1,3)[:,[0,2,1]]*[1,-1,1]*1000
r={'status':'FAIL CAD validity preserved','input_sha256':inputs,'step_readback_checks':rows,'mesh_nonmanifold_edge_count':len(boundary),'mesh_nonmanifold_bounds_mm':[points.min(0).tolist(),points.max(0).tolist()] if len(points) else None,'limits':['No healing or tolerance change applied','Invalid-solid downstream intersections are diagnostic only']}
(ROOT/'inventory/engine/timing-block-fixed-stock-validity.json').write_text(json.dumps(r,indent=2)+'\n')
