"""Isolated estimated air cleaner; no owner fit or OEM dimensional claim.
Local mm frame at seal top center. WIX46174 comparison envelope only.
"""
import build123d as b

def box(x,y,h,z):
    return b.Pos(0,0,z)*b.Box(x,y,h,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def rr(x,y,r,z):
    return b.Plane.XY.offset(z)*b.RectangleRounded(x,y,r)
def tapered(x1,y1,z1,x2,y2,z2,r=8):
    return b.loft([rr(x1,y1,r,z1),rr(x2,y2,r,z2)])
def cylx(r,x,length,y,z):
    return b.Pos(x,y,z)*b.Rot(0,90,0)*b.Cylinder(r,length,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def seal():
    return box(326.7,148.7,4,-4)-box(304,126,6,-5)
def build():
    tray=tapered(310,140,-100,340,164,-7)-tapered(304,134,-97,334,158,-3)
    tray+=box(346,170,3,-7)-box(308,130,5,-8)
    # Short-face fresh-air entry collar, rectangular in the applicable drawing.
    collar=b.Pos(-176,0,-70)*b.Box(32,120,45)
    hole=b.Pos(-176,0,-70)*b.Box(50,114,39)
    tray=(tray+collar)-hole
    lid=b.loft([rr(334,158,8,3),rr(334,158,8,28),rr(326,148,10,48),rr(310,126,12,58)])
    lid-=b.loft([rr(328,152,8,-1),rr(328,152,8,28),rr(320,142,10,46),rr(304,120,12,55)])
    lid+=box(346,170,3,0)-box(304,126,5,-1)
    for y in (-37,37):
        lid+=cylx(30,-198,52,y,30)
        lid+=cylx(32,-192,3,y,30)
        lid-=cylx(27,-202,78,y,30)
    # Molded triangular gussets echo source silhouette; pitch is estimated.
    for x in range(-130,151,22):
        for side in (-1,1):
            # Connected narrow ribs taper toward the roof and tray bottom.
            lid+=b.Pos(x,0,0)*b.extrude(b.Plane.YZ*b.Polygon((side*84,3),(side*73,43),(side*73,3),align=None),amount=3)
            tray+=b.Pos(x,0,0)*b.extrude(b.Plane.YZ*b.Polygon((side*84,-7),(side*74,-48),(side*74,-7),align=None),amount=3)
    # Connected paper zigzag strip with a perimeter media representation.
    points=[]
    for i in range(61): points.append((-152+i*304/60,-42 if i%2==0 else -7))
    polygon=points+[(x,z+0.65) for x,z in reversed(points)]
    face=b.Plane.XZ*b.Polygon(*polygon,align=None)
    pleats=b.Pos(0,63,0)*b.extrude(face,amount=126)
    paper=pleats+(box(308,130,39.5,-43.5)-box(302,124,40,-44))
    return {'air-cleaner-lower-tray-candidate':tray,'air-cleaner-twin-outlet-cover-candidate':lid,
            'air-cleaner-paper-element-candidate':paper,'air-cleaner-perimeter-seal-candidate':seal()}
