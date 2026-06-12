# Power steering pump — Ford C-II style with integral reservoir canister,
# filler neck + cap on the rear top, V-belt pulley at the front.
# Axis along +X; rotations baked per child. 1 unit = 1 inch.
# Origin = record position [92, 35.5, -9].
from build123d import *

AX = Rot(0, 90, 0)
STEEL = Color(0.55, 0.56, 0.57)
DARK = Color(0.22, 0.22, 0.23)
BLACK = Color(0.10, 0.10, 0.11)


def gen_step():
    with BuildPart() as res:
        # reservoir canister
        with Locations(AX * Pos(0, 0, -0.4)):
            Cylinder(2.2, 3.4)
        fillet(res.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[0], radius=0.5)
        # filler neck on the rear top
        with Locations((-1.2, 0, 2.0)):
            Cylinder(0.55, 0.9)
        # pressure fitting, bottom
        with Locations(Pos(-1.0, 0, -2.3) * Rot(90, 0, 0)):
            Cylinder(0.30, 1.0)
    res.part.label = "PS pump reservoir canister"
    res.part.color = STEEL

    with BuildPart() as cap:
        with Locations((-1.2, 0, 2.55)):
            Cylinder(0.72, 0.5)
        fillet(cap.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[-1], radius=0.12)
    cap.part.label = "filler cap w/ dipstick"
    cap.part.color = BLACK

    with BuildPart() as drive:
        # shaft hub + single-groove V pulley
        with Locations(AX * Pos(0, 0, 1.65)):
            Cylinder(0.8, 1.1)
        for x, r in ((2.30, 2.5), (2.75, 2.5)):
            with Locations(AX * Pos(0, 0, x)):
                Cylinder(r, 0.18)
        with Locations(AX * Pos(0, 0, 2.52)):
            Cylinder(2.05, 0.30)
        with Locations(AX * Pos(0, 0, 2.95)):
            Cylinder(0.40, 0.25)
    drive.part.label = "pulley and shaft"
    drive.part.color = DARK

    asm = Compound(children=[res.part, cap.part, drive.part])
    asm.label = "power steering pump, C-II w/ reservoir"
    return asm
