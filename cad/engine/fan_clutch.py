"""Thermal fan-clutch and seven-blade fan comparison with provisional internals."""
import math
import build123d as b

POSITION = (530, 0, 170)
PUMP_POSITION = (440, 0, 170)
CLUTCH_RADIUS = 7.20 * 25.4 / 2
CLUTCH_HEIGHT = 2.83 * 25.4
FAN_MOUNT = 1.25 * 25.4
FAN_PILOT = 2.37 * 25.4
FAN_BOLT_CIRCLE = 3 * 25.4
FAN_RADIUS = 18.9 * 25.4 / 2
SOURCES = ['system-7b01cf423275', 'imperial-fan-clutch-215161',
           'hayden-fan-clutch-operation', 'dorman-620-151']
GAPS = [
    'Imperial lists both 215161 (36 mm hex, M30x1.5 RH) and 215155 (40 mm hex, M33x1.5 RH) for 1994 F-Series 4.9L. This is the 215161 comparison branch; installed nut size is unknown.',
    'Catalog dimensions constrain clutch OD, overall height, fan mount height, fan pilot and four-hole bolt circle. Housing sections, bearing, seals, shear lands, reservoir, valve and spring are educational assumptions, not a production teardown.',
    'Dorman 620-151 supplies a seven-blade, 18.9 inch black stamped-steel comparison and F2UZ8600A cross-reference. Exact 4.9L vehicle fit is not independently established by the saved primary application table; installed fan identity remains unverified.',
    'Blade chord, pitch, twist, angular spacing, root shape, spider, fourteen rivets and all sheet thicknesses are provisional interpretations of the manufacturer photo. No airflow, stress, balance or fan-speed simulation.',
    'Pump nose extension, pulley bore and axial seating at X530 are provisional interface reconciliation. Thread nominal size and right-hand direction are sourced; the model uses smooth clearance envelopes rather than thread helices.',
    'Fan bolts use sourced 5/16-18 nominal diameter and four-hole count; length, head dimensions, thread engagement and hole angular index are provisional. Radiator/shroud clearance is not established.',
    'Silicone fluid and its dynamic fill fraction are described rather than represented as rigid solids. The sealed clutch is not a user-serviceable exploded repair procedure.'
]


def cylinder(radius, length, center):
    return b.Pos(center, 0, 0) * b.Rot(0, 90, 0) * b.Cylinder(radius, length)


def ring(outer, inner, length, center):
    return cylinder(outer, length, center) - cylinder(inner, length + 2, center)


def mounting_holes(shape, center, length, radius=4.1):
    for index in range(4):
        angle = math.radians(45 + index * 90)
        shape -= b.Pos(0, FAN_BOLT_CIRCLE / 2 * math.cos(angle), FAN_BOLT_CIRCLE / 2 * math.sin(angle)) * cylinder(radius, length, center)
    return shape


def hub_interface(shape):
    return shape + ring(14.95, 8.05, 29.5, 92.75)


def pulley_interface(shape):
    return shape - cylinder(15.05, 8, 83.25)


def input_shaft():
    nut = b.extrude(b.Plane.YZ * b.RegularPolygon(18 / math.cos(math.pi / 6), 6), amount=21)
    shape = nut + cylinder(10, 23, 32.5)
    return shape - cylinder(15.05, 17.88, 8.84)


def housing():
    shape = ring(CLUTCH_RADIUS, 85, 28.25, 49.875)
    shape += ring(CLUTCH_RADIUS, 22, 4, FAN_MOUNT + 2)
    shape += ring(28, 22, 12.75, 29.375)
    shape += ring(FAN_PILOT / 2, 22, 2, FAN_MOUNT - 1)
    return mounting_holes(shape, 35, 10)


def rotor():
    shape = ring(79, 10.05, 3, 41.5)
    for radius in (33, 47, 61, 75):
        shape += ring(radius + 3, radius, 6, 46)
    return shape


def partition():
    shape = ring(84.95, 2.6, 2, 53)
    for radius in (26, 40, 54, 68, 82):
        shape += ring(min(radius + 3, 84.95), radius, 5, 49.5)
    for horizontal in (-45, 45):
        shape -= b.Pos(0, horizontal, 0) * cylinder(3, 4, 53)
    return shape


def cover():
    shape = ring(CLUTCH_RADIUS, 2.6, 3, 65.5)
    for index in range(36):
        fin = b.Pos((67 + CLUTCH_HEIGHT) / 2, 55, 0) * b.Box(CLUTCH_HEIGHT - 67, 70, 2)
        shape += b.Rot(index * 10, 0, 0) * fin
    shape += b.Pos(69, 16.2, 0) * b.Box(4, 1.6, 3)
    return shape


def valve():
    return cylinder(2.5, 18, 61) + b.Pos(55, 23, 0) * b.Box(1.5, 46, 7)


def thermal_spring():
    angles = [index * math.tau * 3 / 180 for index in range(181)]
    outside = [(3.1 + 12 * index / 180 + .3) for index in range(181)]
    inside = [radius - .6 for radius in outside]
    points = [(radius * math.cos(angle), radius * math.sin(angle)) for radius, angle in zip(outside, angles)]
    points += [(radius * math.cos(angle), radius * math.sin(angle)) for radius, angle in reversed(list(zip(inside, angles)))]
    return b.Pos(69.5, 0, 0) * b.extrude(b.Plane.YZ * b.Polygon(*points, align=None), amount=1.5)


def fan_spider():
    shape = ring(57, FAN_PILOT / 2 + .1, 2, FAN_MOUNT - 1)
    for index in range(7):
        arm = b.Pos(FAN_MOUNT - 1, 84, 0) * b.Box(2, 74, 26)
        shape += b.Rot(index * 360 / 7, 0, 0) * arm
    shape = mounting_holes(shape, FAN_MOUNT - 1, 4, 4.3)
    for index in range(7):
        for tangent in (-7, 7):
            shape -= b.Rot(index * 360 / 7, 0, 0) * b.Pos(0, 111, tangent) * cylinder(2.55, 5, FAN_MOUNT - 1)
    return shape


def fan_blade():
    root = b.Pos(FAN_MOUNT - 3, 119, 0) * b.Box(2, 26, 26)
    sections = []
    for radial, chord, angle in ((130, 26, 0), (165, 70, 17), (FAN_RADIUS, 74, 22)):
        plane = b.Plane(origin=(FAN_MOUNT - 3, radial, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
        section = plane * b.Rectangle(2, chord)
        section = section.rotate(b.Axis((FAN_MOUNT - 3, radial, 0), (0, 1, 0)), angle)
        sections.append(section)
    blade = root + b.loft(sections)
    blade = blade & cylinder(FAN_RADIUS, 100, FAN_MOUNT)
    for tangent in (-7, 7):
        blade -= b.Pos(0, 111, tangent) * cylinder(2.55, 5, FAN_MOUNT - 3)
    return blade


def rivet():
    return cylinder(2.5, 4, FAN_MOUNT - 2) + cylinder(4.2, 1.2, FAN_MOUNT + .6) + cylinder(4.2, 1.2, FAN_MOUNT - 4.6)


def fan_bolt():
    head = b.Pos(FAN_MOUNT - 7, 0, 0) * b.extrude(b.Plane.YZ * b.RegularPolygon(6.3, 6), amount=5)
    return head + cylinder(5 / 16 * 25.4 / 2, 8, FAN_MOUNT + 2)


def components():
    return {
        'fan-clutch-input-shaft': input_shaft(),
        'fan-clutch-housing': housing(),
        'fan-clutch-bearing': ring(21.95, 10.05, 12, 30),
        'fan-clutch-shaft-seal': ring(21.95, 10.05, 1.2, 23),
        'fan-clutch-drive-rotor': rotor(),
        'fan-clutch-reservoir-partition': partition(),
        'fan-clutch-front-cover': cover(),
        'fan-clutch-control-valve': valve(),
        'fan-clutch-thermal-spring': thermal_spring(),
        'cooling-fan-spider': fan_spider(),
        'cooling-fan-blade': fan_blade(),
        'cooling-fan-rivet': rivet(),
        'cooling-fan-bolt': fan_bolt()
    }


def placements():
    result = [(identifier, identifier, (0, 0, 0), (0, 0, 0)) for identifier in DESCRIPTIONS if identifier not in ('cooling-fan-blade', 'cooling-fan-rivet', 'cooling-fan-bolt')]
    for index in range(7):
        angle = index * 360 / 7
        result.append((f'cooling-fan-blade-{index + 1}', 'cooling-fan-blade', (0, 0, 0), (angle, 0, 0)))
        for side, tangent in enumerate((-7, 7)):
            radians = math.radians(angle)
            result.append((f'cooling-fan-rivet-{index + 1}-{side + 1}', 'cooling-fan-rivet',
                           (0, 111 * math.cos(radians) - tangent * math.sin(radians), 111 * math.sin(radians) + tangent * math.cos(radians)), (0, 0, 0)))
    for index in range(4):
        angle = math.radians(45 + index * 90)
        result.append((f'cooling-fan-bolt-{index + 1}', 'cooling-fan-bolt',
                       (0, FAN_BOLT_CIRCLE / 2 * math.cos(angle), FAN_BOLT_CIRCLE / 2 * math.sin(angle)), (0, 0, 0)))
    return result


def parts():
    shapes = components()
    return {identifier: b.Pos(*POSITION) * b.Pos(*position) * b.Rot(*rotation) * shapes[definition]
            for identifier, definition, position, rotation in placements()}


DESCRIPTIONS = {
    'fan-clutch-input-shaft': ('Fan clutch input shaft and nut', 'The sourced M30x1.5 right-hand attachment drives the input shaft. This 36 mm nut branch is one of two catalog options; its smooth bore represents the thread envelope.', '#8f999f'),
    'fan-clutch-housing': ('Fan clutch output housing', 'Carries the fan and receives torque through viscous shear. Published replacement envelope and fan mounting dimensions constrain this otherwise illustrative casting.', '#9ba6ac'),
    'fan-clutch-bearing': ('Fan clutch bearing · cartridge', 'Supports the output housing around the input shaft while they rotate at different speeds. Bearing dimensions and internal construction are unresolved.', '#65757f'),
    'fan-clutch-shaft-seal': ('Fan clutch shaft seal · envelope', 'Represents fluid retention at the input shaft. Seal profile, material and dimensions remain unresolved.', '#39454a'),
    'fan-clutch-drive-rotor': ('Fan clutch drive rotor', 'The pump-driven rotor shears silicone fluid against the output housing. Concentric shear lands illustrate working area; their number, gaps and shape are provisional.', '#a9b2b5'),
    'fan-clutch-reservoir-partition': ('Fan clutch reservoir partition', 'Separates the forward fluid reservoir from the working region. Illustrative ports let the control valve meter fluid; actual ports and return-pumping passages remain unverified.', '#bab9a3'),
    'fan-clutch-front-cover': ('Fan clutch finned front cover', 'Closes the fluid reservoir and rejects heat through external fins. Fin number and housing closure details are illustrative.', '#adb8bb'),
    'fan-clutch-control-valve': ('Fan clutch fluid-control valve', 'The thermal spring turns a valve that admits silicone fluid to the working area as radiator-exit air warms. Valve geometry and calibration are illustrative.', '#c7a563'),
    'fan-clutch-thermal-spring': ('Fan clutch bimetal spring', 'Senses air leaving the radiator and operates the internal valve. Three turns and the ribbon section are illustrative, with no temperature or motion simulation.', '#c5a96c'),
    'cooling-fan-spider': ('Cooling fan mounting spider', 'Carries the seven stamped blades and attaches to four clutch mounting holes. Stamping contours and rivet positions are provisional.', '#262e32'),
    'cooling-fan-blade': ('Cooling fan stamped blade', 'One of seven blades in the 18.9-inch comparison fan. Counterclockwise rotation viewed from the radiator is sourced for the clutch application; blade chord and pitch are illustrative.', '#303b40'),
    'cooling-fan-rivet': ('Cooling fan blade rivet · provisional', 'Illustrates blade retention to the stamped spider. Two rivets per blade, their diameters and formed heads remain provisional.', '#4d575d'),
    'cooling-fan-bolt': ('Fan-to-clutch bolt', 'Attaches the fan to one of four sourced 5/16-18 clutch holes. Smooth shank, length and hex-head dimensions are illustrative.', '#959ea3')
}


def build(api):
    define, add, group = api
    group('fan-clutch-assembly', 'Thermal fan clutch · comparison study', 'cooling', position=POSITION)
    group('cooling-fan-assembly', 'Seven-blade cooling fan · comparison', 'fan-clutch-assembly')
    for identifier, shape in components().items():
        name, description, color = DESCRIPTIONS[identifier]
        define(identifier, shape, name, description, 'cooling', color, SOURCES, GAPS)
    for identifier, definition, position, rotation in placements():
        parent = 'cooling-fan-assembly' if identifier.startswith('cooling-fan-') else 'fan-clutch-assembly'
        offset = 180 + 35 * list(DESCRIPTIONS).index(definition)
        add(identifier, definition, parent, position, (offset, position[1] * .4, position[2] * .4), rotation)
