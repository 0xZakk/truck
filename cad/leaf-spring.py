# Rear leaf spring — 5-leaf cambered pack, rolled eyes on the main leaf,
# center clamp, rebound clips. Leaves are true arcs (extruded arched strips).
# Runs fore-aft (build X), 2.4" wide. Shared by leaf-spring-l/r.
# 1 unit = 1 inch. Origin = record position.
from build123d import *
import math

N = 5
MAIN_L = 48.0
STEP = 7.0      # each leaf shorter by this
T = 0.45        # leaf thickness
W = 2.4         # leaf width
SAG = 1.8       # main-leaf camber (eyes above center)

DARK = Color(0.22, 0.23, 0.24)
STEEL = Color(0.50, 0.51, 0.52)


def arc_r(chord, sag):
    return (chord * chord / 4 + sag * sag) / (2 * sag)


def gen_step():
    with BuildPart() as pack:
        for i in range(N):
            L = MAIN_L - i * STEP
            # same curvature family as the main leaf
            s = SAG * (L / MAIN_L) ** 2
            r = arc_r(L, s)
            z0 = -i * (T + 0.02)
            with BuildSketch(Plane.XZ):
                with BuildLine():
                    RadiusArc((-L / 2, z0 + s), (L / 2, z0 + s), -r)
                    Line((L / 2, z0 + s), (L / 2, z0 + s - T))
                    RadiusArc((L / 2, z0 + s - T), (-L / 2, z0 + s - T), r)
                    Line((-L / 2, z0 + s - T), (-L / 2, z0 + s))
                make_face()
            extrude(amount=W / 2, both=True)
        # rolled eyes on the main leaf ends
        for sx in (1, -1):
            with Locations(Pos(sx * (MAIN_L / 2 - 0.2), 0, SAG + 0.55) * Rot(90, 0, 0)):
                Cylinder(0.85, W)
            with Locations(Pos(sx * (MAIN_L / 2 - 0.2), 0, SAG + 0.55) * Rot(90, 0, 0)):
                Cylinder(0.45, W + 0.4, mode=Mode.SUBTRACT)
    pack.part.label = "leaf pack, 5 leaves w/ rolled eyes"
    pack.part.color = DARK

    with BuildPart() as hw:
        # center bolt clamp
        with Locations((0, 0, -1.0)):
            Box(1.5, W + 0.5, 3.2)
        # rebound clips
        for x in (-13.0, 13.0):
            with Locations((x, 0, -0.85)):
                Box(1.0, W + 0.4, 2.6)
            with Locations((x, 0, -0.85)):
                Box(1.2, W + 0.1, 2.2, mode=Mode.SUBTRACT)
    hw.part.label = "center clamp and rebound clips"
    hw.part.color = STEEL

    asm = Compound(children=[pack.part, hw.part])
    asm.label = "rear leaf spring, 5-leaf"
    return asm
