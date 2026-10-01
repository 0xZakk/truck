from pathlib import Path
import sys,json,math,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
import waterpump_heater_source_candidate as c
h=b.import_step(c.O/'housing.step');t=b.import_step(c.O/'tube.step');old=b.import_step(c.inlet.O/'nominal-housing.step')
def vol(s):return sum(abs(q.volume)for q in s.solids())if s else 0.
def op(kind,a,z):
 q=kind(a.wrapped,z.wrapped);q.Build();assert q.IsDone();return b.Compound(q.Shape())
def faces(s):return b.Compound(list(s.faces()))
# The full socket lateral face is an independent analytic contact witness.
socket=c.segment(8,c.START,c.ROOT);sf=b.Compound([f for f in socket.faces()if f.geom_type==b.GeomType.CYLINDER]);contact={}
for name,s in [('housing',h),('tube',t)]:contact[name]={'expected_mm2':sf.area,'missing_mm2':op(BRepAlgoAPI_Cut,sf,faces(s)).area,'actual_mm2':op(BRepAlgoAPI_Common,sf,faces(s)).area}
probe=c.sweep(.7)+c.segment(.7,c.ROOT-46*c.DIR,c.START+c.DIR);plug=b.Pos(*(c.ROOT+10*c.DIR))*b.Sphere(2);wall=c.sweep(7.9)-c.sweep(6.6)
rear=b.Pos(350,0,0)*b.Box(78,1000,1000);bearing=b.Pos(538,0,0)*b.Box(144,1000,1000) # X466+ equals retained source frontX26+
added=c.rear.norm(h.cut(old));removed=c.rear.norm(old.cut(h))
metrics={'housing_tube_overlap_mm3':vol(h.intersect(t)),'fluid_probe_obstruction_mm3':vol(probe.intersect(b.Compound([h,t]))),'blocked_probe_negative_control_mm3':vol(probe.intersect(b.Compound([h,t,plug]))),'tube_nominal1_3mm_wall_missing_mm3':vol(wall.cut(t)),'rear_added_mm3':vol(b.Compound(list(added.solids())).intersect(rear)),'rear_removed_mm3':vol(b.Compound(list(removed.solids())).intersect(rear)),'bearing_added_mm3':vol(b.Compound(list(added.solids())).intersect(bearing)),'bearing_removed_mm3':vol(b.Compound(list(removed.solids())).intersect(bearing))}
# Declared changed-stock mask: original boss/bore and new boss/bore only.
mask=c.FRAME*c.segment(13,(-2,-82,15),(-2,-24,15))+c.segment(13,c.ROOT-47*c.DIR,c.ROOT+2*c.DIR)
mask=c.rear.norm(mask)
metrics['added_outside_heater_mask_mm3']=vol(added.cut(mask));metrics['removed_outside_heater_mask_mm3']=vol(removed.cut(mask))
curv=[]
for u in np.linspace(0,1,1001):
 v=3*((1-u)**2*(c.P1-c.P0)+2*(1-u)*u*(c.P2-c.P1)+u*u*(c.P3-c.P2));a=6*((1-u)*(c.P2-2*c.P1+c.P0)+u*(c.P3-2*c.P2+c.P1));curv.append(float(np.linalg.norm(v)**3/np.linalg.norm(np.cross(v,a))))
tools=[]
for typ,pts,x0,x1 in [('pump',[(y-32,z+170)for y,z in c.pump.MOUNTING],389,449),('main',c.rear.main.AXES,379.8,435)]:
 for n,(y,z)in enumerate(pts,1):
  tool=c.pump.cx(10.5,x0,x1,y,z);tools.append({'type':typ,'station':n,'housing_overlap_mm3':vol(tool.intersect(h)),'tube_overlap_mm3':vol(tool.intersect(t))})
inputs=[Path(__file__),Path(c.__file__),c.O/'housing.step',c.O/'tube.step',c.inlet.O/'nominal-housing.step']
r={'status':'Diagnostic; no factoryfit claim','metrics':metrics,'socket_contact':contact,'tube_curvature_sampled':{'samples':1001,'min_centerline_radius_mm':min(curv),'outer_radius_mm':8,'note':'Analytic cubic derivatives sampled; valid solid export separately checks modeled tube topology. Straight/curve tangents continuous by construction.'},'tools':tools,'inputs':{str(p.relative_to(R)):c.rear.sha(p)for p in inputs},'limits':['Nominal matching socket is not a sourced press-fit/retention/sealing specification.','Fluid probe and wall gauge do not establish hydraulic capacity.','Main3 rear tool remains outside this repair.']};(R/'inventory/engine/waterpump-heater-source-interfaces.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
