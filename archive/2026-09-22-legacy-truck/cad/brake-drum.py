# Rear brake drum + backing plate — drum shell w/ stiffening ribs, closed
# outboard face w/ hub + 5 studs, backing plate behind. Spin axis lateral;
# closed face toward viewer -z like the old builder.
# 1 unit = 1 inch. Origin = record position.
from build123d import *

AXL = Rot(90, 0, 0)

R = 5.4
W = 4.0
IRON = Color(0.32, 0.33, 0.34)
DARK = Color(0.26, 0.27, 0.28)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as drum:
        # shell (open toward the backing plate)
        with Locations(AXL):
            Cylinder(R, W)
        with Locations(AXL * Pos(0, 0, 0.45)):
            Cylinder(R - 0.45, W - 0.45, mode=Mode.SUBTRACT)
        # stiffening ribs
        for z in (-0.4, 0.9):
            with Locations(AXL * Pos(0, 0, z)):
                Cylinder(R + 0.18, 0.35)
        # hub boss on the closed face
        with Locations(AXL * Pos(0, 0, -2.3)):
            Cylinder(2.0, 0.7)
        with Locations(AXL * Pos(0, 0, -2.3)):
            Cylinder(1.25, 0.9, mode=Mode.SUBTRACT)
    drum.part.label = "brake drum"
    drum.part.color = IRON

    with BuildPart() as studs:
        for i in range(5):
            with Locations(AXL * Rot(0, 0, i * 72) * Pos(2.75, 0, -2.4)):
                Cylinder(0.25, 1.2)
    studs.part.label = "wheel studs"
    studs.part.color = STEEL

    with BuildPart() as plate:
        # backing plate at the open (inboard) side
        with Locations(AXL * Pos(0, 0, 1.85)):
            Cylinder(R + 0.25, 0.30)
    plate.part.label = "backing plate"
    plate.part.color = DARK

    asm = Compound(children=[drum.part, studs.part, plate.part])
    asm.label = "rear brake drum w/ backing plate"
    return asm
