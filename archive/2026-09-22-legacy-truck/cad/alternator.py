# Alternator — Ford 2G-style, 1994 F-150 4.9L. Cast aluminum drive-end and
# rear housings around the stator band, cooling fan behind the pulley, lower
# mounting ear and top adjuster ear. Axis along +X (belt at the front of the
# engine): rotation baked into every child location (cadpy drops parent
# Compound locations). 1 unit = 1 inch. Origin = record position [92, 38.5, 13].
from build123d import *

AX = Rot(0, 90, 0)   # built +Z (axis) -> +X (forward)

CAST = Color(0.58, 0.60, 0.61)
STEEL = Color(0.62, 0.63, 0.65)
DARK = Color(0.22, 0.22, 0.23)


def gen_step():
    with BuildPart() as housing:
        # stator band (center)
        with Locations(AX):
            Cylinder(2.65, 1.4)
        # drive-end housing, tapering toward the pulley, with vent windows
        with Locations(AX * Pos(0, 0, 1.4)):
            Cone(2.65, 1.9, 1.4)
        # rear housing with vent windows
        with Locations(AX * Pos(0, 0, -1.4)):
            Cone(2.65, 2.1, 1.4)
        # radial vent slots on both cones
        for zc, tilt in ((1.5, 1), (-1.5, -1)):
            for i in range(10):
                loc = AX * Rot(0, 0, i * 36 + 18) * Pos(2.0, 0, zc)
                with Locations(loc):
                    Box(1.1, 0.55, 0.5, mode=Mode.SUBTRACT)
        # lower mounting ear (bolts to the bracket on the block)
        with Locations(AX * Pos(0, -2.9, 0.9) * Rot(90, 0, 0)):
            Cylinder(0.65, 1.6)
        with Locations(AX * Pos(0, -2.9, 0.9) * Rot(90, 0, 0)):
            Cylinder(0.28, 1.8, mode=Mode.SUBTRACT)
        with Locations(AX * Pos(0, -2.35, 0.9)):
            Box(1.3, 1.5, 1.3)
        # top adjuster ear with slot
        with Locations(AX * Pos(0, 2.85, -0.2)):
            Box(0.55, 1.4, 1.0)
        with Locations(AX * Pos(0, 3.05, -0.2) * Rot(0, 90, 0)):
            Cylinder(0.17, 1.0, mode=Mode.SUBTRACT)
    housing.part.label = "alternator housings and stator band"
    housing.part.color = CAST

    with BuildPart() as rear:
        # rectifier end cover + battery stud
        with Locations(AX * Pos(0, 0, -2.8)):
            Cylinder(1.6, 0.5)
        with Locations(AX * Pos(0.9, 0.6, -3.1)):
            Cylinder(0.16, 0.5)
    rear.part.label = "rear cover and battery stud"
    rear.part.color = DARK

    with BuildPart() as drive:
        # external cooling fan behind the pulley
        with Locations(AX * Pos(0, 0, 2.85)):
            Cylinder(1.85, 0.12)
        for i in range(12):
            loc = AX * Rot(0, 0, i * 30) * Pos(1.25, 0, 2.97) * Rot(0, 0, 25)
            with Locations(loc):
                Box(1.1, 0.45, 0.10)
        # V-belt pulley: two flanges + groove hub
        for z, r in ((3.20, 1.55), (3.60, 1.55)):
            with Locations(AX * Pos(0, 0, z)):
                Cylinder(r, 0.16)
        with Locations(AX * Pos(0, 0, 3.40)):
            Cylinder(1.05, 0.55)
        # shaft nut
        with Locations(AX * Pos(0, 0, 3.78)):
            Cylinder(0.42, 0.35)
    drive.part.label = "fan, pulley, shaft nut"
    drive.part.color = STEEL

    asm = Compound(children=[housing.part, rear.part, drive.part])
    asm.label = "alternator, Ford 2G style"
    return asm
