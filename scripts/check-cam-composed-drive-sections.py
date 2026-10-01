#!/usr/bin/env python3
"""Independent BRep sections and strict shaft-core points, no shape reconstruction."""
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import cam_composed_drive_candidate as c
import cam_clockwise_candidate as lobes
O=R/'cad/engine/generated/cam-composed-drive-candidate'
old=b.import_step(c.CAM);new=b.import_step(O/'camshaft-local.step');gear=b.Pos(c.X,0,0)*b.import_step(c.GEAR)
def poly(shape,x):
 s=b.section(shape,b.Plane.YZ.offset(x));assert len(s.faces())==1 and len(s.wires())==1
 return np.array([tuple(s.wires()[0].position_at(i/4096))[1:]for i in range(4096)])
def area(p):return abs(np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1)))/2
def error(a,z):
 def one(a,z):
  _,idx=cKDTree(z).query(a,k=4);idx=np.concatenate([idx,(idx-1)%len(z)],axis=1);p=z[idx];v=z[(idx+1)%len(z)]-p;d=a[:,None,:]-p;t=np.clip(np.sum(d*v,axis=2)/np.sum(v*v,axis=2),0,1)
  return float(np.max(np.min(np.linalg.norm(d-t[:,:,None]*v,axis=2),axis=1)))
 return max(one(a,z),one(z,a))
manifest=json.loads((R/'inventory/engine/full-assembly.json').read_text());stations=lobes.stations(manifest);rows=[];sections={}
for cylinder,kind,x,phase in stations:
 a=poly(old,x);z=poly(new,x);e=error(a,z);ae=abs(area(a)-area(z));assert e<.002 and ae<.02
 rows.append({'cylinder':cylinder,'kind':kind,'x_mm':x,'boundary_error_mm':e,'area_error_mm2':ae});print('lobe',cylinder,kind,e,flush=True)
for x in [c.X-6.001,c.X-5.999,c.X,c.X+5.999,c.X+6.001]:
 source=old if abs(x-c.X)>6 else gear;a=poly(source,x);z=poly(new,x);e=error(a,z);ae=abs(area(a)-area(z));assert e<.002 and ae<.02;sections[str(x)]={'boundary_error_mm':e,'area_error_mm2':ae,'compared_to':'old shaft'if source is old else 'frozen corrected gear'}
# Material continuity along preserved R15 shaft; strict inset radial and seam-near samples.
points=0
for x in [c.X-6.001,c.X-6,c.X-5.999,c.X,c.X+5.999,c.X+6,c.X+6.001]:
 for a in np.linspace(0,math.tau,48,endpoint=False):
  for radius in [0,7.5,14.99]:
   assert new.is_inside((x,radius*math.cos(a),radius*math.sin(a)),tolerance=1e-7);points+=1
# Wrong source tooth profile is independently detectable at an off-center section.
x=c.X+3;a=poly(old,x);z=poly(new,x);wrong=error(a,z);assert wrong>.1
paths=[Path(__file__),Path(c.__file__),Path(lobes.__file__),c.CAM,c.GEAR,O/'camshaft-local.step',R/'inventory/engine/full-assembly.json']
r={'status':'PASS sampled actual sections and core continuity','lobes':rows,'gear_shaft_sections':sections,'strict_R15_inset_core_points':points,'wrong_old_gear_section_boundary_mm':wrong,'limits':['4096 sampled boundary points per section; not continuous Hausdorff proof','No full assembly neighbor or browser inference'],'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}}
(R/'inventory/engine/cam-composed-drive-section-review.json').write_text(json.dumps(r,indent=2)+'\n')
