"""Coherent provisional rear journal/bearing and pushrod gasket clearance.

The original rear journal station intrudes into the cylinder6 intake follower.
Retain its sourced radial envelope and23mm assumed width; move the entire
journal and bearing together4mm rearward. This is not a recovered Ford station.
"""
import build123d as b
OLD_STATION=-330.
NEW_STATION=-334.
WIDTH=23.
CORE_RADIUS=15.
SOURCES=['fsm-2e5473b2bf99','fsm-33bfe47109d5']
GAPS=[
 'Rear cam journal and bearing move from assumedX-330to-334mm to clear the complete cylinder6 intake follower. Journal width23mm, bearing width22mm and axial coordinates remain unverified; source radial dimensions are preserved.',
 'The existing continuous cam bore supports the revised bearing location; actual bearing retention, oil-feed indexing and axial production layout remain unresolved.',
 'The head gasket pushrod openings retain their old clearance and gain a6mm-radius cut at the revisedY90axis. Hole contours and sealing lands remain provisional; positive passage checks do not establish a production gasket.'
]

def axial(radius,width,x=0):return b.Pos(x,0,0)*b.Rot(0,90,0)*b.Cylinder(radius,width)

def cam_interface(shape,journal_radius):
    # Cut only the old journal annulus; keep the continuous shaft and all lobes.
    shape-=axial(30,WIDTH,OLD_STATION)-axial(CORE_RADIUS,WIDTH+2,OLD_STATION)
    shape+=axial(journal_radius,WIDTH,NEW_STATION)
    return shape

def gasket_interface(shape,stations):
    for x in stations:shape-=b.Pos(x,90,0)*b.Cylinder(6,8)
    return shape
