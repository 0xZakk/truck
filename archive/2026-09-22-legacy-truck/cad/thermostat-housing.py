# Thermostat housing (water outlet) — 4.9L (300) I6. Bolts to the FRONT
# face of the head (vertical YZ base plane), dome forward, gooseneck turning
# up-forward to the upper radiator hose (hose path starts at world [94, 38.5, 1];
# head front face is world x=94). 1 unit = 1 inch; +X fwd, +Z up, +Y left.
# Origin = record position [94.2, 38, 1].
from build123d import *

IRON = Color(0.40, 0.41, 0.42)


def gen_step():
    with BuildPart() as h:
        # oval base flange against the head front (bolts top/bottom)
        with BuildSketch(Plane.YZ.offset(-0.2)):
            SlotOverall(4.0, 2.3, rotation=90)
        extrude(amount=0.45)
        # dome over the thermostat, forward
        with Locations(Pos(0.45, 0, 0) * Rot(0, 90, 0)):
            Cylinder(1.30, 0.9)
        # gooseneck turning up-forward
        with Locations(Pos(1.35, 0, 0.55) * Rot(0, 50, 0)):
            Cylinder(0.92, 2.2)
        # hose bead at the outlet
        with Locations(Pos(2.05, 0, 1.4) * Rot(0, 50, 0)):
            Cylinder(1.00, 0.25)
        # flange bolts (top and bottom of the oval)
        for s in (1, -1):
            with Locations(Pos(0.30, 0, s * 1.45) * Rot(0, 90, 0)):
                Cylinder(0.17, 0.35)
    h.part.label = "thermostat housing / water outlet"
    h.part.color = IRON
    return h.part
