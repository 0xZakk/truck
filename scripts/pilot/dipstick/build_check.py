from pathlib import Path
import sys,json,hashlib,math
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'cad/engine/pilot/dipstick'))
import dipstick as d
OUT=ROOT/'cad/engine/pilot/dipstick'; INV=ROOT/'inventory/engine/pilot/dipstick'
BASE=Path('/private/tmp/truck-desktop-integration-20260925')
shapes=d.parts();compound=b.Compound(children=list(shapes.values()))
b.export_step(compound,OUT/'engine-oil-dipstick.step')
scene=trimesh.Scene(); arrays={};report={'status':'candidate only; installation and oil calibration unaccepted','parameters':d.asdict(d.P),'units':'mm','shape_checks':{},'neighbor_checks':{}}
for i,(key,s) in enumerate(shapes.items()):
 v,f=s.tessellate(.1,.12);v=np.array([tuple(x) for x in v]);f=np.array(f)
 arrays['v'+str(i)]=v;arrays['f'+str(i)]=f
 # same CAD-to-GLTF convention as engine: (x,z,-y), metres
 mesh=trimesh.Trimesh(vertices=v[:,[0,2,1]]*np.array([1,1,-1])*.001,faces=f,process=False)
 mesh.visual.face_colors=[165,172,180,255] if i==0 else [223,182,30,255]
 scene.add_geometry(mesh,node_name=key)
 report['shape_checks'][key]={'valid':s.is_valid,'solids':len(s.solids()),'volume_mm3':s.volume,'bounds_mm':[tuple(s.bounding_box().min),tuple(s.bounding_box().max)]}
 assert s.is_valid and len(s.solids())==1
scene.export(str(OUT/'engine-oil-dipstick.glb'))
# Cold reference neighbor check. Does not grant clearance or passage correctness.
manifest=json.loads((BASE/'inventory/engine/full-assembly.json').read_text())
occ={x['id']:x for x in manifest['occurrences']}
installed=d.installed(compound)
for j,key in enumerate(['block','oil-pan','efi-upper-intake','efi-lower-intake','valve-cover','cylinder-head']):
 path=BASE/'cad/engine/generated'/(key+'.step');s=b.import_step(path)
 o=occ[key];s=b.Pos(*o['position_cad_mm'])*b.Rot(*o['rotation_cad_deg'])*s
 common=installed.intersect(s); volume=common.volume if common else 0
 report['neighbor_checks'][key]={'intersection_mm3':volume,'distance_mm':installed.distance_to(s),'baseline_step_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'interpretation':'unresolved passage/interface' if volume>1e-6 else 'no static solid interference in hypothesized pose'}
 v,f=s.tessellate(.8,.5);arrays['n'+str(j)]=np.array([tuple(x) for x in v]);arrays['nf'+str(j)]=np.array(f)
for i,s in enumerate(shapes.values()):
 v,f=d.installed(s).tessellate(.1,.12);arrays['iv'+str(i)]=np.array([tuple(x) for x in v]);arrays['if'+str(i)]=np.array(f)
report['pose']=d.PROVISIONAL_POSE
report['tip_cad_mm']=tuple((b.Pos(*d.PROVISIONAL_POSE['position_cad_mm'])*b.Rot(*d.PROVISIONAL_POSE['rotation_cad_deg'])).position) # tip separately transformed below
report['tip_cad_mm']=list(np.array(d.PROVISIONAL_POSE['position_cad_mm'])+np.array([0,math.sin(math.radians(8.5))*(-d.P.blade_axial_length),-math.cos(math.radians(8.5))*d.P.blade_axial_length]))
report['unverified']=['Seating datum to tip length','Oil ADD/FULL calibration positions and range','Guide tube centerline/bore and block entry','Installed routing and handle location','Material grade and all cross sections','Extraction path and whole-engine moving clearances']
report['source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'reference/engine/pilot/dipstick').glob('*.jpg')}
report['module_sha256']=hashlib.sha256(Path(d.__file__).read_bytes()).hexdigest()
report['baseline_manifest_sha256']=hashlib.sha256((BASE/'inventory/engine/full-assembly.json').read_bytes()).hexdigest()
report['outputs']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*') if p.suffix in ['.step','.glb']}
(INV/'validation.json').write_text(json.dumps(report,indent=2)+'\n');np.savez_compressed(OUT/'visual-meshes.npz',**arrays)
print(json.dumps({'shape_checks':report['shape_checks'],'neighbor_checks':report['neighbor_checks'],'tip':report['tip_cad_mm']},indent=2))
