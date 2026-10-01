#!/usr/bin/env python3
"""Audit actual supplied phase/contact contracts before geometry adaptation."""
from pathlib import Path
import sys,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_valvetrain_contract as c
import valve_source_layout as v
from valve_source_integration import state as installed_state
from assembly_math import transforms
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-valvetrain-contract';OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'inventory/engine/timing-valvetrain-contract-validation.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());occ={o['id']:o for o in m['occurrences']};defs={d['id']:d for d in m['definitions']}
assert m['valvetrain_model']=='source-sized-v2'
ids=['cylinder-head','intake-valve','exhaust-valve','lifter-body','rocker-arm','pushrod','rocker-fulcrum','lifter-pushrod-cup']
paths={k:ROOT/defs[k]['step'].lstrip('/') for k in ids}
camfile=ROOT/'cad/engine/generated/timing-coupled-core-candidate/camshaft.step'
watch=[Path(__file__),Path(c.__file__),ROOT/'inventory/engine/full-assembly.json',camfile]+list(paths.values())+[ROOT/'cad/engine'/x for x in ['timing_axis_kinematic_candidate.py','timing_coupled_core_candidate.py','valve_source_layout.py','valve_source_integration.py','valvetrain_dispatch.py','assembly_math.py','valve_dimensions_candidate.py','valve_layout_integration.py']]
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
r={'status':'RUNNING','inputs':inputs,'phase_contract':{'cam_angle_deg':'-theta/2+degrees(K*axial)','effective_crank':'theta-2*degrees(K*axial)','effective_crank_shift_at_minus0p1_deg':c.effective_crank(0,-.1),'source':'Inherited hypothetical replacement envelope, not Ford/owner calibration'},'numeric':[]}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
save()
for cylinder in range(1,7):
 for kind in ['intake','exhaust']:
  tag=f'c{cylinder}-{kind}'
  assert occ[tag+'-rocker']['valvetrain']['model']=='source-sized-v2'
  assert occ[tag+'-valve']['position_cad_mm'][1:]==[-12.,261]
  row={'cylinder':cylinder,'kind':kind,'source_x_mm':occ[tag+'-valve']['position_cad_mm'][0]}
  closure=[];curve=[];omitted=[];baseerror=[];phaseerror=[];pad=[]
  for theta in range(721):
   old=installed_state(theta,cylinder,kind);baseline=c.state(theta,cylinder,kind,shifted=False)
   baseerror.append(max(abs(old[z]-baseline[z]) for z in ['angle','valve_lift','closure_error']))
   for axial in [0,-.1]:
    new=c.state(theta,cylinder,kind,axial);closure.append(abs(new['closure_error']));pad.append(abs(new['pad_y']+12))
    curve.append(abs(new['valve_lift']-c.state(theta,cylinder,kind,axial,False)['valve_lift']))
    omitted.append(abs(math.dist(old['top'],new['bottom'])-v.PUSHROD_CENTERS))
    phaseerror.append(abs(new['lifter_lift']-c.state(theta,cylinder,kind,0)['lifter_lift']))
  peak=c.PROPOSED['solve'](.247*25.4,kind);rest=c.PROPOSED['rest'](kind,c.PROPOSED['PIVOT_Y']);original=v.rest(kind,v.PIVOT_Y)
  retained=c.PROPOSED['solve'](.247*25.4,kind,c.BASE['PIVOT_Y'])
  row.update(max_baseline_solver_error=max(baseerror),max_closure_error_mm=max(closure),max_curve_change_mm=max(curve),max_pad_slide_mm=max(pad),omitted_rocker_min_ball_length_error_mm=min(omitted),omitted_axial_phase_max_lifter_error_mm=max(phaseerror),proposed_peak_valve_lift_mm=peak['valve_lift'],nominal_peak_residual_mm=peak['valve_lift']-.395*25.4,retained_pivot_peak_valve_lift_mm=retained['valve_lift'],pivot_delta_yz_mm=[c.PROPOSED['PIVOT_Y']-v.PIVOT_Y,rest['pivot_z']-original['pivot_z']],rest_rocker_angle_delta_deg=math.degrees(rest['angle']-original['angle']))
  assert max(baseerror)<1e-10 and max(closure)<1e-8 and min(omitted)>1
  r['numeric'].append(row)
r['adapter_datums']={'baseline':{k:c.BASE[k] for k in ['PIVOT_Y','PUSHROD_Y','LOWER_BALL_Z','CUP_Z']},'proposed':{k:c.PROPOSED[k] for k in ['PIVOT_Y','PUSHROD_Y','LOWER_BALL_Z','CUP_Z']},'lifter_branch_delta_yz_mm':c.DELTA,'valve_axis_change_mm':0,'pushrod_centers_mm':v.PUSHROD_CENTERS}
print('Twelve numerical contracts audited',flush=True);save()
shapes={k:b.import_step(p) for k,p in paths.items()};cam=b.import_step(camfile);r['cam_lifter_contacts']=[]
# Event-relative rest, check-height slopes, peak and opposite slope, both axial
# endpoints. X tangent follows cam translation but stays on stationary follower.
for cylinder in range(1,7):
 for kind in ['intake','exhaust']:
  tag=f'c{cylinder}-{kind}';x=occ[tag+'-valve']['position_cad_mm'][0]
  center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(cylinder)*120
  for offset in [-150,-96,0,96,150]:
   for axial in [0,-.1]:
    theta=(center+offset)%720;s=c.state(theta,cylinder,kind,axial)
    cp=c.cam_frame(theta,axial)*cam
    body=b.Pos(x,90+c.DELTA[0],114.8+c.DELTA[1]+s['lifter_lift'])*shapes['lifter-body']
    witness=b.Vertex(*c.tangent(theta,cylinder,kind,axial,x))
    a=witness.distance_to(cp);z=witness.distance_to(body)
    oldbody=b.Pos(x,90,114.8+s['lifter_lift'])*shapes['lifter-body']
    fault=witness.distance_to(oldbody)
    row={'cylinder':cylinder,'kind':kind,'crank_degrees':theta,'axial_mm':axial,'cam_surface_gap_mm':a,'shifted_lifter_surface_gap_mm':z,'unshifted_lifter_witness_gap_mm':fault}
    assert max(a,z)<.002,row
    # Flat foot numerical contact witness must leave both surfaces when moved
    # outward; use exterior direction rather than accepting an interior vertex.
    row['plus0p1_normal_fault_mm']=max((b.Pos(0,0,.1)*witness).distance_to(cp),(b.Pos(0,0,.1)*witness).distance_to(body))
    assert row['plus0p1_normal_fault_mm']>.05,row
    r['cam_lifter_contacts'].append(row)
  print(tag,'cam contact PASS',flush=True);save()
# Actual installed head guide cylinder and stem envelope remain at old valve Y.
base=transforms(m,0);head=base['cylinder-head']*shapes['cylinder-head'];r['guide_stem_datums']=[]
for cylinder in range(1,7):
 for kind in ['intake','exhaust']:
  tag=f'c{cylinder}-{kind}';x=occ[tag+'-valve']['position_cad_mm'][0]
  bore=b.Pos(x,-12,290)*b.Cylinder(.3438*25.4/2-1e-5,20)
  intrusion=vol(head.intersect(bore))
  ring=(b.Pos(x,-12,290)*b.Cylinder(4.9,20)).cut(b.Pos(x,-12,290)*b.Cylinder(.3438*25.4/2+1e-5,22))
  missing=vol(ring.cut(head))
  # Stem only: clip fixed local section that sweeps through guide over10.04mm.
  valve=shapes[kind+'-valve'];clip=b.Pos(0,0,34)*b.Cylinder(10,32)
  stem=valve.intersect(clip);outside=vol(stem.cut(b.Pos(0,0,34)*b.Cylinder(v.STEM_D/2+1e-5,34)))
  row={'cylinder':cylinder,'kind':kind,'axis_y_mm':-12,'guide_probe_world_z_mm':[280,300],'bore_radius_mm':.3438*25.4/2,'stem_radius_mm':v.STEM_D/2,'diametral_clearance_mm':.3438*25.4-v.STEM_D,'bore_intrusion_mm3':intrusion,'annular_support_missing_mm3':missing,'stem_outside_mm3':outside}
  r['guide_stem_datums'].append(row)
  assert max(intrusion,missing,outside)<1e-5,row
# Verify supplied baseline rocker/pushrod contacts on actual installed STEP at
# rest and peak before proposing replacement socket/pad coordinates.
r['installed_linkage_contacts']=[]
for cylinder in range(1,7):
 for kind in ['intake','exhaust']:
  tag=f'c{cylinder}-{kind}';center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(cylinder)*120
  for offset in [-150,0]:
   theta=(center+offset)%720;frames=transforms(m,theta);s=installed_state(theta,cylinder,kind);x=occ[tag+'-valve']['position_cad_mm'][0]
   placed={suffix:frames[tag+'-'+suffix]*shapes[occ[tag+'-'+suffix]['definition']] for suffix in ['rocker','valve','pushrod','lifter-pushrod-cup','fulcrum']}
   witness=b.Vertex(x,s['pad_y'],261+v.LENGTHS[kind]-s['valve_lift'])
   gaps={'pad_valve_witness':max(witness.distance_to(placed['rocker']),witness.distance_to(placed['valve']))}
   for a,z in [('rocker','pushrod'),('pushrod','lifter-pushrod-cup'),('rocker','fulcrum')]:gaps[a+'__'+z]=placed[a].distance_to(placed[z])
   row={'cylinder':cylinder,'kind':kind,'crank_degrees':theta,'contact_gaps_mm':gaps}
   r['installed_linkage_contacts'].append(row)
   assert max(gaps.values())<.002,row
save()
assert all(sha(ROOT/p)==h for p,h in inputs.items())
r['status']='PASS phase/contact contract and numeric proposal; new rocker/head adapters NOT BUILT'
r['limits']=['120 cam/lifter surface witnesses are sampled contacts, not continuous collision proof.','Common estimated rocker preserves nominal intake peak; exhaust residual reported, not scaled away.','No new rocker solid or head pedestal/passage/cover adaptation; remaining neighbors untested.','Valve guide CAD probes cover central20mm support; no production bore straightness/clearance claim.','Linkage springs, valve seats, piston clearance, hydraulic preload and oil-feed alignment require later coordinated checks.']
save();print(r['status'],flush=True)
