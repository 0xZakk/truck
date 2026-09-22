# Engine mount — rubber-isolated mount between block boss and the No. 2
# crossmember (bolted pair already whitelisted). Stamped frame bracket,
# bonded rubber biscuit, block-side bracket w/ through-bolt.
# Shared by engine-mount-l/r. 1 unit = 1 inch. Origin = record position.
from build123d import *

RUBBER = Color(0.12, 0.12, 0.12)
DARK = Color(0.26, 0.27, 0.28)
STEEL = Color(0.55, 0.56, 0.57)


def gen_step():
    with BuildPart() as frame_brkt:
        # stamped channel on the crossmember
        with Locations((0, 0, -1.9)):
            Box(4.0, 3.4, 0.8)
        for s in (1, -1):
            with Locations((0, s * 1.5, -1.15)):
                Box(4.0, 0.4, 1.0)
    frame_brkt.part.label = "frame-side bracket"
    frame_brkt.part.color = DARK

    with BuildPart() as biscuit:
        # bonded rubber isolator with waist
        with Locations((0, 0, -0.2)):
            Cylinder(1.45, 1.9)
        with Locations((0, 0, -0.2)):
            Cylinder(1.62, 0.5)
    biscuit.part.label = "rubber isolator"
    biscuit.part.color = RUBBER

    with BuildPart() as block_brkt:
        # block-side bracket plate + through-bolt
        with Locations((0, 0, 1.0)):
            Box(3.4, 2.6, 0.6)
        with Locations((0, 0, 1.6)):
            Box(2.2, 2.0, 0.8)
        with Locations(Pos(0, 0, -0.2) * Rot(90, 0, 0)):
            Cylinder(0.22, 3.6)
    block_brkt.part.label = "block-side bracket + through-bolt"
    block_brkt.part.color = STEEL

    asm = Compound(children=[frame_brkt.part, biscuit.part, block_brkt.part])
    asm.label = "engine mount, rubber isolated"
    return asm
