# Intake manifold — 4.9L (300) I6 EFI. Log-style plenum with six angled
# runners down to the head flange (head is to the LEFT of this part: build +Y),
# throttle body on a front riser with its bore facing the fender-mounted air
# cleaner (build -Y / viewer +Z). Injector bosses along the runner roots.
# 1 unit = 1 inch. Origin = record position [79, 36, 8.5].
from build123d import *

L = 26.0
ALU = Color(0.55, 0.56, 0.55)
CAST = Color(0.42, 0.43, 0.44)


def gen_step():
    with BuildPart() as man:
        # plenum log
        with Locations((0, -0.9, 0.4)):
            Box(L, 3.4, 3.6)
        fillet(man.edges().filter_by(Axis.X), radius=0.9)
        # head flange
        with Locations((0, 2.45, -0.4)):
            Box(L, 0.5, 3.4)
        # six runners: plenum down/over to the flange
        for i in range(6):
            x = -12.5 + i * 5
            loc = Pos(x, 0.8, -0.1) * Rot(35, 0, 0)
            with Locations(loc):
                Box(2.7, 1.9, 3.4)
        # throttle body riser + bore toward the air cleaner
        with Locations((6.0, -0.9, 2.4)):
            Box(3.4, 3.0, 1.2)
        with Locations(Pos(6.0, -1.2, 2.9) * Rot(90, 0, 0)):
            Cylinder(1.55, 2.6)
        # injector bosses along the runner roots
        for i in range(6):
            x = -12.5 + i * 5
            with Locations(Pos(x, 1.4, 1.6) * Rot(-40, 0, 0)):
                Cylinder(0.42, 1.4)
    man.part.label = "intake manifold, 4.9L EFI log w/ throttle body"
    man.part.color = ALU
    return man.part
