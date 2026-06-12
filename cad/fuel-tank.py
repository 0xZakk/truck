# Fuel tank — 1994 F-150, midship steel tank between the rails ahead of the
# rear axle. Two stamped halves with a crimp seam flange around the middle,
# two mounting straps, sender/pump module on top, filler inlet on the right
# rear corner. 1 unit = 1 inch; +X fwd, +Z up, +Y left.
# Origin = record position [-30, 11, -8.5].
from build123d import *

L, W, H = 32.0, 12.0, 12.0

STEEL = Color(0.60, 0.61, 0.60)
DARK = Color(0.30, 0.31, 0.32)
RING = Color(0.45, 0.46, 0.47)


def gen_step():
    with BuildPart() as tank:
        Box(L, W, H)
        fillet(tank.edges(), radius=1.6)
        # crimp seam flange around the waist
        with BuildSketch(Plane.XY):
            RectangleRounded(L + 0.8, W + 0.8, radius=1.8)
            RectangleRounded(L - 2.0, W - 2.0, radius=1.4, mode=Mode.SUBTRACT)
        extrude(amount=0.35, both=True)
    tank.part.label = "fuel tank, stamped halves w/ seam"
    tank.part.color = STEEL

    with BuildPart() as straps:
        for x in (-9.0, 9.0):
            # band under the tank + tabs up both sides to the frame
            with Locations((x, 0, -H / 2 - 0.14)):
                Box(1.4, W + 0.6, 0.22)
            for s in (1, -1):
                with Locations((x, s * (W / 2 + 0.24), -H / 2 + 1.8)):
                    Box(1.4, 0.22, 5.5)
    straps.part.label = "tank mounting straps"
    straps.part.color = DARK

    with BuildPart() as topgear:
        # sender / pump module lock ring + fittings (feed/return lines run
        # along the left rail: world z ~ -14..-19)
        with Locations((6.0, 4.6, H / 2)):
            Cylinder(2.2, 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((6.0, 4.6, H / 2 + 0.5)):
            Cylinder(1.5, 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
        for dx, dy in ((-0.8, 0.5), (0.8, 0.5)):
            with Locations((6.0 + dx, 4.6 + dy, H / 2 + 0.8)):
                Cylinder(0.28, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # filler inlet toward the right rear (filler neck path starts at
        # local (16, -2.5, +3))
        with Locations(Pos(15.0, -2.5, 3.6) * Rot(0, 55, 0)):
            Cylinder(1.45, 2.8)
    topgear.part.label = "sender module and filler inlet"
    topgear.part.color = RING

    asm = Compound(children=[tank.part, straps.part, topgear.part])
    asm.label = "fuel tank, midship"
    return asm
