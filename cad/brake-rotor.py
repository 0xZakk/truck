# Front brake rotor — vented disc w/ radial vanes between the two friction
# faces, hub hat, 5 wheel studs on the 5.5" bolt circle. Spin axis lateral
# (build Y); hat faces viewer -z like the old builder so both corner records
# drop in unchanged. 1 unit = 1 inch. Origin = record position.
from build123d import *

AXL = Rot(90, 0, 0)   # built +Z (spin axis) -> viewer +z (lateral)

R = 6.5
FACE_T = 0.34
GAP = 0.42
IRON = Color(0.45, 0.46, 0.47)
DARK = Color(0.30, 0.31, 0.32)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as disc:
        # two friction faces
        for z in (GAP / 2 + FACE_T / 2, -(GAP / 2 + FACE_T / 2)):
            with Locations(AXL * Pos(0, 0, z)):
                Cylinder(R, FACE_T)
        # radial cooling vanes
        for i in range(24):
            with Locations(AXL * Rot(0, 0, i * 15) * Pos(4.6, 0, 0)):
                Box(3.2, 0.30, GAP)
        # inner vane support ring
        with Locations(AXL):
            Cylinder(3.4, GAP)
    disc.part.label = "vented rotor disc"
    disc.part.color = IRON

    with BuildPart() as hat:
        with Locations(AXL * Pos(0, 0, -1.4)):
            Cylinder(3.0, 1.8)
        with Locations(AXL * Pos(0, 0, -1.4)):
            Cylinder(2.55, 2.0, mode=Mode.SUBTRACT)
        with Locations(AXL * Pos(0, 0, -0.6)):
            Cylinder(3.0, 0.4)
        # center bore
        with Locations(AXL * Pos(0, 0, -0.6)):
            Cylinder(1.35, 0.6, mode=Mode.SUBTRACT)
    hat.part.label = "rotor hat"
    hat.part.color = DARK

    with BuildPart() as studs:
        for i in range(5):
            with Locations(AXL * Rot(0, 0, i * 72) * Pos(2.75, 0, 0.85)):
                Cylinder(0.25, 1.7)
    studs.part.label = "wheel studs, 5 on 5.5"
    studs.part.color = STEEL

    asm = Compound(children=[disc.part, hat.part, studs.part])
    asm.label = "front brake rotor, vented"
    return asm
