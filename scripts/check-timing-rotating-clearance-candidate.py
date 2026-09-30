#!/usr/bin/env python3
"""CAD containment + Lipschitz certificates, not a sparse-pose clearance claim."""
from pathlib import Path
import sys,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_rotating_clearance_candidate as c
from assembly_math import transforms
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-rotating-clearance-candidate';OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'inventory/engine/timing-rotating-clearance-candidate-validation.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def dump(p,q):p.write_text(json.dumps(q,indent=2)+'\n')
m,shapes,cam=c.inputs();occ=m['occurrences'];full=json.loads(c.MANIFEST.read_text());defs={d['id']:d for d in full['definitions']}
watch=[Path(__file__),Path(c.__file__),c.MANIFEST,c.CAM]+[ROOT/'cad/engine'/f for f in ['assembly_math.py','timing_coupled_core_candidate.py','cad_metrics.py','valve_layout_integration.py','valve_layout_candidate.py']]+[ROOT/'inventory/engine/timing-coupled-core-candidate-validation.json']+[ROOT/defs[k]['step'].lstrip('/') for k in shapes]
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
r={'status':'RUNNING','inputs':inputs,'scope':'Actual frozen camshaft/lobes versus crankshaft and every piston/rod group occurrence; no installed or production-fidelity claim','mechanism':m['mechanism'],'cam_axis_yz_mm':c.AXIS,'coverage':'All crank angles (hence full720degree engine cycle), all cam rotations, axial[-0.1,0]; static radial supports independent of cam phase. Rod proof uses Lipschitz bounds between5degree samples.','occurrences':[o['id'] for o in occ]}
def save():dump(REPORT,r)
save()
assert len({o['id'] for o in occ})==len(occ)
groups={a['id']:a for a in m['assemblies']}
for o in occ:
 g=groups[o['parent']]
 expected='crank' if o['id']=='crankshaft' else 'rod' if o['parent'].startswith('rod-group-') else 'piston'
 assert g['motion']['type']==expected
 assert g.get('rotation_cad_deg',[0,0,0])==[0,0,0]
 assert g['position_cad_mm'][1:]==[0,0]
 parent=g['parent']
 while parent in groups:
  g=groups[parent]
  assert not g.get('motion') and g.get('rotation_cad_deg',[0,0,0])==[0,0,0] and g.get('position_cad_mm',[0,0,0])==[0,0,0]
  parent=g['parent']
assert next(o for o in occ if o['id']=='crankshaft')['position_cad_mm']==[0,0,0]
assert next(o for o in occ if o['id']=='crankshaft').get('rotation_cad_deg',[0,0,0])==[0,0,0]
# Every support uses exact CAD difference, not mesh radius as an acceptance test.
r['cam_support_outside_mm3']=vol(cam.cut(c.cylinder(c.CAM_RADIUS,c.AXIS)))
r['crank_support_outside_mm3']=vol(shapes['crankshaft'].cut(c.cylinder(c.CRANK_RADIUS)))
assert max(r['cam_support_outside_mm3'],r['crank_support_outside_mm3'])<1e-5
r['crank_all_rotation_gap_bound_mm']=math.hypot(*c.AXIS)-c.CAM_RADIUS-c.CRANK_RADIUS
assert r['crank_all_rotation_gap_bound_mm']>0
poses=transforms(m,0);r['piston_certificates']=[]
for o in occ:
 if not o['parent'].startswith('piston-group-'):continue
 q=poses[o['id']]*shapes[o['definition']];bb=q.bounding_box()
 gap=c.AXIS[0]-c.CAM_RADIUS-bb.max.Y
 assert gap>0
 r['piston_certificates'].append({'id':o['id'],'world_y_max_mm':bb.max.Y,'all_motion_y_gap_bound_mm':gap})
# Rod transforms rotate only around X and do not change X. Axial cam movement
# means relevant baseline cam slice is [rod xmin,rod xmax+0.1]. Clip with overlap
# margin; exact cylinder containment makes all cam angles/axial poses safe.
r['rod_cam_slice_certificates']=[]
for o in occ:
 if not o['parent'].startswith('rod-group-'):continue
 bb=(poses[o['id']]*shapes[o['definition']]).bounding_box();lo=bb.min.X-1e-5;hi=bb.max.X+.10001
 clip=b.Pos((lo+hi)/2,*c.AXIS)*b.Box(hi-lo,100,100)
 s=cam.intersect(clip)
 outside=vol(s.cut(c.cylinder(c.ROD_STATION_RADIUS,c.AXIS)))
 assert outside<1e-5
 r['rod_cam_slice_certificates'].append({'id':o['id'],'baseline_cam_x_interval_mm':[lo,hi],'cam_radius_bound_mm':c.ROD_STATION_RADIUS,'outside_mm3':outside})
print('Crank, piston and all rod-station support containment PASS',flush=True);save()
# A point p on rod geometry moves with |p'| <= R+alpha_max_derivative*|p|,
# per crank radian, alpha'=-(R/L)cos(t)/sqrt(1-(R/L)^2sin(t)^2).
# Conservative alpha derivative R/sqrt(L²-R²). Distance to a fixed support
# is1-Lipschitz under this rigid displacement. Nearest sample is<=2.5degrees.
R=m['mechanism']['stroke_mm']/2;L=m['mechanism']['rod_length_mm'];step=5
support=c.cylinder(c.ROD_STATION_RADIUS,c.AXIS)
r['rod_motion_certificates']=[]
representatives=[o for o in occ if o['parent']=='rod-group-1']
for o in representatives:
 q=b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0]))*shapes[o['definition']]
 bb=q.bounding_box();rho=math.hypot(max(abs(bb.min.Y),abs(bb.max.Y)),max(abs(bb.min.Z),abs(bb.max.Z)))
 speed=R+R/math.sqrt(L*L-R*R)*rho;allow=speed*math.radians(step/2)
 rows=[]
 for theta in range(0,360,step):
  frame=transforms(m,theta)[o['id']]
  distance=(frame*shapes[o['definition']]).distance_to(support)
  rows.append({'crank_degrees':theta,'distance_mm':distance})
 minimum=min(rows,key=lambda z:z['distance_mm']);lower=minimum['distance_mm']-allow
 entry={'representative':o['id'],'sample_step_degrees':step,'speed_bound_mm_per_crank_radian':speed,'between_sample_allowance_mm':allow,'minimum_sample':minimum,'all_motion_gap_bound_mm':lower,'samples':rows,'reused_for':[z['id'] for z in occ if z['parent'].startswith('rod-group-') and z['id'].split('-',1)[1]==o['id'].split('-',1)[1]]}
 assert lower>0,entry
 # Verify each reused role has identical local geometry/offset and assembly
 # X-only cylinder placement, equal motion law, and merely a phase offset.
 groups={a['id']:a for a in m['assemblies']}
 for z in occ:
  if z['id'] not in entry['reused_for']:continue
  assert all(z.get(k)==o.get(k) for k in ['definition','position_cad_mm','rotation_cad_deg'])
  g=groups[z['parent']];assert g['position_cad_mm'][1:]==[0,0] and g.get('rotation_cad_deg',[0,0,0])==[0,0,0]
  assert g['motion']['type']=='rod'
 r['rod_motion_certificates'].append(entry);print(o['id'],lower,flush=True);save()
# Actual shared-transform closure, and wrong-sign rod tilt negative control.
r['motion_contract_checks']=[]
for theta in [0,90,180,270,360,540,720]:
 frames=transforms(m,theta)
 for i in range(1,7):
  rod=frames[f'c{i}-connecting-rod-1'];piston=frames[f'c{i}-piston-1']
  error=((rod*b.Vertex(0,0,L)).center()-(piston*b.Vertex(0,0,0)).center()).length
  assert error<1e-7
 r['motion_contract_checks'].append({'crank_degrees':theta,'six_small_end_closures_below_mm':1e-7})
wrong=b.Pos(284.48,-R,0)*b.Rot(-math.degrees(math.asin(-R/L)),0,0)*b.Vertex(0,0,L)
right=transforms(m,90)['c1-piston-1']*b.Vertex(0,0,0)
r['faults']={'wrong_rod_rotation_sign_closure_error_mm':(wrong.center()-right.center()).length}
assert r['faults']['wrong_rod_rotation_sign_closure_error_mm']>100
bad=b.Pos(0,-60,0)*cam
r['faults']['cam_axis_shift_minus60y_actual_crank_overlap_mm3']=vol(bad.intersect(shapes['crankshaft']))
assert r['faults']['cam_axis_shift_minus60y_actual_crank_overlap_mm3']>.1
assert all(sha(ROOT/p)==h for p,h in inputs.items())
r['status']='PASS conservative continuous rotating-clearance candidate; not installed'
r['limits']=['Actual shapes remain estimated; this certifies supplied geometry only.','No new lobe/valve timing calibration. Camshaft uses frozen complete keyed-group transform; no gear slipping.','Block, cover, valve linkage, distributor and pump remain separate dependencies.','Exact support differences use1e-5mm3 numerical audit tolerance, not a physical permitted interference.','No new STEP/GLB geometry generated; original STEP bytes are bound. Source comparison remains frozen prior evidence.']
save();print(r['status'],flush=True)
