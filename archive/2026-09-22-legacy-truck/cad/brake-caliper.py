# Front brake caliper — single-piston sliding caliper at 12 o'clock over
# the rotor: outer/inner halves, bridge, piston boss, bleeder, pad ears.
# 1 unit = 1 inch; +X fwd, +Z up, +Y left. Origin = record position.
from build123d import *

CAST = Color(0.48, 0.49, 0.50)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as body:
        # inner and outer halves straddling the rotor (rotor plane y=0)
        for y in (1.35, -1.35):
            with Locations((0, y, -0.4)):
                Box(3.6, 1.5, 3.0)
        # bridge over the rotor edge
        with Locations((0, 0, 1.0)):
            Box(3.6, 4.2, 0.9)
        fillet(body.edges().filter_by(Axis.Y), radius=0.28)
        # piston boss on the inboard half
        with Locations(Pos(0, 2.0, -0.5) * Rot(90, 0, 0)):
            Cylinder(1.15, 0.8)
        # pad guide ears
        for x in (1.9, -1.9):
            with Locations((x, 0, -0.6)):
                Box(0.5, 3.2, 1.4)
    body.part.label = "caliper casting"
    body.part.color = CAST

    with BuildPart() as hw:
        # bleeder screw up on the inboard half
        with Locations(Pos(0.9, 2.0, 1.35) * Rot(0, 20, 0)):
            Cylinder(0.16, 0.9)
        # banjo fitting
        with Locations(Pos(-0.9, 2.35, 0.2) * Rot(90, 0, 0)):
            Cylinder(0.30, 0.5)
    hw.part.label = "bleeder + banjo fitting"
    hw.part.color = STEEL

    asm = Compound(children=[body.part, hw.part])
    asm.label = "front brake caliper"
    return asm
