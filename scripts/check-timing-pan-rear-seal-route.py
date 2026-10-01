#!/usr/bin/env python3
"""Independent declared rear seal corridor against actual exported contact faces."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from timing_cover_attachment_v2 import norm
from oil_pan_joint_v9_candidate import x_cylinder
O=ROOT/'cad/engine/generated/timing-pan-rear-seal-review';F=ROOT/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate'
pan=norm(b.import_step(F/'pan.step'));gasket=norm(b.import_step(F/'pan-gasket.step'))
# Four millimeter corridor selected independently, within the declared 15mm rear arch.
# Surface at outer gasket radius53.1 meets the flat underside exactly at Z-34.
y=math.sqrt(53.1**2-34**2)
ring=norm((x_cylinder(53.1,-378,-374)-x_cylinder(52.1,-379,-373)) & (b.Pos(-376,0,-117)*b.Box(8,140,166)))
curves=[f for f in ring.faces() if f.geom_type==b.GeomType.CYLINDER]
# Identify outer radius from actual surface centroid/area via bounding box extrema.
outer=max(curves,key=lambda f:f.area)
flats=[b.Face(b.Wire.make_polygon([(-378,s*y,-34),(-374,s*y,-34),(-374,s*60,-34),(-378,s*60,-34)],close=True)) for s in [-1,1]]
route=b.Compound([outer,*flats])
def missing(faces,owner):
 q=BRepAlgoAPI_Cut(faces.wrapped,b.Compound(list(owner.faces())).wrapped);assert q.IsDone();return sum(f.area for f in b.Compound(q.Shape()).faces())
# Independent defect interrupts the entire selected four-mm corridor at arch bottom.
fault=norm(pan-(b.Pos(-376,0,-54)*b.Box(6,3,6)))
r={'scope':'Rear arch-to-flat-land contact corridor only; not whole perimeter or fluid containment','corridor_x_mm':[-378,-374],'corridor_width_mm':4,'radius_mm':53.1,'flat_join_z_mm':-34,'join_y_mm':[-y,y],'flat_endpoints_y_mm':[-60,60],'route_area_mm2':route.area,'pan_missing_area_mm2':missing(route,pan),'gasket_missing_area_mm2':missing(route,gasket),'fault_missing_area_mm2':missing(route,fault),'inherited_full_face_unbacked_area_mm2':25.535584654528463}
b.export_step(route,O/'contact-route.step')
# Actual exact sections for reproducible visual review.
for x in [-376,-367.5]:
 for name,shape in [('pan',pan),('gasket',gasket)]:
  sec=b.section(shape,b.Plane.YZ.offset(x));segments=[]
  for edge in sec.edges():
   segments.append([list(edge.position_at(i/100)) for i in range(101)])
  (O/f'{name}-section-{x}.json').write_text(json.dumps(segments))
r['status']='PASS bounded rear contact corridor' if r['pan_missing_area_mm2']<1e-5 and r['gasket_missing_area_mm2']<1e-5 and r['fault_missing_area_mm2']>1 else 'FAIL'
r['input_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),F/'pan.step',F/'pan-gasket.step',ROOT/'cad/engine/oil_pan_joint_v9_candidate.py']}
(ROOT/'inventory/engine/timing-pan-rear-seal-route-review.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
