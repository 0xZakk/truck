#!/usr/bin/env python3
"""Authored landmark-only numeric proposal; never calibrates a 3-D camera."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reference/engine'
PREFIX='fuel-rail-layout-20261003'
# Manual centers of socket mouths; perspective/transverse offsets remain explicit.
views={
 'physical1987_view1':{'sockets':[[327,348],[479,422],[676,506],[902,611],[1155,720],[1437,841]],'regulator_base':[484,374],'socket_pick_px':12,'feature_transverse_projection_px':45,'other_features':{'mount_front':[410,422],'mount_middle':[810,590],'mount_rear':[1329,829],'front_loop_tip':[325,294],'rear_return_mouth':[1356,689],'rear_supply_mouth':[1496,788]},'label':'Physical 1987 comparison, view 1'},
 'Ford1994_V5855F':{'sockets':[[367,320],[309,286],[258,259],[197,229],[139,204],[88,177]],'regulator_base':[331,298],'socket_pick_px':9,'feature_transverse_projection_px':16,'other_features':{'mount_front':[349,304],'mount_middle':[237,251],'mount_rear':[97,182],'front_loop_tip':[405,344],'rear_mouth_A':[65,95],'rear_mouth_B':[94,97]},'label':'Exact-year Ford exploded diagram'}
}
rng=np.random.default_rng(20261003)
fig,axes=plt.subplots(2,2,figsize=(13,9))
report={}
for ax,(name,v) in zip(axes[0],views.items()):
 pts=np.array(v['sockets'],float); direction=pts[-1]-pts[0];direction/=np.linalg.norm(direction)
 origin=pts[0].copy();t=(pts-origin)@direction;q=np.arange(6.)
 def fit(t):
  f=least_squares(lambda p:(p[0]*q+p[1])/(1+p[2]*q)-t,[t[-1]/5,0,0],bounds=([-1e4,-1e4,-.15],[1e4,1e4,.15]))
  return f.x
 def inv(t,p): return (p[1]-t)/(t*p[2]-p[0])
 p=fit(t);tf=(np.array(v['regulator_base'])-origin)@direction;station=float(inv(tf,p))
 samples=[]
 for _ in range(1000):
  pert=t+rng.uniform(-v['socket_pick_px'],v['socket_pick_px'],6)
  pp=fit(pert);samples.append(float(inv(tf+rng.uniform(-v['feature_transverse_projection_px'],v['feature_transverse_projection_px']),pp)))
 limits=np.percentile(samples,[2.5,97.5]).tolist()
 residual=((p[0]*q+p[1])/(1+p[2]*q)-t)
 report[name]={'manual_pixels':v,'projection_direction':direction.tolist(),'rational_1d_coefficients':p.tolist(),'socket_rms_px':float(np.sqrt(np.mean(residual**2))),'regulator_station_in_injector_gaps':station,'pick_and_projection_sensitivity_95percent':limits,'method_limit':'Heuristic along-row projection, not metric registration or statistical confidence. Off-row feature has perspective bias; no 3-D pose inferred.'}
 ax.plot(pts[:,0],pts[:,1],'o-',label='I1(front) to I6(rear)')
 for i,pt in enumerate(pts):ax.annotate(f'I{i+1}',pt,xytext=(4,5),textcoords='offset points')
 ax.scatter(*v['regulator_base'],marker='x',s=100,color='red',label=f'Regulator base q≈{station:.2f}')
 report[name]['other_projected_stations_NOT_3D']={k:float(inv((np.array(pt)-origin)@direction,p)) for k,pt in v['other_features'].items()}
 for k,pt in v['other_features'].items():
  ax.scatter(*pt,marker='+',color='gray');ax.annotate(k.replace('mount_','M:').replace('rear_','R:'),pt,xytext=(3,-10),textcoords='offset points',fontsize=6)
 ax.invert_yaxis();ax.set_aspect('equal');ax.set_title(v['label']);ax.legend(fontsize=8);ax.set_xlabel('source pixel x');ax.set_ylabel('source pixel y')
# Model axes retained, no source factory scale.
xs=259.48-113.792*np.arange(6)
reg=[174.136,-139,385] # q=.75, transverse offset24 explicitly estimated
params={'units':'mm','status':'NUMERIC REVIEW PROPOSAL; NO CAD AUTHORIZATION','scale':'Existing six injector axes; not factory measurement','injector_axes':[[float(x),-163,294] for x in xs],'rail_mount_seats':[[x,-178,363.95] for x in [-250,-40,220]],'regulator_group':{'position':reg,'rotation_deg':[0,0,0],'q':.75,'q_review_range':[.3,1.3],'y_offset_estimate':24,'y_offset_review_range':[16,40],'y_sign':'headward +Y provisional; mirrored -Y remains explicit alternative','z_estimate':385,'z_review_range':[377,393]},'supply_run':{'y':-163,'z':369,'OD':12,'ID':9},'return_run':{'y':-139,'z':369,'OD':8,'ID':5.6},'rear_couplings':{'supply':{'origin':[-354.997,-163,410],'group_rotation_deg':[0,90,0]},'return':{'origin':[-332.238,-139,410],'group_rotation_deg':[0,90,0]},'q_stations':[5.4,5.2],'q_range':[4.4,6.1],'exit_axis':[0,0,1],'tilt_review_deg':20,'z_review_range':[395,425],'roll':'unchanged internal relative clocking is provisional, not source acceptance'},'front_supply_loop':{'front_tip_x':293.618,'q_tip':-.3,'q_tip_range':[-.8,.1],'z':369,'tube_OD':12,'tube_ID':9,'bend_centerline_radius_estimate':18,'radius_review_range':[12,30],'role':'supply-rail front end loops into regulator input flange; return outlet stays separate'},'return_bends':{'centerline_radius_estimate':12,'review_range':[8,24],'minimum_straight_seal_lead_estimate':15},'vacuum':{'nipple_axis':[0,0,1],'new_hose_start':[174.136,-139,420],'fixed_manifold_fitting_end':[0,-55,460],'fixed_manifold_port_axis':[0,1,0],'OD':12,'main_ID':8.2,'socket_ID':8.3,'control_points':[[174.136,-139,420],[174.136,-139,444],[145,-120,460],[80,-90,460],[0,-75,460],[0,-55,460]],'routing':'estimated smooth spline, not traced production hose; preserve last tangent +Y'},'diagnostic_port':{'position':[100,-163,378],'action':'retain current station and IDs initially; check rail continuity and new regulator envelope'},'all_unmarked_numeric_terms':'existing model values or explicitly proposed estimates; no newly verified factory mm; sensitivity ranges are review scenarios not tolerances'}
ax=axes[1,0];ax.scatter(xs,[-163]*6,label='protected injector axes');ax.scatter([-250,-40,220],[-178]*3,marker='s',label='protected rail seats')
ax.plot([293.618,-354.997],[-163,-163],label='supply run, estimated');ax.plot([174.136,-332.238],[-139,-139],label='return run, estimated');ax.scatter(reg[0],reg[1],marker='o',s=170,facecolors='none',edgecolors='red',label='regulator q=.75')
ax.plot([174.136,-332.238],[-187,-187],'--',color='gray',label='explicit mirrored-Y alternative')
ax.set_title('Proposed plan; front +X at left');ax.invert_xaxis();ax.set_xlabel('engine X mm');ax.set_ylabel('engine Y mm');ax.legend(fontsize=8)
ax=axes[1,1];ax.plot([293.618,-354.997],[369,369],label='supply run');ax.plot([-336.997,-354.997,-354.997],[369,387,410],label='rear bend envelope sketch');ax.scatter(reg[0],reg[2],color='red',label='regulator group');ax.plot([p[0] for p in params['vacuum']['control_points']],[p[2] for p in params['vacuum']['control_points']],':',label='vacuum control polygon');ax.invert_xaxis();ax.set_xlabel('engine X mm');ax.set_ylabel('engine Z mm');ax.set_title('Elevation proposal; polylines are NOT finished tube paths');ax.legend(fontsize=8)
fig.suptitle('Source landmarks and numeric review — source topology, estimated 3-D terms',fontsize=14);fig.tight_layout();fig.savefig(OUT/(PREFIX+'-review.png'),dpi=150)
(OUT/(PREFIX+'-measurements.json')).write_text(json.dumps(report,indent=2)+'\n')
(OUT/(PREFIX+'-parameters.json')).write_text(json.dumps(params,indent=2)+'\n')
print(json.dumps(report,indent=2))
