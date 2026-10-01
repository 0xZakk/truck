#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import timing_valvetrain_inclined_hypothesis as c
import valve_source_layout as original
import timing_valvetrain_contract as vertical
paths=[Path(__file__),Path(c.__file__),Path(original.__file__),Path(vertical.__file__),ROOT/'inventory/engine/full-assembly.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}
r={'status':'NUMERIC COMPARISON; no CAD adaptation or factory calibration','inputs':inputs,'hypotheses':[],'limits':['Integer0..720 crank and both axial endpoints only; not continuous sweep or actual CAD contact proof.','Circular passage sufficient-containment bounds use current estimatedR6 atY90 and actual modeled tube diameter; gasket/cover source dimensions remain unknown.','UpperY88 is a sensitivity scenario, not a selected production datum or permission to move socket.','All original files/reports frozen; source rod length and valve axes unchanged.']}
for upper in [90.,88.]:
 h=c.layout(upper);row={'upper_socket_y_mm':upper,'pivot_y_mm':h['pivot_y'],'cup_local_z_mm':h['cup_z'],'branches':[]}
 for i in range(1,7):
  for kind in ['intake','exhaust']:
   closure=[];tilts=[];sections={z:[] for z in [254.,255.5,304.,333.5,334.]};tops=[];curve=[]
   for theta in range(721):
    for axial in [0,-.1]:
     s=c.state(h,theta,i,kind,axial);closure.append(abs(s['closure_error']));tops.append(s['top'][0]);tilts.append(math.degrees(math.atan2(s['top'][0]-s['bottom'][0],s['top'][1]-s['bottom'][1])))
     curve.append(abs(s['valve_lift']-vertical.state(theta,i,kind,axial)['valve_lift']))
     for z in sections:
      center,half=c.section_y(s,z);sections[z].append({'theta':theta,'axial':axial,'center_y':center,'positive_y':center+half,'R6_Y90_sufficient_gap':6-abs(center-90)-half})
   peak=h['solve'](.247*25.4,kind)
   branch={'id':f'c{i}-{kind}','peak_valve_lift_mm':peak['valve_lift'],'nominal_peak_residual_mm':peak['valve_lift']-.395*25.4,'maximum_closure_error_mm':max(closure),'tilt_range_degrees':[min(tilts),max(tilts)],'top_y_range_mm':[min(tops),max(tops)],'max_curve_change_from_vertical_hypothesis_mm':max(curve),'sections':{str(z):{'minimum_sufficient_gap':min(a,key=lambda x:x['R6_Y90_sufficient_gap']),'maximum_positive_y':max(a,key=lambda x:x['positive_y'])} for z,a in sections.items()}}
   assert max(closure)<1e-8
   row['branches'].append(branch)
 r['hypotheses'].append(row)
assert all(sha(ROOT/p)==h for p,h in inputs.items())
p=ROOT/'inventory/engine/timing-valvetrain-inclined-hypothesis-validation.json';p.write_text(json.dumps(r,indent=2)+'\n')
for h in r['hypotheses']:print(h['upper_socket_y_mm'],h['pivot_y_mm'],h['cup_local_z_mm'],h['branches'][0])
