# Battery — Group 65 top-post (Motorcraft), with steel tray and hold-down
# rod, RH fender apron. Case 9 x 6.8 x 7.5 tall to match the old builder's
# envelope (real group 65 is ~12x7.5x7.6; envelope kept until photo pass).
# 1 unit = 1 inch; +X fwd, +Z up, +Y left. Origin = record position [96, 33, 22];
# case is centered on the origin, tray hangs below.
from build123d import *

W = 9.0      # fore-aft (X)
D = 6.8      # left-right (Y)
H = 7.5      # vertical (Z)

CASE = Color(0.13, 0.13, 0.14)
LID = Color(0.18, 0.18, 0.19)
TRAY = Color(0.25, 0.26, 0.27)
LEAD = Color(0.55, 0.56, 0.58)
RED = Color(0.55, 0.10, 0.08)


def gen_step():
    with BuildPart() as case:
        Box(W, D, H - 0.7)
        # vertical side ribs
        for x in range(-3, 4):
            for s in (1, -1):
                with Locations((x * 1.2, s * D / 2, -0.6)):
                    Box(0.25, 0.12, H - 2.4)
        fillet(case.edges().filter_by(Axis.Z).group_by(SortBy.LENGTH)[-1], radius=0.3)
    case.part.label = "battery case, group 65"
    case.part.color = CASE

    with BuildPart() as lid:
        with Locations((0, 0, (H - 0.7) / 2)):
            Box(W * 0.98, D * 0.98, 0.7, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # two flush cell covers
        for x in (-2.0, 2.0):
            with Locations((x, 0, (H - 0.7) / 2 + 0.7)):
                Box(3.6, 4.6, 0.15, align=(Align.CENTER, Align.CENTER, Align.MIN))
    lid.part.label = "battery lid and cell covers"
    lid.part.color = LID

    top_z = (H - 0.7) / 2 + 0.7
    with BuildPart() as posts:
        # tapered lead posts, positive front-right
        for x in (W / 2 - 1.2, -(W / 2 - 1.2)):
            with Locations((x, -(D / 2 - 1.1), top_z)):
                Cone(0.42, 0.36, 0.75, align=(Align.CENTER, Align.CENTER, Align.MIN))
    posts.part.label = "battery posts"
    posts.part.color = LEAD

    with BuildPart() as tray:
        # stamped steel tray under the case
        with Locations((0, 0, -(H - 0.7) / 2)):
            Box(W + 0.9, D + 0.9, 0.45, align=(Align.CENTER, Align.CENTER, Align.MAX))
        # lip
        with Locations((0, 0, -(H - 0.7) / 2)):
            Box(W + 0.9, D + 0.9, 0.55, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, -(H - 0.7) / 2 + 0.01)):
            Box(W + 0.5, D + 0.5, 0.8, mode=Mode.SUBTRACT,
                align=(Align.CENTER, Align.CENTER, Align.MIN))
        # hold-down rod at the front-right corner
        with Locations((W / 2 + 0.25, D / 2 + 0.25, 0)):
            Cylinder(0.12, H + 0.4)
    tray.part.label = "battery tray and hold-down"
    tray.part.color = TRAY

    asm = Compound(children=[case.part, lid.part, posts.part, tray.part])
    asm.label = "battery, group 65 top-post with tray"
    return asm
