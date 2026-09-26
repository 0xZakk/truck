"""Unselected 10/11-inch clutch boundary studies, not production assemblies."""
import math

import build123d as cad

import flywheel

VARIANTS = {'10-inch-R2': 254.0, '11-inch-2F': 279.4}
SOURCES = ['ford-manual-clutch-boundary', 'luk-flywheel', 'hicengine-ffm68']
GAPS = [
    'Owner-confirmed M5OD-R2 and Ford R2 drawing support the10-inch baseline. Installed disc diameter is not physically verified;11-inch remains an uninstalled upgrade comparison.',
    'Only nominal disc diameter, ten-spline catalog designation and functional architecture are sourced. All section thicknesses, radial subdivisions and axial stack are illustrative.',
    'The disc damper is an unresolved cartridge. The diaphragm is an unslotted conical envelope: spring counts, fingers, fulcrums, straps, rivets, clamp force and release motion remain unresolved.',
    'Hub bore is a nominal spline envelope, not a manufactured ten-tooth involute. Pilot bearing and transmission release components are not reconstructed or selected.',
    'Six cover fasteners follow the existing assumed flywheel pattern. Smooth shanks omit threads and retain an assumed two-millimeter blind-hole bottom clearance.',
    'The shared cover envelope permits comparison of two disc diameters; it is not evidence that the production covers interchange.',
    'LuK note55 requires six grade8,3/8-16 by1-inch bolts and lock washers for an11-inch upgrade. The current assumed fasteners and flywheel holes do not meet that upgrade specification.'
]


def ring(outer, inner, height, base):
    placement = cad.Pos(0, 0, base)
    return placement * (cad.Cylinder(outer, height, align=(cad.Align.CENTER, cad.Align.CENTER, cad.Align.MIN)) - cad.Cylinder(inner, height, align=(cad.Align.CENTER, cad.Align.CENTER, cad.Align.MIN)))


def cover_holes():
    return [(147.5 * math.cos(angle), 147.5 * math.sin(angle)) for angle in [index * math.tau / 6 + math.pi / 6 for index in range(6)]]


def components(variant):
    radius = VARIANTS[variant] / 2
    cover = ring(155, 140, 3, 25) + ring(143, 140, 30, 28) + ring(143, 40, 2, 58)
    for horizontal, vertical in cover_holes():
        cover -= cad.Pos(horizontal, vertical, 24) * cad.Cylinder(4.3, 5, align=(cad.Align.CENTER, cad.Align.CENTER, cad.Align.MIN))
        cover -= cad.Pos(horizontal, vertical, 28) * cad.Cylinder(7, 7, align=(cad.Align.CENTER, cad.Align.CENTER, cad.Align.MIN))
    lower = cad.Pos(0, 0, 43) * (cad.Circle(139) - cad.Circle(132))
    upper = cad.Pos(0, 0, 55) * (cad.Circle(47) - cad.Circle(40))
    damper = ring(74, 25, 7, 28)
    for horizontal, vertical in flywheel.HOLES:
        damper -= cad.Pos(horizontal, vertical, 27) * cad.Cylinder(10, 3.5, align=(cad.Align.CENTER, cad.Align.CENTER, cad.Align.MIN))
    result = {
        'clutch-front-friction-facing': ring(radius, 75, 3, 25),
        'clutch-disc-carrier': ring(radius - 2, 74, 2, 28),
        'clutch-rear-friction-facing': ring(radius, 75, 3, 30),
        'clutch-disc-damper-cartridge': damper,
        'clutch-splined-hub-envelope': ring(25, 26.9875 / 2, 27, 25),
        'clutch-pressure-ring': ring(139.7, 75, 10, 33),
        'clutch-diaphragm-envelope': cad.loft([lower, upper]),
        'clutch-cover-study': cover,
    }
    bolt = cad.Pos(0, 0, 17) * cad.Cylinder(4, 11, align=(cad.Align.CENTER, cad.Align.CENTER, cad.Align.MIN))
    bolt += cad.Pos(0, 0, 28) * cad.extrude(cad.RegularPolygon(6.5, 6), amount=5)
    for index, (horizontal, vertical) in enumerate(cover_holes(), 1):
        result[f'clutch-cover-bolt-{index}'] = cad.Pos(horizontal, vertical, 0) * bolt
    return result


def parts(variant):
    return {identifier: flywheel.MOUNT * shape for identifier, shape in components(variant).items()}


def build(api, variant, comparison_only=False):
    if not comparison_only:
        import manual_clutch_load_path
        manual_clutch_load_path.require_complete_load_path(variant)
    define, add, group = api
    group('manual-clutch-boundary', f'Clutch boundary · unverified {variant}', 'crank-motion')
    for index, (identifier, shape) in enumerate(components(variant).items()):
        define(identifier, shape, identifier.replace('-', ' ').title(), 'Unselected engine-side clutch construction study; functional sections are separated but unresolved interiors and all assumed interface dimensions remain explicit.', 'rotating', '#8d9297', SOURCES, GAPS)
        add(identifier, identifier, 'manual-clutch-boundary', flywheel.POSITION, (-250 - index * 20, 0, 0), flywheel.ROTATION)
