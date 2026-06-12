# Twin I-Beam front axle beam — forged I-section spanning most of the track,
# pivot bushing boss at the inboard end, spindle knuckle at the outboard end.
# Beam runs laterally (build Y): outboard = +Y (left record as-is; the right
# record carries rotation [0,180,0]). 1 unit = 1 inch. Origin = record position.
from build123d import *

LEN = 44.0
H = 2.9        # section height
FW = 3.0       # flange width (fore-aft)
FT = 0.6       # flange thickness
WT = 1.1       # web thickness

CAST = Color(0.34, 0.35, 0.36)
DARK = Color(0.25, 0.26, 0.27)


def gen_step():
    with BuildPart() as beam:
        # I-section extruded along Y
        with BuildSketch(Plane.XZ):
            with Locations((0, H / 2 - FT / 2)):
                Rectangle(FW, FT)
            with Locations((0, -H / 2 + FT / 2)):
                Rectangle(FW, FT)
            Rectangle(WT, H - 2 * FT)
        extrude(amount=LEN / 2 - 2, both=True)
        # pivot bushing boss, inboard end (bolt axis fore-aft)
        with Locations(Pos(0, -(LEN / 2 - 1.2), 0) * Rot(0, 90, 0)):
            Cylinder(1.55, 3.0)
        with Locations(Pos(0, -(LEN / 2 - 1.2), 0) * Rot(0, 90, 0)):
            Cylinder(0.65, 3.4, mode=Mode.SUBTRACT)
        # outboard rise to the knuckle
        with Locations((0, LEN / 2 - 1.6, 0.6)):
            Box(3.0, 4.4, 4.2)
    beam.part.label = "I-beam, forged"
    beam.part.color = CAST

    with BuildPart() as spindle:
        # kingpin boss + spindle pin pointing outboard
        with Locations((0, LEN / 2 - 1.0, 0.8)):
            Cylinder(1.3, 5.0)
        with Locations(Pos(0, LEN / 2 + 0.6, 0.8) * Rot(-90, 0, 0)):
            Cone(1.0, 0.6, 3.2)
    spindle.part.label = "knuckle and spindle"
    spindle.part.color = DARK

    asm = Compound(children=[beam.part, spindle.part])
    asm.label = "Twin I-Beam axle beam"
    return asm
