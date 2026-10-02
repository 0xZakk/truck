"""Local MTE5041 comparison specimen; see act-online-20261002-specimen.md."""
from pathlib import Path
import math
import build123d as b
O=Path(__file__).parent/'generated/act-online-20261002-specimen'
PARAMETERS={'hex_AF_mm':25,'pitch_mm':25.4/18,'thread_span_mm':15,'cut_helix_height_mm':12,'estimated_runouts_mm':1.5,'hex_height_mm':5.5,'collar_height_mm':2,'connector_above_collar_mm':22,'connector_OD_mm':18.5,'guard_reach_mm':10,'thread_crest_upper_diameter_estimate_mm':17.1,'thread_profile':'illustrative60deg taper; truncations/gauge/start unverified','frame':'Z0 threaded probe-side end, NOT gauge plane; +Z connector; mm; no vehicle pose'}
def cyl(r,z,h):return b.Pos(0,0,z+h/2)*b.Cylinder(r,h)
def build():
 shell=b.Cone(8.55-15/32,8.55,15,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 path=b.Helix(25.4/18,12,8.55-13.5/32,center=(0,0,1.5),cone_angle=math.degrees(math.atan(1/32)))
 profile=b.Plane(origin=path@0,x_dir=(1,0,0),z_dir=path%0)*b.Polygon((-.64,0),(.2,-.485),(.2,.485),align=None)
 shell=shell-b.sweep(profile,path=path,is_frenet=True)
 shell+=b.Pos(0,0,15)*b.extrude(b.RegularPolygon(25/math.sqrt(3),6),amount=5.5)
 shell+=cyl(12,20.5,2)
 shell-=cyl(4,-.1,20.1)
 shell-=cyl(9.25,20,3)
 outer=b.Polygon((-4.7,.4),(-2,-10),(2,-10),(4.7,.4),align=None)
 inner=b.Polygon((-2.8,-1),(-.7,-8.3),(.7,-8.3),(2.8,-1),align=None)
 guard=b.Pos(0,1.2,0)*b.extrude(b.Plane.XZ*(outer-inner),amount=2.4)
 shell+=guard
 # Explicit inferred feedthrough seat through guard bridge; not a source-measured cavity.
 shell-=cyl(4,0,20)
 shell-=cyl(.7,-1.1,1.2)
 ins=cyl(4,0,20)+cyl(9.25,20,24.5)+cyl(.7,-1,1)
 ins-=cyl(6.6,26,20)
 ins-=cyl(7.6,40,6)
 # Visible keys; rotational registration to engine/harness is unknown.
 for x,y,z,w,d,h in [(0,-9.5,22.5,1.6,1.7,22),(-3.2,9,27,1.4,2,17.5),(3.2,9,27,1.4,2,17.5)]:
  ins+=b.Pos(x,y,z+h/2)*b.Box(w,d,h)
 parts={'act-online-metal-shell':shell}
 for i,x in enumerate((-2.6,2.6),1):
  ins-=b.Pos(x,0,0)*cyl(.95,24,23)
  parts[f'act-online-contact-{i}']=b.Pos(x,0,0)*cyl(.95,24,13)
 parts['act-online-insulator']=ins
 parts['act-online-mouth-liner']=cyl(7.6,40,4.5)-cyl(6.6,39.9,4.7)
 # Visible blue encapsulation only; no hidden semiconductor or fabricated wiring.
 bead=cyl(1.2,-4.8,3.8)+b.Pos(0,0,-4.8)*b.Sphere(1.2)
 parts['act-online-visible-sensing-encapsulation']=bead
 return parts
