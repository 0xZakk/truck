#!/usr/bin/env python3
"""Isolate inherited runner triangulation failure and its bounded replacement."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
import numpy as np
import trimesh
from OCP.BRepTools import BRepTools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import exhaust_front_profile as f
OUT=ROOT/'cad/engine/generated/exhaust-rear-collector-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=f.runner_path(0);tail=p.trim(.27,1)
profiles=[b.Plane(origin=p@t,x_dir=(1,0,0),z_dir=p%t)*b.Circle(18) for t in [.27,.40,.55,.70,.85,1]]
shapes={'entry_transition':f.transition(0,True),'original_outer_sweep':b.sweep(b.Plane(origin=tail@0,x_dir=(1,0,0),z_dir=tail%0)*b.Circle(18),path=tail),'original_void':f.runner_void(0),'replacement_outer':f.transition(0,True).fuse(b.loft(profiles,ruled=True))}
results={}
for name,s in shapes.items():
 BRepTools.Clean_s(s.wrapped);v,tri=s.tessellate(.1,.15)
 m=trimesh.Trimesh(np.array([tuple(x) for x in v])/1000,np.array(tri));m.update_faces(m.nondegenerate_faces());m.update_faces(m.unique_faces());m.remove_unreferenced_vertices()
 results[name]=dict(cad_valid=s.is_valid,solids=len(s.solids()),watertight=bool(m.is_watertight),triangles=len(m.faces))
assert all(results[k]['watertight'] for k in ['entry_transition','original_void','replacement_outer'])
assert not results['original_outer_sweep']['watertight']
# Sample the newly reconstructed branch sidewalls in the saved candidate,
# away from the intended openings into the collector. No global thickness claim.
from cad_metrics import solid_volume
saved=b.import_step(OUT/'exhaust-rear.step');wall_samples=[]
for x in [-31.896,-145.688,-259.48]:
 for t in [.30,.40,.55]:
  for sign in [-1,1]:
   pt=p@t;probe=b.Pos(x+sign*16.5,pt.Y,pt.Z)*b.Sphere(.35)
   common=saved&probe;hit=sum(abs(solid_volume(q,'adaptive')) for q in common.solids())
   missing=abs(solid_volume(probe,'adaptive'))-hit
   wall_samples.append(dict(x=x,path_parameter=t,side=sign,missing_mm3=missing))
assert max(q['missing_mm3'] for q in wall_samples)<.001,wall_samples
(OUT/'seam-diagnosis.json').write_text(json.dumps(dict(status='PASS failure isolated and bounded exterior replacement verified',script_sha256=sha(Path(__file__)),source_sha256=sha(Path(f.__file__)),results=results,saved_candidate_sha256=sha(OUT/'exhaust-rear.step'),runner_wall_samples=wall_samples,scope='Probe supports exterior sweep replacement only; whole candidate and exact interface checks remain required.'),indent=2)+'\n');print(results)
