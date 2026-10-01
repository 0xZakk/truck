from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import online_heater_route_candidate as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c.O.mkdir(exist_ok=True);rows={}
for variant in c.END_X:
 s=c.tube(variant)
 if isinstance(s,b.ShapeList):s=b.Compound(s)
 p=c.O/(variant+'-tube.step');b.export_step(s,p);s=b.import_step(p)
 assert s.is_valid and len(s.solids())==1
 v,f=s.tessellate(.035,.09);v=np.array([tuple(q)for q in v]);m=trimesh.Trimesh(v,np.array(f));m.merge_vertices(digits_vertex=6)
 assert m.is_watertight and m.is_winding_consistent
 gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp)
 g=trimesh.load(gp,force='mesh');gv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;bounds=np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)]);err=float(np.max(abs(np.array([gv.min(0),gv.max(0)])-bounds)))
 assert err<.025
 rows[variant]={'step':str(p.relative_to(R)),'step_sha256':sha(p),'glb_sha256':sha(gp),'valid':s.is_valid,'solids':len(s.solids()),'watertight':g.is_watertight,'bounds_mm':bounds.tolist(),'bounds_error_mm':err,'endpoint_mm':c.controls(variant)[-1].tolist()}
 print(variant,rows[variant],flush=True)
inputs=[Path(__file__),Path(c.__file__),Path(c.old.__file__),R/'docs/components/online-heater-research.md',R/'reference/engine/online-heater-captures/gmb-1251810-view3.jpeg',c.old.O/'housing.step']
r={'status':'PASS export only','parts':rows,'root_mm':c.ROOT.tolist(),'terminal_direction':c.ENDDIR.tolist(),'housing_unchanged':str((c.old.O/'housing.step').relative_to(R)),'input_sha256':{str(p.relative_to(R)):sha(p)for p in inputs}}
(R/'inventory/engine/online-heater-route-export.json').write_text(json.dumps(r,indent=2)+'\n')
