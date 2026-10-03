"""Frozen baseline cup; run with repository .venv-cad/bin/python."""
from pathlib import Path
import sys,json,hashlib,platform,importlib.metadata as md,datetime
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'cad/engine/generated/text-to-cad-20261003/baseline'
sys.path.insert(0,str(ROOT/'cad/engine'))
from intake_runner_exterior_integration import export_mesh
ID='block-core-cup-mps59a'
OD,H,T,RO,RI=52.578,8.7122,1.,1.5,.5

def build(od=OD,height=H,thickness=T,outer_radius=RO,inner_radius=RI):
    outer=b.Cylinder(od/2,height,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    outer=b.fillet([e for e in outer.edges() if abs(e.center().Z)<1e-6],outer_radius)
    cavity=b.Pos(0,0,thickness)*b.Cylinder(od/2-thickness,height+2,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    cavity=b.fillet([e for e in cavity.edges() if abs(e.center().Z-thickness)<1e-6],inner_radius)
    result=outer-cavity
    result.label=ID
    return result

def bounds(shape):
    bb=shape.bounding_box()
    return np.array([tuple(bb.min),tuple(bb.max)])

def probe_set():
    probes=[('floor-center', (0,0,.5),True)]
    for a in np.linspace(0,2*np.pi,12,endpoint=False):
        for r,z,occupied,name in [(12,.5,True,'floor'),(24,2,False,'cavity'),(0,H-.2,False,'opening'),(OD/2-.5,4,True,'wall'),(OD/2+.3,4,False,'outside')]:
            probes.append((name,(r*np.cos(a),r*np.sin(a),z),occupied))
    return probes

def mesh_inside(mesh,point):
    # Generalized winding number, avoiding optional ray-tree dependencies.
    tri=mesh.triangles-np.array(point)
    a,c,d=tri[:,0],tri[:,1],tri[:,2]
    la,lc,ld=[np.linalg.norm(x,axis=1) for x in (a,c,d)]
    num=np.einsum('ij,ij->i',a,np.cross(c,d))
    den=la*lc*ld+np.einsum('ij,ij->i',a,c)*ld+np.einsum('ij,ij->i',c,d)*la+np.einsum('ij,ij->i',d,a)*lc
    return abs(np.sum(2*np.arctan2(num,den))/(4*np.pi))>.5

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    part=build();step=OUT/f'{ID}.step';glb=OUT/f'{ID}.glb'
    b.export_step(part,step,unit=b.Unit.MM)
    saved=b.import_step(step)
    export=export_mesh(saved,glb,'#aeb5bc')
    mesh=trimesh.load(glb,force='mesh');mesh.merge_vertices(digits_vertex=8)
    mesh.vertices=np.asarray(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
    expected=np.array([[-OD/2,-OD/2,0],[OD/2,OD/2,H]])
    errors={'cad_nominal':float(abs(bounds(saved)-expected).max()),'step_roundtrip':float(abs(bounds(saved)-bounds(part)).max()),'mesh_cad':float(abs(mesh.bounds-bounds(saved)).max())}
    probes=probe_set()
    cad_checks=[{'name':name,'xyz_mm':list(p),'expected':want,'actual':bool(saved.is_inside(p))} for name,p,want in probes]
    mesh_checks=[{'name':name,'xyz_mm':list(p),'expected':want,'actual':bool(mesh_inside(mesh,p))} for name,p,want in probes]
    missing=saved-b.Pos(0,0,1)*b.Cylinder(20,4)
    blocked=saved+b.Pos(0,0,H-1)*b.Cylinder(OD/2-T+.2,1,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    controls={}
    for label,shape in [('missing-floor',missing),('blocked-opening',blocked)]:
        cp=OUT/f'control-{label}.step';b.export_step(shape,cp,unit=b.Unit.MM);shape=b.import_step(cp)
        rejected=[name for name,p,want in probes if bool(shape.is_inside(p))!=want]
        controls[label]={'rejected':bool(rejected),'failed_probe_names':rejected}
    checks={'valid_one_positive_solid':bool(saved.is_valid and len(saved.solids())==1 and saved.volume>0),'bounds':all(e<=.025 for e in errors.values()),'mesh_watertight':bool(mesh.is_watertight),'mesh_winding':bool(mesh.is_winding_consistent),'mesh_one_component':len(mesh.split(only_watertight=False))==1,'cad_probes':all(x['expected']==x['actual'] for x in cad_checks),'mesh_probes':all(x['expected']==x['actual'] for x in mesh_checks),'controls':all(x['rejected'] for x in controls.values())}
    vs,fs=saved.tessellate(.07,.08)
    np.savez_compressed(OUT/'render-data.npz',cad_vertices=np.array([tuple(v) for v in vs]),cad_faces=np.array(fs),mesh_vertices=mesh.vertices,mesh_faces=mesh.faces)
    files=[step,glb,Path(__file__),ROOT/'cad/engine/intake_runner_exterior_integration.py',ROOT/'docs/benchmarks/text-to-cad-20261003/BRIEF.md',ROOT/'reference/engine/research-2026-09-23/melling-expansion-plug-guide.pdf']
    report={'status':'PASS' if all(checks.values()) else 'FAIL','started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parameters_mm':dict(OD=OD,H=H,T=T,outer_radius=RO,inner_radius=RI),'environment':{'python':sys.version,'platform':platform.platform(),'packages':{n:md.version(n) for n in ['build123d','cadquery-ocp','numpy','trimesh']}},'checks':checks,'bounds_error_mm':errors,'cad_volume_mm3':saved.volume,'mesh_volume_mm3':mesh.volume,'mesh_faces':len(mesh.faces),'export_helper':export,'cad_probes':cad_checks,'mesh_probes':mesh_checks,'negative_controls':controls,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (HERE/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','checks','bounds_error_mm','environment','negative_controls']},indent=2));assert all(checks.values())
if __name__=='__main__':main()
