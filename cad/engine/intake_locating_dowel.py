"""Single Ford intake locating dowel with explicit provisional joint adapters."""
import build123d as cad

POSITION = (0, -132.7, 298)
RADIUS = 7.9375 / 2
LENGTH = 25.4
PIN_FIRST = POSITION[1] - LENGTH / 2
PIN_LAST = POSITION[1] + LENGTH / 2
HEAD_ORIGIN_Z = 255.5
SOURCES = ['ford-intake-manifold-dowel', 'ford-1996-manifold-fastener-table']
GAPS = [
    'Ford1994 specifies one locating dowel through the intake gasket into the lower intake. The1996 factory comparison table gives5/16 inch diameter by1 inch length; identity and dimensions on the1994 truck remain unverified.',
    'The7.9375 by25.4 mm comparison pin replaces the earlier arbitrary6 by23.5 mm candidate. WorldX0/Z298 and axial centerY-132.7 are dry-interface assumptions, not measured Ford datums.',
    'Head and intake sockets use0.05 mm radial clearance for geometric checking. They do not establish the real press/sliding fits or retention.',
    'The dowel locates the joint but does not clamp it. The front lifting-eye stud/bolt study is separate; fourteen other manifold attachment stations and shared clamping details remain unresolved.'
]


def along_y(radius, first, last, x=0, z=298):
    return cad.Pos(x, (first + last) / 2, z) * cad.Rot(90, 0, 0) * cad.Cylinder(radius, last - first)


def pin():
    return along_y(RADIUS, PIN_FIRST, PIN_LAST)


def head_interface(shape):
    return shape - along_y(RADIUS + .05, -134, -118, z=298 - HEAD_ORIGIN_Z)


def lower_interface(shape):
    shape += along_y(8, -146.4, -135.5)
    return shape - along_y(RADIUS + .05, -145.9, -134.5)


def gasket_interface(shape):
    shape += along_y(6, -135.5, -133)
    return shape - along_y(RADIUS + .2, -136, -132.5)


def parts():
    return {'intake-head-locating-dowel': pin()}


ADAPTERS = {'cylinder-head': head_interface, 'efi-lower-intake': lower_interface,
            'efi-head-intake-gasket': gasket_interface}


def build(api):
    define, add, group = api
    group('intake-head-locator', 'Intake/head locating interface · provisional', 'induction')
    define('intake-head-locating-dowel', pin(), 'Intake manifold locating dowel', 'Locates the intake gasket and lower manifold relative to the cylinder head. It enters separate blind sockets; it is not a substitute for the missing manifold clamp fasteners.', 'induction', '#9fa8ad', SOURCES, GAPS)
    add('intake-head-locating-dowel', 'intake-head-locating-dowel', 'intake-head-locator', explode=(0, -65, 0))
