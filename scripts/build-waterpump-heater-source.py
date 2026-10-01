from pathlib import Path
import sys,json,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import waterpump_heater_source_candidate as c
c.O.mkdir(exist_ok=True)
def vol(s):return sum(abs(q.volume)for q in s.solids())if s else 0.
def bb(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
h,t,old=c.build();frozen=c.inlet.O/'nominal-housing.step';prior=b.import_step(frozen);replay={'added_mm3':vol(old.cut(prior)),'removed_mm3':vol(prior.cut(old))};print('REPLAY',replay,flush=True);assert max(replay.values())<1e-5
parts={}
for name,s in [('housing',h),('tube',t)]:
 p=c.O/(name+'.step');b.export_step(s,p);s=b.import_step(p);assert s.is_valid and len(s.solids())==1
 v,f=s.tessellate(.035,.09);v=np.array([tuple(q)for q in v]);m=trimesh.Trimesh(v,np.array(f));m.merge_vertices(digits_vertex=6);assert m.is_watertight and m.is_winding_consistent
 gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp);g=trimesh.load(gp,force='mesh');gv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;err=float(np.max(abs(np.array([gv.min(0),gv.max(0)])-bb(s))));assert err<.025
 parts[name]={'step_sha256':c.rear.sha(p),'glb_sha256':c.rear.sha(gp),'valid':s.is_valid,'solids':len(s.solids()),'watertight':g.is_watertight,'mesh_bounds_error_mm':err,'world_bounds_mm':bb(s).tolist()};print(name,parts[name],flush=True)
r={'status':'PASS export only','source_replay':replay,'parts':parts,'root_world_mm':c.ROOT.tolist(),'hose_boundary_world_mm':c.END.tolist(),'hose_boundary_direction':c.ENDDIR.tolist(),'inputs':{str(p.relative_to(R)):c.rear.sha(p)for p in [Path(__file__),Path(c.__file__),Path(c.inlet.__file__),frozen,c.inlet.SOURCE,R/'inventory/engine/waterpump-heater-source-registration.json']}};(R/'inventory/engine/waterpump-heater-source-export.json').write_text(json.dumps(r,indent=2)+'\n')
