"""Water-pump pulley fit study on the existing provisional pump hub."""
import math
import build123d as b

POSITION = (440, 0, 170)
BELT_CENTER_X = 473.56
RADIUS = 75.0
WIDTH = 28.0
SOURCES = ['system-7b01cf423275', 'gates-1994-drive']
GAPS = [
    'Ford service procedure establishes a separate pulley and threaded fan-clutch assembly, but supplies no pulley dimensions.',
    'Gates S7004 shows backside contact at the central upper wheel; identifying that wheel as the water pump is an interpretation. Smooth rim is provisional pending an identified production-pulley photograph.',
    '150 mm diameter, 28 mm rim width, dish section, four-hole 50 mm bolt circle and all fastener dimensions are illustrative. Four bolts follow the existing provisional hub holes, not a sourced production bolt count.',
    'Pulley sits on the existing pump hub front at global X522. Its assumed dish depth aligns the smooth rim with the current illustrative damper belt center X473.56; neither datum establishes factory belt alignment.',
    'Fan-clutch threaded nose, thread dimensions, belt routing, working belt ratio and rotational animation remain unresolved. Smooth fastener shanks do not model threads or production clamping fit.'
]


def cylinder(radius, length, center):
    return b.Pos(center, 0, 0) * b.Rot(0, 90, 0) * b.Cylinder(radius, length)


def pulley():
    rear = BELT_CENTER_X - POSITION[0] - WIDTH / 2
    front = rear + WIDTH
    profile = b.Polygon((rear, 75), (front, 75), (84.5, 39),
                        (84.5, 8.1), (82, 8.1), (82, 38),
                        (front - 2.5, 72.5), (rear, 72.5), align=None)
    shape = b.revolve(profile, axis=b.Axis.X)
    for index in range(4):
        angle = index * math.tau / 4
        shape -= b.Pos(0, 25 * math.cos(angle), 25 * math.sin(angle)) * cylinder(3.5, 6, 83.25)
    from fan_clutch import pulley_interface
    return pulley_interface(shape)


def bolt():
    head = b.Pos(84.5, 0, 0) * b.extrude(b.Plane.YZ * b.RegularPolygon(5.5, 6), amount=4)
    return head + cylinder(3, 10.5, 79.25)


def parts():
    result = {'water-pump-pulley': b.Pos(*POSITION) * pulley()}
    for index in range(4):
        angle = index * math.tau / 4
        result[f'water-pump-pulley-bolt-{index + 1}'] = b.Pos(POSITION[0], 25 * math.cos(angle), POSITION[2] + 25 * math.sin(angle)) * bolt()
    return result


def build(api):
    define, add, group = api
    group('water-pump-pulley-assembly', 'Water pump pulley · fit study', 'water-pump-assembly')
    define('water-pump-pulley', pulley(), 'Water pump pulley',
           'A dished smooth-rim study transfers belt force through the existing pump hub. Its diameter, dish offset and belt alignment are provisional.',
           'cooling', '#343b40', SOURCES, GAPS)
    define('water-pump-pulley-bolt', bolt(), 'Water pump pulley bolt · provisional',
           'Illustrates retention through the four existing hub holes. Fastener count, dimensions, threads and production attachment architecture remain unverified.',
           'cooling', '#939da5', SOURCES, GAPS)
    add('water-pump-pulley', 'water-pump-pulley', 'water-pump-pulley-assembly', explode=(470, 0, 0))
    for index in range(4):
        angle = index * math.tau / 4
        add(f'water-pump-pulley-bolt-{index + 1}', 'water-pump-pulley-bolt',
            'water-pump-pulley-assembly', (0, 25 * math.cos(angle), 25 * math.sin(angle)),
            (530, 25 * math.cos(angle), 25 * math.sin(angle)))
