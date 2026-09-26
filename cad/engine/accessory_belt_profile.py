"""Shared PK comparison geometry; not a verified Ford production groove trace."""
import math

import build123d as cad

RIB_COUNT = 6
RIB_PITCH = 3.56
GROOVE_ANGLE = 40.0
GROOVE_DEPTH = 3.45
RIB_HEIGHT = 2.7
RIB_TIP_HALF_WIDTH = 0.12
CORD_ABOVE_RIB_ROOT = 1.6
BACK_ABOVE_CORD = 0.2
BELT_WIDTH = 21.36
CONTACT_CLEARANCE = 0.15
BELT_PLANE_X = 473.56
NOMINAL_EFFECTIVE_LENGTH = 2491.0
SOURCES = ['gates-pk-belt-dimensions', 'optibelt-pk-profile']
GAPS = [
    'Six ribs and nominal 2491 mm effective length follow Gates K060980/6PK2491. The fitted construction-study loop is not asserted to have this catalog length.',
    'PK comparison pitch 3.56 mm, 40 degree groove angle and 3.45 mm minimum depth follow the Optibelt technical manual. Sharp groove roots, crest shape, belt width, backing, rib truncation and clearance remain study approximations, not full standard compliance.',
    'Optibelt distinguishes effective diameter from tension-cord pitch diameter. Treating current pulley outside radii as effective radii is an explicit diagnostic assumption; installed gauge diameters and neutral-axis position remain unmeasured.',
    'A 1.6 mm cord offset is a PK comparison value; 0.2 mm back cover, 2.7 mm rib height and 0.15 mm display clearance are assumed. Ribs and backing are one belt solid, not separately counted physical parts.',
    'Normalization repairs only the outer groove band before recutting a common profile. Pulley diameters, centers, webs, bearings and mounting interfaces are not moved.'
]


def rib_centers():
    return [(index - (RIB_COUNT - 1) / 2) * RIB_PITCH for index in range(RIB_COUNT)]


def regroove_x(shape, radius, center=(0, 0, 0)):
    frame = cad.Pos(*center)
    annulus = cad.Cylinder(radius, 21.5) - cad.Cylinder(radius - 3.5, 23.5)
    shape += frame * cad.Rot(0, 90, 0) * annulus
    tangent = math.tan(math.radians(GROOVE_ANGLE / 2))
    for axial_position in rib_centers():
        half_width = (GROOVE_DEPTH + 0.5) * tangent
        profile = cad.Polygon((axial_position - half_width, radius + 0.5),
                              (axial_position, radius - GROOVE_DEPTH),
                              (axial_position + half_width, radius + 0.5), align=None)
        shape -= frame * cad.revolve(profile, axis=cad.Axis.X)
    return shape


def normalize_definition(identifier, shape):
    if identifier == 'alternator-pulley':
        return cad.Rot(0, -90, 0) * regroove_x(cad.Rot(0, 90, 0) * shape, 35)
    if identifier == 'ps-pump-pulley':
        return cad.Rot(0, -90, 0) * regroove_x(cad.Rot(0, 90, 0) * shape, 5.17 * 25.4 / 2)
    if identifier == 'damper-inertia-ring':
        return regroove_x(shape, 6.42 * 25.4 / 2, (19, 0, 0))
    if identifier == 'ac-compressor-clutch-pulley':
        return regroove_x(shape, 72.5, (100, 0, 0))
    if identifier == 'thermactor-pulley':
        return regroove_x(shape, 70, (BELT_PLANE_X, -280, 100))
    return shape


def belt_section_points():
    root = -CORD_ABOVE_RIB_ROOT
    tip = root - RIB_HEIGHT
    half_root = RIB_TIP_HALF_WIDTH + RIB_HEIGHT * math.tan(math.radians(GROOVE_ANGLE / 2))
    points = [(-BELT_WIDTH / 2, BACK_ABOVE_CORD), (BELT_WIDTH / 2, BACK_ABOVE_CORD), (BELT_WIDTH / 2, root)]
    for center in reversed(rib_centers()):
        points.extend([(center + half_root, root), (center + RIB_TIP_HALF_WIDTH, tip),
                       (center - RIB_TIP_HALF_WIDTH, tip), (center - half_root, root)])
    points.append((-BELT_WIDTH / 2, root))
    return points
