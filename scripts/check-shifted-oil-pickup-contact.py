#!/usr/bin/env python3
"""Independent actual exported insertion/lumen probes; bounded scope only."""
import sys,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import shifted_oil_pickup_candidate as c
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/shifted-oil-pickup-candidate';m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());poses=transforms(m)
q=b.import_step(OUT/'oil-pickup-tube-world.step');old=poses['oil-pickup-tube']*b.import_step(ROOT/'cad/engine/generated/oil-pickup-tube.step');pump=b.Pos(*c.DELTA)*poses['oil-pump-housing']*b.import_step(ROOT/'cad/engine/generated/oil-pump-housing.step');frame=b.Pos(*c.DELTA)*c.drive.PUMP_FRAME
vol=lambda s:sum(x.volume for x in s.solids()) if s else 0.
rows=[]
for x in [-32.8,-32,-31.2]:
 row={'local_x_mm':x}
 for name,s,r in [('tube_wall',q,5.4),('pump_backing',pump,6.1),('tube_lumen',q,4.7),('pump_lumen',pump,4.7),('stale_tube_wall',old,5.4)]:
  pts=[(frame*b.Vertex(x,r*math.cos(i*math.tau/24),5+r*math.sin(i*math.tau/24))).center() for i in range(24)]
  row[name]=sum(s.is_inside(p,tolerance=1e-7) for p in pts)
 rows.append(row);print(row,flush=True)
# Whole straight insertion lumen and a radial wall body, independent of sampled points.
lumen=frame*b.Pos(-32,0,5)*b.Rot(0,90,0)*b.Cylinder(4.7,1.8)
wall=frame*b.Pos(-32,0,5)*b.Rot(0,90,0)*(b.Cylinder(5.9,1.8)-b.Cylinder(4.9,2))
backing=frame*b.Pos(-32,0,5)*b.Rot(0,90,0)*(b.Cylinder(6.2,1.8)-b.Cylinder(6.01,2))
checks={'lumen_tube_overlap_mm3':vol(lumen.intersect(q)),'lumen_pump_overlap_mm3':vol(lumen.intersect(pump)),'wall_missing_from_tube_mm3':vol(wall.cut(q)),'backing_missing_from_pump_mm3':vol(backing.cut(pump)),'stale_wall_missing_mm3':vol(wall.cut(old))}
# Swept interior probe covers whole revised upstream curve and crosses its retained-tail seam.
_,data=c.build(old)
oldpath=c.original_path();tail_extension=oldpath.trim(data['parameter'],data['parameter']+.002)
fullprobe_path=b.Wire(list(data['path'].edges())+[tail_extension])
head_lumen=b.sweep(b.Plane(origin=data['start'],x_dir=(0,1,0),z_dir=(-1,0,0))*b.Circle(4.7),path=fullprobe_path,is_frenet=True)
checks['whole_revised_curve_lumen_overlap_mm3']=vol(head_lumen.intersect(q))
assert checks['whole_revised_curve_lumen_overlap_mm3']<1e-5
# Exposed shared cylindrical wall via explicit actual common of coincident faces.
commons=[]
for f in q.faces():
 if f.geom_type!=b.GeomType.CYLINDER:continue
 for g in pump.faces():
  if g.geom_type!=b.GeomType.CYLINDER:continue
  common=f.intersect(g)
  if common and common.area>1e-5:commons.append(common.area)
checks['actual_shared_cylindrical_face_area_mm2']=sum(commons)
assert all(r['tube_wall']==24 and r['pump_backing']==24 and r['tube_lumen']==0 and r['pump_lumen']==0 and r['stale_tube_wall']==0 for r in rows)
assert all(checks[k]<1e-5 for k in ['lumen_tube_overlap_mm3','lumen_pump_overlap_mm3','wall_missing_from_tube_mm3','backing_missing_from_pump_mm3'])
assert checks['stale_wall_missing_mm3']>50 and checks['actual_shared_cylindrical_face_area_mm2']>50
paths=['scripts/check-shifted-oil-pickup-contact.py','cad/engine/shifted_oil_pickup_candidate.py','inventory/engine/shifted-oil-pickup-candidate-validation.json','cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube-world.step','cad/engine/generated/oil-pump-housing.step','cad/engine/generated/oil-pickup-tube.step','inventory/engine/full-assembly.json']
r={'status':'PASS actual local insertion and bore; complete fluid circuit unresolved','inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'sample_count_per_ring':24,'section_probes':rows,'actual_volume_and_face_controls':checks,'limits':['1.8mm test band within estimated3mm insertion; nominal radius6 contact does not prove pressure seal or retention','Remaining tube continuity follows retained tail plus valid single-solid head join; no flow simulation','Downstream bell clearance inherited, not repaired','Pump discharge and block gasket/gallery unresolved']}
p=ROOT/'inventory/engine/shifted-oil-pickup-contact-validation.json';p.write_text(json.dumps(r,indent=2)+'\n');print(checks,flush=True)
