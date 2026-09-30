#!/usr/bin/env python3
"""Bounded numeric feasibility; no CAD import, file writes except report."""
import hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import timing_axis_kinematic_candidate as k
b=k.layout();c=k.layout(True)
assert abs(b['PIVOT_Y']-51.0718402496357)<1e-9
assert abs(b['PUSHROD_CENTERS']-250.00335443437204)<1e-9
rows=[];wrong_rod=[]
pivots={kind:c['PIVOT_Y'] for kind in ['intake','exhaust']}
# One-degree grid plus known event centers/edges/check-height stations.
for cyl in range(1,7):
 for kind in ['intake','exhaust']:
  phases=set(range(721));center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(cyl)*120
  phases.update((center+x)%720 for x in [-135,-96,0,96,135])
  samples=[]
  for phase in sorted(phases):
   lift=k.cam_lift(phase,cyl,kind);old=b['solve'](lift,kind);new=c['solve'](lift,kind,pivots[kind])
   samples.append((abs(old['closure_error']),abs(new['closure_error']),abs(new['valve_lift']-old['valve_lift']),new['valve_lift'],new['angle']))
   wrong_rod.append(abs(math.dist(old['top'],new['bottom'])-b['PUSHROD_CENTERS']))
  peak=c['solve'](k.MAX_CAM_LIFT,kind,pivots[kind])
  rows.append({'cylinder':cyl,'kind':kind,'sample_count':len(phases),'baseline_max_closure_error_mm':max(x[0] for x in samples),'candidate_max_closure_error_mm':max(x[1] for x in samples),'max_lift_curve_change_mm':max(x[2] for x in samples),'candidate_peak_valve_lift_mm':peak['valve_lift'],'target_peak_delta_mm':peak['valve_lift']-k.TARGET_VALVE_LIFT,'minimum_valve_lift_mm':min(x[3] for x in samples),'rocker_angle_range_deg':[math.degrees(min(x[4] for x in samples)),math.degrees(max(x[4] for x in samples))]})
assert max(x['candidate_max_closure_error_mm'] for x in rows)<1e-8
assert abs(c['solve'](k.MAX_CAM_LIFT,'intake')['valve_lift']-k.TARGET_VALVE_LIFT)<1e-8
# Common rocker retained. Exhaust peak is reported, not waived or calibrated away.
bd,cd=k.drive(),k.drive(True)
assert abs(math.dist(cd['shaft_top'],cd['shaft_bottom'])-cd['shaft_length_mm'])<1e-9
assert abs(math.dist(cd['gear'],[227.584,90+k.DELTA[0],72+k.DELTA[1]])-36)<1e-9
wrong_drive_offset=math.dist(bd['gear'],cd['gear'])
wrong_bearing_offset=math.hypot(*k.DELTA)
assert min(wrong_rod)>1 and wrong_drive_offset>6 and wrong_bearing_offset>6
inputs=['cad/engine/timing_axis_kinematic_candidate.py','scripts/check-timing-axis-kinematic-candidate.py','cad/engine/valve_source_layout.py','cad/engine/valve_dimensions_candidate.py','cad/engine/valve_layout_integration.py','cad/engine/oil_drive_layout.py','cad/engine/oil_pump_drive.py']
r={'status':'PASS numeric closure with common rocker; nominal lift comparison UNRESOLVED; NOT CAD fit or production datum','units':'mm/degrees','input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},'same_ray_center_mm':k.CENTER,'delta_yz_mm':k.DELTA,'constraints':{'valve_y':-12,'valve_base_z':261,'pushrod_overall_mm':257.556,'pushrod_ball_centers_mm':b['PUSHROD_CENTERS'],'intermediate_shaft_length_mm':cd['shaft_length_mm'],'cam_max_lift_mm':k.MAX_CAM_LIFT,'intake_peak_target_mm':k.TARGET_VALVE_LIFT},'baseline':{key:b[key] for key in ['PIVOT_Y','PUSHROD_Y','LOWER_BALL_Z','CUP_Z']},'pivot_y_by_kind_mm':pivots,'shared_pivot_exhaust_peak_residual_mm':c['solve'](k.MAX_CAM_LIFT,'exhaust')['valve_lift']-k.TARGET_VALVE_LIFT,'baseline_exhaust_peak_residual_mm':b['solve'](k.MAX_CAM_LIFT,'exhaust')['valve_lift']-k.TARGET_VALVE_LIFT,'candidate':{key:c[key] for key in ['PIVOT_Y','PUSHROD_Y','LOWER_BALL_Z','CUP_Z']},'rest':{kind:{'baseline':b['rest'](kind,b['PIVOT_Y']),'candidate':c['rest'](kind,pivots[kind])} for kind in ['intake','exhaust']},'all_12_numeric_sweeps':rows,'drive':{'baseline':bd,'candidate':cd,'shaft_endpoint_length_error_mm':abs(math.dist(cd['shaft_top'],cd['shaft_bottom'])-cd['shaft_length_mm'])},'negative_controls':{'old_rocker_top_to_shifted_lower_ball_min_length_error_mm':min(wrong_rod),'unshifted_bearing_axis_offset_mm':wrong_bearing_offset,'unshifted_drive_frame_offset_mm':wrong_drive_offset,'detected':True},'limitations':['Discrete numeric sampling, no solids/contact/clearance validation','Common rocker/pivot preserved; exhaust nominal peak residual and intermediate curve changes UNRESOLVED, not a source-lift pass or tolerance waiver','Pivot and cup offset remain estimated freedoms; new rocker geometry and pedestal/passages required','Connected drive rigid translation preserves assumed engagement, not physical fit or valid crossed-helical teeth','No canonical or baseline proof writes']}
path=ROOT/'inventory/engine/timing-axis-kinematic-candidate-validation.json';path.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'status':r['status'],'candidate':r['candidate'],'first_two':rows[:2],'negative_controls':r['negative_controls']},indent=2))
