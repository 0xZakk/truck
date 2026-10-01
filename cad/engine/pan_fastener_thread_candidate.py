"""Isolated replacement for unreliable legacy male thread; nominal data retained."""
import math
import build123d as b
DIAMETER=7.9375;PITCH=25.4/18;LENGTH=22.098
ROOT_RADIUS=3.2
PROFILE_HALF_WIDTH=.1+(DIAMETER/2-3.0)/math.sqrt(3)

def solid(s):
 ss=list(s.solids())
 if len(ss)!=1:raise ValueError(f'Expected one solid, got {len(ss)}')
 return b.Solid(ss[0].wrapped)
def cz(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
def screw():
 # One-turn radial/axial loft avoids a long pipe sweep's fragile seams.
 # Algorithmic reference: bd_warehouse thread.py _make_thread_loop
 # https://github.com/gumyr/bd_warehouse (Apache-2.0); independently expressed.
 profile=b.Plane.XZ*b.Polygon((3.0,-PROFILE_HALF_WIDTH),(DIAMETER/2,-.10),(DIAMETER/2,.10),(3.0,PROFILE_HALF_WIDTH),align=None)
 loop=solid(b.loft([b.Pos(0,0,PITCH*i/12)*b.Rot(0,0,360*i/12)*profile for i in range(13)]))
 coils=[b.Pos(0,0,PITCH*i)*loop for i in range(-1,math.ceil(LENGTH/PITCH)+1)]
 body=solid(cz(ROOT_RADIUS,-PITCH,LENGTH+PITCH).fuse(*coils))
 body=solid(body.intersect(b.Pos(0,0,(1.7+LENGTH)/2)*b.Box(20,20,LENGTH-1.7)))
 head=b.Pos(0,0,-5.3)*b.extrude(b.RegularPolygon(12.7/math.sqrt(3),6),amount=5.3)
 return solid(body+cz(ROOT_RADIUS,0,1.71)+cz(DIAMETER/2,0,1.6)+head)

def female(male):
 return solid(cz(4.17,7.8,22.3)-solid(male+cz(4,22,23)))
