from pathlib import Path
import sys,json,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import waterpump_source_offset_inlet_candidate as c
c.O.mkdir(exist_ok=True)
def vol(s):return sum(abs(q.volume)for q in s.solids())if s else 0.
def bounds(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
parts={};rows={};replay=None
for angle in c.ANGLES:
 name='nominal'if angle==c.NOMINAL else 'low-offset'if angle==min(c.ANGLES)else'high-offset'
 shape,old,base,outer,passage=c.build(angle);canonical=c.FRAME*b.import_step(c.SOURCE)
 if replay is None:
  replay={'added_mm3':vol(old.cut(canonical)),'removed_mm3':vol(canonical.cut(old))};print('REPLAY',replay,flush=True)
  assert max(replay.values())<1e-5,replay
 p=c.O/(name+'-housing.step');b.export_step(shape,p);back=b.import_step(p);assert back.is_valid and len(back.solids())==1
 v,f=back.tessellate(.04,.1);v=np.array([tuple(q)for q in v]);mesh=trimesh.Trimesh(v,np.array(f));mesh.merge_vertices(digits_vertex=6);assert mesh.is_watertight and mesh.is_winding_consistent
 gp=p.with_suffix('.glb');trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces).export(gp);gl=trimesh.load(gp,force='mesh');gv=gl.vertices[:,[0,2,1]]*[1,-1,1]*1000;err=float(np.max(abs(np.array([gv.min(0),gv.max(0)])-bounds(back))));assert err<.025
 a=math.radians(c.ANGLE);end=(440+c.inlet.AXIS_X,-32+c.inlet.END_Y*math.cos(a)-angle*math.sin(a),170+c.inlet.END_Y*math.sin(a)+angle*math.cos(a));direction=(0,math.cos(a),math.sin(a))
 rows[name]={'angle_deg':c.ANGLE,'offset_mm':angle,'step_sha256':c.rear.sha(p),'glb_sha256':c.rear.sha(gp),'valid':back.is_valid,'solids':len(back.solids()),'watertight':gl.is_watertight,'mesh_bounds_error_mm':err,'world_bounds_mm':bounds(back).tolist(),'hose_free_end_world_mm':list(end),'hose_outward_direction':list(direction)};print(name,rows[name],flush=True)
r={'status':'PASS exports and exact oldsource replay; interface checks pending','replay':replay,'parts':rows,'inputs':{str(p.relative_to(R)):c.rear.sha(p)for p in [Path(__file__),Path(c.__file__),Path(c.pump.__file__),Path(c.inlet.__file__),Path(c.rear.__file__),c.SOURCE,c.FROZEN_REAR]},'limits':['Dimensionallyunverified construction; photo orientation is not a manufacturingtolerance.','No radiator hose exists; free-end boundary changes need vehicle routing.','Heaterorientation/access unchanged and unresolved.']};(R/'inventory/engine/waterpump-source-offset-inlet-export.json').write_text(json.dumps(r,indent=2)+'\n')
