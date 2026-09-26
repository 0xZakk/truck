"""Provisional two-lobe timing-cover envelope around the corrected gear axes.

Coordinates are local to the existing cover rootX403. Profiles, depth, walls and
all unmodeled bosses remain assumptions, not a traced production casting.
"""
import math
import build123d as b


def envelope(r1,r2):
    cy,cz=90,72
    direction=math.atan2(cz,cy)
    offset=math.acos((r1-r2)/math.hypot(cy,cz))
    normals=[(math.cos(direction+t),math.sin(direction+t)) for t in [-offset,offset]]
    a,c=normals
    bridge=b.Polygon((r1*a[0],r1*a[1]),(cy+r2*a[0],cz+r2*a[1]),
                     (cy+r2*c[0],cz+r2*c[1]),(r1*c[0],r1*c[1]),align=None)
    return b.Circle(r1)+b.Pos(cy,cz)*b.Circle(r2)+bridge


def cover_shape():
    outer=b.Pos(-12,0,0)*b.extrude(b.Plane.YZ*envelope(52,88),amount=24)
    inner=b.Pos(-14,0,0)*b.extrude(b.Plane.YZ*envelope(48,84),amount=22)
    cover=outer-inner
    cover-=b.Rot(0,90,0)*b.Cylinder(24,40)
    cover-=b.Pos(11,0,0)*b.Rot(0,90,0)*b.Cylinder(27.1,10)
    return cover
