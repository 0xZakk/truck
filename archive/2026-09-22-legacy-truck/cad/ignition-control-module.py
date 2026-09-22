# Ignition control module (TFI-IV, remote mount) — on 1994 trucks the TFI
# module lives on a finned aluminum heat sink on the radiator core support
# (driver side), not on the distributor. Gray module w/ molded connector,
# heat-sink plate w/ vertical fins behind it. 1 unit = 1 inch; +X fwd,
# +Z up, +Y left. Origin = record position [102.3, 38, -18].
from build123d import *

ALU = Color(0.60, 0.62, 0.64)
GREY = Color(0.45, 0.46, 0.48)
BLACK = Color(0.12, 0.12, 0.13)


def gen_step():
    with BuildPart() as sink:
        # heat-sink plate against the core support, fins facing rearward
        with Locations((0.25, 0, 0)):
            Box(0.25, 2.4, 3.4)
        for y in (-0.9, -0.3, 0.3, 0.9):
            with Locations((-0.15, y, 0)):
                Box(0.55, 0.18, 3.0)
    sink.part.label = "TFI heat sink"
    sink.part.color = ALU

    with BuildPart() as module:
        # TFI module body on the plate, rearward face
        with Locations((-0.62, 0, 0.2)):
            Box(0.55, 1.4, 2.6)
        fillet(module.edges().filter_by(Axis.X), radius=0.15)
        # mounting screws
        for z in (1.35, -1.15):
            with Locations(Pos(-0.95, 0, z) * Rot(0, 90, 0)):
                Cylinder(0.10, 0.25)
    module.part.label = "TFI-IV module"
    module.part.color = GREY

    with BuildPart() as conn:
        # molded harness connector exiting the bottom
        with Locations((-0.62, 0, -1.45)):
            Box(0.5, 0.9, 0.5)
    conn.part.label = "harness connector"
    conn.part.color = BLACK

    asm = Compound(children=[sink.part, module.part, conn.part])
    asm.label = "ignition control module (TFI), remote on core support"
    return asm
