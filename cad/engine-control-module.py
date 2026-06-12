# EEC-IV engine control module (PCM) — aluminum case behind the driver kick
# panel, big 60-pin connector facing the firewall (the KB notes it swaps with
# one 10mm bolt + loosening the fender liner). Case thickness along X to fit
# the record envelope (2 x 6 x 5). 1 unit = 1 inch; +X fwd, +Z up, +Y left.
# Origin = record position [44, 33, -22].
from build123d import *

ALU = Color(0.62, 0.64, 0.66)
BLACK = Color(0.12, 0.12, 0.13)


def gen_step():
    with BuildPart() as case:
        # folded aluminum case
        Box(1.6, 4.9, 5.9)
        fillet(case.edges().filter_by(Axis.Y), radius=0.2)
        # lid ribs
        for z in (-1.8, 0, 1.8):
            with Locations((-0.85, 0, z)):
                Box(0.1, 4.4, 0.5)
        # mounting flanges top + bottom w/ bolt holes
        for s in (1, -1):
            with Locations((0.2, 0, s * 3.25)):
                Box(1.2, 4.9, 0.6)
            with Locations((0.2, 1.6, s * 3.25)):
                Cylinder(0.20, 0.7, mode=Mode.SUBTRACT)
    case.part.label = "EEC-IV case"
    case.part.color = ALU

    with BuildPart() as conn:
        # 60-pin connector block on the forward face (through the firewall)
        with Locations((1.15, 0, -0.3)):
            Box(0.75, 3.6, 1.35)
        fillet(conn.edges().filter_by(Axis.X), radius=0.25)
        # connector bolt boss in the middle
        with Locations(Pos(1.6, 0, -0.3) * Rot(0, 90, 0)):
            Cylinder(0.28, 0.4)
    conn.part.label = "60-pin EEC connector"
    conn.part.color = BLACK

    asm = Compound(children=[case.part, conn.part])
    asm.label = "EEC-IV engine control module"
    return asm
