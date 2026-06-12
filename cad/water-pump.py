# Water pump — 4.9L (300) I6. Cast volute on the block's front face, vertical
# lower-hose inlet under the volute (hose starts at world [96.5, 27, 0]),
# shaft hub + pulley whose face sits at world x=99.7 — the fan clutch hub
# bolts there (bolted pair whitelisted in check_geometry).
# 1 unit = 1 inch; +X fwd, +Z up, +Y left. Origin = record position [97, 30, 0].
from build123d import *

AX = Rot(0, 90, 0)   # built +Z (axis) -> +X (forward)

IRON = Color(0.38, 0.39, 0.40)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as body:
        # block-mounting plate
        with Locations(AX * Pos(0, 0, -1.6)):
            Box(4.6, 4.6, 0.6)
        # volute
        with Locations(AX * Pos(0, 0, -0.4)):
            Cylinder(2.5, 1.8)
        fillet(body.edges().filter_by(GeomType.CIRCLE).group_by(Axis.X)[-1], radius=0.5)
        # scroll bump toward the lower outlet
        with Locations(AX * Pos(-1.2, -1.2, -0.4)):
            Cylinder(1.6, 1.7)
        # vertical lower-hose inlet under the volute, offset to the passenger
        # side so the crank pulley rim clears it
        with Locations((-0.5, -1.2, -2.35)):
            Cylinder(1.05, 1.9)
        # heater hose nipple, upper left
        with Locations(Pos(0.2, 2.4, 1.4) * Rot(90, 0, 0)):
            Cylinder(0.34, 1.6)
        # bolt bosses on the plate
        for dy, dz in ((1.9, 1.9), (-1.9, 1.9), (1.9, -1.9), (-1.9, -1.9)):
            with Locations(AX * Pos(dy, dz, -1.75)):
                Cylinder(0.32, 0.35)
    body.part.label = "water pump casting"
    body.part.color = IRON

    with BuildPart() as drive:
        # shaft hub
        with Locations(AX * Pos(0, 0, 1.2)):
            Cylinder(0.95, 1.6)
        # pulley: face at local x=2.7 (world 99.7, fan clutch bolts here)
        with Locations(AX * Pos(0, 0, 2.35)):
            Cylinder(2.6, 0.35)
        with Locations(AX * Pos(0, 0, 2.0)):
            Cylinder(2.3, 0.35)
    drive.part.label = "pump hub and pulley"
    drive.part.color = STEEL

    asm = Compound(children=[body.part, drive.part])
    asm.label = "water pump, 4.9L"
    return asm
