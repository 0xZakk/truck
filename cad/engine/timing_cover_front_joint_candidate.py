"""Estimated coordinated front joint, isolated; no canonical installation."""
import math
import build123d as b
from dataclasses import replace
import timing_cover_shell_candidate as c
import timing_cover_joint_candidate as source
import oil_pan_joint_v9_candidate as old
P=replace(c.Parameters(),scale_mm_per_reference_pixel=.26223302269259874,source_crank_pixel=(588.5373742452892,930.4751087566926),rotation_deg=-.039823552987937626)
PLANE=-24.5; CUT=335.; FRONT_START=365.; FRONT_END=399.; LEFT=-149.; RIGHT=213.; RADIUS=59.4

def joined(shape):
 if isinstance(shape,b.ShapeList):shape=b.Compound(children=list(shape))
 if not shape or not shape.solids():return b.Compound(children=[])
 return old.joined(shape)

def clip_x(shape,lo,hi):return shape.intersect(b.Pos((lo+hi)/2,0,0)*b.Box(hi-lo,1000,1000))
def clip_z(shape,lo,hi):return shape.intersect(b.Pos(0,0,(lo+hi)/2)*b.Box(1500,1500,hi-lo))
def smooth(points):
 # Two bounded corner subdivisions, each point displaced <=0.4 mm.
 # Total displacement <=0.8 mm, below8reference pixels(2.098 mm).
 for _ in range(2):
  out=[]
  for x,y in zip(points,points[1:]+points[:1]):
   d=math.dist(x,y);f=min(.25,.4/max(d,1e-12));out += [(x[0]*(1-f)+y[0]*f,x[1]*(1-f)+y[1]*f),(x[0]*f+y[0]*(1-f),x[1]*f+y[1]*(1-f))]
  points=out
 return points

def face(points):return b.Plane.YZ*b.Polygon(*smooth(points),align=None)
def top(y):return min(PLANE,-math.sqrt(max(0,RADIUS**2-y*y))) if abs(y)<RADIUS else PLANE
def band_profile(bottom_offset,top_offset):
 # Exact circle samples are geometry estimates; fine chords kept reproducible.
 a=math.sqrt(RADIUS**2-PLANE**2)
 ys=[LEFT]+[-a+2*a*i/96 for i in range(97)]+[RIGHT]
 lower=[(y,top(y)+bottom_offset) for y in ys];upper=[(y,top(y)+top_offset) for y in reversed(ys)]
 return b.Plane.YZ*b.Polygon(*(lower+upper),align=None)
def disk(r,x,y,z0,z1):return b.Pos(x,y,(z0+z1)/2)*b.Cylinder(r,z1-z0)
def vertical_sweep(blank,start,stop):
 # Blank is2mm thick at everyXY; adjacent translated copies share full faces.
 s=b.Pos(0,0,start)*blank
 for z in range(start+2,stop+1,2):s=joined(s+b.Pos(0,0,z)*blank)
 return s

def front_blank(bottom=-2,upper=0):
 s=c.extrude_x(band_profile(bottom,upper),FRONT_START,FRONT_END-FRONT_START)
 for old_y,new_y in [(-135.5,-132.),(111.5,196.)]:
  sections=[b.Plane(origin=(x,y,z+(bottom+upper)/2),x_dir=(0,1,0),z_dir=(1,0,0))*b.Rectangle(width,upper-bottom) for x,y,z,width in [(CUT,old_y,-32,11),(359.,old_y+.8*(new_y-old_y),PLANE,29.4),(FRONT_START,new_y,PLANE,34)]]
  s=joined(s+b.loft(sections,ruled=True))
 # Five revised stations;20other stations remain exactly as before.
 stations=[(365.5,y,PLANE-7.6) for y in (-132.,196.)]
 stations += [(390.,y,top(y)-7.6) for y in (-110.,0.,180.)]
 # Flat pad for every revised clamp, even on the rising side transition.
 for x,y,head in stations:
  z=head+7.6
  s=joined(s-disk(8,x,y,z-170,z+180))
  s=joined(s+disk(8,x,y,z+bottom,z+upper))
 return joined(s),stations

def build(pan_world=None):
 points=[c.yz(q,P) for q in source.OUTLINE_NORMALIZED]
 main_face=face(points);main=c.extrude_x(main_face,373,.8);main=clip_z(main,PLANE,500)
 land=clip_z(c.extrude_x(main_face,363,10),PLANE,500)
 outer_top=clip_z(c.extrude_x(face(points[:45]),0,1),PLANE,500)
 # Get a2Dface by rebuilding the top arch plus estimated lower bridge.
 outer=face(points[:45]+[(RIGHT,PLANE),(RIGHT,-70),(LEFT,-70),(LEFT,PLANE)])
 full=c.extrude_x(outer,373.8,41.2)
 # Lower boundary follows proposed pan seat, not the old interfering bridge.
 below=c.extrude_x(band_profile(-150,0),360,70)
 full-=below
 # Source-following internal cavity; rear sealing flange restored independently.
 inner=b.offset(outer,amount=-6)
 shell=full-c.extrude_x(inner,372.8,39.2)
 shell+=clip_z(c.extrude_x(main_face,373.8,4),PLANE,500)
 shell+=c.cx(38,406,418);shell-=c.cx(27,410,419);shell-=c.cx(24,372,410.1)
 for cam in (c.CURRENT_CAM,P.cam_yz):shell-=c.cx(84.947,378.009375,392.509375,*cam)
 shell-=c.cx(44.18,378.009375,392.509375)
 for pt in source.HOLES_NORMALIZED:
  y,z=c.yz(pt,P);shell+=clip_z(c.cx(9,373.8,415,y,z),PLANE,500);shell-=c.cx(4.2,372,417,y,z);main-=c.cx(4.2,372,375,y,z);land-=c.cx(3.3,366,374,y,z)
 blank,stations=front_blank();upper=front_blank(0,10)[0];lower=front_blank(-6,-2)[0]
 # Cover rear bridge may reach behind its flange only outside future block land.
 # The main gasket occupies its actual0.8mm seam at the two open terminals.
 land=joined(land+clip_x(upper,-500,365))
 cover_upper=clip_x(upper,365,500)-land-main
 shell+=cover_upper
 # Terminal sealant occupies explicit0.5mm-high pockets, never fills old gaps.
 pockets=clip_z(c.extrude_x(main_face,371.8,4),PLANE,PLANE+.5)
 sealant=pockets.intersect(shell+land+main)
 shell-=pockets;land-=pockets;main-=pockets
 # Front side mounting pads on the future block patch; merge only proposed dry
 # material, never broad canonical engine changes.
 for x,y,head in stations:
  z=head+7.6
  if x<373:land=joined(land+clip_x(disk(10,x,y,z,z+16),-500,373))
  else:shell+=disk(10,x,y,z,z+16)
  hole=disk(4.15,x,y,z-1,z+15)
  if x<373:land-=hole
  else:shell-=hole
  blank-=disk(4.3,x,y,head,head+10);lower-=disk(4.3,x,y,head,head+10)
 # Replace only the front gasket region; keep rear/long rails unchanged.
 gasket=clip_x(old.gasket_shape(),-500,CUT)+blank
 # Return front flange as a valid local patch first; full body can be supplied
 # from the unchanged v9 build for a complete pan candidate.
 pan=lower
 if pan_world is not None:
  kept=pan_world-(b.Pos(500,0,174)*b.Box(330,1000,500)) # x335..665,z-76..424
  # Transition neck: atX335 it matches original walls; new front wall closesX399.
  profiles=[];inners=[]
  for x,yl,yr in [(335,-123,109),(365,LEFT,RIGHT),(399,LEFT,RIGHT)]:
   profiles.append(b.Plane(origin=(x,(yl+yr)/2,-38),x_dir=(0,1,0),z_dir=(1,0,0))*b.Rectangle(yr-yl,76))
  for x,yl,yr in [(330,-120,106),(365,LEFT+4,RIGHT-4),(395,LEFT+4,RIGHT-4)]:
   inners.append(b.Plane(origin=(x,(yl+yr)/2,-38),x_dir=(0,1,0),z_dir=(1,0,0))*b.Rectangle(yr-yl,80))
  neck=b.loft(profiles,ruled=True)-b.loft(inners,ruled=True)
  neck-=c.extrude_x(band_profile(-6,160),365,50)
  # Side transition tops are clipped by the complete front gasket underside.
  neck-=front_blank(-6,160)[0]
  # A sealed shoulder connects the widened upper neck to the original body.
  shoulder=b.Pos(0,0,-80)*b.extrude(b.Polygon((335,-123),(365,LEFT),(399,LEFT),(399,RIGHT),(365,RIGHT),(335,109),align=None),amount=4)
  opening=b.Pos(0,-7,-85)*b.extrude(b.RectangleRounded(720,226,21),amount=20)
  shoulder-=opening
  pan=joined(kept+neck+lower+shoulder)
 # Define the compressed gasket/seal volumes as the explicit material boundary.
 # Subsequent full-face probes must still prove seating after this partition.
 below_seat=front_blank(-160,0)[0]
 shell=joined(shell-below_seat)
 land=joined(joined(land-below_seat)-sealant)
 shell=joined(shell-land)
 pan=joined(joined(joined(pan-gasket)-shell)-land)
 return {'cover':shell,'main-gasket':main,'future-block-land':land,'front-terminal-sealant':sealant,'pan-gasket':gasket,'pan':pan}, {'parameters':P.__dict__,'terminal_plane_mm':PLANE,'terminal_pocket_height_mm':.5,'front_stations':stations,'all_stations':[s for s in old.STATIONS if s[0]<CUT]+stations,'front_blank':front_blank()[0],'upper':upper,'lower':lower,'main_face':main_face,'source_points':points,'outer_mask':full}
