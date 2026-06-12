# Shock absorber — gas shock used at all four corners (front/rear records
# apply their own tilt rotations). Body tube, upper dust shield over the
# rod, stud top mount w/ bushing, bottom eye ring. Vertical axis.
# 1 unit = 1 inch. Origin = record position.
from build123d import *

DARK = Color(0.16, 0.17, 0.18)
STEEL = Color(0.62, 0.63, 0.65)
RUBBER = Color(0.12, 0.12, 0.12)


def gen_step():
    with BuildPart() as body:
        # main tube
        with Locations((0, 0, 0)):
            Cylinder(0.95, 7.0)
        fillet(body.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[0], radius=0.25)
        # bottom eye (bolt axis lateral)
        with Locations(Pos(0, 0, -4.0) * Rot(90, 0, 0)):
            Torus(0.78, 0.30)
    body.part.label = "shock body and lower eye"
    body.part.color = DARK

    with BuildPart() as upper:
        # rod (reaches into the stud-mount bushing stack)
        with Locations((0, 0, 5.1)):
            Cylinder(0.30, 3.6)
        # dust shield tube overlapping the body
        with Locations((0, 0, 3.6)):
            Cylinder(1.05, 2.8)
        fillet(upper.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[-1], radius=0.2)
    upper.part.label = "rod and dust shield"
    upper.part.color = STEEL

    with BuildPart() as mount:
        # stud-mount bushings + washer stack
        with Locations((0, 0, 7.0)):
            Cylinder(0.80, 0.55)
        with Locations((0, 0, 7.6)):
            Cylinder(0.55, 0.55)
        with Locations((0, 0, 8.05)):
            Cylinder(0.25, 0.5)
    mount.part.label = "upper stud mount bushings"
    mount.part.color = RUBBER

    asm = Compound(children=[body.part, upper.part, mount.part])
    asm.label = "shock absorber, gas"
    return asm
