"""Numerical reference from frozen CAD candidate; stdout is consumed by Node."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import cam_clockwise_candidate as cam
import timing_valvetrain_inclined_candidate as inclined
angles=sorted(set(range(0,721,5))|{(c+p)%720 for c in (246,468) for p in range(0,720,120)})
rows=[]
for q in angles:
 for axial in (0,-.1):
  for cylinder in range(1,7):
   for kind in ('intake','exhaust'):
    s=cam.state(q,cylinder,kind,axial)
    rows.append([q,axial,cylinder,kind,s])
files=['cad/engine/'+p for p in ('cam_clockwise_candidate.py','timing_valvetrain_inclined_candidate.py','timing_valvetrain_inclined_hypothesis.py','timing_axis_kinematic_candidate.py','engine_clockwise_pose_candidate.py','timing_coupled_core_candidate.py','valve_source_layout.py')]
import engine_clockwise_pose_candidate as motion
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
e=json.loads((ROOT/'inventory/engine/crank-clockwise-candidate-validation.json').read_text())
import math
sliders=[]
for q in angles:
 for i,phase in enumerate(m['mechanism']['cylinder_phases_deg']):
  measured=math.degrees(math.atan2(-e['actual_axes'][i]['yz'][0],e['actual_axes'][i]['yz'][1]))
  x=next(a['position_cad_mm'][0] for a in m['assemblies'] if a['id']==f'rod-group-{i+1}')
  r=m['mechanism']['stroke_mm']/2;l=m['mechanism']['rod_length_mm']
  frames=motion.corrected_slider_frames(q,phase,r,l,x,measured_cad_rest_phase_degrees=measured)
  sliders.append([q,phase,r,l,x,measured,{k:list(v.position) for k,v in frames.items()},math.radians(frames['rod'].orientation.X)])
import crossed_oil_drive_endplay_candidate as drive
shafts=[[q,x,*drive.angles(q,x)] for q in angles for x in (0,-.1)]
files+=['cad/engine/crossed_oil_drive_endplay_candidate.py']
files+=['inventory/engine/full-assembly.json','inventory/engine/crank-clockwise-candidate-validation.json']
print(json.dumps({'rows':rows,'sliders':sliders,'shafts':shafts,'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}}))
