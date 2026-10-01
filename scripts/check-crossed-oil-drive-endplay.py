#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import crossed_oil_drive_endplay_candidate as c
from cad_metrics import solid_volume
O=R/'cad/engine/generated/crossed-oil-drive-endplay';O.mkdir(exist_ok=True)
P=R/'cad/engine/generated/crossed-oil-drive-corrected-pair'
cp=P/'cam-drive-gear-local.step';dp=P/'distributor-drive-gear-local.step'
assert hashlib.sha256(cp.read_bytes()).hexdigest()=='a8c0288344579f739983e3b7a29858c4806f364351917be11b3cf82bf5b23b29'
assert hashlib.sha256(dp.read_bytes()).hexdigest()=='b875ee0a6669664c9d3246c175e188c3db561334e42ffc5d9aee937bc60b08f8'
cam=b.import_step(cp);dist=b.import_step(dp)
rows=[]
def check(q,x,label='nominal',error=0):
 f=c.frames(q,x);p=f['cam']*cam;t=f['distributor']*b.Rot(0,0,error)*dist
 distance=p.distance_to(t);common=p.intersect(t) if distance<1e-7 else None
 try:vol=solid_volume(common) if common is not None else 0;err=None
 except Exception as e:vol=None;err=str(e)
 ca,da=c.angles(q,x);residual=math.radians(ca+da+error)-c.CROSSED_LEAD_RAD_PER_MM*x
 row=dict(event_degrees=q,axial_mm=x,label=label,cam_degrees=ca,distributor_degrees=da+error,phase_error_degrees=error,registration_residual_rad=residual,distance_mm=distance,overlap_mm3=vol,metric_error=err)
 rows.append(row);print(row,flush=True)
 (O/'partial-rows.json').write_text(json.dumps(rows,indent=2)+'\n')
 if common is not None and vol and vol>0:b.export_step(common,O/(label+'-overlap.step'))
for x in [0.,-.05,-.1]:
 for q in [0.,11.25,22.5]:check(q,x)
for error in [-1.,1.]:check(11.25,-.1,'phase-'+str(error),error)
check(11.25,-.1,'omitted-endplay',-math.degrees((c.CROSSED_LEAD_RAD_PER_MM-c.K)*-.1))
# Independent actual edge geometry: x-translation moves fitted helical phase intercept.
lead=[]
for e in cam.edges():
 pts=np.array([tuple(e.position_at(float(t)))for t in np.linspace(0,1,17)])
 if np.ptp(pts[:,0])<10:continue
 theta=np.unwrap(np.arctan2(pts[:,2],pts[:,1]));fit=np.polyfit(pts[:,0],theta,1)
 if abs(fit[0]-1/18)>1e-6:continue
 moved=pts.copy();moved[:,0]-=.1
 changed=np.polyfit(moved[:,0],theta,1)
 lead.append({'slope':float(fit[0]),'intercept_change_at_minus_0p1_mm':float(changed[1]-fit[1])})
assert len(lead)==304
bad_inputs=[]
for q,x in [(float('nan'),0),(0,-.1001),(0,.0001)]:
 try:c.angles(q,x);bad_inputs.append(False)
 except ValueError:bad_inputs.append(True)
inputs=[Path(__file__),Path(c.__file__),cp,dp,R/'cad/engine/oil_drive_layout.py',R/'cad/engine/timing_coupled_core_candidate.py']
r={'scope':'Nominal registration and bounded actual STEP poses, not continuous or loaded contact proof','rows':rows,'actual_cam_edge_translation_fit':lead,'invalid_input_rejected':bad_inputs,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs}}
(R/'inventory/engine/crossed-oil-drive-endplay-review.json').write_text(json.dumps(r,indent=2)+'\n')
