from pathlib import Path
import sys,json
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import timing_pump_rear_flange_candidate as c
new,old,cutters,paths,m,poses=c.build();c.O.mkdir(exist_ok=True);rows={}
def bounds(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
for k,s in new.items():
 assert s.is_valid and len(s.solids())==1
 p=c.O/(k+'.step');b.export_step(s,p);back=b.import_step(p);assert back.is_valid and len(back.solids())==1
 v,f=back.tessellate(.025,.08);v=np.array([tuple(x)for x in v]);mesh=trimesh.Trimesh(v,np.array(f));mesh.merge_vertices(digits_vertex=6);assert mesh.is_watertight and mesh.is_winding_consistent
 gp=c.O/(k+'.glb');trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces).export(gp);gl=trimesh.load(gp,force='mesh');vv=gl.vertices[:,[0,2,1]]*[1,-1,1]*1000
 err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-bounds(back))));assert err<.025
 rows[k]={'step_sha256':c.sha(p),'glb_sha256':c.sha(gp),'world_bounds_mm':bounds(back).tolist(),'mesh_bounds_error_mm':err,'watertight':gl.is_watertight,'components':len(gl.split()),'euler_number':gl.euler_number,'faces':len(back.faces()),'solids':len(back.solids()),'valid':back.is_valid};print(k,rows[k],flush=True)
r={'status':'PASS world-coordinate exports only; gates pending','parts':rows,'frame':'All exported shapes use worldCAD coordinates, millimeters; no canonical installer','inputs':{str(p.relative_to(R)):c.sha(p)for p in [*paths.values(),Path(c.__file__),Path(__file__),R/'inventory/engine/full-assembly.json']}};(R/'inventory/engine/timing-pump-rear-flange-export.json').write_text(json.dumps(r,indent=2)+'\n')
