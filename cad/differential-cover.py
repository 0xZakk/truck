# Differential cover — Ford 8.8 stamped steel cover on the rear axle:
# domed shell, bolt flange w/ 10 bolts, fill plug. Faces rearward (-X);
# flange against the housing at the +x side like the old builder.
# 1 unit = 1 inch. Origin = record position [-73.6, 14.9, 0].
from build123d import *

AX = Rot(0, 90, 0)
STEEL = Color(0.55, 0.56, 0.57)
DARK = Color(0.35, 0.36, 0.37)


def gen_step():
    with BuildPart() as cover:
        # domed shell
        with Locations(AX * Pos(0, 0, -0.1)):
            Cylinder(4.4, 1.2)
        fillet(cover.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[0], radius=0.6)
        # bolt flange
        with Locations(AX * Pos(0, 0, 0.7)):
            Cylinder(4.75, 0.35)
        # fill plug
        with Locations(AX * Pos(0, 2.2, -0.85)):
            Cylinder(0.55, 0.4)
    cover.part.label = "diff cover, stamped"
    cover.part.color = STEEL

    with BuildPart() as bolts:
        for i in range(10):
            with Locations(AX * Rot(0, 0, i * 36) * Pos(4.15, 0, 0.95)):
                Cylinder(0.18, 0.35)
    bolts.part.label = "cover bolts"
    bolts.part.color = DARK

    asm = Compound(children=[cover.part, bolts.part])
    asm.label = "differential cover, Ford 8.8"
    return asm
