# Cooling fan + thermal fan clutch — 1994 F-150 4.9L. Six steel blades on a
# riveted plate; the clutch hub bolts to the water-pump pulley (pulley face
# world x=99.7, bolted joint, whitelisted in check_geometry). Packaging is
# tight and real: blades (x<=99.76) clear the radiator rear tank face
# (100.2-0.4=99.8) and the clutch fins (x<=100.1) clear the core (100.2).
# The fan axis must run along +X: cadpy drops a parent Compound location on
# export, so the 90-deg Y rotation is baked into every child location (AX).
# 1 unit = 1 inch. Origin = record position [99, 30, 0].
from build123d import *

BLADES = 6
TIP_R = 8.3       # ~17" fan
ROOT_R = 3.95     # clears the water-pump lower inlet
PITCH = 15        # blade pitch, degrees
PLANE = 0.45      # blade plane along the axis (world 99.45)

AX = Rot(0, 90, 0)   # maps built +Z (axis) onto +X (truck forward)

STEEL = Color(0.62, 0.63, 0.65)
ZINC = Color(0.70, 0.71, 0.70)
BLACK = Color(0.12, 0.12, 0.13)


def gen_step():
    with BuildPart() as fan:
        # fan plate (bolts to the clutch flange), with center hole
        with Locations(AX * Pos(0, 0, 0.60)):
            Cylinder(2.7, 0.20)
        with Locations(AX * Pos(0, 0, 0.60)):
            Cylinder(1.2, 0.30, mode=Mode.SUBTRACT)
        # six pitched blades
        blade_len = TIP_R - ROOT_R + 0.5
        for i in range(BLADES):
            loc = (AX * Rot(0, 0, i * 360 / BLADES)
                   * Pos((ROOT_R + TIP_R) / 2, 0, PLANE) * Rot(PITCH, 0, 0))
            with Locations(loc):
                Box(blade_len, 2.4, 0.085)
        # rivets
        for i in range(BLADES):
            loc = AX * Rot(0, 0, i * 360 / BLADES + 30) * Pos(2.25, 0, 0.72)
            with Locations(loc):
                Cylinder(0.13, 0.10)
    fan.part.label = "fan, 6-blade steel"
    fan.part.color = BLACK

    with BuildPart() as clutch:
        # hub flange against the pump pulley
        with Locations(AX * Pos(0, 0, 0.60)):
            Cylinder(1.15, 0.20)
        # clutch body
        with Locations(AX * Pos(0, 0, 0.78)):
            Cylinder(1.70, 0.36)
        # bimetal face with radial cooling fins toward the radiator
        with Locations(AX * Pos(0, 0, 1.01)):
            Cylinder(2.10, 0.10)
        for i in range(12):
            loc = AX * Rot(0, 0, i * 30) * Pos(1.30, 0, 1.10)
            with Locations(loc):
                Box(1.5, 0.10, 0.10)
    clutch.part.label = "thermal fan clutch"
    clutch.part.color = ZINC

    asm = Compound(children=[fan.part, clutch.part])
    asm.label = "cooling fan with thermal clutch"
    return asm
