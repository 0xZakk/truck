"""Isolated MODEL joint proposal, never factory dimensions or installed fit.
Dimensionless Fel-Pro outline is primary. Dorman supports cavity/7 bosses/bridge.
"""
from dataclasses import dataclass
import math
import build123d as b
import timing_cover_joint_candidate as source

@dataclass(frozen=True)
class Parameters:
    scale_mm_per_reference_pixel:float=.24
    source_crank_pixel:tuple=(595.,955.)
    rotation_deg:float=0.
    block_seat_x:float=373.
    gasket_thickness:float=.8
    cover_front_x:float=415.
    seal_center_x:float=414.
    cam_yz:tuple=(95.1098209901611,76.08785679212887)
    gear_center_x:float=385.259375
    gear_face_width:float=14.
    block_land_depth:float=10.
    cam_clearance:float=1.
    gear_axial_clearance:float=.25

CURRENT_CAM=(90.,72.)
SOURCE_RADII=(43.18,83.947)

def yz(pt,p):
    y=(pt[0]*1600-p.source_crank_pixel[0])*p.scale_mm_per_reference_pixel
    z=(p.source_crank_pixel[1]-pt[1]*1600)*p.scale_mm_per_reference_pixel
    a=math.radians(p.rotation_deg)
    return (y*math.cos(a)-z*math.sin(a),y*math.sin(a)+z*math.cos(a))

def face(points):
    # Corner-cut subdivision smooths the hand trace within its source-pixel
    # uncertainty. Dense planar chords avoid unstable near-coincident splines.
    for _ in range(2):
        points=[q for a,d in zip(points,points[1:]+points[:1])
                for q in [(a[0]*.75+d[0]*.25,a[1]*.75+d[1]*.25),
                          (a[0]*.25+d[0]*.75,a[1]*.25+d[1]*.75)]]
    return b.Plane.YZ*b.Polygon(*points,align=None)

def extrude_x(profile,x,length):return b.Pos(x,0,0)*b.extrude(profile,amount=length,dir=(1,0,0))
def cx(r,start,end,y=0,z=0):
    return b.Pos(start,y,z)*b.Rot(0,90,0)*b.Cylinder(r,end-start,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))

def profiles(p):
    points=[yz(q,p) for q in source.OUTLINE_NORMALIZED]
    # A formed lower bridge is visible but its actual section is unmeasured.
    # Keep it an explicit study contour, NOT a proven match to OS34601R.
    outer=points[:45]+[(110,-30),(65,-48),(35,-62),(0,-68),(-40,-60),(-82,-32)]
    inner=points[46:79]+[(-80,-28),(-42,-43),(0,-52),(42,-43),(80,-26),(130,-8)]
    return face(points),face(outer),face(inner)

def build(p=Parameters()):
    gasket_face,outer,inner=profiles(p);seat=p.block_seat_x;rear=seat+p.gasket_thickness
    gasket=extrude_x(gasket_face,seat,p.gasket_thickness)
    shell=extrude_x(outer,rear,p.cover_front_x-rear)
    shell-=extrude_x(inner,rear-1,p.cover_front_x-rear-2)
    shell+=extrude_x(gasket_face,rear,4)  # continuous source-shaped rear seating flange
    # Same crank/seal axis and occurrence as canonical. Existing seal OD27,
    # axial410..418 is supported by this estimated boss, without moving seal.
    shell+=cx(38,p.seal_center_x-8,p.seal_center_x+4)
    shell-=cx(27,p.seal_center_x-4,p.seal_center_x+5)
    shell-=cx(24,rear-1,p.seal_center_x-3.9)
    # Estimated internal relief only, preserving the source-shaped rear seat.
    # Both source-OD envelope options must clear without changing exterior.
    for cam in (CURRENT_CAM,p.cam_yz):
        shell-=cx(SOURCE_RADII[1]+p.cam_clearance,
                  p.gear_center_x-p.gear_face_width/2-p.gear_axial_clearance,
                  p.gear_center_x+p.gear_face_width/2+p.gear_axial_clearance,*cam)
    # Exterior stiffening pattern is visible in Dorman photos; positions and
    # section are estimated. This raised round pad is NOT a camshaft datum.
    shell+=cx(24,p.cover_front_x,p.cover_front_x+1.5,110,95)
    for end in [(52,145),(163,153),(185,88),(78,48)]:
        dy,dz=end[0]-110,end[1]-95
        shell+=b.Pos(p.cover_front_x+.75,(end[0]+110)/2,(end[1]+95)/2)*b.Rot(math.degrees(math.atan2(dz,dy)),0,0)*b.Box(1.5,math.hypot(dy,dz),3)
    land=extrude_x(gasket_face,seat-p.block_land_depth,p.block_land_depth)
    for pt in source.HOLES_NORMALIZED:
        y,z=yz(pt,p)
        shell+=cx(9,rear,p.cover_front_x,y,z)
        shell-=cx(4.2,rear-1,p.cover_front_x+1,y,z)
        gasket-=cx(4.2,seat-1,rear+1,y,z)
        # Proposed blind socket only, no thread/fastener calibration claimed.
        land-=cx(3.3,seat-7,seat+1,y,z)
    return {'timing-cover-shell-candidate':shell,'timing-cover-main-gasket-candidate':gasket,'timing-cover-block-land-proposal':land}

def gear_envelopes(p):
    a=p.gear_center_x-p.gear_face_width/2;c=p.gear_center_x+p.gear_face_width/2
    return (cx(SOURCE_RADII[0],a,c),cx(SOURCE_RADII[1],a,c,*p.cam_yz))
