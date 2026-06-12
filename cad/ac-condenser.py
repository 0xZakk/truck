# A/C condenser — 1994 F-150. Slim parallel-flow core ahead of the radiator,
# tucked between the radiator core front (world x=102.6) and the grille's
# rear face (103.05): slab spans world x 102.75..103.45 at the headers.
# Sized to clear the radiator tank bands (y<=36.4, y>=16.0).
# 1 unit = 1 inch; +X fwd, +Z up, +Y left. Origin = record position [103.2, 27, 0].
from build123d import *

CORE_W = 24.0     # left-right
CORE_H = 19.6     # vertical
CORE_T = 0.40
HDR_R = 0.30      # side header tubes
ZC = -1.2         # core center sits at world y=25.8 (band 16.0..35.6)

ALU = Color(0.55, 0.57, 0.58)


def gen_step():
    with BuildPart() as cond:
        Box(CORE_T, CORE_W, CORE_H)
        # vertical fin grooves, front face only (rear hides against the radiator)
        for y in range(-11, 12):
            with Locations((CORE_T / 2, float(y), 0)):
                Box(0.10, 0.5, CORE_H - 0.8, mode=Mode.SUBTRACT)
        # side header tubes
        for s in (1, -1):
            with Locations((0, s * (CORE_W / 2 + HDR_R - 0.1), 0)):
                Cylinder(HDR_R, CORE_H + 0.8)
        # (refrigerant line stubs omitted: invisible behind the grille and
        # they'd collide with the radiator core or grille bars)
    part = cond.part.moved(Location((0, 0, ZC)))
    part.label = "A/C condenser, parallel-flow"
    part.color = ALU
    return part
