"""Fail-closed baseline reproduction before crank phase candidate export."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import math,numpy as np,trimesh
import engine_clockwise_pose_candidate as motion
import crank_clockwise_candidate as c
OUT=ROOT/'cad/engine/generated/crank-clockwise-candidate';OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=ROOT/'cad/engine/generated/crankshaft.step'
paths=[Path(motion.__file__),ROOT/'cad/engine/generated/rod.step',ROOT/'cad/engine/generated/piston.step',base,Path(c.__file__),Path(c.e.__file__),Path(__file__),ROOT/'inventory/engine/full-assembly.json',ROOT/'reference/engine/engine-rotation-convention-review.json']
for name in ['flywheel','pilot_bearing','damper_attachment']:paths.append(ROOT/'cad/engine'/(name+'.py'))
r={'status':'RUNNING','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths},'event_phases':c.EVENT_PHASES,'proposed_rest_phases':c.REST_PHASES}
report=ROOT/'inventory/engine/crank-clockwise-candidate-validation.json'
def save():report.write_text(json.dumps(r,indent=2)+'\n')
def volume(s):return sum(abs(x.volume) for x in s.solids()) if s else 0.
save();print('rebuild original source phases',flush=True)
old=b.import_step(base);replay=c.shape(c.EVENT_PHASES)
r['baseline_reproduction']={'missing_mm3':volume(old.cut(replay)),'added_mm3':volume(replay.cut(old)),'valid':replay.is_valid}
print(r['baseline_reproduction'],flush=True);save()
if sum(r['baseline_reproduction'][k] for k in ['missing_mm3','added_mm3'])>.1:
 r['status']='FAIL original source does not reproduce canonical; no candidate adopted';save();raise SystemExit(1)
print('build rephased candidate',flush=True);new=c.shape()
assert new.is_valid and len(new.solids())==1
c.e.STEP=OUT;c.e.OUT=OUT
c.e.define('crankshaft',new,'Clockwise crankshaft candidate','Corrected throw rest phases; provisional production contours.','rotating',prepared=True)
rt=b.import_step(OUT/'crankshaft.step')
r['roundtrip_difference_mm3']=volume(new.cut(rt))+volume(rt.cut(new));assert r['roundtrip_difference_mm3']<.1
added=b.Compound(children=list(new.cut(old).solids()));removed=b.Compound(children=list(old.cut(new).solids()))
guards={'front-end':b.Pos(750,0,0)*b.Box(800,1000,1000),'rear-end':b.Pos(-750,0,0)*b.Box(800,1000,1000)}
for i,x in enumerate(c.e.MAINS):guards[f'main-{i+1}']=b.Pos(x,0,0)*c.e.cx(c.e.MAIN_R,32)
r['protected_regions']={}
for name,guard in guards.items():
 error=volume(added.intersect(guard))+volume(removed.intersect(guard));assert error<.1,(name,error)
 r['protected_regions'][name]=error
allowed=None
for x,a,z in zip(c.e.CYLINDERS,c.EVENT_PHASES,c.REST_PHASES):
 if a==z:continue
 band=b.Pos(x,0,0)*b.Box(82.000002,1000,1000)
 allowed=band if allowed is None else allowed+band
r['outside_changed_throw_bands_mm3']=volume(added.cut(allowed))+volume(removed.cut(allowed));assert r['outside_changed_throw_bands_mm3']<.1
mesh=trimesh.load(OUT/'crankshaft.glb',force='mesh');mesh.merge_vertices()
assert mesh.is_watertight and mesh.is_winding_consistent
v=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=rt.bounding_box()
r['mesh_bounds_error_mm']=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
assert r['mesh_bounds_error_mm']<.2
r['mesh']={'watertight':True,'winding_consistent':True,'triangles':len(mesh.faces),'sha256':sha(OUT/'crankshaft.glb')}
def axes(shape):
 rows=[]
 for f in shape.faces():
  if f.geom_type!=b.GeomType.CYLINDER:continue
  cyl=f.geom_adaptor().Cylinder();axis=cyl.Axis();p=axis.Location()
  if abs(axis.Direction().X())<.999999:continue
  bb=f.bounding_box();rows.append({'r':cyl.Radius(),'yz':[p.Y(),p.Z()],'x':(bb.min.X+bb.max.X)/2})
 return rows
journals=sorted([a for a in axes(rt) if abs(math.hypot(*a['yz'])-c.e.R)<1e-6 and 26<a['r']<28],key=lambda a:-a['x']);assert len(journals)==6
rodaxes=axes(b.import_step(ROOT/'cad/engine/generated/rod.step'));big=next(a for a in rodaxes if 28<a['r']<29);small=next(a for a in rodaxes if 12<a['r']<13)
pin=next(a for a in axes(b.import_step(ROOT/'cad/engine/generated/piston.step')) if 12<a['r']<13)
L=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())['mechanism']['rod_length_mm']
def point(frame,xyz):return b.Vector(xyz).transform(b.Matrix(frame.wrapped.Transformation()))
worst=0.;wrong=0.
for a,phase in zip(journals,c.EVENT_PHASES):
 y,z=a['yz'];rest=math.degrees(math.atan2(-y,z))%360
 for q in range(721):
  pose=motion.corrected_slider_frames(q,phase,c.e.R,L,a['x'],measured_cad_rest_phase_degrees=rest)
  journal=point(motion.crank_frame(q),(a['x'],y,z));bigworld=point(pose['rod'],(0,*big['yz']))
  smallworld=point(pose['rod'],(0,*small['yz']));pinworld=point(pose['piston'],(0,*pin['yz']))
  worst=max(worst,(journal-bigworld).length,(smallworld-pinworld).length)
  bad=point(b.Rot(q,0,0),(a['x'],y,z));wrong=max(wrong,(bad-bigworld).length)
assert worst<1e-6 and wrong>100
r['actual_axes']=journals;r['linkage']={'poses_per_branch':721,'branches':6,'maximum_axis_closure_error_mm':worst,'wrong_rotation_fault_mm':wrong,'scope':'Actual exported cylinder axes and rigid pose identities, no whole-neighbor collision proof'}
r['candidate_step_sha256']=sha(OUT/'crankshaft.step')
r['status']='PASS bounded crank phase/export/interface/axis-closure candidate; neighbors and installation pending'
assert all(sha(ROOT/p)==h for p,h in r['input_sha256'].items())
save();print(r['status'],flush=True)
