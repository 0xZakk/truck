# Exhaust manifold — 4.9L (300) I6 EFI: the front/rear split-log pair under
# the intake, six ports off the head flange feeding two logs that merge into
# the downward collector at the rear (headpipe picks up at world [87, 28, 8.5]).
# Head is to the LEFT of this part: build +Y. 1 unit = 1 inch.
# Origin = record position [79, 31.5, 8.5].
from build123d import *

L = 26.0
IRON = Color(0.30, 0.29, 0.28)


def gen_step():
    with BuildPart() as man:
        # head flange strip
        with Locations((0, 2.3, 0.3)):
            Box(L, 0.45, 2.9)
        # six port elbows
        for i in range(6):
            x = -12.5 + i * 5
            with Locations(Pos(x, 1.2, 0.3) * Rot(90, 0, 0)):
                Cylinder(1.05, 2.2)
        # two log runners (front and rear castings)
        for xc in (-6.5, 6.5):
            with Locations(Pos(xc, 0.2, 0.1) * Rot(0, 90, 0)):
                Cylinder(1.35, 12.0)
        # crossover joining the logs
        with Locations(Pos(0, 0.2, 0.1) * Rot(0, 90, 0)):
            Cylinder(1.1, 4.0)
        # collector turning down to the headpipe at local (+8, -3.5)
        with Locations(Pos(8.0, 0.2, -1.6)):
            Cylinder(1.30, 3.6)
        # collector flange (3-bolt donut)
        with Locations(Pos(8.0, 0.2, -3.3)):
            Cylinder(1.75, 0.4)
    man.part.label = "exhaust manifold, 4.9L split-log pair"
    man.part.color = IRON
    return man.part
