# Horn — disc-type behind the grille, spiral trumpet face, mounting bracket.
# Axis along +X (faces forward). 1 unit = 1 inch.
# Origin = record position [92, 42, -16].
from build123d import *

AX = Rot(0, 90, 0)
BLACK = Color(0.12, 0.12, 0.13)
DARK = Color(0.30, 0.31, 0.32)


def gen_step():
    with BuildPart() as body:
        # back can
        with Locations(AX * Pos(0, 0, -0.4)):
            Cylinder(2.1, 1.4)
        fillet(body.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[0], radius=0.5)
        # front face with spiral ridge rings
        with Locations(AX * Pos(0, 0, 0.55)):
            Cylinder(2.3, 0.5)
        for r in (0.6, 1.2, 1.8):
            with Locations(AX * Pos(0, 0, 0.92)):
                Cylinder(r + 0.12, 0.22)
            with Locations(AX * Pos(0, 0, 0.90)):
                Cylinder(r, 0.3, mode=Mode.SUBTRACT)
        # spade terminal
        with Locations((-1.3, 0, -1.0)):
            Box(0.5, 0.3, 0.8)
    body.part.label = "horn, disc type"
    body.part.color = BLACK

    with BuildPart() as bracket:
        with Locations((-0.6, 0, -2.3)):
            Box(1.6, 0.8, 1.6)
    bracket.part.label = "horn bracket"
    bracket.part.color = DARK

    asm = Compound(children=[body.part, bracket.part])
    asm.label = "horn"
    return asm
