# Valve (rocker) cover — 4.9L (300) I6, 1994 F-150. Ford F3TZ-6582-H.
# Stamped-steel shell: perimeter bolt flange, tapered lofted body, oil filler
# cap up front, PCV grommet at the rear. 1 unit = 1 inch; +X fwd, +Z up, +Y left.
# Part-local origin matches the old builder: flange underside at z = -1.5
# (record position y=40.5 -> flange sits on the head at world y=39).
from build123d import *

L = 29.0          # flange length (head is 30")
W = 7.0           # flange width
FLANGE_T = 0.10   # stamped flange thickness
H = 4.0           # shell height above flange underside
Z0 = -1.5         # flange underside, part-local
TOP = Z0 + H

BOLT_D = 0.28     # 1/4" cover bolts, clearance
CAP_X = 8.5       # oil filler toward the front (+X)
PCV_X = -9.0      # PCV grommet toward the rear

BLACK = Color(0.10, 0.10, 0.11)
CAP_BLACK = Color(0.04, 0.04, 0.045)
RUBBER = Color(0.16, 0.16, 0.17)


def gen_step():
    with BuildPart() as cover:
        # perimeter mounting flange
        with BuildSketch(Plane.XY.offset(Z0)):
            RectangleRounded(L, W, radius=0.9)
        extrude(amount=FLANGE_T)
        # tapered stamped body, lofted from flange inset to crowned top
        with BuildSketch(Plane.XY.offset(Z0 + FLANGE_T)):
            RectangleRounded(L - 0.9, W - 1.0, radius=0.8)
        with BuildSketch(Plane.XY.offset(TOP)):
            RectangleRounded(L - 4.0, W - 3.2, radius=1.2)
        loft()
        fillet(cover.edges().group_by(Axis.Z)[-1], radius=0.45)
        # oil filler neck
        with BuildSketch(Plane.XY.offset(TOP - 0.2)):
            with Locations((CAP_X, 0)):
                Circle(0.80)
        extrude(amount=0.55)
        # flange bolt holes: 4 per long side + 1 each end
        hole_pts = [(x, s * (W / 2 - 0.28)) for s in (1, -1) for x in (-10.5, -3.5, 3.5, 10.5)]
        hole_pts += [(s * (L / 2 - 0.30), 0) for s in (1, -1)]
        with BuildSketch(Plane.XY.offset(Z0 + FLANGE_T)):
            with Locations(*hole_pts):
                Circle(BOLT_D / 2)
        extrude(amount=-FLANGE_T, mode=Mode.SUBTRACT)
    cover.part.label = "valve cover shell, stamped steel, black"
    cover.part.color = BLACK

    with BuildPart() as cap:
        # twist-on oil filler cap with grip flats around the rim
        with Locations((CAP_X, 0, TOP + 0.625)):
            Cylinder(1.05, 0.55)
        fillet(cap.edges().group_by(Axis.Z)[-1], radius=0.12)
        with Locations((CAP_X, 0, TOP + 0.625)):
            with PolarLocations(1.08, 8):
                Box(0.30, 0.16, 0.55, mode=Mode.SUBTRACT)
    cap.part.label = "oil filler cap"
    cap.part.color = CAP_BLACK

    with BuildPart() as pcv:
        # PCV valve grommet at the rear of the cover
        with Locations((PCV_X, 0, TOP - 0.05)):
            Cylinder(0.62, 0.45, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((PCV_X, 0, TOP + 0.40)):
            Cylinder(0.40, 0.55, align=(Align.CENTER, Align.CENTER, Align.MIN))
    pcv.part.label = "PCV grommet and valve stub"
    pcv.part.color = RUBBER

    asm = Compound(children=[cover.part, cap.part, pcv.part])
    asm.label = "valve cover - 4.9L 300 I6 (F3TZ-6582-H)"
    return asm
