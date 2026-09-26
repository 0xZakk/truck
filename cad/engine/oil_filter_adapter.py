"""Filter mounting and two-port gallery boundary study, not a complete oil circuit."""
import math
import build123d as b
from oil_filter import POSITION, ROTATION

FRAME = b.Pos(*POSITION) * b.Rot(*ROTATION)
SOURCES = ['fsm-d975f341ee63', 'fsm-6f023139b5f8', 'ford-industrial-csg649',
           'wix-51515-envelope', 'enginequest-oil-filter-adapter']
GAPS = [
    'The insert is a hollow stepped comparison envelope, not a reconstructed E4TZ-6890-A anti-drainback service insert. No unsourced valve mechanism is added.',
    'Filter position, inclined boss, gallery routing, insert lengths, block-end thread diameter and sealing lands are provisional. Filter-side 3/4-16 uses coincident nominal male/female envelopes, not helical thread contact.',
    'Two deliberately open side interfaces bound this gallery study. They are not production external ports and remain disconnected from the pump and main oil gallery. The engine lubrication circuit is incomplete.',
    'No separate adapter gasket or additional bypass valve is inferred. The existing filter gasket, internal flap and illustrative bypass remain separate components; seal compression and anti-drainback performance are not simulated.'
]


def cylinder(radius, lower, upper):
    return b.Pos(0, 0, (lower + upper) / 2) * b.Cylinder(radius, upper - lower)


def inlet_void():
    annulus = cylinder(30, -4, 1) - cylinder(22, -5, 2)
    feed = b.Pos(0, 27, 0) * cylinder(4, -16, 1)
    boundary = b.Solid.make_cylinder(4, 42, b.Plane(origin=(-42, 27, -12), z_dir=(1, 0, 0)))
    return annulus + feed + boundary


def outlet_void():
    return cylinder(6.4, -34, 13) + b.Solid.make_cylinder(6.4, 42, b.Plane(origin=(0, 0, -29), z_dir=(1, 0, 0)))


def insert():
    body = cylinder(12, -22, -3) + cylinder(14, -3, 0) + cylinder(9.525, 0, 12)
    body -= cylinder(6.4, -23, 13)
    body -= b.Pos(0, 0, 7) * b.extrude(b.RegularPolygon(7.7, 6), amount=6)
    return body


def boss_addition():
    boss = FRAME * cylinder(39, -70, 0)
    boss &= b.Pos(70, 217.4, 28) * b.Box(200, 200, 200)
    return boss


def block_interface(shape):
    shape += boss_addition()
    seat = cylinder(12.05, -22, -3) + cylinder(14.05, -3, .1)
    return shape - FRAME * seat - FRAME * inlet_void() - FRAME * outlet_void()


def gallery_boundaries():
    return {
        'unfiltered-inlet': {'center_cad_mm': tuple((FRAME * b.Vertex(-math.sqrt(39 ** 2 - 27 ** 2), 27, -12)).center()),
                            'radius_mm': 4, 'connects_to': 'Filter baseplate outer inlet annulus',
                            'unresolved': 'Pump delivery route upstream'},
        'filtered-outlet': {'center_cad_mm': tuple((FRAME * b.Vertex(39, 0, -29)).center()),
                           'radius_mm': 6.4, 'connects_to': 'Hollow insert and filter clean center',
                           'unresolved': 'Main oil gallery downstream'},
    }


def filter_api(api):
    define, add, group, spring = api

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), claims=()):
        gaps = [gap for gap in gaps if 'block sealing boss' not in gap]
        if identifier == 'oil-filter-baseplate':
            function = 'Outer inlet holes communicate with the boss inlet annulus; the central threaded-envelope bore receives the hollow mounting insert. Complete pump/main-gallery routing and actual thread contact remain unresolved.'
        define(identifier, shape, name, function, system, color,
               list(dict.fromkeys(list(sources) + SOURCES)), list(gaps) + GAPS, claims)

    return define_part, add, group, spring


def build(api):
    define, add, group = api
    group('oil-filter-adapter-assembly', 'Filter mount and gallery boundary study', 'lubrication',
          position=POSITION, rotation=ROTATION)
    define('oil-filter-mounting-insert', insert(), 'Hollow oil filter mounting insert · comparison study',
           'Retains the filter at the block sealing boss and returns filtered oil through its separate central passage. This is not the verified E4TZ anti-drainback insert and has no invented internal valve.',
           'lubrication', '#9aabb3', SOURCES, GAPS)
    add('oil-filter-mounting-insert', 'oil-filter-mounting-insert', 'oil-filter-adapter-assembly', explode=(0, 0, 90))
