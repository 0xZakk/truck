"""Build/check local specimen; does not install or certify an engine interface."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import online_airbox_duct_specimen as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c.O.mkdir(exist_ok=True)
resume='--resume-pairs' in sys.argv
recovery=None
if resume:
 recovery=json.loads((c.O/'completed-probes-recovery.json').read_text())
 assert all(sha(R/p)==h for p,h in recovery['files'].items())
 parts={p.stem:b.import_step(p) for p in c.O.glob('online-*.step')}
else:parts=c.build()
rows={};meshes={}
for name,s in parts.items():
 print('export',name,flush=True)
 assert s.is_valid and len(s.solids())==1,(name,len(s.solids()))
 p=c.O/(name+'.step')
 if not resume:b.export_step(s,p)
 s=b.import_step(p);parts[name]=s
 v,f=s.tessellate(.025,.08);m=trimesh.Trimesh(np.array([tuple(q) for q in v]),np.array(f));m.merge_vertices(digits_vertex=6)
 assert m.is_watertight and m.is_winding_consistent and m.volume>0,name
 gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp)
 g=trimesh.load(gp,force='mesh');gv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
 bounds=np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
 err=float(np.max(abs(np.array([gv.min(0),gv.max(0)])-bounds)));assert err<.05,(name,err)
 meshes[name]=m
 rows[name]={'step':str(p.relative_to(R)),'step_sha256':sha(p),'glb':str(gp.relative_to(R)),'glb_sha256':sha(gp),'valid':s.is_valid,'solid_count':len(s.solids()),'volume_mm3':s.volume,'watertight':m.is_watertight,'winding_consistent':m.is_winding_consistent,'bounds_mm':bounds.tolist(),'mesh_bounds_error_mm':err}
probe=[]
for short in (False,True):
 name='online-airbox-duct-'+('short' if short else 'long');s=parts[name];ss=c.stations(short);n=0
 for a,z in ([] if resume else zip(ss[:-1],ss[1:])):
  x,y,r=(np.array(a)+z)/2
  assert not s.is_inside((x,y,0))
  for angle in np.linspace(0,2*np.pi,16,endpoint=False):
   for radius,expect in [(r-c.WALL-.2,False),(r-c.WALL+.2,True),(r-.2,True),(r+.2,False)]:
    point=(x,y+radius*np.cos(angle),radius*np.sin(angle))
    assert s.is_inside(point)==expect,(name,x,angle,radius,expect)
    n+=1
 if resume:n=recovery['counts'][int(short)]
 print('radial probes '+('reused' if resume else 'passed'),name,n,flush=True)
 probe.append({'part':name,'actual_STEP_radial_probes':n,'coverage':'Each axial interval midpoint,16 angles,4 radial positions; sampled','construction_bound':'Ruled circular sections with positive inner radius and3mm radial offset; this is not constant normal wall thickness'})
# Wrong solid-cuff control fails the same empty-center predicate.
control=b.Pos(8,60,0)*b.Rot(0,90,0)*b.Cylinder(42.5,16)
assert control.is_inside((8,60,0))
# Thin-wall control misses an actual required skin point.
thin=c.ring(0,60,42.0,16,.5)
assert not thin.is_inside((8,60+40,0))
pairs=[]
for (an,a),(bn,z) in itertools.combinations(parts.items(),2):
 ab=a.bounding_box();bb=z.bounding_box()
 if any(tuple(ab.max)[i]<tuple(bb.min)[i]-1e-5 or tuple(bb.max)[i]<tuple(ab.min)[i]-1e-5 for i in range(3)):continue
 overlap=a&z;vol=0 if overlap is None else (sum(x.volume for x in overlap) if isinstance(overlap,b.ShapeList) else overlap.volume)
 assert vol<.1,(an,bn,vol)
 pairs.append({'a':an,'b':bn,'overlap_mm3':vol,'distance_mm':a.distance_to(z)})
scene=trimesh.Scene()
for name,m in meshes.items():scene.add_geometry(m,geom_name=name,node_name=name)
scene.export(c.O/'specimen-mm.glb') # explicitly named mm inspection mesh, not runtime asset
inputs=[Path(__file__),Path(c.__file__),R/'reference/engine/online-airbox-research.json']
report={'status':'PASS local geometry only; installation NOT RUN','reused_radial_probe_evidence':recovery,'parameters':c.PARAMETERS,'parts':rows,'radial_probes':probe,'negative_controls':{'solid_cuff_detected':True,'half_mm_wall_detected':True},'local_exact_pairs':pairs,'unverified':['world placement','insertion fit and sealing','source accurate cuff profiles/walls','continuous flex','vehicle neighbor clearance','retainer function and hidden construction','thread/slot detail of clamp hardware'],'inputs':{str(p.relative_to(R)):sha(p) for p in inputs}}
(R/'reference/engine/online-airbox-duct-specimen.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',flush=True)
