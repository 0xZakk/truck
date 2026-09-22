# Brake vacuum booster + master cylinder — 1994 F-150. Clamshell stamped
# booster (two domed shells, crimped band) on the firewall, cast-iron master
# cylinder with plastic reservoir + two caps ahead of it. Axis along +X
# (booster rear against the firewall, MC forward). Rotations baked per child.
# 1 unit = 1 inch. Origin = record position [74, 40, -16].
from build123d import *

AX = Rot(0, 90, 0)
SHELL = Color(0.20, 0.21, 0.22)
IRON = Color(0.40, 0.41, 0.42)
RES = Color(0.80, 0.79, 0.74)
CAPC = Color(0.13, 0.13, 0.14)


def gen_step():
    with BuildPart() as booster:
        # rear shell
        with Locations(AX * Pos(0, 0, -1.7)):
            Cylinder(3.9, 1.7)
        # front shell
        with Locations(AX * Pos(0, 0, 1.0)):
            Cylinder(3.9, 2.0)
        fillet(booster.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[0], radius=0.9)
        fillet(booster.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[-1], radius=0.9)
        # crimp band
        with Locations(AX * Pos(0, 0, -0.1)):
            Cylinder(4.02, 0.5)
        # vacuum check valve, front shell upper
        with Locations(Pos(1.6, 0, 2.6) * Rot(0, 35, 0)):
            Cylinder(0.45, 1.3)
    booster.part.label = "vacuum booster, clamshell"
    booster.part.color = SHELL

    with BuildPart() as mc:
        # mounting flange + cylinder body
        with Locations(AX * Pos(0, 0, 3.1)):
            Box(0.4, 3.2, 3.2)
        with Locations(AX * Pos(0, -0.3, 5.0)):
            Cylinder(1.25, 3.8)
        # end plug
        with Locations(AX * Pos(0, -0.3, 7.0)):
            Cylinder(0.85, 0.5)
    mc.part.label = "master cylinder casting"
    mc.part.color = IRON

    with BuildPart() as res:
        # dual-bowl plastic reservoir
        with Locations((5.0, 0.3, 1.6)):
            Box(3.4, 2.2, 2.0)
        fillet(res.edges().filter_by(Axis.Z), radius=0.5)
    res.part.label = "brake fluid reservoir"
    res.part.color = RES

    with BuildPart() as caps:
        for x in (4.1, 5.9):
            with Locations((x, 0.3, 2.65)):
                Cylinder(0.62, 0.30)
    caps.part.label = "reservoir caps"
    caps.part.color = CAPC

    asm = Compound(children=[booster.part, mc.part, res.part, caps.part])
    asm.label = "brake booster + master cylinder"
    return asm
