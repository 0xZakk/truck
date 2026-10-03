"""Export and check isolated exterior regions; no installation/manufacturing acceptance."""
from pathlib import Path
import sys,json,hashlib,math,platform,importlib.metadata,itertools
import numpy as np
import build123d as b,trimesh
from OCP.BRepMesh import BRepMesh_IncrementalMesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import ho2s_specimen_20261003 as c
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
pre=R/'reference/engine/ho2s-specimen-20261003-pre-cad.json'
frozen=json.loads(pre.read_text())
for p,h in frozen['contract'].items():assert sha(R/p)==h
for p,h in frozen['prior_frozen_ledgers'].items():assert sha(R/p)==h
c.O.mkdir(exist_ok=True);print('Build27 regions',flush=True);regions=c.build();assert len(regions)==27
assets={};shapes={};reports={}
for name,row in regions.items():
 s=row['shape'];assert s.is_valid and len(s.solids())==1 and s.volume>0,name
 step=c.O/(name+'.step');b.export_step(s,step);fresh=b.import_step(step)
 assert fresh.is_valid and len(fresh.solids())==1 and fresh.volume>0,name
 assert abs(fresh.volume-s.volume)<.001,name
 shapes[name]=fresh
 # Existing screw/ACT export convention and established precision gates.
 BRepMesh_IncrementalMesh(fresh.wrapped,.012,False,.08,True)
 v,f=fresh.tessellate(.012,.08);mesh=trimesh.Trimesh(np.array([tuple(q) for q in v]),np.array(f));mesh.merge_vertices(digits_vertex=6)
 raw_faces=len(mesh.faces);raw_volume=mesh.volume
 # Existing exporter cleanup: remove only zero-area/duplicate faces, never fill holes.
 mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices()
 removed_faces=raw_faces-len(mesh.faces);assert abs(mesh.volume-raw_volume)<.0001,name
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,name
 glb=step.with_suffix('.glb');g=trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces)
 g.visual.vertex_colors=np.array(row['color'])*255;g.export(glb)
 actual=trimesh.load(glb,force='mesh');assert actual.is_watertight and actual.is_winding_consistent and actual.volume>0,name
 vback=actual.vertices[:,[0,2,1]]*[1,-1,1]*1000
 bounds=np.array([tuple(fresh.bounding_box().min),tuple(fresh.bounding_box().max)])
 delta=float(np.max(abs(np.array([vback.min(0),vback.max(0)])-bounds)));assert delta<.05,(name,delta)
 reports[name]={'frame':row['frame'],'color':row['color'],'meaning':row['meaning'],'valid':True,'solid_count':1,'cad_volume_mm3':fresh.volume,'mesh_volume_mm3':mesh.volume,'removed_degenerate_duplicate_faces':removed_faces,'mesh_cleanup_volume_delta_mm3':abs(mesh.volume-raw_volume),'mesh_watertight':True,'mesh_winding_consistent':True,'bounds_mm':bounds.tolist(),'bounds_error_mm':delta,'step':str(step.relative_to(R)),'glb':str(glb.relative_to(R))}
 for p in [step,glb]:assets[str(p.relative_to(R))]=sha(p)
 print('PASS export',name,flush=True)
rows=[]
def thread_check(shape,record=False):
 vals=[]
 for angle in range(8):
  theta=angle*math.pi/4
  for turn in [1,2,3]:
   for offset,want in [(0,True),(.5,False)]:
    z=(turn+angle/8+offset)*1.5;pt=(8.75*math.cos(theta),8.75*math.sin(theta),z)
    got=shape.is_inside(pt);vals.append(got==want)
    if record:rows.append({'point_mm':pt,'expected':want,'actual':got})
 return all(vals)
assert thread_check(shapes['mounting-shell'],True),rows
smooth=c.threaded_mount(True);assert not thread_check(smooth)
b.export_step(smooth,c.O/'control-smooth-thread.step')
slots=[]
def slot_check(shape,record=False):
 results=[]
 for angle in range(4):
  theta=angle*math.pi/2
  for z in [10,15,20]:
   for radius in [5.1,5.3,5.5]:
    p=(radius*math.cos(theta),radius*math.sin(theta),z);got=shape.is_inside(p);results.append(not got)
    if record:slots.append({'point_mm':p,'expected':False,'actual':got})
  # Metal must remain between slots; a fully absent cap fails too.
  theta+=math.pi/4
  for z in [10,15,20]:results.append(shape.is_inside((5.3*math.cos(theta),5.3*math.sin(theta),z)))
 return all(results)
assert slot_check(shapes['slotted-protective-cap'],True),slots
blocked=c.protective_cap(True);assert not slot_check(blocked);b.export_step(blocked,c.O/'control-closed-cap.step')
def mouth_check(shape):
 return all(not shape.is_inside((x,y,z)) for x,y in [(0,0),(5,0),(-5,0),(0,5),(0,-5)] for z in [42,43]) and shape.is_inside((8,0,43))
assert mouth_check(shapes['connector-housing']);blocked=c.connector_housing(True);assert not mouth_check(blocked);b.export_step(blocked,c.O/'control-blocked-mouth.step')
for z in [-35,-20,-10]:assert not shapes['main-shell'].is_inside((0,0,z)) and shapes['main-shell'].is_inside((9.5,0,z))
assert shapes['mounting-shell'].is_inside((0,10.95,-5)) and not shapes['mounting-shell'].is_inside((0,11.05,-5))
assert not shapes['seat-ring'].is_inside((0,0,-1)) and shapes['seat-ring'].is_inside((10,0,-1))
for x,y in c.SENSOR_XY:assert not shapes['exit-insulator'].is_inside((x,y,-65))
for x,y in c.CONNECTOR_XY:assert not shapes['connector-support-face'].is_inside((x,y,34.5))
# Pairwise same-frame local audit; two frames must never be treated as installed overlap.
clashes=[];tested=0
for (na,a),(nb,d) in itertools.combinations(shapes.items(),2):
 if regions[na]['frame']!=regions[nb]['frame']:continue
 tested+=1;inter=a.intersect(d);volume=0 if inter is None else sum(s.volume for s in inter.solids())
 if volume>.1:clashes.append({'a':na,'b':nb,'volume_mm3':volume})
print('Overlap audit',tested,clashes,flush=True)
assert not clashes,clashes
for p in c.O.glob('control-*.step'):assets[str(p.relative_to(R))]=sha(p)
inputs=[Path(__file__),Path(c.__file__),R/'cad/engine/pan_fastener_thread_candidate.py',pre,R/'docs/components/ho2s-specimen-20261003-contract.md',R/'reference/engine/ho2s-specimen-20261003-contract-amendment.json',R/'cad/requirements-engine-lock.txt']
report={'status':'PASS isolated estimated exterior only','regions':reports,'parameters':c.P,'thread_probes':rows,'slot_void_probes':slots,'smooth_thread_rejected':True,'closed_cap_rejected':True,'blocked_mouth_rejected':True,'additional_material_void_hex_probes':True,'same_frame_pairs_tested':tested,'overlaps_over_point1_mm3':clashes,'asset_hashes':assets,'inputs':{str(p.relative_to(R)):sha(p) for p in inputs},'environment':{'python':platform.python_version(),'platform':platform.platform(),'packages':{p:importlib.metadata.version(p) for p in ['build123d','cadquery-ocp','trimesh','numpy']}},'limits':'Sampled profiles/passages, inferred material regions; no thread gauge, gas response, electrical continuity, complete hidden BOM, installation, flow, service or browser acceptance.'}
(R/'reference/engine/ho2s-specimen-20261003-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS all checks',flush=True)
