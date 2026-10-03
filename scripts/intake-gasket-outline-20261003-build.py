"""Build/check isolated traced gasket; report unsupported sealing land explicitly."""
from pathlib import Path
import json, hashlib
import build123d as b
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
PREFIX='intake-gasket-outline-20261003'
out=ROOT/'cad/engine/generated'/PREFIX;out.mkdir(parents=True,exist_ok=True)
contour_path=ROOT/'reference/engine'/f'{PREFIX}-contour.json'
p_path=ROOT/'cad/engine/intake-joint-candidate-20261003-parameters.json'
c=json.loads(contour_path.read_text());p=json.loads(p_path.read_text())
xy=c['world_xy_mm'][:-1]
# JSON coordinates are lists; Polygon's flatten_sequence treats them as nested
# sequences, losing point boundaries. Explicit Vectors retain the exact trace.
profile=b.Face(b.Wire.make_polygon([b.Vector(x,y,0) for x,y in xy],close=True))
assert profile.is_valid and profile.area>0, 'Invalid source outline'
for u in p['port_stations']:
    profile-=b.Pos(284.48-568.96*u,-228)*b.Circle(25.5)
for h in p['holes']:
    u,v=h['normalized_uv'];profile-=b.Pos(284.48-568.96*u,-228-568.96*v)*b.Circle(5.5)
shape=b.Pos(0,0,360)*b.extrude(profile,amount=1.5)
assert shape.is_valid and len(shape.solids())==1 and shape.volume>0
step=out/'efi-upper-intake-gasket.step';b.export_step(shape,step);reload=b.import_step(step)
box=lambda s:np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
vertices,faces=reload.tessellate(.025,.08);v=np.array([tuple(t) for t in vertices])
mesh=trimesh.Trimesh(vertices=(v[:,[0,2,1]]*np.array([1,1,-1])/1000).astype(np.float32),faces=faces)
mesh.update_faces(mesh.area_faces>0);mesh.remove_unreferenced_vertices();mesh.visual.vertex_colors=[115,121,115,255]
glb=out/'efi-upper-intake-gasket.glb';glb.write_bytes(trimesh.Scene(mesh).export(file_type='glb'))
actual=trimesh.load(glb,force='mesh');actual.merge_vertices(digits_vertex=8)
vv=np.asarray(actual.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
np.savez_compressed(out/'mesh.npz',vertices=vv,faces=actual.faces)
r={'readiness':'isolated candidate; not installed','inputs_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [contour_path,p_path,Path(__file__)]},'valid':shape.is_valid,'solids':len(shape.solids()),'roundtrip_valid':reload.is_valid,'roundtrip_solids':len(reload.solids()),'roundtrip_volume_delta_mm3':abs(shape.volume-reload.volume),'roundtrip_bounds_error_mm':float(abs(box(shape)-box(reload)).max()),'mesh_watertight':bool(actual.is_watertight),'mesh_components':len(actual.split()),'mesh_winding':bool(actual.is_winding_consistent),'mesh_volume_positive':bool(actual.volume>0),'mesh_bounds_error_mm':float(abs(np.array([vv.min(0),vv.max(0)])-box(reload)).max()),'triangles':len(actual.faces),'source_limits':c['limits'],'mating_face_support':{}}
for key,z in [('efi-lower-intake',359.9),('efi-upper-intake',361.5)]:
    f=ROOT/'cad/engine/generated/intake-joint-candidate-20261003'/(key+'.step');host=b.import_step(f)
    slab=b.Pos(0,0,z)*b.extrude(profile,amount=.1)
    try:
        missing=slab-host
        volume=sum(s.volume for s in missing.solids()) if missing is not None else None
        r['mating_face_support'][key]={'missing_volume_mm3':volume,'missing_area_mm2':None if volume is None else volume/.1,'result_valid':None if missing is None else missing.is_valid,'host_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'status':'PASS' if volume is not None and volume<.1 else 'FAIL'}
    except Exception as e:r['mating_face_support'][key]={'status':'ERROR','error':str(e)}
r['artifacts']={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [step,glb]}
assert r['valid'] and r['solids']==1 and r['roundtrip_valid'] and r['roundtrip_solids']==1
assert r['mesh_watertight'] and r['mesh_components']==1 and r['mesh_winding'] and r['mesh_volume_positive'] and r['mesh_bounds_error_mm']<.025
(ROOT/'reference/engine'/f'{PREFIX}-build.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
