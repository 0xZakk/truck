# Inline fuel filter — 1994 F-150 4.9L EFI, frame-rail mounted steel
# canister with hairpin-clip quick connects on both ends.
# Axis along +X. 1 unit = 1 inch. Origin = record position [22, 12, -14].
from build123d import *

AX = Rot(0, 90, 0)
STEEL = Color(0.65, 0.66, 0.67)


def gen_step():
    with BuildPart() as f:
        with Locations(AX):
            Cylinder(1.0, 3.8)
        fillet(f.edges().filter_by(GeomType.CIRCLE), radius=0.3)
        # necked ends + tube stubs
        for s in (1, -1):
            with Locations(AX * Pos(0, 0, s * 2.1)):
                Cone(0.75 if s > 0 else 0.35, 0.35 if s > 0 else 0.75, 0.5)
            with Locations(AX * Pos(0, 0, s * 2.85)):
                Cylinder(0.30, 1.0)
            # quick-connect collar
            with Locations(AX * Pos(0, 0, s * 3.05)):
                Cylinder(0.45, 0.3)
    f.part.label = "inline fuel filter, quick-connect"
    f.part.color = STEEL
    return f.part
