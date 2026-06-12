# Starter relay (fender-mounted solenoid) — the classic Ford can on the RH
# apron: phenolic body, steel mounting foot below, two big copper studs
# pointing UP w/ brass nuts + small S-terminal spade (cables land at world
# y=42). 1 unit = 1 inch; +X fwd, +Z up, +Y left.
# Origin = record position [89, 40.5, 24].
from build123d import *

BLACK = Color(0.13, 0.13, 0.14)
STEEL = Color(0.58, 0.59, 0.60)
COPPER = Color(0.72, 0.45, 0.30)
BRASS = Color(0.72, 0.60, 0.30)


def gen_step():
    with BuildPart() as body:
        Box(2.4, 2.4, 1.8)
        fillet(body.edges().filter_by(Axis.Z), radius=0.55)
    body.part.label = "relay body, phenolic"
    body.part.color = BLACK

    with BuildPart() as foot:
        with Locations((0, 0, -1.0)):
            Box(2.4, 2.6, 0.4)
        for s in (1, -1):
            with Locations((0, s * 1.45, -1.0)):
                Box(0.6, 0.6, 0.5, mode=Mode.SUBTRACT)
    foot.part.label = "mounting foot"
    foot.part.color = STEEL

    with BuildPart() as studs:
        for y in (-0.7, 0.7):
            with Locations((0, y, 1.35)):
                Cylinder(0.20, 0.9)
            with Locations((0, y, 1.55)):
                Cylinder(0.34, 0.22)
        # small S terminal spade between the studs
        with Locations((0.65, 0, 1.15)):
            Box(0.30, 0.25, 0.45)
    studs.part.label = "battery/starter studs + S terminal"
    studs.part.color = COPPER

    asm = Compound(children=[body.part, foot.part, studs.part])
    asm.label = "starter relay, fender mounted"
    return asm
