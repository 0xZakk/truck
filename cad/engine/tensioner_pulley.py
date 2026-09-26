"""Gates 38022 envelope study with provisional section and installed station."""
import build123d as cad

POSITION = (473.56, 0, 435)
ROTATION = (0, 90, 0)
OUTSIDE_DIAMETER = 90
WIDTH = 37.5
BORE = 17
BEARING_OUTSIDE_DIAMETER = 40
BEARING_WIDTH = 17
SOURCES = ['gates-38022', 'gates-1994-drive', 'ford-accessory-routing']
GAPS = [
    '90 mm outside diameter, 37.5 mm width and 17 mm bearing bore are Gates replacement specifications; installed identity is unverified.',
    'Rim thickness 3 mm, web thickness 3 mm, bearing outer diameter 40 mm and bearing width 17 mm are illustrative assumptions.',
    'The bearing is an unresolved cartridge envelope, not a reconstruction of races, balls, cage or seals.',
    'Pulley center and belt plane are provisional. The axial center follows the illustrative damper groove center, not a measured production datum. A support study is modeled separately; the belt, engine bracket and operating motion remain unfinished.'
]


def ring(outer_radius, inner_radius, width):
    return cad.Cylinder(outer_radius, width) - cad.Cylinder(inner_radius, width + 2)


def components():
    rim = ring(OUTSIDE_DIAMETER / 2, OUTSIDE_DIAMETER / 2 - 3, WIDTH)
    web = ring(OUTSIDE_DIAMETER / 2 - 2, BEARING_OUTSIDE_DIAMETER / 2, 3)
    bearing = ring(BEARING_OUTSIDE_DIAMETER / 2, BORE / 2, BEARING_WIDTH)
    return {'tensioner-pulley-wheel': rim + web, 'tensioner-pulley-bearing': bearing}


def parts():
    mount = cad.Pos(*POSITION) * cad.Rot(*ROTATION)
    return {identifier: mount * shape for identifier, shape in components().items()}


def build(api):
    define, add, group = api
    group('accessory-drive', 'Accessory drive · unfinished')
    group('tensioner-pulley-assembly', 'Tensioner pulley · envelope study', 'accessory-drive')
    descriptions = {
        'tensioner-pulley-wheel': ('Tensioner pulley wheel', 'The smooth steel surface contacts the back of the accessory belt. The rim and web are one illustrative wheel; a separate support study carries the bearing, while the belt and engine bracket remain missing.', '#33383c'),
        'tensioner-pulley-bearing': ('Tensioner pulley bearing · unresolved cartridge', 'Allows the pulley wheel to turn around its stationary mounting axis. Only the 17 mm bore is sourced; the outer envelope and internal construction remain unresolved.', '#929ba1')
    }
    for identifier, shape in components().items():
        name, function, color = descriptions[identifier]
        define(identifier, shape, name, function, 'accessory-drive', color, SOURCES, GAPS)
        offset = 100 if identifier.endswith('wheel') else 170
        add(identifier, identifier, 'tensioner-pulley-assembly', POSITION, (offset, 0, 0), ROTATION)
