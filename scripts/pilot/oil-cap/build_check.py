from pathlib import Path
import sys,json,hashlib,math
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[3]
BASE=Path('/private/tmp/truck-desktop-integration-20260925')
sys.path.insert(0,str(ROOT/'cad/engine/pilot/oil-cap'))
sys.path.insert(0,str(BASE/'cad/engine'))
from oil_cap import parts,Parameters,POSITION
from assembly_math import transforms
from dataclasses import asdict
OUT=ROOT/'cad/engine/pilot/oil-cap'
REPORT=ROOT/'inventory/engine/pilot/oil-cap'
shapes=parts(); report={'status':'candidate_only','parameters':asdict(Parameters()),'checks':{},'baseline':str(BASE),'hashes':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(v.volume for v in s.solids()) if s else 0
meshes={}
for ident,s in shapes.items():
    target=OUT/f'{ident}.step';b.export_step(s,target)
    rt=b.import_step(target)
    vertices,faces=s.tessellate(.12,.15)
    xyz=np.array([[v.X,v.Y,v.Z] for v in vertices]);f=np.array(faces)
    m=trimesh.Trimesh(vertices=xyz,faces=f);meshes[ident]=m
    glbm=trimesh.Trimesh(vertices=xyz[:,[0,2,1]]*np.array([1,1,-1])/1000,faces=f)
    glbm.visual=trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(baseColorFactor=[50,55,59,255] if ident=='oil-filler-cap' else [101,89,64,255],metallicFactor=0,roughnessFactor=.75))
    (OUT/f'{ident}.glb').write_bytes(trimesh.Scene(glbm).export(file_type='glb'))
    report['checks'][ident]={'valid':s.is_valid,'solids':len(s.solids()),'step_valid':rt.is_valid,'step_volume_error_mm3':abs(vol(s)-vol(rt)),'mesh_watertight':m.is_watertight,'bounds_mm':m.bounds.tolist(),'volume_mm3':vol(s)}
    assert s.is_valid and rt.is_valid and len(s.solids())==1 and m.is_watertight
    report['hashes'][str(target.relative_to(ROOT))]=sha(target)
manifest=BASE/'inventory/engine/full-assembly.json';data=json.loads(manifest.read_text());poses=transforms(data)
coverfile=BASE/'cad/engine/generated/valve-cover.step';cover=poses['valve-cover']*b.import_step(coverfile)
placed={k:b.Pos(*POSITION)*s for k,s in shapes.items()}
report['hashes']['frozen_manifest']=sha(manifest);report['hashes']['frozen_cover_step']=sha(coverfile)
cap=placed['oil-filler-cap'];seal=placed['oil-filler-cap-seal']
report['checks']['interfaces']={'cap_cover_overlap_mm3':vol(cap & cover),'seal_cover_overlap_mm3':vol(seal & cover),'seal_cover_distance_mm':seal.distance_to(cover),'cap_seal_overlap_mm3':vol(cap & seal),'cap_seal_distance_mm':cap.distance_to(seal),'radial_thread_to_smooth_hole_gap_mm':(34-Parameters().thread_major)/2,'retention_engagement':'FAIL: frozen cover is smooth diameter 34; no female thread exists','seal_contact_annular_area_mm2':math.pi*(22**2-17**2),'contact_area_method':'coplanar circular annulus: cover hole radius17, seal outer22, cap datum419, cover top413'}
# Broad phase using frozen GLB bounds in CAD coordinates, followed by exact STEP distance/intersection.
defs={d['id']:d for d in data['definitions']};near=[]
box=cap.bounding_box();lo=np.array(tuple(box.min));hi=np.array(tuple(box.max))
for o in data['occurrences']:
    if o['id'] in ['oil-filler-cap','valve-cover']:continue
    f=BASE/defs[o['definition']]['glb'].lstrip('/')
    if not f.exists():continue
    mesh=trimesh.load(f,force='mesh');v=mesh.vertices
    cad=np.column_stack([v[:,0],-v[:,2],v[:,1]])*1000
    l=poses[o['id']];pts=np.array([tuple(b.Vertex(*a).moved(l).center()) for a in np.array([[x,y,z] for x in [cad[:,0].min(),cad[:,0].max()] for y in [cad[:,1].min(),cad[:,1].max()] for z in [cad[:,2].min(),cad[:,2].max()]])])
    if np.all(pts.max(0)>=lo-15) and np.all(pts.min(0)<=hi+15):
        sf=BASE/defs[o['definition']]['step'].lstrip('/');s=l*b.import_step(sf)
        near.append({'id':o['id'],'distance_mm':cap.distance_to(s),'overlap_mm3':vol(cap&s)})
        report['hashes'][str(sf)]=sha(sf)
report['checks']['neighbors_within_15mm_broadphase']=near
report['checks']['service_motion']={'status':'illustrative_only','reason':'Pitch is assumed; smooth cover cannot validate unscrewing engagement. No operational rotation when installed.'}
report['hashes']['builder']=sha(ROOT/'cad/engine/pilot/oil-cap/oil_cap.py')
report['hashes']['checker']=sha(Path(__file__))
(REPORT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
# Hand off only triangle arrays to the bundled plotting runtime.
v,f=(cover & (b.Pos(*POSITION)*b.Pos(0,0,-20)*b.Box(115,115,80))).tessellate(.5,.3)
np.savez_compressed(OUT/'review-meshes.npz',cap_v=meshes['oil-filler-cap'].vertices,cap_f=meshes['oil-filler-cap'].faces,seal_v=meshes['oil-filler-cap-seal'].vertices,seal_f=meshes['oil-filler-cap-seal'].faces,cover_v=np.array([tuple(q) for q in v]),cover_f=np.array(f))
print(json.dumps(report['checks'],indent=2))
