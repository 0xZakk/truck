# Radiator — 1994 F-150 4.9L, downflow (top + bottom tanks), manual trans
# (no cooler lines). Port locations preserved from the old builder so the
# hose cables still land: upper inlet rear face, top right (y=-10, z=+10);
# lower outlet rear face, bottom left (y=+10, z=-9.5); filler neck top right.
# 1 unit = 1 inch; +X fwd, +Z up, +Y left. Origin = record position [101,26,0].
from build123d import *

CORE_W = 26.0     # left-right
CORE_H = 21.0     # vertical
CORE_T = 2.4      # fore-aft
TANK_W = 30.0
TANK_H = 3.0
TANK_T = 3.2
TANK_ZC = 12.0    # top tank center height (bottom tank at -12)

BLACK = Color(0.10, 0.10, 0.11)
CORE_DARK = Color(0.13, 0.12, 0.11)
STEEL = Color(0.62, 0.63, 0.65)
BRASS = Color(0.72, 0.60, 0.30)


def gen_step():
    with BuildPart() as core:
        Box(CORE_T, CORE_W, CORE_H)
        # shallow vertical fin grooves on both faces
        cuts = [(s * CORE_T / 2, y) for s in (1, -1) for y in range(-12, 13)]
        for x, y in cuts:
            with Locations((x, float(y), 0)):
                Box(0.12, 0.55, CORE_H - 1.0, mode=Mode.SUBTRACT)
        # steel side channels
        for s in (1, -1):
            with Locations((0, s * (CORE_W / 2 + 0.4), 0)):
                Box(CORE_T + 0.4, 0.8, CORE_H + 1.5)
    core.part.label = "radiator core and side channels"
    core.part.color = CORE_DARK

    with BuildPart() as tanks:
        for zc in (TANK_ZC, -TANK_ZC):
            with Locations((0, 0, zc)):
                Box(TANK_T, TANK_W, TANK_H)
        fillet(tanks.edges().filter_by(Axis.Y), radius=0.7)
        # upper hose inlet: rear face, top right
        with BuildSketch(Plane.YZ.offset(-TANK_T / 2 - 1.6)):
            with Locations((-10.0, 10.5)):
                Circle(1.0)
        extrude(amount=2.0)
        # lower hose outlet: rear face, bottom left
        with BuildSketch(Plane.YZ.offset(-TANK_T / 2 - 1.6)):
            with Locations((10.0, -9.5)):
                Circle(1.1)
        extrude(amount=2.0)
        # drain petcock under the bottom tank, left
        with Locations((0, 12.5, -TANK_ZC - TANK_H / 2 - 0.3)):
            Cylinder(0.30, 0.6)
    tanks.part.label = "top and bottom tanks with hose ports"
    tanks.part.color = BLACK

    with BuildPart() as filler:
        # brass filler neck on the top tank, right side
        with Locations((0, -11.0, TANK_ZC + TANK_H / 2)):
            Cylinder(0.85, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    filler.part.label = "filler neck"
    filler.part.color = BRASS

    with BuildPart() as cap:
        with Locations((0, -11.0, TANK_ZC + TANK_H / 2 + 1.0)):
            Cylinder(1.05, 0.45, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(cap.edges().group_by(Axis.Z)[-1], radius=0.10)
        # cap ears
        with Locations((0, -11.0, TANK_ZC + TANK_H / 2 + 1.30)):
            Box(2.5, 0.7, 0.25)
    cap.part.label = "radiator cap"
    cap.part.color = STEEL

    asm = Compound(children=[core.part, tanks.part, filler.part, cap.part])
    asm.label = "radiator - downflow, 4.9L manual"
    return asm
