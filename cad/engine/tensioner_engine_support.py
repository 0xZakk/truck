"""Provisional dry mounting load path behind the Gates tensioner cartridge study."""
import build123d as cad

from accessory_brackets import axial, web, engine_foot, bolt
from tensioner_arm import POSITION, ROTATION

SOURCES = ['gates-38131-instructions', 'ford-accessory-routing', 'tensioner-engine-support']
GAPS = [
    'Gates supports the central mounting fastener and locating-pin/bushing architecture. This rear bracket, engine attachment topology, casting contour and every dimension are provisional construction geometry, not a sourced factory bracket.',
    'A 20 mm rear pad seats the existing cartridge back at X400.56. Its central blind bore receives an extended smooth fastener with 14 mm engagement and 2 mm tip clearance; helical threads and production fit remain unmodeled.',
    'The modeled optional locating bushing enters a 12.7 mm bracket bore, corresponding to Gates large-hole option. Exact installed bracket option is unverified; the 5/16 inch option is not simultaneously modeled.',
    'Separate dry blind block/head bosses provide an explicit mechanical path. Hole positions, bolt counts, grade, preload, stiffness, belt force and spring travel have not been verified.',
    'No pulley center or spring pivot moves in this adapter. The belt-length residual is not disguised by repositioning the tensioner.'
]


def bracket():
    shape = axial(32, 20, (390.56, -75, 435))
    shape += web(380.56, (-75, 435), (-65, 220), 18, 20)
    for vertical in (220, 285):
        shape += engine_foot(-65, vertical, 390.56, -65)
        shape -= axial(5.5, 32, (388, -65, vertical))
        shape -= axial(11, 20, (395, -65, vertical))
    shape -= axial(5.8, 17, (393.06, -75, 435))
    shape -= axial(6.35, 13, (395.06, -75, 455))
    return shape


def mount_bolt_local():
    shape = cad.Pos(-75, 0, -54) * cad.Cylinder(5.5, 66)
    shape += cad.Pos(-75, 0, -21) * cad.extrude(cad.RegularPolygon(12, 6), amount=6)
    return shape


def block_interface(shape):
    shape += axial(12, 24, (361, -65, 220))
    return shape - axial(5.2, 17, (365.5, -65, 220))


def head_interface(shape):
    shape += axial(12, 24, (361, -65, 285 - 255.5))
    return shape - axial(5.2, 17, (365.5, -65, 285 - 255.5))


def parts(include_replacement=True):
    result = {
        'tensioner-engine-bracket': bracket(),
        'tensioner-bracket-block-bolt': bolt(359, 385, -65, 220, 4.9),
        'tensioner-bracket-head-bolt': bolt(359, 385, -65, 285, 4.9)
    }
    if include_replacement:
        result['tensioner-mounting-bolt'] = cad.Pos(*POSITION) * cad.Rot(*ROTATION) * mount_bolt_local()
    return result


def build(api):
    define, add, group = api
    group('tensioner-engine-mount', 'Tensioner engine attachment · provisional', 'accessory-drive')
    for index, (identifier, shape) in enumerate(parts(False).items()):
        name = identifier.replace('-', ' ').title()
        function = 'Transfers cartridge reaction into separate dry block/head attachments while registering the locating bushing. Factory bracket identity and casting dimensions remain unresolved.' if identifier.endswith('bracket') else 'Illustrates smooth fastener engagement in the assumed blind engine boss; threads and clamp preload remain unmodeled.'
        define(identifier, shape, name, function, 'accessory-drive', '#919c9e', SOURCES, GAPS)
        add(identifier, identifier, 'tensioner-engine-mount', (0, 0, 0), (120 + index * 40, -30, 0))
