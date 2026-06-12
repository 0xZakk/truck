# Harmonic balancer + crank pulley — 4.9L (300) I6. Inertia ring on the
# rubber-bonded hub, bolted two-groove V-belt pulley, center crank bolt.
# Axis along +X; rotations baked per child (cadpy drops parent locations).
# 1 unit = 1 inch. Origin = record position [95.6, 23, 0].
from build123d import *

AX = Rot(0, 90, 0)

DARK = Color(0.20, 0.20, 0.21)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as damper:
        # inertia ring
        with Locations(AX * Pos(0, 0, -0.6)):
            Cylinder(3.25, 1.5)
        fillet(damper.edges().filter_by(GeomType.CIRCLE), radius=0.15)
        # hub face
        with Locations(AX * Pos(0, 0, 0.35)):
            Cylinder(1.6, 0.5)
    damper.part.label = "harmonic balancer (damper ring + hub)"
    damper.part.color = DARK

    with BuildPart() as pulley:
        # two-groove V-belt pulley: three flanges with groove spacers
        for z, r in ((0.65, 3.5), (1.10, 3.5), (1.55, 3.5)):
            with Locations(AX * Pos(0, 0, z)):
                Cylinder(r, 0.18)
        for z in (0.875, 1.325):
            with Locations(AX * Pos(0, 0, z)):
                Cylinder(2.9, 0.30)
        # pulley center web
        with Locations(AX * Pos(0, 0, 0.70)):
            Cylinder(1.9, 0.25)
        # four pulley bolts into the balancer hub
        for i in range(4):
            loc = AX * Rot(0, 0, i * 90 + 45) * Pos(1.15, 0, 0.85)
            with Locations(loc):
                Cylinder(0.16, 0.3)
    pulley.part.label = "crank V-belt pulley, two groove"
    pulley.part.color = STEEL

    with BuildPart() as bolt:
        # crank bolt + washer on the pulley's front face
        with Locations(AX * Pos(0, 0, 1.73)):
            Cylinder(0.55, 0.18)
        with Locations(AX * Pos(0, 0, 2.02)):
            Cylinder(0.34, 0.40)
    bolt.part.label = "crank bolt"
    bolt.part.color = STEEL

    asm = Compound(children=[damper.part, pulley.part, bolt.part])
    asm.label = "harmonic balancer + crank pulley"
    return asm
