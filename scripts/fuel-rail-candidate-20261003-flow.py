#!/usr/bin/env python3
"""Actual OCC cavity connectivity; seated/open valve and drilled bypass control."""
from pathlib import Path
import sys,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepCheck import BRepCheck_Analyzer
OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003'
def cyl(r,a,z,x,y):return b.Pos(x,y,(a+z)/2)*b.Cylinder(r,z-a)
def cut(a,c):
 op=BRepAlgoAPI_Cut(a.wrapped,c.wrapped);op.Build()
 if not op.IsDone() or op.Shape().IsNull() or not BRepCheck_Analyzer(op.Shape()).IsValid():raise RuntimeError('OCC cavity Cut failed or invalid')
 return b.Compound(op.Shape())
def memberships(solids,point):return [i for i,s in enumerate(solids) if s.is_inside(point,1e-6)]
reports={}
for label,sign in [('plus',1),('minus',-1)]:
 folder=OUT/label;gx=174.136;gy=-163+24*sign
 ids=['fuel-supply-rail','fuel-return-tube','regulator-lower-housing','regulator-gasket','regulator-inlet-screen','regulator-valve-seat','regulator-valve','regulator-diaphragm','regulator-o-ring']
 shapes={i:b.import_step(folder/(i+'.step')) for i in ids}
 envelope=cyl(17,377.6,389.05,gx,gy)
 rows={}
 for state in ['seated','lifted_0.5mm','bypass_negative']:
  fluid=envelope
  bypass=b.Pos(gx+6,gy,380.2)*b.Rot(0,90,0)*b.Cylinder(1.2,16)
  if state=='bypass_negative':
   # Equivalent drilled cavity: add the actual cutter to the verified seated
   # cavity. Cutter does not touch any retained component, so it drills only
   # rail flange/return stem. Avoid rerunning a tangent ball-seat cut.
   for ident,shape in shapes.items():
    if ident not in ['fuel-supply-rail','fuel-return-tube']:
     hit=shape & bypass
     if hit and sum(abs(x.volume) for x in hit.solids())>1e-7:raise RuntimeError('Bypass touches retained '+ident)
   # OCC fuse is invalid at the ideal tangent seat. A connectivity graph of
   # individually valid fluid solids and their positive-volume intersections
   # with the actual drilled cylinder avoids treating that invalid union as evidence.
   fluid=seated_fluid
   bridge=bypass & envelope
   bridge_hits=[sum(abs(z.volume) for z in (sol & bridge).solids()) for sol in fluid.solids()]
   if not bridge.is_valid or any(z.volume<0 for z in bridge.solids()):raise RuntimeError('invalid drilled bridge')
  else:
   for ident,shape in shapes.items():
    shape=shape & cyl(21,377.0,390,gx,gy)
    if ident=='regulator-valve' and state=='lifted_0.5mm':shape=b.Pos(0,0,.5)*shape
    fluid=cut(fluid,shape)
    if any(sol.volume < -1e-6 for sol in fluid.solids()): raise RuntimeError(f'Negative oriented fluid volume after {state}/{ident}')
  if state=='seated':seated_fluid=fluid
  solids=list(fluid.solids());points={'supply_gallery':(gx+12,gy,380),'pressure_chamber':(gx+8,gy,388),'central_return':(gx,gy,379)}
  member={k:memberships(solids,v) for k,v in points.items()}
  connected=lambda a,c:bool(set(member[a])&set(member[c])) or (state=='bypass_negative' and any(bridge_hits[i]>1e-6 for i in member[a]) and any(bridge_hits[i]>1e-6 for i in member[c]))
  rows[state]={'valid':fluid.is_valid,'method':('positive-volume intersection graph of seated cavity solids and valid actual drill; no invalid union accepted' if state=='bypass_negative' else 'envelope minus actual STEP components'),'solid_count':len(solids),'solid_volumes_mm3':[s.volume for s in solids],'marker_components':member,'supply_to_chamber':connected('supply_gallery','pressure_chamber'),'supply_to_return':connected('supply_gallery','central_return'),'chamber_to_return':connected('pressure_chamber','central_return')}
  if state=='bypass_negative':rows[state]['drill_intersection_volumes_mm3']=bridge_hits
  b.export_step(fluid,folder/('fluid-'+state+'.step'))
  print(label,state,rows[state],flush=True)
 probes={}
 for k in range(8):
  angle=k*math.pi/4;point=(gx+11.5*math.cos(angle),gy+11.5*math.sin(angle),383.7)
  probes[str(k)]={'open':bool(memberships(list(seated_fluid.solids()),point))}
 plug=cyl(2.6,383.1,383.9,gx+11.5,gy)
 blocked=cut(seated_fluid,plug)
 probes['0']['blocked_control_detected']=not bool(memberships(list(blocked.solids()),(gx+11.5,gy,383.7)))
 rows['inlet_probes']=probes
 rows['input_sha256']={str((folder/(i+'.step')).relative_to(ROOT)):hashlib.sha256((folder/(i+'.step')).read_bytes()).hexdigest() for i in ids}
 rows['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 rows['acceptance']={'seated_isolation':rows['seated']['supply_to_chamber'] and not rows['seated']['supply_to_return'],'lifted_opens':rows['lifted_0.5mm']['supply_to_return'],'bypass_control_detected':rows['bypass_negative']['supply_to_return']}
 reports[label]=rows
 (OUT/'flow.json').write_text(json.dumps(reports,indent=2)+'\n')
