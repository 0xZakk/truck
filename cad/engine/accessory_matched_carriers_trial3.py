"""Trial3: estimated dogleg open cradle and rear/outboard engine load paths."""
import math
import build123d as b
import accessory_matched_carriers_candidate as old
import accessory_brackets as base
CENTERS=old.CENTERS;FACES=old.FACES;EARS=old.EARS;ENGINE_SEATS=old.ENGINE_SEATS;SELECT=old.SELECT
union=old.union

def beam(a,z,r=7):
 d=tuple(q-p for p,q in zip(a,z));length=math.sqrt(sum(v*v for v in d));origin=tuple(p-2*v/length for p,v in zip(a,d));plane=b.Plane(origin=origin,z_dir=d)
 return plane*b.Box(2*r,2*r,length+4,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def carrier():
 shape=old.band('ALT');f=FACES['AP'];y,z=CENTERS['AP'];inner=EARS['AP'][1];outer=EARS['AP'][0]
 for ey,ez in EARS['AP']:shape=union(shape,base.boss(f,ey,ez,11,5.5))
 path=[inner,(inner[0],z+26),(-170,z+26),(y,z-75),outer]
 for a,c in zip(path[:-1],path[1:]):shape=union(shape,base.web(f,a,c,14))
 upper=(FACES['ALT']+5,EARS['ALT'][1][0]+7,CENTERS['ALT'][1]);front=(449,-160,180);lower=(f+5,-160,z+26)
 for a,c in [(upper,front),(front,lower),((394,-160,90),(394,-160,310)),((394,-160,180),front)]:shape=union(shape,beam(a,c))
 for ey,ez in ENGINE_SEATS:
  shape=union(shape,base.engine_foot(ey,ez,394,-160))
 shape=shape.intersect(b.Pos(673,0,0)*b.Box(600,2000,2000))
 for ey,ez in ENGINE_SEATS:shape=shape.cut(base.axial(5.5,22,(379,ey,ez)),base.axial(11,20,(395,ey,ez)))
 for g in EARS:
  f=FACES[g]
  for ey,ez in EARS[g]:
   shape=shape.cut(base.axial(5.5,30,(f+5,ey,ez)))
   shape=shape.cut(base.axial(12,100,(f-50,ey,ez)),base.axial(11,60,(f+40,ey,ez)))
 return shape
