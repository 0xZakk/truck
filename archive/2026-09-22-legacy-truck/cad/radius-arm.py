# Radius arm — Twin I-Beam forged arm: forked front end clamping the beam,
# tapered shaft running rearward, threaded rear end through the frame
# bushing bracket (washers + nut). Runs fore-aft: +X is the beam (front)
# end. Shared by radius-arm-l/r. 1 unit = 1 inch. Origin = record position
# (old AABB 30 x 2 x 6.5 -> x spans -15..+15).
from build123d import *

CAST = Color(0.32, 0.33, 0.34)
DARK = Color(0.24, 0.25, 0.26)


def gen_step():
    with BuildPart() as arm:
        # tapered main shaft: deep channel at the front, slimming rearward
        with BuildSketch(Plane.YZ.offset(-9.0)):
            RectangleRounded(1.5, 2.0, radius=0.4)
        with BuildSketch(Plane.YZ.offset(15.0)):
            RectangleRounded(1.9, 3.2, radius=0.5)
        loft()
        # forked front end: two ears that clamp the I-beam
        for s in (1, -1):
            with Locations((14.2, s * 1.05, -0.2)):
                Box(2.6, 0.5, 3.0)
        # beam clamp bolt
        with Locations(Pos(14.6, 0, 0.6) * Rot(90, 0, 0)):
            Cylinder(0.22, 3.0)
        # threaded rear rod into the frame bracket
        with Locations(Pos(-12.0, 0, 0) * Rot(0, 90, 0)):
            Cylinder(0.55, 6.0)
    arm.part.label = "radius arm, forged"
    arm.part.color = CAST

    with BuildPart() as bush:
        # bushing washers + nut at the rear end
        for x, r, t in ((-13.6, 1.3, 0.5), (-14.5, 1.3, 0.5)):
            with Locations(Pos(x, 0, 0) * Rot(0, 90, 0)):
                Cylinder(r, t)
        with Locations(Pos(-15.0, 0, 0) * Rot(0, 90, 0)):
            Cylinder(0.5, 0.45)
    bush.part.label = "rear bushings and nut"
    bush.part.color = DARK

    asm = Compound(children=[arm.part, bush.part])
    asm.label = "radius arm"
    return asm
