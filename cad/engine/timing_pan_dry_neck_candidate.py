"""Estimated dry-side neck: explicit normal-offset walls, no hardware relief."""
import math
from pathlib import Path
import build123d as b
from timing_cover_attachment_v2 import norm
import timing_cover_front_joint_candidate as joint
ROOT=Path(__file__).resolve().parents[2]
FROZEN=ROOT/'cad/engine/generated/timing-cover-attachment-v2'
OUTER=[(335,-123),(354,-121.5),(378,-121.5),(378,184),(354,184),(335,109)]
WALL=4.
LEFT_SLOPE=1.5/19
RIGHT_SLOPE=75/19
# Parallel-line intersections, exact4mm normal offsets along each segment.
LEFT_B=-123-LEFT_SLOPE*335+WALL*math.sqrt(1+LEFT_SLOPE**2)
RIGHT_B=109-RIGHT_SLOPE*335-WALL*math.sqrt(1+RIGHT_SLOPE**2)
LEFT_KNEE=(-117.5-LEFT_B)/LEFT_SLOPE
RIGHT_KNEE=(180-RIGHT_B)/RIGHT_SLOPE
INNER=[(330,LEFT_SLOPE*330+LEFT_B),(LEFT_KNEE,-117.5),(374,-117.5),(374,180),(RIGHT_KNEE,180),(330,RIGHT_SLOPE*330+RIGHT_B)]
def box(x0,x1,y0,y1,z0,z1):return b.Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*b.Box(x1-x0,y1-y0,z1-z0)
def prism(points,z0,z1):return norm(b.Pos(0,0,z0)*b.extrude(b.Polygon(*points,align=None),amount=z1-z0))
def build():
 old=norm(b.import_step(FROZEN/'pan.step'))
 kept=norm(old.cut(box(335,500,-500,500,-80,200)))
 flange=norm(old.intersect(joint.front_blank(-6,-2)[0]))
 wall=norm(prism(OUTER,-76,0).cut(prism(INNER,-81,1)))
 wall=norm(wall.cut(joint.front_blank(-6,160)[0]))
 # Lower cross-section follows unchanged v9 loft at Z-80 (10/14 above-90).
 t=10/14;yc=-12+5*t;ow=242-10*t;iw=236-10*t
 lower_outer=b.Pos(0,yc,-80)*b.extrude(b.RectangleRounded(726,ow,24),amount=4)
 lower_inner=b.Pos(0,yc,-81)*b.extrude(b.RectangleRounded(720,iw,21),amount=6)
 lower_outer=norm(lower_outer.intersect(box(335,500,-500,500,-81,-75)))
 shoulder_outer=norm(prism(OUTER,-80,-76).fuse(lower_outer))
 opening=norm(lower_inner.intersect(prism(INNER,-81,-75)))
 shoulder=norm(shoulder_outer.cut(opening))
 pan=norm(kept.fuse(wall,flange,shoulder))
 return pan,old
