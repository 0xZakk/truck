"""Isolated rear entry correction; collector and EGR reconstruction remain open."""
import build123d as cad
import exhaust_front_profile as front
import egr_tube

PORTS = (-31.896, -145.688, -259.48)
FITTING_INSERTION_LENGTH = 12.5
SOURCES = ['dorman-674186-profile-specification', 'dorman-674186-head-facing-photo',
           'dorman-674186-opposite-photo', 'dorman-674186-overview-photo',
           'dorman-674186-catalog-application']
GAPS = [
    'Manufacturer674-186 photos and catalog application support three rounded-rectangular rear entries, not their dimensions or installed casting identity.',
    'Entry28x28mm, corner3mm, outer36x36mm and transition stations reuse provisional front study dimensions; no pixel scaling is used.',
    'This incremental entry correction retains the old collector and EGR end connection. Both remain unsupported form/routing studies pending joint reconstruction; this is not a completed rear manifold.',
    'The provisional EGR fitting insertion envelope is shortened from19mm to12.5mm so its tip ends0.5mm before the collector inner wall rather than intruding into the collector and rear runner. This is a geometric clearance assumption, not a verified thread engagement or retention specification.',
    'Production flange lands, head attachment, outlet flange, auxiliary ports, wall thickness and thermal/flow performance remain unverified.'
]


def rear_casting():
    shape = cad.Pos(PORTS[1], -180, 230) * cad.extrude(cad.RectangleRounded(280, 48, 12), amount=24, both=True)
    for horizontal in PORTS:
        path = front.runner_path(0).trim(.27, 1)
        sweep = cad.sweep(cad.Plane(origin=path @ 0, x_dir=(1, 0, 0), z_dir=path % 0) * cad.Circle(18), path=path)
        outer = front.transition(0, outside=True).fuse(sweep)
        outer &= cad.Pos(0, -183, front.PORT_Z) * cad.Box(80, 100, 100)
        shape += cad.Pos(horizontal, 0, 0) * outer
    shape += cad.Pos(PORTS[1], -180, 175) * cad.Cylinder(27, 70)
    cavity = cad.Pos(PORTS[1], -180, 230) * cad.extrude(cad.RectangleRounded(268, 36, 8), amount=18, both=True)
    cavity += cad.Pos(PORTS[1], -180, 175) * cad.Cylinder(20, 86)
    for horizontal in PORTS:
        cavity += front.runner_void(horizontal)
    return egr_tube.manifold_interface(shape - cavity)


def rear_interface(previous_shape):
    """Rebuild consistently rather than overlapping imported and analytic runners."""
    return rear_casting()


def fitting_interface(previous_shape):
    return egr_tube.manifold_fitting(insertion_length=FITTING_INSERTION_LENGTH)


def head_interface(shape):
    world = cad.Pos(0, 0, front.HEAD_ORIGIN_Z) * shape
    for horizontal in PORTS:
        world += cad.extrude(front.section(horizontal, -115, 36, 6), amount=18)
        world -= front.head_void(horizontal)
    return cad.Pos(0, 0, -front.HEAD_ORIGIN_Z) * world


ADAPTERS = {'exhaust-rear': rear_interface, 'cylinder-head': head_interface,
            'egr-tube-manifold-fitting': fitting_interface}
