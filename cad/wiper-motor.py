# Wiper motor — cowl-mounted: motor can + round gearbox housing + output
# crank arm. Axis along +X like the old builder. 1 unit = 1 inch.
# Origin = record position [58, 46, -6].
from build123d import *

AX = Rot(0, 90, 0)
DARK = Color(0.25, 0.25, 0.26)
CAST = Color(0.50, 0.51, 0.52)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as motor:
        with Locations(AX * Pos(0, 0, -0.6)):
            Cylinder(1.55, 2.8)
        fillet(motor.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[0], radius=0.45)
        # through-bolts
        for s in (1, -1):
            with Locations(AX * Pos(0, s * 1.1, -0.5)):
                Cylinder(0.10, 3.0)
    motor.part.label = "wiper motor can"
    motor.part.color = DARK

    with BuildPart() as gear:
        # round gearbox housing
        with Locations(AX * Pos(0, 0, 1.45)):
            Cylinder(1.85, 1.3)
        fillet(gear.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[-1], radius=0.35)
        # mounting ears
        for ang in (60, 180, 300):
            with Locations(AX * Rot(0, 0, ang) * Pos(2.1, 0, 1.0)):
                Cylinder(0.45, 0.3)
    gear.part.label = "wiper gearbox"
    gear.part.color = CAST

    with BuildPart() as crank:
        # output shaft + crank arm
        with Locations((1.45, 0, 1.5)):
            Cylinder(0.35, 1.0)
        with Locations((1.45, 0.9, 1.95)):
            Box(0.5, 2.4, 0.25)
        with Locations((1.45, 2.0, 1.75)):
            Cylinder(0.18, 0.5)
    crank.part.label = "output crank"
    crank.part.color = STEEL

    asm = Compound(children=[motor.part, gear.part, crank.part])
    asm.label = "windshield wiper motor"
    return asm
