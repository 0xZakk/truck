#!/usr/bin/env python3
"""Isolated export/core proof and finite backlash/axial coupling checks."""
from pathlib import Path
import sys,json,hashlib,math,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
from OCP.BRepTools import BRepTools
import timing_gear_backlash_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-gear-backlash-candidate';OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'inventory/engine/timing-gear-backlash-candidate-validation.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def comp(q):return b.Compound(children=list(q.solids()))
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
def write(name,r):(OUT/name).write_text(json.dumps(r,indent=2)+'\n')
def inputs():
 files=[Path(__file__),Path(c.__file__),Path(c.base.__file__),Path(c.refinement.__file__),Path(c.land.__file__),ROOT/'cad/engine/cad_metrics.py',ROOT/'reference/engine/timing-gear-backlash-review.json',ROOT/'inventory/engine/timing-gear-backlash-diagnostic.json',ROOT/'inventory/engine/timing-thrust-land-candidate-validation.json']
 ledger=json.loads((ROOT/'reference/engine/timing-gear-backlash-review.json').read_text())
 for row in ledger['sources']:
  p=ROOT/row['path'];assert sha(p)==row['sha256'];files.append(p)
 land=json.loads((ROOT/'inventory/engine/timing-thrust-land-candidate-validation.json').read_text())
 for key in ['cam','crank']:
  p=ROOT/f'cad/engine/generated/timing-thrust-land-candidate/{key}-timing-gear.step';assert sha(p)==land['exports'][key+'-timing-gear']['step_sha256'];files.append(p)
 return {str(p.relative_to(ROOT)):sha(p) for p in files}
def stable(w):assert all(sha(ROOT/p)==h for p,h in w.items())
def build():
 watched=inputs();parts=c.parts();exports={};guards={};old={}
 for key,q in parts.items():
  print('Built',key,flush=True);assert q.is_valid and len(q.solids())==1
  offset=(c.GEAR_X,*c.base.CAM_YZ) if key=='cam' else (c.GEAR_X,0,0)
  old[key]=b.Pos(*[-x for x in offset])*b.import_step(ROOT/f'cad/engine/generated/timing-thrust-land-candidate/{key}-timing-gear.step')
  radius=c.PARAMS['transverse_module_mm']*c.PARAMS[key+'_teeth']/2-1.25*c.PARAMS['transverse_module_mm']-.5
  guard=c.land.cylinder(radius,30)
  core=comp(q.intersect(guard));prior=comp(old[key].intersect(guard));error=diff(core,prior);assert error<1e-5,(key,error)
  tip=c.PARAMS[key+'_tip_diameter_mm']/2
  envelope=c.land.cylinder(tip+.000001,14.000002)
  outside=vol(q.cut(envelope))+vol(old[key].cut(envelope));assert outside<1e-5
  guards[key]=dict(core_radius_mm=radius,core_difference_mm3=error,outside_tooth_envelope_mm3=outside,tooth_ring_mm=[radius,tip],axial_span_mm=[-7,7])
  sp=OUT/(key+'.step');b.export_step(q,sp);rt=b.import_step(sp);assert rt.is_valid and len(rt.solids())==1
  volume_error=abs(vol(q)-vol(rt));assert volume_error<.001
  BRepTools.Clean_s(q.wrapped);v,f=q.tessellate(.05,.1)
  mesh=trimesh.Trimesh(np.array([tuple(p) for p in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(f),process=False);mesh.merge_vertices();mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(key+'.glb');mesh.export(gp)
  actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8);assert actual.is_watertight and actual.nondegenerate_faces().all() and actual.unique_faces().all()
  vv=actual.vertices[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert err<.15
  exports[key]=dict(step_sha256=sha(sp),glb_sha256=sha(gp),valid=True,solids=1,watertight=True,triangles=len(actual.faces),bounds_error_mm=err,roundtrip_volume_error_mm3=volume_error)
  print('Core and export',key,guards[key],exports[key],flush=True)
 probe=b.Pos(-4,24,0)*b.Sphere(.5);guard=c.land.cylinder(77.2,30);fault=diff(comp(parts['cam'].intersect(guard)),comp((parts['cam']-probe).intersect(guard)));assert fault>.4
 stable(watched);write('build-report.json',dict(status='PASS isolated core and exports',input_sha256=watched,parameters=c.PARAMS,exports=exports,protected_core=guards,core_fault_detected_mm3=fault,base_globals_unchanged=c.base.PARAMS['backlash_mm']==.12))
def motion():
 watched=inputs();build=json.loads((OUT/'build-report.json').read_text());assert build['input_sha256']==watched
 parts={k:b.import_step(OUT/(k+'.step')) for k in ['crank','cam']}
 for k in parts:assert sha(OUT/(k+'.step'))==build['exports'][k]['step_sha256']
 phi=c.base.AXIS_ANGLE;region=b.Pos(0,40.6*math.cos(phi),40.6*math.sin(phi))*b.Rot(math.degrees(phi),0,0)*b.Box(16.4,14,44)
 def measure(theta,extra=0,axial=0):
  a=comp((b.Rot(theta,0,0)*parts['crank']).intersect(region));z=comp((b.Pos(axial,*c.base.CAM_YZ)*b.Rot(-theta/2+extra,0,0)*parts['cam']).intersect(region))
  return dict(crank_degrees=theta,cam_extra_degrees=extra,axial_mm=axial,overlap_mm3=vol(a.intersect(z)),gap_mm=a.distance_to(z))
 bracketrows=[];brackets=[];radius=c.PARAMS['transverse_module_mm']*58/2
 for theta in [0,180/29]:
  sides=[]
  for sign in [-1,1]:
   rows=[]
   for magnitude in [.025,.030]:
    row=measure(theta,sign*magnitude);rows.append(row);bracketrows.append(row);print('Contact',row,flush=True);write('contact-progress.json',bracketrows)
   free=[abs(r['cam_extra_degrees']) for r in rows if r['overlap_mm3']<1e-5 and r['gap_mm']>1e-6];hit=[abs(r['cam_extra_degrees']) for r in rows if r['overlap_mm3']>1e-5];assert free and hit,rows
   sides.append([max(free),min(hit)])
  play=[math.radians(sum(s[i] for s in sides))*radius for i in [0,1]];assert .0508<=play[0]<=play[1]<=.1016
  brackets.append(dict(crank_degrees=theta,pitch_circle_play_mm=play))
 k=c.CAM_K_RAD_PER_MM;delta=-.1;correction=math.degrees(k*delta)
 fixed=measure(0,0,delta);wrong=measure(0,-correction,delta);correct=measure(0,correction,delta)
 write('axial-sign-witnesses.json',dict(fixed_phase=fixed,opposite_sign=wrong,correct_sign=correct,k_rad_per_mm=k))
 assert fixed['overlap_mm3']>1e-5 and wrong['overlap_mm3']>1e-5
 assert correct['overlap_mm3']<1e-5 and correct['gap_mm']>1e-6
 rows=[]
 for theta in np.linspace(0,360/29,25):
  for axial in [0.,-.1]:
   r=measure(float(theta),math.degrees(k*axial),axial);rows.append(r);print('Sweep',r,flush=True);write('sweep-progress.json',rows)
   assert r['overlap_mm3']<1e-5 and r['gap_mm']>1e-6
 stable(watched)
 report=dict(status='PASS isolated midpoint-clearance study; fixed-phase axial hypothesis FAIL; coupled motion finite checks PASS; UNINSTALLED',input_sha256=watched,build=build,contact_rows=bracketrows,two_sided_brackets=brackets,service_range_mm=[.0508,.1016],service_interpretation='Tangential pitch-circle indicator assumed; source tip radius/direction unspecified',axial_sign_witnesses=dict(fixed_phase=fixed,opposite_sign=wrong,correct_sign=correct),cam_k_rad_per_mm=k,sweep=rows,continuous_axial_argument='At each sampled crank angle only: generator cam hand=-1 gives cross-section angle k*x. Translating delta and rotating k*delta preserves that angle at every world X. Crank spans X[-7,7]; shifted cam spans[-7+delta,7+delta], so their common axial slab is a subset of neutral slab for delta in[-0.1,0]. Tooth-profile helix invariant in that slab; neutral nonintersection therefore bounds every intermediate axial position. Core remains below tooth ring and is excluded from this gear-pair-only argument.',limits=['25 rotations over one tooth period, not continuous rotation dynamics or loaded contact','Midpoint fit is not production calibration; source indicator radius/direction remains unknown','Coupled cam rotation changes core/valvetrain phase; no whole-core or full-engine coupled motion proof','All module/profile/axis/helix/thrust-land dimensions remain previously stated estimates'])
 REPORT.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--motion',action='store_true');a=p.parse_args()
 if a.build:build()
 if a.motion:motion()
 if not(a.build or a.motion):p.error('Use --build then --motion')
