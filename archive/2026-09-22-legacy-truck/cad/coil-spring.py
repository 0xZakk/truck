# Front coil spring — Twin-I-Beam front suspension. True swept helix,
# 6 active turns, ~0.7" wire, vertical axis. Used by front-coil-l and
# front-coil-r records. 1 unit = 1 inch. Origin = record position.
from build123d import *

TURNS = 6
HEIGHT = 11.0
RADIUS = 2.3
WIRE_R = 0.34

STEEL = Color(0.30, 0.31, 0.33)


def gen_step():
    helix = Helix(pitch=HEIGHT / TURNS, height=HEIGHT, radius=RADIUS,
                  center=(0, 0, -HEIGHT / 2))
    with BuildPart() as sp:
        with BuildLine():
            add(helix)
        with BuildSketch(Plane(origin=helix @ 0, z_dir=helix % 0)):
            Circle(WIRE_R)
        sweep()
    sp.part.label = "front coil spring, 6 turns"
    sp.part.color = STEEL
    return sp.part
