#!/usr/bin/env python3
"""Source replay, bounded lobe revision, export and sampled actual contacts."""
from pathlib import Path
import sys,json,hashlib,math,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import cam_clockwise_candidate as c
OUT=ROOT/'cad/engine/generated/cam-clockwise-candidate';OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
def save(kind,r):(ROOT/f'inventory/engine/cam-clockwise-candidate-{kind}-validation.json').write_text(json.dumps(r,indent=2)+'\n')
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']}
watch=[Path(__file__),Path(c.__file__),c.PROFILE,c.BASE,ROOT/'inventory/engine/full-assembly.json']+[ROOT/'cad/engine'/p for p in ['valve_motion_candidate.py','valve_layout_candidate.py','valve_layout_integration.py','engine_clockwise_pose_candidate.py','timing_coupled_core_candidate.py','timing_valvetrain_inclined_candidate.py','timing_valvetrain_inclined_hypothesis.py','timing_valvetrain_adapter_candidate.py','timing_axis_kinematic_candidate.py','valve_source_layout.py','cad_metrics.py']]
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
def stable():assert all(sha(ROOT/p)==h for p,h in inputs.items())
def build():
 import numpy as np,trimesh
 from OCP.BRepTools import BRepTools
 old=b.Pos(0,-c.AXIS[0],-c.AXIS[1])*b.import_step(c.BASE)
 replay=c.revise_local(old,m,1);error=diff(old,replay);print('Replay',error,flush=True);assert error<1e-5
 new=c.revise_local(old,m,-1);assert new.is_valid and len(new.solids())==1
 protected_old=old;protected_new=new;rows=[]
 for i,kind,x,phase in c.stations(m):
  mask=b.Pos(x,0,0)*b.Rot(0,90,0)*b.Cylinder(26.0001,15.0002);protected_old=protected_old.cut(mask);protected_new=protected_new.cut(mask)
  core=b.Pos(x,0,0)*b.Rot(0,90,0)*b.Cylinder(17.9,14.9)
  core_error=vol(core.cut(old))+vol(core.cut(new));print('Core',i,kind,core_error,flush=True);assert core_error<1e-5
  slab=b.Pos(x,0,0)*b.Box(14.9,60,60)
  local_change=diff(old.intersect(slab),new.intersect(slab))
  rows.append(dict(cylinder=i,kind=kind,x_mm=x,old_phase_deg=phase,new_phase_deg=-phase,core_difference_mm3=core_error,boolean_changed_mm3_untrusted=local_change));print('Station',rows[-1],flush=True)
 outside=diff(protected_old,protected_new);assert outside<1e-5
 # Critical protected-region control: remove an actual shaft interior sphere.
 probe=b.Pos(0,0,0)*b.Sphere(.5);fault=diff(protected_old,protected_old.cut(probe));assert fault>.4
 p=OUT/'camshaft-local.step';b.export_step(new,p);rt=b.import_step(p);assert rt.is_valid and len(rt.solids())==1
 roundtrip=abs(vol(new)-vol(rt));assert roundtrip<.001
 world=b.Pos(0,*c.AXIS)*rt;wp=OUT/'camshaft.step';b.export_step(world,wp)
 BRepTools.Clean_s(rt.wrapped);v,f=rt.tessellate(.05,.1)
 mesh=trimesh.Trimesh(np.array([tuple(p) for p in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/'camshaft-local.glb';mesh.export(gp)
 actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8)
 assert actual.is_watertight and actual.is_winding_consistent and actual.volume>0
 vv=actual.vertices[:,[0,2,1]]*[1,-1,1]*1000;bb=rt.bounding_box();bounds=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert bounds<.15
 stable();r=dict(status='PASS bounded source replay, phase-only revision and export',inputs=inputs,replay_difference_mm3=error,outside_masks_difference_mm3=outside,stations=rows,protected_region_fault_mm3=fault,exports={str(p.relative_to(ROOT)):sha(p) for p in [p,wp,gp]},roundtrip_volume_error_mm3=roundtrip,mesh={'watertight':True,'winding_consistent':True,'positive_volume':True,'triangles':len(actual.faces),'bounds_error_mm':bounds},limits=['Crossed-drive geometry unchanged but corrected handedness unsupported','No whole-engine or browser acceptance']);save('build',r);print(r['status'],flush=True)
def contact():
 prior=json.loads((ROOT/'inventory/engine/cam-clockwise-candidate-build-validation.json').read_text());assert prior['inputs']==inputs
 p=OUT/'camshaft.step';assert sha(p)==prior['exports'][str(p.relative_to(ROOT))];cam=b.import_step(p)
 lifterpath=ROOT/defs['lifter-body']['step'].lstrip('/');lifter=b.import_step(lifterpath)
 r=dict(status='RUNNING',inputs=inputs,build_report_sha256=sha(ROOT/'inventory/engine/cam-clockwise-candidate-build-validation.json'),lifter_sha256=sha(lifterpath),contacts=[],controls=[])
 old=b.import_step(c.BASE)
 for cylinder,kind,x,phase in c.stations(m):
  # Actual exported station, clipped away from distant irrelevant lobes.
  clip=b.Pos(x,*c.AXIS)*b.Box(15.00001,60,60);lobe=cam.intersect(clip);oldlobe=old.intersect(clip)
  for offset in [-150,-96,0,96,150]:
   for axial in [0.,-.1]:
    q=(2*phase+offset)%720;s=c.state(q,cylinder,kind,axial);posed=c.cam_frame(q,axial)*lobe
    body=b.Pos(x,c.AXIS[0],114.8+c.AXIS[1]-72+s['lifter_lift'])*lifter
    w=b.Vertex(*c.tangent(q,cylinder,kind,axial,x))
    overlap=vol(posed.intersect(body));assert overlap<1e-5,(cylinder,kind,q,axial,overlap)
    row=dict(overlap_mm3=overlap,cylinder=cylinder,kind=kind,event_deg=q,offset_deg=offset,axial_mm=axial,cam_witness_gap_mm=w.distance_to(posed),lifter_witness_gap_mm=w.distance_to(body),normal_fault_mm=(b.Pos(0,0,.1)*w).distance_to(posed))
    assert max(row['cam_witness_gap_mm'],row['lifter_witness_gap_mm'])<.002,row
    assert row['normal_fault_mm']>.05,row
    r['contacts'].append(row)
    if offset==-96 and axial==0:
     omitted=w.distance_to(c.cam_frame(q,0)*oldlobe)
     wrong=b.Pos(0,*c.AXIS)*b.Rot(-q/2,0,0)*b.Pos(0,-c.AXIS[0],-c.AXIS[1])*lobe
     r['controls'].append(dict(cylinder=cylinder,kind=kind,omitted_rephase_gap_mm=omitted,wrong_spin_gap_mm=w.distance_to(wrong)))
  save('contact',r);print('Contact',cylinder,kind,'PASS',flush=True)
 assert max(v['omitted_rephase_gap_mm'] for v in r['controls'])>.1
 assert max(v['wrong_spin_gap_mm'] for v in r['controls'])>.1
 stable();r['status']='PASS 120 sampled actual cam/lifter contact witnesses and phase/sign controls';r['limits']=['Surface witnesses plus normal controls are sampled contact checks, not whole-lobe continuous collision proof','Unchanged profile law and reflected tangent have analytic symmetry; actual spline approximation remains bounded by sampled surface test','Crossed drive and spring compressed CAD are not accepted by linkage-frame helper'];save('contact',r);print(r['status'],flush=True)
a=argparse.ArgumentParser();a.add_argument('--build',action='store_true');a.add_argument('--contact',action='store_true');args=a.parse_args()
if args.build:build()
if args.contact:contact()
if not(args.build or args.contact):a.error('Choose --build or --contact')
