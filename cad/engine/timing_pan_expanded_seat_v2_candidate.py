"""Isolated X300 seat v2 with full socket flats; uses frozen shared analytic API."""
from pathlib import Path
import build123d as b
from timing_cover_attachment_v2 import norm
import timing_pan_expanded_seat_v2_contract as seat
ROOT=Path(__file__).resolve().parents[2]
FROZEN=ROOT/'cad/engine/generated/timing-cover-attachment-v2'
def box(x0,x1,y0,y1,z0,z1):return b.Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*b.Box(x1-x0,y1-y0,z1-z0)
def prism(points,z0,z1):return norm(b.Pos(0,0,z0)*b.extrude(b.Polygon(*points,align=None),amount=z1-z0))
def build():
 old=norm(b.import_step(FROZEN/'pan.step'));old_gasket=norm(b.import_step(FROZEN/'pan-gasket.step'))
 kept=norm(old.cut(box(300,500,-500,500,-80,200)))
 flange=seat.pan_flange();gasket=norm(seat.clip_x(old_gasket,-500,300).fuse(seat.gasket_band()))
 wall=norm(prism(seat.wall_outer,-76,0).cut(prism(seat.wall_inner,-81,1)))
 wall=norm(wall.intersect(seat.upper_wall_envelope()))
 t=10/14;yc=-12+5*t
 lower_outer=b.Pos(0,yc,-80)*b.extrude(b.RectangleRounded(726,242-10*t,24),amount=4)
 lower_outer=norm(lower_outer.intersect(box(300,500,-500,500,-81,-75)))
 lower_inner=b.Pos(0,yc,-81)*b.extrude(b.RectangleRounded(720,236-10*t,21),amount=6)
 shoulder_outer=norm(prism(seat.wall_outer,-80,-76).fuse(lower_outer))
 opening=norm(lower_inner.intersect(prism(seat.wall_inner,-81,-75)))
 shoulder=norm(shoulder_outer.cut(opening))
 pan=norm(kept.fuse(wall,flange,shoulder))
 return {'pan':pan,'pan-gasket':gasket}, {'pan':old,'pan-gasket':old_gasket}, {'flange':flange,'wall':wall,'shoulder':shoulder}
