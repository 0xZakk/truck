# Oil filter — Motorcraft FL-1A spin-on (white can), low on the block.
# Axis along +X like the old builder; threaded base toward the block (-X).
# Crimp ribs at the base end, domed outer end. NOTE: filter side pending
# owner-photo verification. 1 unit = 1 inch. Origin = record position [86, 25, -8].
from build123d import *

AX = Rot(0, 90, 0)
WHITE = Color(0.85, 0.85, 0.83)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as can:
        with Locations(AX):
            Cylinder(1.70, 4.2)
        # domed outer end
        fillet(can.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[-1], radius=0.55)
        # crimp ribs near the base
        for x in (-1.65, -1.35):
            with Locations(AX * Pos(0, 0, x)):
                Cylinder(1.76, 0.14)
    can.part.label = "oil filter can, FL-1A"
    can.part.color = WHITE

    with BuildPart() as base:
        with Locations(AX * Pos(0, 0, -2.25)):
            Cylinder(1.74, 0.30)
    base.part.label = "filter base plate"
    base.part.color = STEEL

    asm = Compound(children=[can.part, base.part])
    asm.label = "oil filter, spin-on FL-1A"
    return asm
