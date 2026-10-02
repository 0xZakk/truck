"""Scoped local refinement checks; checkpoint stages avoid repeating completed work."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import airbox_refined_20261002 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
volume=lambda s:0 if s is None else sum(x.volume for x in s) if isinstance(s,b.ShapeList) else s.volume
c.O.mkdir(exist_ok=True);checkpoint=c.O/'validation-stages.json'
inputs={str(p.relative_to(R)):sha(p) for p in [Path(c.__file__),R/'reference/engine/online-airbox-research.json',R/'docs/components/airbox-refined-20261002-contract.md']}
resume='--resume' in sys.argv
if resume:
 state=json.loads(checkpoint.read_text());assert state['inputs']==inputs
 for p,h in state['asset_hashes'].items():assert sha(R/p)==h,p
 parts={n:b.import_step(R/q['step']) for n,q in state['parts'].items()}
else:
 state={'inputs':inputs,'parts':{},'asset_hashes':{},'probes':{}}
 parts=c.build()
 for name,s in parts.items():
  print('export',name,flush=True);assert s.is_valid and len(s.solids())==1,(name,len(s.solids()))
  p=c.O/(name+'.step');b.export_step(s,p);s=b.import_step(p);parts[name]=s
  from OCP.BRepMesh import BRepMesh_IncrementalMesh
  BRepMesh_IncrementalMesh(s.wrapped,.02,False,.08,True)
  v,f=s.tessellate(.025,.08);m=trimesh.Trimesh(np.array([tuple(q) for q in v]),np.array(f));m.merge_vertices(digits_vertex=6)
  assert m.is_watertight and m.is_winding_consistent and m.volume>0,name
  gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp)
  g=trimesh.load(gp,force='mesh');gv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
  bounds=np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
  err=float(np.max(abs(np.array([gv.min(0),gv.max(0)])-bounds)));assert err<.05,(name,err)
  state['parts'][name]={'step':str(p.relative_to(R)),'glb':str(gp.relative_to(R)),'volume_mm3':s.volume,'valid':s.is_valid,'solids':len(s.solids()),'watertight':g.is_watertight,'winding_consistent':g.is_winding_consistent,'bounds_mm':bounds.tolist(),'mesh_bounds_error_mm':err}
  state['asset_hashes'].update({str(p.relative_to(R)):sha(p),str(gp.relative_to(R)):sha(gp)})
 checkpoint.write_text(json.dumps(state,indent=2)+'\n')
for short in (False,True):
 name='online-airbox-duct-'+('short' if short else 'long')
 if name in state['probes']:continue
 s=parts[name];first=110 if short else 86;last=290 if short else 254;start=26 if short else 0
 xs=sorted(set([start+8,start+24,first-25]+list(range(first,last+1,6))+[last+16,last+32,350,380,440,490,550]))
 n=0
 for x in xs:
  y,r=c.profile(x,short);assert not s.is_inside((x,y,0)),(name,x,'blocked')
  for a in np.linspace(0,2*np.pi,8,endpoint=False):
   for rr,expect in [(r-1.5,True),(r-c.WALL-.4,False),(r+.4,False)]:
    assert s.is_inside((x,y+rr*np.cos(a),rr*np.sin(a)))==expect,(name,x,a,rr,expect)
    n+=1
 state['probes'][name]={'axial_sections':len(xs),'radial_points':n,'axis_points':len(xs),'coverage':'Sampled crests/valleys every half pitch, cuff and smooth-shoulder stations; not continuous flexibility','locations_x_mm':xs}
 checkpoint.write_text(json.dumps(state,indent=2)+'\n');print('probes PASS',name,n,flush=True)
# Actual wrong-piece controls, using identical point predicates.
plug=b.Pos(8,60,0)*b.Rot(0,90,0)*b.Cylinder(42.5,16)
assert plug.is_inside((8,60,0))
thin=b.extrude(b.Plane(origin=(0,60,0),x_dir=(0,1,0),z_dir=(1,0,0))*(b.Circle(42.5)-b.Circle(42)),amount=16)
assert not thin.is_inside((8,101,0))
pairs=[]
for (an,a),(bn,z) in itertools.combinations(parts.items(),2):
 ab=a.bounding_box();bb=z.bounding_box()
 if any(tuple(ab.max)[i]<tuple(bb.min)[i]-1e-5 or tuple(bb.max)[i]<tuple(ab.min)[i]-1e-5 for i in range(3)):continue
 vol=volume(a&z);gap=a.distance_to(z);pairs.append({'a':an,'b':bn,'overlap_mm3':vol,'gap_mm':gap})
 print('pair',an,bn,vol,gap,flush=True)
state['local_pairs']=pairs;state['checker_sha256']=sha(Path(__file__));state['negative_controls']={'blocked_cuff_detected':True,'half_mm_wall_detected':True};state['status']='PASS local only' if all(p['overlap_mm3']<.1 for p in pairs) else 'FAIL local overlaps'
state['reused_clamps']={str(p.relative_to(R)):sha(p) for p in sorted(c.OLD.glob('online-airbox-clamp-*.step'))}
state['scope_limits']=['all physical dimensions estimated','no source-calibrated ellipse','no installed frame/fit','sampled solid probes not continuous deformation','clamp thread engagement omitted']
(R/'reference/engine/airbox-refined-20261002-check.json').write_text(json.dumps(state,indent=2)+'\n')
print(state['status'],flush=True)
