"""Actual exterior included: shell, diaphragm and lower seal paths stay distinct."""
from pathlib import Path
import json,hashlib,build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepCheck import BRepCheck_Analyzer
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';OUT=BASE/'r5'
ids=['fuel-supply-rail','fuel-return-tube','regulator-lower-housing','regulator-upper-housing','regulator-diaphragm','regulator-gasket','regulator-inlet-screen','regulator-valve-seat','regulator-valve','regulator-o-ring']
def cyl(r,a,z,x,y):return b.Pos(x,y,(a+z)/2)*b.Cylinder(r,z-a)
def cut(a,c):
 op=BRepAlgoAPI_Cut(a.wrapped,c.wrapped);op.Build()
 if not op.IsDone() or op.Shape().IsNull() or not BRepCheck_Analyzer(op.Shape()).IsValid():raise RuntimeError('invalid cavity cut')
 q=b.Compound(op.Shape())
 if any(s.volume< -1e-7 for s in q.solids()):raise RuntimeError('negative cavity solid')
 return q
r={}
for label,sign in [('plus',1),('minus',-1)]:
 gx=174.136;gy=-163+24*sign;shapes={i:b.import_step(OUT/label/(i+'.step')) for i in ids};old={i:b.import_step(BASE/'r4'/label/(i+'.step')) for i in ['regulator-lower-housing','regulator-upper-housing']};rows={}
 for state in ['seated','lifted_0.5mm','original_shell_negative','pierced_diaphragm_negative']:
  fluid=cyl(30,375,429,gx,gy)
  for ident,s in shapes.items():
   if state=='original_shell_negative' and ident in old:s=old[ident]
   if state=='lifted_0.5mm' and ident=='regulator-valve':s=b.Pos(0,0,.5)*s
   if state=='pierced_diaphragm_negative' and ident=='regulator-diaphragm':s=cut(s,cyl(1,388.9,390.1,gx+12,gy))
   fluid=cut(fluid,s)
  fluid=cut(fluid,cyl(2.51,427.5,429.1,gx,gy))
  solids=list(fluid.solids());points={'pressure':(gx+8,gy,388.5),'return':(gx,gy,379),'vacuum':(gx+12,gy,397),'external':(gx+25,gy,389)};members={k:[i for i,s in enumerate(solids) if s.is_inside(p,1e-6)] for k,p in points.items()};con=lambda a,c:bool(set(members[a])&set(members[c]))
  rows[state]={'valid':fluid.is_valid,'positive_volumes_mm3':[s.volume for s in solids],'marker_components':members,'pressure_to_return':con('pressure','return'),'pressure_to_external':con('pressure','external'),'pressure_to_vacuum':con('pressure','vacuum'),'vacuum_to_external':con('vacuum','external')};print(label,state,rows[state],flush=True)
  (OUT/label/('exterior-fluid-'+state+'.json')).write_text(json.dumps(rows[state],indent=2)+'\n')
 rows['interpretation']={'shell_contact_and_vacuum_separation_pass':not rows['seated']['pressure_to_vacuum'] and not rows['seated']['vacuum_to_external'],'original_shell_control_detected':rows['original_shell_negative']['pressure_to_vacuum'],'pierced_diaphragm_control_detected':rows['pierced_diaphragm_negative']['pressure_to_vacuum'],'closed_valve_isolates_return':not rows['seated']['pressure_to_return'],'open_valve_reaches_return':rows['lifted_0.5mm']['pressure_to_return'],'whole_pressure_enclosure_pass':not rows['seated']['pressure_to_external']}
 rows['domain']={'radial_extent_mm':30,'z_interval_mm':[375,429],'vacuum_cap_radius_mm':2.51,'vacuum_cap_z_mm':[427.5,429.1],'legitimate_lower_ports':'Supply and return tube walls cross lower domain boundaryZ375; their bore cross-sections terminate there. Exterior volume retained around full circumference and down past flange bottom377.5, so stem/O-ring leakage is not capped.','not_modeled':'Pressure/flowrate, material compression, true diaphragm/spring movement. Valve displacement is a cavity-control study.'}
 rows['input_sha256']={str((OUT/label/(i+'.step')).relative_to(ROOT)):hashlib.sha256((OUT/label/(i+'.step')).read_bytes()).hexdigest() for i in ids};rows['control_input_sha256']={str((BASE/'r4'/label/(i+'.step')).relative_to(ROOT)):hashlib.sha256((BASE/'r4'/label/(i+'.step')).read_bytes()).hexdigest() for i in old};rows['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();r[label]=rows;(OUT/'exterior-flow.json').write_text(json.dumps(r,indent=2)+'\n')
