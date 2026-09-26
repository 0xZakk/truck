"""Isolated IAC attachment study, issue 44. All dimensions are estimated mm.

Factory evidence establishes two diagonal mounting fasteners and reverse-seated
pintle topology, not these dimensions or this spring/joint construction.
Input solids and output solids use the existing IAC local frame. No shared writes.
"""
import build123d as b
BOLTS=((-16.,-21.),(16.,21.))
ORIGIN=(397.,25.,540.)
PARAMS=dict(shaft_radius=2.5,clearance_radius=2.8,receiver_radius=2.55,
            head_radius=4.5,head_height=4.,underhead_z=-10.,tip_z=-23.,
            receiver_bottom_z=-24.,flange_bottom_z=-13.,gasket_bottom_z=-14.,
            spring_wire_radius=.4,spring_mean_radius=3.,spring_turns=5.75)
def cx(r,length):return b.Rot(0,90,0)*b.Cylinder(r,length)
def zc(r,lo,hi,x=0,y=0):return b.Pos(x,y,(lo+hi)/2)*b.Cylinder(r,hi-lo)
def ear(x,y,lo,hi):
    # A broad neck joins the round ear to the existing casting, not a tangent join.
    return zc(7,lo,hi,x,y)+b.Pos(x,y/2,(lo+hi)/2)*b.Box(14,abs(y),hi-lo)
def screw(radius=2.5):
    head=b.Pos(0,0,-8)*b.extrude(b.RegularPolygon(4.5,6),amount=2,both=True)
    return head+zc(radius,-23,-10)
def spring(pintle_travel=0):
    """Illustrative closed/ground end compression spring; no force calibration."""
    left,right=-23.,-4.+pintle_travel; length=right-left
    helix=b.Pos(left+.6,0,0)*b.Rot(0,90,0)*b.Helix((length-1.2)/5.75,length-1.2,3)
    s=b.sweep(b.Plane(origin=helix@0,z_dir=helix%0)*b.Circle(.4),helix)
    for x in [left+.4,right-.4]:s+=b.Pos(x,0,0)*(cx(3.5,.8)-cx(2.5,1.))
    return s
def build(body,gasket,throttle,armature):
    """Return changed solids plus two screws and illustrative spring.

    throttle must already be transformed into IAC local frame. Unmodified inputs
    are not overwritten. Receiver bores represent a thread envelope only.
    """
    for x,y in BOLTS:
        body=body+ear(x,y,-13,-10)
        gasket=gasket+ear(x,y,-14,-13)
        throttle=throttle+ear(x,y,-28,-14)
        body=body-zc(2.8,-14,-9,x,y)
        gasket=gasket-zc(2.8,-15,-12,x,y)
        throttle=throttle-zc(2.55,-24,-13,x,y)
    # Reapply the existing ports after the flange neck unions. No plug or
    # narrowing is allowed merely to provide screw material.
    for x in [-12,12]:
        body-=zc(5,-18,2,x,0)
        gasket-=zc(5,-15,-12,x,0)
        throttle-=zc(5,-35,-11,x,0)
    # Contact sleeve eliminates the radial disconnect, but represents a bonded
    # educational joint, not a verified production swage/press fit.
    armature+=b.Pos(44.75,0,0)*(cx(1.65,17.5)-cx(1.5,18))
    result={'iac-valve-body':body,'iac-gasket':gasket,'throttle-housing':throttle,
            'iac-armature':armature,'iac-return-spring-estimated':spring()}
    for i,(x,y) in enumerate(BOLTS,1):result[f'iac-mount-screw-{i}-estimated']=b.Pos(x,y,0)*screw()
    return result
