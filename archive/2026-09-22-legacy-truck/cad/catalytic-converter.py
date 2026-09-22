# Catalytic converter — 1994 F-150 underbody. Round-body converter with
# spun inlet/outlet cones and a wrap-around lower heat shield.
# Axis along +X; inlet faces forward (+x toward the headpipe at local +6.5).
# 1 unit = 1 inch. Origin = record position [38, 12, 14].
from build123d import *

AX = Rot(0, 90, 0)
STEEL = Color(0.58, 0.59, 0.60)
SHIELD = Color(0.72, 0.72, 0.70)


def gen_step():
    with BuildPart() as body:
        with Locations(AX):
            Cylinder(2.2, 11.0)
        # spun cones to pipe stubs
        with Locations(AX * Pos(0, 0, 6.25)):
            Cone(2.2, 1.05, 1.5)
        with Locations(AX * Pos(0, 0, -6.25)):
            Cone(1.05, 2.2, 1.5)
        # pipe stubs
        for x in (7.6, -7.6):
            with Locations(AX * Pos(0, 0, x)):
                Cylinder(1.05, 1.2)
    body.part.label = "catalytic converter body"
    body.part.color = STEEL

    with BuildPart() as shield:
        # corrugated lower half-shield
        with Locations(AX):
            Cylinder(2.55, 8.0)
        with Locations(AX):
            Cylinder(2.38, 8.2, mode=Mode.SUBTRACT)
        with Locations((0, 0, 1.2)):
            Box(9.0, 5.4, 2.8, mode=Mode.SUBTRACT)
        for x in (-2.4, 0, 2.4):
            with Locations(AX * Pos(0, 0, x)):
                Cylinder(2.62, 0.35)
            with Locations(AX * Pos(0, 0, x)):
                Cylinder(2.40, 0.45, mode=Mode.SUBTRACT)
            with Locations((0, 0, 1.2)):
                Box(9.0, 5.6, 2.9, mode=Mode.SUBTRACT)
    shield.part.label = "converter heat shield"
    shield.part.color = SHIELD

    asm = Compound(children=[body.part, shield.part])
    asm.label = "catalytic converter w/ heat shield"
    return asm
