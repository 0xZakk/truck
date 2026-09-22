# Muffler — 1994 F-150, oval-case rear muffler. Offset inlet (front, +x) and
# outlet (rear), rolled end caps with crimp seams. Oval section made by
# scaling a circle profile. 1 unit = 1 inch; +X fwd, +Z up, +Y left.
# Origin = record position [-84, 11, 14].
from build123d import *

BODY_L = 16.0
RX = 3.0     # vertical half (will be squashed)
SQ = 0.72    # vertical squash factor

DARK = Color(0.35, 0.36, 0.37)
STEEL = Color(0.58, 0.59, 0.60)


def gen_step():
    with BuildPart() as body:
        # oval case: extruded ellipse along X
        with BuildSketch(Plane.YZ):
            Ellipse(RX, RX * SQ)
        extrude(amount=BODY_L / 2, both=True)
        # rolled end caps
        for x in (BODY_L / 2 - 0.2, -BODY_L / 2 + 0.2):
            with BuildSketch(Plane.YZ.offset(x - 0.25)):
                Ellipse(RX + 0.08, (RX + 0.08) * SQ)
            extrude(amount=0.5)
    body.part.label = "muffler oval case"
    body.part.color = DARK

    with BuildPart() as pipes:
        # inlet stub front (offset right: viewer z +1.2 = build y -1.2),
        # outlet rear offset left — matching the mid/tailpipe path ends
        with Locations(Pos(BODY_L / 2 + 0.9, -1.2, 0) * Rot(0, 90, 0)):
            Cylinder(1.05, 2.2)
        with Locations(Pos(-BODY_L / 2 - 0.9, 1.2, 0) * Rot(0, 90, 0)):
            Cylinder(1.05, 2.2)
    pipes.part.label = "inlet and outlet stubs"
    pipes.part.color = STEEL

    asm = Compound(children=[body.part, pipes.part])
    asm.label = "muffler, oval case"
    return asm
