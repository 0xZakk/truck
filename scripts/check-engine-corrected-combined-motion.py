#!/usr/bin/env python3
"""Bounded phase-correlation review, conservative reuse and actual named snapshot."""
from pathlib import Path
import sys,json,math,hashlib,argparse,itertools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import engine_corrected_combined_candidate as c
OUT=ROOT/'cad/engine/generated/engine-corrected-combined-candidate';OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'inventory/engine/engine-corrected-combined-motion-validation.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def bounds(q):
 bb=q.bounding_box();return [list(bb.min),list(bb.max)]
def broad(a,z):return all(min(a[1][i],z[1][i])-max(a[0][i],z[0][i])>1e-7 for i in range(3))
def witness(a,z):
 common=a.intersect(z)
 if common:
  for s in common.solids():
   p=s.center()
   if a.is_inside(p,tolerance=1e-7) and z.is_inside(p,tolerance=1e-7):return list(p)
 aa,zz=bounds(a),bounds(z)
 lo=[max(aa[0][i],zz[0][i]) for i in range(3)];hi=[min(aa[1][i],zz[1][i]) for i in range(3)]
 for p in itertools.product(*[[l+(h-l)*t for t in [.2,.5,.8]] for l,h in zip(lo,hi)]):
  if a.is_inside(p,tolerance=1e-7) and z.is_inside(p,tolerance=1e-7):return list(p)
 return None
m,paths,sh=c.load();occ={o['id']:o for o in m['occurrences']};groups={a['id']:a for a in m['assemblies']}
report_paths=['crank-clockwise-candidate-validation.json','cam-clockwise-candidate-delivery-validation.json','timing-rotating-clearance-candidate-validation.json','timing-rocker-crest-delivery-validation.json','timing-front-block-expanded-seat-v3-delivery-validation.json','timing-pan-expanded-seat-v2-candidate-validation.json']
watch=[Path(__file__),Path(c.__file__),c.MANIFEST]+list(set(paths.values()))+[ROOT/'inventory/engine'/p for p in report_paths]+[ROOT/'cad/engine'/p for p in ['cam_clockwise_candidate.py','engine_clockwise_pose_candidate.py','assembly_math.py','cad_metrics.py']]
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
r=json.loads(REPORT.read_text()) if REPORT.exists() else dict(status='RUNNING',inputs=inputs,coverage={},conflicts=[])
assert r['inputs']==inputs,'Changed combined inputs; preserve report before new revision'
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
def stable():assert all(sha(ROOT/p)==h for p,h in inputs.items())
def cylinder(radius,xlo,xhi,axis=(0,0)):return b.Pos((xlo+xhi)/2,*axis)*b.Rot(0,90,0)*b.Cylinder(radius,xhi-xlo)
def compare(key,a,zkey,z,meta=None):
 row=dict(a=key,b=zkey,**(meta or {}))
 if not broad(bounds(a),bounds(z)):row['bounds_separated']=True;row['overlap_mm3']=0.;return row
 overlap=vol(a.intersect(z));row.update(bounds_separated=False,overlap_mm3=overlap)
 if overlap>.1:row['strict_material_witness']=witness(a,z);r['conflicts'].append(row)
 return row

def supports():
 prior=json.loads((ROOT/'inventory/engine/timing-rotating-clearance-candidate-validation.json').read_text())
 for p,h in prior['inputs'].items():assert sha(ROOT/p)==h,p
 rows={}
 for key,radius,axis in [('camshaft',25.622251,c.cam.AXIS),('crankshaft',87.546001,(0,0))]:
  outside=vol(sh[key].cut(cylinder(radius,-600,600,axis)));assert outside<1e-5
  rows[key]=dict(radius_mm=radius,outside_mm3=outside)
 rows['cam_crank_all_angle_gap_mm']=math.hypot(*c.cam.AXIS)-25.622251-87.546001
 assert rows['cam_crank_all_angle_gap_mm']>0
 slices=[];seen=set()
 for row in prior['rod_cam_slice_certificates']:
  lo,hi=row['baseline_cam_x_interval_mm'];interval=(lo,hi)
  if interval in seen:continue
  seen.add(interval);piece=sh['camshaft'].intersect(b.Pos((lo+hi)/2,*c.cam.AXIS)*b.Box(hi-lo,100,100))
  outside=vol(piece.cut(cylinder(15.001,-600,600,c.cam.AXIS)));assert outside<1e-5
  slices.append(dict(x_interval_mm=interval,outside_mm3=outside))
 rows['fresh_cam_rod_slices']=slices
 # Rod geometry, local placements and source mechanism are identical by manifest
 # and input hashes. q->-q-2*event_phase traverses exactly the old full pose set.
 rows['rod_certificate_reuse']=[{k:x[k] for k in ['representative','all_motion_gap_bound_mm','speed_bound_mm_per_crank_radian','between_sample_allowance_mm','reused_for']} for x in prior['rod_motion_certificates']]
 rows['piston_cam_minimum_all_motion_y_gap_mm']=min(x['all_motion_y_gap_bound_mm'] for x in prior['piston_certificates'])
 fixed=c.posed(m,sh,0);cb=sh['camshaft'].bounding_box()
 cam_envelope=cylinder(25.622251,cb.min.X-.1,cb.max.X,c.cam.AXIS)
 rows['cam_block_envelope_overlap_mm3']=vol(cam_envelope.intersect(fixed['block']))
 rows['cam_block_envelope_gap_mm']=cam_envelope.distance_to(fixed['block'])
 rows['cam_block_continuous_certificate']=rows['cam_block_envelope_overlap_mm3']<1e-5 and rows['cam_block_envelope_gap_mm']>1e-6
 rows['cam_pan_bounds_separated']=not broad(bounds(cam_envelope),bounds(fixed['oil-pan']))
 stock=[('rear-flywheel-register',cylinder(22.200001,-398,-393)),('main-axis',cylinder(30.462221,-387,357.376)),('nose',cylinder(21.000001,333.376,490.12)),('rear-register',cylinder(45.000001,-387,-363)),('rear-flange',cylinder(51.000001,-393,-383))]
 for i,phase in enumerate(m['mechanism']['cylinder_phases_deg'],1):
  x=groups[f'rod-group-{i}']['position_cad_mm'][0];stock.append((f'throw-{i}',cylinder(87.546001,x-41,x+41)))
 remaining=sh['crankshaft']
 for _,s in stock:remaining=remaining.cut(s)
 rows['crank_swept_stock_containment_outside_mm3']=vol(remaining);assert rows['crank_swept_stock_containment_outside_mm3']<1e-5
 rows['crank_stock_stationary']=[]
 for name,s in stock:
  for key in ['block','oil-pan']:
   v=vol(s.intersect(fixed[key]));gap=s.distance_to(fixed[key]);rows['crank_stock_stationary'].append(dict(stock=name,neighbor=key,overlap_mm3=v,gap_mm=gap,continuous_clear=v<1e-5 and gap>1e-6))
 # Stock overlap is inconclusive, not a physical conflict; actual shifted crank
 # is a separate material-positive negative control on this neighborhood.
 bad=b.Pos(0,60,0)*sh['crankshaft'];fault=vol(bad.intersect(fixed['block']));assert fault>.1
 rows['translated_crank_fault_mm3']=fault;rows['translated_crank_fault_witness']=witness(bad,fixed['block']);assert rows['translated_crank_fault_witness']
 r['supports']=rows;r['coverage']['support_reuse']='Continuous cam/crank/rod/piston proof only where fresh containment passes; rod phase reversal is a full-motion reparameterization.'
 stable();save();print('Support stage complete',rows['cam_block_envelope_overlap_mm3'],[(x['stock'],x['neighbor'],x['overlap_mm3']) for x in rows['crank_stock_stationary'] if not x['continuous_clear']],flush=True)

def triage():
 fixed=c.posed(m,sh,0);rows=[]
 # Parentwise critical phases include two transverse extrema, TDC/BDC and the
 # frozen closest rod/cam angle with its opposite flank. Other phases untested.
 for i,phi in enumerate(m['mechanism']['cylinder_phases_deg'],1):
  ids=[o['id'] for o in m['occurrences'] if o['parent']==f'rod-group-{i}']
  for t in [0,55,90,180,270,305]:
   q=(-t-phi)%360;frames=c.frames(m,q)
   for key in ids:
    shape=frames[key]*sh[key]
    for neighbor in ['block','oil-pan']:rows.append(compare(key,shape,neighbor,fixed[neighbor],dict(event_deg=q,local_crank_deg=t)))
   r['rod_stationary_samples']=rows;save();print('Rod',i,t,'conflicts',len(r['conflicts']),flush=True)
 # Only actual poses for stock-inconclusive crank/block/pan certificates.
 inconclusive={x['neighbor'] for x in r['supports']['crank_stock_stationary'] if not x['continuous_clear']}
 for q in [0,55,90,180,270,305]:
  crank=c.motion.crank_frame(q)*sh['crankshaft']
  for neighbor in inconclusive:rows.append(compare('crankshaft',crank,neighbor,fixed[neighbor],dict(event_deg=q)))
 if not r['supports']['cam_block_continuous_certificate']:
  for q in range(0,720,60):
   for axial in [0,-.1]:rows.append(compare('camshaft',c.motion.cam_frame(q,axial)*sh['camshaft'],'block',fixed['block'],dict(event_deg=q,axial_mm=axial)))
 r['rod_stationary_samples']=rows;r['coverage']['rod_stationary']='6 local phases x6 cylinders x8 rod constituents x2 neighbors; finite actual CAD, not continuous';stable();save()

def piston_valves():
 rows=[];radius=m['mechanism']['stroke_mm']/2;length=m['mechanism']['rod_length_mm'];fixed=c.posed(m,sh,0)
 for i,phi in enumerate(m['mechanism']['cylinder_phases_deg'],1):
  piston=sh[f'c{i}-piston-1'];top=piston.bounding_box().max.Z
  for kind in ['intake','exhaust']:
   vid=f'c{i}-{kind}-valve';bottom=sh[vid].bounding_box().min.Z;minimum=None
   for q in range(721):
    t=math.radians(q+phi);height=radius*math.cos(t)+math.sqrt(length**2-(radius*math.sin(t))**2)
    for axial in [0,-.1]:
     lift=c.cam.state(q,i,kind,axial)['valve_lift'];gap=occ[vid]['position_cad_mm'][2]+bottom-lift-height-top
     if minimum is None or gap<minimum['vertical_gap_mm']:minimum=dict(cylinder=i,kind=kind,event_deg=q,axial_mm=axial,vertical_gap_mm=gap)
   frames=c.frames(m,minimum['event_deg'],minimum['axial_mm']);p=frames[f'c{i}-piston-1']*piston;v=frames[vid]*sh[vid]
   minimum.update(compare(f'c{i}-piston-1',p,vid,v));minimum['actual_distance_mm']=p.distance_to(v);rows.append(minimum)
 r['piston_valve_minima']=rows;r['coverage']['piston_valve']='721 event samples x6 cylinders x2 valves x2 axial endpoints using conservative vertical bounds, actual CAD at12 minima; no continuous certificate';stable();save()

def snapshot():
 q=55.;placed=c.posed(m,sh,q,0);children=[];pose=c.frames(m,q,0);records=[]
 for key,shape in placed.items():
  shape.label=key;children.append(shape)
  t=pose[key].wrapped.Transformation();records.append(dict(id=key,source=str(paths[key].relative_to(ROOT)),source_sha256=sha(paths[key]),matrix_3x4=[[t.Value(i,j) for j in range(1,5)] for i in range(1,4)],world_bounds_mm=bounds(shape)))
 p=OUT/'combined-q55.step';b.export_step(b.Compound(children=children),p)
 layout=dict(event_deg=q,cam_axial_mm=0,parts=records,omissions=['Valve springs: compressed geometry intentionally not substituted with rest spring','Crossed distributor/oil drive and accessories','All other engine occurrences outside selected snapshot'])
 lp=OUT/'combined-q55-layout.json';lp.write_text(json.dumps(layout,indent=2)+'\n')
 r['snapshot']=dict(step_sha256=sha(p),layout_sha256=sha(lp),parts=len(records),event_deg=q,axial_mm=0)
 r['coverage']['crest_reuse']='Nominal axial0 upper linkage law exactly unchanged; prior216-frame API replay and exact crest/head/cover bytes support prior sampled target-branch results. New block not silently substituted into old neighbor proof.'
 stable();r['status']='FAIL actual conflicts found; snapshot is diagnostic' if r['conflicts'] else 'PASS bounded combined-motion checks; missing coverage retained';r['missing_coverage']=['Crossed distributor/oil-drive region pending','Continuous whole rod/block/pan sweep','Whole-engine interactions beyond selected scope','Old pan/block aggregate acceptance gaps remain','Valve spring compressed geometry absent from snapshot','New block versus full upper-linkage sweep not exhaustively repeated','Browser NOT RUN'];save();print(r['status'],flush=True)
a=argparse.ArgumentParser()
for name in ['supports','triage','piston-valves','snapshot']:a.add_argument('--'+name,action='store_true')
args=a.parse_args();save()
if args.supports:supports()
if args.triage:triage()
if args.piston_valves:piston_valves()
if args.snapshot:snapshot()
