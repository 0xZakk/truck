"""Actual STEP/GLB and coarse helical specimen checks; no host acceptance."""
from pathlib import Path
import sys,hashlib,json
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import airbox_screw_online_20261002 as c
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
c.O.mkdir(exist_ok=True);print('build',flush=True);s=c.build();assert s.is_valid and len(s.solids())==1
p=c.O/'air-cleaner-body-bracket-screw.step';b.export_step(s,p);s=b.import_step(p);assert s.is_valid and len(s.solids())==1
print('mesh',flush=True)
from OCP.BRepMesh import BRepMesh_IncrementalMesh
BRepMesh_IncrementalMesh(s.wrapped,.012,False,.08,True)
v,f=s.tessellate(.012,.08);m=trimesh.Trimesh(np.array([tuple(q) for q in v]),np.array(f));m.merge_vertices(digits_vertex=6)
assert m.is_watertight and m.is_winding_consistent and m.volume>0
out=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(out)
g=trimesh.load(out,force='mesh');vv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
bounds=np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)]);err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-bounds)));assert err<.05
print('thread probes',flush=True);pitch=c.PARAMETERS['pitch'];rows=[]
def predicate(shape):
 vals=[]
 for theta in np.linspace(0,2*np.pi,8,endpoint=False):
  for k in range(2,7):
   crest=(k+theta/(2*np.pi))*pitch
   for off,expected in [(0,True),(pitch/2,False)]:
    pt=(2.95*np.cos(theta),2.95*np.sin(theta),crest+off)
    actual=shape.is_inside(pt);vals.append(actual==expected)
    if shape is s:rows.append({'theta':float(theta),'z':float(crest+off),'expected_inside':expected,'actual_inside':actual})
 return all(vals)
assert predicate(s);smooth=c.build(True);assert not predicate(smooth)
region=c.cz(3.2,2,14);actual=s & region;blank=c.envelope() & region;removed=blank.volume-actual.volume;assert removed>50
# Independent axial/radial probes confirm positive core, tapered envelope and head bearing.
for z in [0.5,5,10,14,16,18,18.9]:assert s.is_inside((0,0,z))
for z in [15.5,17,18.5]:
 r=3.15+(z-15)*(.08-3.15)/4
 assert not s.is_inside((r+.1,0,z))
assert s.is_inside((5.5,0,-.35)) and not s.is_inside((5.9,0,-.35))
assert s.is_inside((0,3.95,-2)) and not s.is_inside((0,4.05,-2))
report={'status':'PASS isolated estimated specimen, not installed/manufacturing acceptance','parameters':c.PARAMETERS,'step':str(p.relative_to(R)),'glb':str(out.relative_to(R)),'asset_hashes':{str(q.relative_to(R)):sha(q) for q in [p,out]},'valid':s.is_valid,'solid_count':len(s.solids()),'cad_volume_mm3':s.volume,'mesh_volume_mm3':m.volume,'watertight':m.is_watertight,'winding_consistent':m.is_winding_consistent,'bounds_mm':bounds.tolist(),'mesh_bounds_error_mm':err,'thread_probes':rows,'thread_removed_vs_blank_mm3':removed,'smooth_control_rejected':True,'tip_core_and_head_probes':True,'scope':'80 sampled helical crest/root probes at8 angles×5 full thread turns; no thread gauge/fit proof. Estimated taper/core has separate probes.','inputs':{str(q.relative_to(R)):sha(q) for q in [Path(__file__),Path(c.__file__),R/'cad/engine/pan_fastener_thread_candidate.py',R/'docs/components/airbox-screw-online-20261002-contract.md',R/'reference/engine/airbox-host-online-20261002.json']}}
(R/'reference/engine/airbox-screw-online-20261002-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',flush=True)
