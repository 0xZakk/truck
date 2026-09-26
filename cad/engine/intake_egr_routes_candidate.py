"""Isolated coordinated EGR route study for compact-plenum proposal.

No production bend dimensions, wall thickness or thermal/strength claim.
The existing replacement OD and fixed exhaust/EVR endpoints are preserved.
"""
import build123d as b
import egr_tube as original

DELTA=(167.,0.,25.)
END=(-245.,25.,459.)
HOSE_END=(-245.,85.,562.)

def route():
    # Compact rearward bow, with fixed exhaust and vertical valve tangents.
    # Control coordinates are estimated, not catalog bend dimensions.
    return b.Bezier(original.START,(-470,-180,230),(-435,25,530),(-245,25,409),END)

def parts():
    path=route();ro=original.OUTSIDE_DIAMETER/2;ri=ro-original.WALL
    tube=original.sweep_ring(path,ro,ri)
    tube+=b.Pos(*END)*original.ring(ro,ri,5)
    tube+=b.Pos(END[0],END[1],END[2]+5)*original.ring(11,ri,5)
    sleeve=original.sweep_ring(path.trim(.08,.88),12.5,ro+.2)
    start=(-420,-41,410)
    hosepath=b.Bezier(start,(-420,10,410),(-440,90,485),
                      (-345,125,562),(-245,125,562),HOSE_END)
    plane=b.Plane(origin=start,z_dir=(0,1,0))
    hose=b.sweep(plane*(b.Circle(6)-b.Circle(4.2)),path=hosepath,is_frenet=True)
    mount=b.Pos(*HOSE_END)*b.Rot(90,0,0)
    # Idealized fitted bore matches the current estimated2mm nipple radius.
    # This nominal contact does not establish compression or vacuum sealing.
    taper=b.Cone(6,3.85,12,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))-b.Cone(4.2,2.0,12,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    tip=b.Pos(0,0,12)*b.extrude(b.Circle(3.85)-b.Circle(2.0),amount=10)
    hose+=mount*(taper+tip)
    return {'egr-exhaust-tube':tube,'egr-tube-heat-sleeve':sleeve,
            'egr-tube-valve-nut':b.Pos(*DELTA)*original.valve_nut(),
            'egr-control-vacuum-hose':hose}
