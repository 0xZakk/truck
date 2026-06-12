# Ignition coil — oil-filled can on the fender apron, HT tower + two
# primary terminals, mounting band clamp. Vertical axis.
# 1 unit = 1 inch. Origin = record position [72, 35, -7].
from build123d import *

DARK = Color(0.20, 0.21, 0.22)
BLACK = Color(0.10, 0.10, 0.11)
BRASS = Color(0.72, 0.60, 0.30)
STEEL = Color(0.60, 0.61, 0.62)


def gen_step():
    with BuildPart() as can:
        Cylinder(1.35, 4.0)
        # rolled top seam
        with Locations((0, 0, 2.05)):
            Cylinder(1.45, 0.30)
        # mounting band clamp w/ ear
        with Locations((0, 0, -0.8)):
            Cylinder(1.45, 0.5)
        with Locations((1.65, 0, -0.8)):
            Box(0.8, 0.5, 0.5)
    can.part.label = "coil can w/ band clamp"
    can.part.color = DARK

    with BuildPart() as top:
        # molded cap + HT tower
        with Locations((0, 0, 2.2)):
            Cylinder(1.30, 0.45, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, 2.65)):
            Cylinder(0.48, 0.95, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(top.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[-1], radius=0.1)
    top.part.label = "cap and HT tower"
    top.part.color = BLACK

    with BuildPart() as terms:
        for s in (1, -1):
            with Locations((s * 0.75, 0, 2.65)):
                Cylinder(0.14, 0.45, align=(Align.CENTER, Align.CENTER, Align.MIN))
    terms.part.label = "primary terminals"
    terms.part.color = BRASS

    asm = Compound(children=[can.part, top.part, terms.part])
    asm.label = "ignition coil, oil-filled can"
    return asm
