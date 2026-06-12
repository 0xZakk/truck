# Thermostat housing (water outlet) — 4.9L (300) I6. Cast elbow on the front
# of the head: oval 2-bolt base, dome, gooseneck angled up-forward to the
# upper radiator hose (hose path starts at world [94, 38.5, 1]).
# 1 unit = 1 inch; +X fwd, +Z up, +Y left. Origin = record position [94, 38.5, 1].
from build123d import *

IRON = Color(0.40, 0.41, 0.42)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as h:
        # oval base flange (bolts fore-aft on the head's outlet pad)
        with BuildSketch(Plane.XY.offset(-1.0)):
            SlotOverall(4.2, 2.4, rotation=0)
        extrude(amount=0.4)
        # dome over the thermostat
        with Locations((0, 0, -0.6)):
            Cylinder(1.35, 1.4, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(h.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[-1], radius=0.4)
        # gooseneck: angled up-forward toward the radiator
        with Locations(Pos(0.4, 0, 0.7) * Rot(0, 55, 0)):
            Cylinder(0.95, 2.6)
        # hose bead at the outlet end
        with Locations(Pos(1.45, 0, 1.45) * Rot(0, 55, 0)):
            Cylinder(1.03, 0.25)
        # flange bolts
        for s in (1, -1):
            with Locations((s * 1.55, 0, -0.55)):
                Cylinder(0.18, 0.3)
    h.part.label = "thermostat housing / water outlet"
    h.part.color = IRON
    return h.part
