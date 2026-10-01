#!/usr/bin/env python3
"""Actual frozen STEP checks; no geometry export or canonical mutation."""
from pathlib import Path
import sys,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import engine_clockwise_pose_candidate as c
REPORT=ROOT/'inventory/engine/engine-clockwise-pose-candidate-validation.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/timing_coupled_core_candidate.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'inventory/engine/full-assembly.json',ROOT/'inventory/engine/timing-gear-backlash-candidate-validation.json',ROOT/'inventory/engine/engine-rotation-convention-diagnostic.json']
parts={}
for key in ['crank','cam']:
 p=ROOT/f'cad/engine/generated/timing-gear-backlash-candidate/{key}.step';files.append(p);parts[key]=b.import_step(p)
 prior=json.loads((ROOT/'inventory/engine/timing-gear-backlash-candidate-validation.json').read_text())
 assert sha(p)==prior['build']['exports'][key]['step_sha256']
for key in ['crankshaft','rod','piston']:
 p=ROOT/f'cad/engine/generated/{key}.step';files.append(p);parts[key]=b.import_step(p)
 assert parts[key].is_valid and len(parts[key].solids())==1
watched={str(p.relative_to(ROOT)):sha(p) for p in files}
r={'status':'RUNNING','baseline':'9ab3c575','input_sha256':watched,'scope':'Read-only exported CAD and isolated corrected pose helper; no installed correction','gear_samples':[]}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def comp(q):return b.Compound(children=list(q.solids()))
def point(frame,xyz):return b.Vector(xyz).transform(b.Matrix(frame.wrapped.Transformation()))
def cylinders(shape):
 rows=[]
 for f in shape.faces():
  if f.geom_type!=b.GeomType.CYLINDER:continue
  cylinder=f.geom_adaptor().Cylinder();axis=cylinder.Axis();p=axis.Location();d=axis.Direction()
  if abs(d.X())<.999999:continue
  bb=f.bounding_box()
  rows.append(dict(radius_mm=cylinder.Radius(),axis_yz_mm=[p.Y(),p.Z()],station_x_mm=(bb.min.X+bb.max.X)/2))
 return rows
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())['mechanism'];R=m['stroke_mm']/2;L=m['rod_length_mm'];phases=m['cylinder_phases_deg']
# Geometry-derived cylindrical axes, not assumed mesh markers.
journals=[a for a in cylinders(parts['crankshaft']) if abs(math.hypot(*a['axis_yz_mm'])-R)<1e-6 and 26<a['radius_mm']<28]
journals.sort(key=lambda a:-a['station_x_mm']);assert len(journals)==6
rodaxes=cylinders(parts['rod']);big=next(a for a in rodaxes if 28<a['radius_mm']<29);small=next(a for a in rodaxes if 12<a['radius_mm']<13)
pin=next(a for a in cylinders(parts['piston']) if 12<a['radius_mm']<13)
assert abs(math.dist(big['axis_yz_mm'],small['axis_yz_mm'])-L)<1e-6
r['actual_geometry_axes']={'journals':journals,'rod_big':big,'rod_small':small,'piston_pin':pin}
maxima={'legacy_cad_matching_pose_closure_mm':0.,'rod_small_to_piston_pin_mm':0.,'required_new_pose_vs_legacy_cad_mm':0.,'double_phase_fault_mm':0.};rejections=[]
for i,a in enumerate(journals):
 y,z=a['axis_yz_mm'];rest=math.degrees(math.atan2(-y,z))%360;a['measured_rest_phase_deg']=rest;x=a['station_x_mm']
 for q in range(0,721,5):
  frames=c.slider_frames(q,rest,R,L,x);actual=point(c.crank_frame(q),(x,y,z))
  bigworld=point(frames['rod'],(0,*big['axis_yz_mm']));smallworld=point(frames['rod'],(0,*small['axis_yz_mm']));pinworld=point(frames['piston'],(0,*pin['axis_yz_mm']))
  maxima['legacy_cad_matching_pose_closure_mm']=max(maxima['legacy_cad_matching_pose_closure_mm'],(actual-bigworld).length)
  maxima['rod_small_to_piston_pin_mm']=max(maxima['rod_small_to_piston_pin_mm'],(smallworld-pinworld).length)
  required=point(c.slider_frames(q,-phases[i],R,L,x)['rod'],(0,0,0))
  maxima['required_new_pose_vs_legacy_cad_mm']=max(maxima['required_new_pose_vs_legacy_cad_mm'],(actual-required).length)
  double=point(c.slider_frames(q,2*rest,R,L,x)['rod'],(0,0,0))
  maxima['double_phase_fault_mm']=max(maxima['double_phase_fault_mm'],(actual-double).length)
 try:c.corrected_slider_frames(0,phases[i],R,L,x,measured_cad_rest_phase_degrees=rest)
 except ValueError:rejections.append(i+1)
r['linkage']={'sample_step_deg':5,'poses_per_branch':145,'maxima':maxima,'unrephased_cylinders_rejected':rejections,'actual_export_corrected_firing_compatibility':'FAIL: preserved legacy crank needs bounded throw rephasing; matching old CAD poses alone do not preserve firing sequence'}
assert maxima['legacy_cad_matching_pose_closure_mm']<1e-6 and maxima['rod_small_to_piston_pin_mm']<1e-6 and maxima['double_phase_fault_mm']>80 and rejections==[2,3,4,5]
save();print('Actual linkage axes checked',maxima,flush=True)
phi=math.atan2(c.AXIS[1],c.AXIS[0]);region=b.Pos(c.GEAR_X,40.6*math.cos(phi),40.6*math.sin(phi))*b.Rot(math.degrees(phi),0,0)*b.Box(16.4,14,44)
def measure(q,axial=0,extra=0):
 frames=c.gear_frames(q,axial)
 crank=comp((frames['crank']*parts['crank']).intersect(region))
 camshape=frames['cam']*parts['cam']
 if extra:camshape=b.Pos(0,*c.AXIS)*b.Rot(extra,0,0)*b.Pos(0,-c.AXIS[0],-c.AXIS[1])*camshape
 cam=comp(camshape.intersect(region));assert len(crank.solids()) and len(cam.solids())
 return {'event_deg':q,'axial_mm':axial,'cam_extra_deg':extra,'overlap_mm3':vol(crank.intersect(cam)),'gap_mm':crank.distance_to(cam)}
for i in range(13):
 for axial in [0.,-.1]:
  row=measure(i*(360/29)/12,axial);r['gear_samples'].append(row);save();print('Gear',row,flush=True)
  assert row['overlap_mm3']<1e-5 and row['gap_mm']>1e-6
faults={'wrong_cam_sign':measure(3,0,-3),'wrong_axial_compensation':measure(0,-.1,-2*math.degrees(c.K*-.1)),'duplicated_phase':measure(0,0,360/58/2)}
r['gear_faults']=faults
assert all(v['overlap_mm3']>1e-5 for v in faults.values()),faults
r['gear_scope']={'status':'PASS sampled clockwise crank / counterclockwise cam','angular_samples':13,'axial_endpoints_mm':[0,-.1],'tooth_counts':[29,58],'center_distance_mm':math.hypot(*c.AXIS),'continuous_rotation':'NOT PROVEN; one negative tooth period sampled','axial_interpolation':'Inherited exact helical correction K*delta retains cross-section angle, unchanged exported pair; neutral common slab contains shifted overlap slab.','phase':'Exported local tooth phase applied exactly once; no additional gear phase','backlash':'Frozen geometry and relative poses unchanged in reverse traversal; preserved prior two-sided bracket, no loaded dynamics'}
r['unsupported']=['Current crank export cannot preserve requested firing order with corrected rotation until throws are rephased','Cam lobe rephasing not performed','Crossed distributor/oil-drive handedness and contact unresolved','Whole-engine neighbors/endplay and browser NOT RUN']
assert all(sha(ROOT/p)==h for p,h in watched.items())
r['status']='PASS bounded helper/gear diagnostics; preserved crank export FAIL corrected-firing compatibility';save();print(r['status'],flush=True)
