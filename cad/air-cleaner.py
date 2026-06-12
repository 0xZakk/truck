# Air cleaner assembly — 1994 F-150 4.9L EFI. Remote canister on the RH
# fender apron: vertical drum, domed lid w/ wing nut, snorkel facing the
# grille, elbow duct toward the throttle body. NOTE: geometry to be verified
# against owner photos (record carries the VERIFY note).
# 1 unit = 1 inch; +X fwd, +Z up, +Y left (here +Y points at the engine,
# since the part sits on the RIGHT fender). Origin = record position.
from build123d import *

R = 5.0          # drum radius
DRUM_H = 5.0     # drum height
Z_BOT = -3.0     # drum bottom, part-local
Z_TOP = Z_BOT + DRUM_H
SNORK_R = 1.5    # inlet snorkel (forward)
DUCT_R = 1.75    # outlet duct (toward engine)

BLACK = Color(0.10, 0.10, 0.11)
STEEL = Color(0.62, 0.63, 0.65)


def gen_step():
    with BuildPart() as body:
        # drum
        Cylinder(R, DRUM_H, align=(Align.CENTER, Align.CENTER, Align.MIN),
                 rotation=(0, 0, 0))
        # base pan lip
        with Locations((0, 0, 0.25)):
            Cylinder(R + 0.25, 0.5)
        # snorkel: forward inlet off the drum wall (kept short of the
        # fender-mounted starter relay at x=+9)
        with BuildSketch(Plane.YZ.offset(0)):
            with Locations((0, 1.8)):
                Circle(SNORK_R)
        extrude(amount=R + 1.5)
        # outlet duct: elbow stub toward the engine (+Y)
        with BuildSketch(Plane.XZ.offset(0)):
            with Locations((0, 2.6)):
                Circle(DUCT_R)
        extrude(amount=-(R + 3.5))
        fillet(body.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[0],
               radius=0.3)
    # shift so drum bottom sits at Z_BOT
    shell = body.part.moved(Location((0, 0, Z_BOT)))
    shell.label = "air cleaner housing, molded, black"
    shell.color = BLACK

    with BuildPart() as lid:
        # domed lid with rolled rim
        with Locations((0, 0, Z_TOP)):
            Cylinder(R + 0.30, 0.45, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, Z_TOP + 0.45)):
            Cylinder(R - 1.2, 0.55, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(lid.edges().group_by(Axis.Z)[-1], radius=0.4)
    lid.part.label = "air cleaner lid"
    lid.part.color = BLACK

    with BuildPart() as nut:
        # center stud + wing nut
        with Locations((0, 0, Z_TOP + 1.0)):
            Cylinder(0.16, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, Z_TOP + 1.25)):
            Box(1.6, 0.32, 0.38)
            Cylinder(0.30, 0.38)
    nut.part.label = "lid wing nut"
    nut.part.color = STEEL

    asm = Compound(children=[shell, lid.part, nut.part])
    asm.label = "air cleaner assembly - 4.9L EFI remote canister"
    return asm
