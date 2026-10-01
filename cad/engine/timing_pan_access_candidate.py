"""Estimated constructed access wall; isolated from frozen v2 and canonical pan."""
from pathlib import Path
import build123d as b
import timing_cover_front_joint_candidate as j
from timing_cover_attachment_v2 import norm
ROOT=Path(__file__).resolve().parents[2]
FROZEN=ROOT/'cad/engine/generated/timing-cover-attachment-v2'
OUTER=[(335,-123,109),(354,-139.4666666667,184),(365,-149,184),(378,-149,184)]
INNER=[(330,-120,106),(350,-137.3333333333,180),(365,-145,180),(374,-145,180)]
def box(x0,x1,y0,y1,z0,z1):return b.Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*b.Box(x1-x0,y1-y0,z1-z0)
def envelope(rows,z0,z1):
 return norm(b.loft([b.Plane(origin=(x,(yl+yr)/2,(z0+z1)/2),x_dir=(0,1,0),z_dir=(1,0,0))*b.Rectangle(yr-yl,z1-z0) for x,yl,yr in rows],ruled=True))
def build():
 old=norm(b.import_step(FROZEN/'pan.step'))
 kept=norm(old.cut(box(335,500,-500,500,-80,200)))
 # Original complete flange, including five untouched full washer seats.
 flange=norm(old.intersect(j.front_blank(-6,-2)[0]))
 wall=norm(envelope(OUTER,-76,0).cut(envelope(INNER,-81,1)))
 wall=norm(wall.cut(j.front_blank(-6,160)[0]))
 polygon=[(x,l)for x,l,r in OUTER]+[(x,r)for x,l,r in reversed(OUTER)]
 shoulder=b.Pos(0,0,-80)*b.extrude(b.Polygon(*polygon,align=None),amount=4)
 opening=b.Pos(0,-7,-85)*b.extrude(b.RectangleRounded(720,226,21),amount=20)
 shoulder=norm(shoulder.cut(opening))
 pan=norm(kept.fuse(wall,flange,shoulder))
 return pan,old
