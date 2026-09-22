# Distributor — 4.9L EFI (EEC-IV / TFI-IV): vertical shaft at the front of
# the engine, black cap with 6 plug towers + center coil tower, TFI ignition
# module on the base flank, hold-down clamp. No vacuum advance on EFI.
# 1 unit = 1 inch; +X fwd, +Z up, +Y left. Origin = record position [95, 33, 4].
# Old envelope: body r2 h4 vertical, cap to +3.8, towers to +4.6.
from build123d import *

IRON = Color(0.40, 0.41, 0.42)
CAP = Color(0.13, 0.13, 0.14)
GREY = Color(0.45, 0.46, 0.47)


def gen_step():
    with BuildPart() as body:
        # housing
        Cylinder(1.05, 4.4)
        # base / clamp flange
        with Locations((0, 0, -2.0)):
            Cylinder(1.6, 0.4)
        # hold-down clamp ear
        with Locations((-1.9, 0, -2.0)):
            Box(1.4, 0.9, 0.35)
        # TFI module on the flank
        with Locations((0.0, -1.35, -0.6)):
            Box(1.0, 0.6, 2.4)
    body.part.label = "distributor housing w/ TFI module"
    body.part.color = IRON

    with BuildPart() as cap:
        # cap base
        with Locations((0, 0, 2.2)):
            Cylinder(1.55, 1.3, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(cap.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[-1], radius=0.25)
        # six plug towers
        with PolarLocations(1.05, 6):
            with Locations((0, 0, 3.5)):
                Cylinder(0.34, 0.9, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # center coil tower
        with Locations((0, 0, 3.5)):
            Cylinder(0.38, 1.05, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cap.part.label = "distributor cap, 6 towers"
    cap.part.color = CAP

    asm = Compound(children=[body.part, cap.part])
    asm.label = "distributor, EEC-IV TFI"
    return asm
