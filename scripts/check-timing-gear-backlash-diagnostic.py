#!/usr/bin/env python3
"""Two-sided free-play diagnostic of the frozen estimated timing pair."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_gear_pair_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-gear-pair-candidate'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
paths=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/cad_metrics.py',OUT/'crank.step',OUT/'cam.step'];inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}
parts={key:b.import_step(OUT/(key+'.step')) for key in ['crank','cam']}
region=b.Pos(0,40.6*math.cos(c.AXIS_ANGLE),40.6*math.sin(c.AXIS_ANGLE))*b.Rot(math.degrees(c.AXIS_ANGLE),0,0)*b.Box(16,14,44)
rows=[]
for theta in [0,180/c.PARAMS['crank_teeth']]:
 a=b.Compound(children=list((b.Rot(theta,0,0)*parts['crank']).intersect(region).solids()))
 for extra in [-.09,-.08,.08,.09]:
  cam=b.Pos(0,*c.CAM_YZ)*b.Rot(-theta/2+extra,0,0)*parts['cam'];z=b.Compound(children=list(cam.intersect(region).solids()));overlap=vol(a.intersect(z));gap=a.distance_to(z)
  row=dict(crank_degrees=theta,cam_extra_degrees=extra,overlap_mm3=overlap,local_gap_mm=gap);rows.append(row);print(row,flush=True)
assert all(sha(ROOT/p)==h for p,h in inputs.items())
brackets=[]
radius=c.PARAMS['transverse_module_mm']*c.PARAMS['cam_teeth']/2
for theta in sorted({r['crank_degrees'] for r in rows}):
 q=[r for r in rows if r['crank_degrees']==theta]
 sides=[]
 for sign in [-1,1]:
  side=[r for r in q if sign*r['cam_extra_degrees']>0]
  free=[abs(r['cam_extra_degrees']) for r in side if r['overlap_mm3']<1e-5 and r['local_gap_mm']>1e-6]
  hit=[abs(r['cam_extra_degrees']) for r in side if r['overlap_mm3']>1e-5]
  assert free and hit,'Contact bracket unavailable'
  sides.append([max(free),min(hit)])
 angular=[sum(s[i] for s in sides) for i in [0,1]]
 circular=[math.radians(a)*radius for a in angular]
 brackets.append(dict(crank_degrees=theta,two_sided_angular_play_deg=angular,pitch_circle_play_mm=circular,exceeds_service_max_under_pitch_circle_interpretation=circular[0]>.004*25.4))
r=dict(status='FAIL service-backlash comparison; frozen estimated gear pair remains unaccepted',input_sha256=inputs,rows=rows,brackets=brackets,pitch_radius_mm=radius,analytical_tooth_thinning_pair_play_mm=2*c.PARAMS['backlash_mm'],service_range_mm=[.002*25.4,.004*25.4],limits=['Two sampled crank phases, fixed axial position. No continuous loaded-contact proof.','Service excerpt specifies dial indicator but does not state tip radius/direction; pitch-circle interpretation is explicit and needs corroboration.','Analytic ideal involute thinning is not exact faceted CAD. Two-sided CAD bracket independently measures the exported hypothesis.','Do not replace rotational free play with the unloaded single-pose nearest-surface distance. No canonical geometry changed.'])
assert all(x['exceeds_service_max_under_pitch_circle_interpretation'] for x in brackets)
(ROOT/'inventory/engine/timing-gear-backlash-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
