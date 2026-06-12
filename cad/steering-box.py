# Steering gear — Ford recirculating-ball power box on the left rail.
# Cast housing w/ ribbed valve body, input shaft up to the column,
# sector shaft down to the pitman arm, side cover w/ adjuster, mount bosses.
# Bolts to the frame rail (whitelisted). 1 unit = 1 inch; +X fwd, +Z up,
# +Y left. Origin = record position [83, 24, -19].
from build123d import *

IRON = Color(0.36, 0.37, 0.38)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as housing:
        # main housing
        Box(5.4, 5.0, 6.2)
        fillet(housing.edges().filter_by(Axis.Y), radius=1.0)
        # valve body on top w/ ribs
        with Locations((0.4, 0, 3.4)):
            Cylinder(1.7, 1.6)
        for z in (3.0, 3.5, 4.0):
            with Locations((0.4, 0, z)):
                Cylinder(1.82, 0.18)
        # side adjuster cover (outboard face) + locknut
        with Locations(Pos(0, -2.8, 0.6) * Rot(90, 0, 0)):
            Cylinder(1.6, 0.7)
        with Locations(Pos(0, -3.25, 0.6) * Rot(90, 0, 0)):
            Cylinder(0.45, 0.4)
        # sector shaft housing down
        with Locations((0, 0, -3.9)):
            Cylinder(1.45, 2.0)
    housing.part.label = "steering gear housing"
    housing.part.color = IRON

    with BuildPart() as shafts:
        # input (worm) shaft toward the column (up/rearward)
        with Locations(Pos(-1.0, 0, 4.6) * Rot(0, -28, 0)):
            Cylinder(0.55, 2.6)
        # sector shaft stub to the pitman arm
        with Locations((0, 0, -5.3)):
            Cylinder(0.75, 1.2)
    shafts.part.label = "input and sector shafts"
    shafts.part.color = STEEL

    asm = Compound(children=[housing.part, shafts.part])
    asm.label = "power steering gear, recirculating ball"
    return asm
