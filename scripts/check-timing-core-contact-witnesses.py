#!/usr/bin/env python3
"""Planar axial contact witnesses and bounded fault control, isolated core only."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-core-migration-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=['cam-timing-gear','cam-gear-spacer','cam-thrust-plate','camshaft','cam-bearing-2']+[f'cam-thrust-{x}-{i}' for x in ['bolt','washer'] for i in [1,2]]
paths={x:OUT/(x+'.step') for x in names};inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()};parts={x:b.import_step(p) for x,p in paths.items()}
def faces(q):return [(f,f.bounding_box().min.X) for f in q.faces() if f.bounding_box().size.X<1e-5]
def area(a,d):
 result=0.
 for f,x in faces(parts[a]):
  for g,y in faces(parts[d]):
   if abs(x-y)<1e-6:
    common=f.intersect(g)
    if common:result+=sum(v.area for v in common.faces())
 return result
pairs=[('camshaft','cam-gear-spacer'),('camshaft','cam-thrust-plate'),('cam-timing-gear','cam-thrust-plate'),('cam-timing-gear','cam-gear-spacer'),('cam-thrust-plate','cam-gear-spacer')]+[(f'cam-thrust-washer-{i}','cam-thrust-plate') for i in [1,2]]+[(f'cam-thrust-bolt-{i}',f'cam-thrust-washer-{i}') for i in [1,2]]
contacts=[{'a':a,'b':d,'coplanar_axial_face_overlap_area_mm2':area(a,d)} for a,d in pairs]
bearing=parts['cam-bearing-2'];bb=bearing.bounding_box();shaft=parts['camshaft'].intersect(b.Pos((bb.min.X+bb.max.X)/2,0,0)*b.Box(bb.size.X+2,600,600))
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
correct=vol(shaft.intersect(bearing));bad=vol(shaft.intersect(b.Pos(0,1,0)*bearing))
assert correct<.1 and bad>.1
assert inputs=={str(p.relative_to(ROOT)):sha(p) for p in paths.values()},'Input changed during check'
gear=parts['cam-timing-gear'].intersect(b.Pos(385.259375,95.1098209901611,76.08785679212888)*b.Rot(0,90,0)*b.Cylinder(50,30))
gear_plate_gap=gear.distance_to(parts['cam-thrust-plate'])
axial_gaps=[]
for pf,px in faces(parts['cam-thrust-plate']):
 if pf.normal_at().X<.99:continue
 for gf,gx in faces(parts['cam-timing-gear']):
  if gf.normal_at().X>-.99 or gx<px:continue
  common=pf.intersect(b.Pos(px-gx,0,0)*gf)
  witness=sum(f.area for f in common.faces()) if common else 0
  if witness>1e-6:axial_gaps.append({'gap_mm':gx-px,'projected_face_area_mm2':witness})
r={'status':'CHECKED planar axial witnesses; PASS shifted-bearing fault sensitivity','input_sha256':inputs,'checker_sha256':sha(Path(__file__)),'contacts':contacts,'gear_to_plate_local_gap_mm':gear_plate_gap,'opposing_gear_plate_axial_projection_witnesses':axial_gaps,'nominal_stack_endplay_mm':0.1,'warning':'Nominal spacer-minus-plate thickness does not establish actual axial thrust endplay; relief geometry requires opposing-face review','negative_control':{'correct_bearing_overlap_mm3':correct,'one_mm_lateral_shift_overlap_mm3':bad},'limits':['Zero contact area may mean designed gap or unresolved contact, never silently a contact pass','Only planar faces normal to axial X considered','No loads/press-fit or block/socket seating acceptance']}
(ROOT/'inventory/engine/timing-core-contact-witnesses.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
