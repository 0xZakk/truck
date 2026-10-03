"""Isolated Auveco13019 envelope; estimated thread/point/head details, no host."""
from pathlib import Path
import math
import build123d as b
from pan_fastener_thread_candidate import solid,cz
O=Path(__file__).parent/'generated/airbox-screw-online-20261002'
PARAMETERS={'major_diameter':6.3,'pitch':1.81,'length_under_head':19.,'washer_head_od':11.5,'hex_af':8.,'estimated_root_diameter':4.5,'estimated_flange_thickness':.7,'estimated_hex_height':3.4,'estimated_top_bevel':.3,'estimated_point_length':4.,'estimated_tip_radius':.08,'estimated_crest_halfwidth':.08,'estimated_profile_halfwidth':.65,'estimated_right_handed':True}
def envelope():
 p=PARAMETERS;r=p['major_diameter']/2;tip=p['length_under_head'];start=tip-p['estimated_point_length']
 return solid(cz(r,0,start)+b.Pos(0,0,start)*b.Cone(r,p['estimated_tip_radius'],tip-start,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN)))
def head():
 p=PARAMETERS;f=p['estimated_flange_thickness'];h=p['estimated_hex_height'];r=p['hex_af']/math.sqrt(3)
 hexagon=b.Pos(0,0,-f-h)*b.extrude(b.RegularPolygon(r,6),amount=h)
 limit=cz(r,-f-h+p['estimated_top_bevel'],-f)+b.Pos(0,0,-f-h)*b.Cone(r-p['estimated_top_bevel'],r,p['estimated_top_bevel'],align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 return solid((hexagon & limit)+cz(p['washer_head_od']/2,-f,0))
def build(smooth=False):
 p=PARAMETERS;blank=envelope()
 if smooth:return solid(blank+head())
 root=p['estimated_root_diameter']/2;major=p['major_diameter']/2;pitch=p['pitch']
 profile=b.Plane.XZ*b.Polygon((root-.12,-p['estimated_profile_halfwidth']),(major,-p['estimated_crest_halfwidth']),(major,p['estimated_crest_halfwidth']),(root-.12,p['estimated_profile_halfwidth']),align=None)
 loop=solid(b.loft([b.Pos(0,0,pitch*i/24)*b.Rot(0,0,360*i/24)*profile for i in range(25)]))
 ridge=[]
 def tapered_section(z,angle):
  # Scale axial profile width with radial taper: avoids degenerate wide
  # polygons passing through the tiny endpoint. Crest inset stays in cone.
  slope=(major-p['estimated_tip_radius'])/p['estimated_point_length']
  factor=max(p['estimated_tip_radius']/major,min(1.,1-(z-(p['length_under_head']-p['estimated_point_length']))*slope/major))
  points=[]
  for radius,dz in [(root-.6,-p['estimated_profile_halfwidth']),(major-p['estimated_crest_halfwidth']*slope,-p['estimated_crest_halfwidth']),(major-p['estimated_crest_halfwidth']*slope,p['estimated_crest_halfwidth']),(root-.6,p['estimated_profile_halfwidth'])]:
   points.append((radius*factor,z+dz*factor))
  return b.Rot(0,0,angle)*(b.Plane.XZ*b.Polygon(*points,align=None))
 for k in range(-1,math.ceil(p['length_under_head']/pitch)):
  if (k+1)*pitch+p['estimated_profile_halfwidth']<p['length_under_head']-p['estimated_point_length']:
   ridge.append(b.Pos(0,0,pitch*k)*loop)
  else:
   sections=[tapered_section(pitch*(k+i/24),360*i/24) for i in range(25) if pitch*(k+i/24)<p['length_under_head']-.02]
   if len(sections)>1:ridge.append(solid(b.loft(sections,ruled=True)))
 start=p['length_under_head']-p['estimated_point_length']
 core=solid(cz(root,-pitch,start)+b.Pos(0,0,start)*b.Cone(root,p['estimated_tip_radius']*root/major,p['estimated_point_length'],align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN)))
 slab=b.Pos(0,0,p['length_under_head']/2)*b.Box(30,30,p['length_under_head'])
 clipped=[]
 for turn in ridge:
  intersection=turn & slab
  if intersection is not None:clipped.extend(intersection.solids())
 body=solid(core.fuse(*clipped))
 return solid((body & slab)+head())
