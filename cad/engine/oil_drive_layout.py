"""Provisional connected drive layout constrained by the Melling shaft envelope."""
import math
import build123d as b
from assembly_math import transforms
from oil_pump_drive import LENGTH, ACROSS_FLATS, shaft as intermediate_shaft, retainer

TILT = 20.0
DRIVE_X = 227.584
GEAR_SPACING = 36.0
GEAR_Z = 72 - GEAR_SPACING * math.sin(math.radians(TILT))
GEAR_Y = 90 + GEAR_SPACING * math.cos(math.radians(TILT))
GEAR_FRAME = b.Pos(DRIVE_X, GEAR_Y, GEAR_Z) * b.Rot(-TILT, 0, 0)
DISTRIBUTOR_FRAME = GEAR_FRAME * b.Pos(0, 0, 85)
UPPER_LIFT = 50.0
INTERMEDIATE_TOP = -53.0
INTERMEDIATE_BOTTOM = INTERMEDIATE_TOP - LENGTH
PUMP_FRAME = GEAR_FRAME * b.Pos(-3.5, 0, INTERMEDIATE_BOTTOM - 17)
SOURCES = ['ford-industrial-csg649', 'fsm-a3698a10af15', 'melling-intermediate-shaft-dimensions']
GAPS = [
    '20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.',
    'Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.',
    'Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.',
    'Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.'
]


def helical_gear(width=12, phase=0):
    pitch = GEAR_SPACING / 2
    teeth = 16
    normal_module = 2 * pitch * math.cos(math.radians(45)) / teeth
    pressure = math.atan(math.tan(math.radians(20)) / math.cos(math.radians(45)))
    base = pitch * math.cos(pressure)
    root = pitch - 1.25 * normal_module
    tip = pitch + normal_module

    def involute(radius):
        parameter = math.sqrt(max(0, (radius / base) ** 2 - 1))
        return parameter - math.atan(parameter)

    half = math.pi / (2 * teeth) - .25 / (2 * pitch)
    radii = [max(base, root) + (tip - max(base, root)) * index / 7 for index in range(8)]
    points = []
    for index in range(teeth):
        angle = math.tau * index / teeth
        profile = [(root, angle - math.pi / teeth), (root, angle - half - involute(pitch))]
        profile += [(radius, angle - half - involute(pitch) + involute(radius)) for radius in radii]
        profile += [(radius, angle + half + involute(pitch) - involute(radius)) for radius in reversed(radii)]
        profile += [(root, angle + half + involute(pitch))]
        points += [(radius * math.cos(angle), radius * math.sin(angle)) for radius, angle in profile]
    twist = -math.degrees(width / pitch)
    section = b.Polygon(*points, align=None).face()
    shape = b.Solid.extrude_linear_with_rotation(section, (0, 0, 0), (0, 0, width), twist)
    return b.Pos(0, 0, -width / 2) * b.Rot(0, 0, phase - twist / 2) * shape


def cam_interface(shape):
    gear = b.Pos(DRIVE_X, 0, 0) * b.Rot(0, 90, 0) * helical_gear(12, 2.5)
    return shape + gear


def distributor_gear():
    shape = helical_gear(12, 11.25) + axial_cylinder(9, 5.9, 24)
    shape -= axial_cylinder(6.05, -7, 25)
    shape -= b.Solid.make_cylinder(1.55, 22, b.Plane(origin=(-11, 0, 15), z_dir=(1, 0, 0)))
    return shape


def axial_cylinder(radius, lower, upper):
    return b.Pos(0, 0, (lower + upper) / 2) * b.Cylinder(radius, upper - lower)


def distributor_shaft_interface(shape):
    lower = shape.intersect(b.Pos(0, 0, -179.5) * b.Box(100, 100, 241))
    upper = shape.intersect(b.Pos(0, 0, 120.5) * b.Box(100, 100, 359))
    body = lower + axial_cylinder(5.9, -60, -58 + UPPER_LIFT)
    body += b.Pos(0, 0, UPPER_LIFT) * upper
    body += axial_cylinder(5.9, INTERMEDIATE_TOP - 95, -102)
    socket = b.Pos(0, 0, INTERMEDIATE_TOP - 96) * b.extrude(b.RegularPolygon((ACROSS_FLATS + .08) / math.sqrt(3), 6), amount=15)
    return body - socket


def distributor_housing_interface(shape):
    lower = shape.intersect(b.Pos(0, 0, -100) * b.Box(150, 150, 200))
    upper = shape.intersect(b.Pos(0, 0, 100) * b.Box(150, 150, 200))
    neck = axial_cylinder(13, -.2, UPPER_LIFT + .2) - axial_cylinder(9, -1, UPPER_LIFT + 1)
    return lower + neck + b.Pos(0, 0, UPPER_LIFT) * upper


def rotor_shaft_interface(shape):
    upper = axial_cylinder(6, 10, 21)
    socket = b.Pos(0, 0, 11) * b.extrude(b.RegularPolygon((ACROSS_FLATS + .08) / math.sqrt(3), 6), amount=19)
    return (shape + upper) - socket


def pump_housing_interface(shape):
    return shape - b.Pos(3.5, 0, 0) * b.Cylinder(6.15, 50)


def pump_mount_supports():
    supports = []
    for station in (-28,):
        offset = math.copysign(10, station)
        foot = PUMP_FRAME * b.Pos(station, 28, 16) * b.extrude(b.Ellipse(14, 9), amount=8)
        endpoint = (PUMP_FRAME * b.Vertex(station, 28, 20)).center() + b.Vector(offset, 0, 0)
        start = b.Vector(DRIVE_X - 3.5 + station + offset, 97, -18)
        direction = endpoint - start
        column = b.Solid.make_cylinder(4, direction.length, b.Plane(origin=start, z_dir=direction))
        support = foot + column
        support -= PUMP_FRAME * b.Pos(station, 28, 20) * b.Cylinder(3.2, 40)
        support -= PUMP_FRAME * b.Pos(station, 28, 26.2) * b.Cylinder(5.6, 4.4)
        supports.append(support)
    mirror = b.Plane(origin=(DRIVE_X - 3.5, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    supports.append(supports[0].mirror(mirror))
    return supports


def pump_mount_bolt():
    shank = axial_cylinder(3, 4, 24)
    head = b.Pos(0, 0, 24) * b.extrude(b.RegularPolygon(5.2, 6), amount=4)
    return shank + head


def block_interface(shape):
    upper_boss = axial_cylinder(22, -15, 48.5)
    lower_boss = axial_cylinder(10, INTERMEDIATE_TOP - 11, -12)
    clamp_pad = b.Pos(0, 23.5, 46.5) * b.Box(22, 47, 14)
    clamp_pad -= axial_cylinder(19.2, 35, 60)
    body = shape + GEAR_FRAME * (upper_boss + lower_boss + clamp_pad)
    neck_bore = axial_cylinder(13.15, 8, 110)
    gear_pocket = axial_cylinder(20, -8, 8)
    lower_bore = axial_cylinder(6.2, INTERMEDIATE_TOP - 12, 8)
    bolt_bore = b.Pos(0, 37, 0) * axial_cylinder(4.1, 15, 65)
    for cutter in (neck_bore, gear_pocket, lower_bore, bolt_bore):
        body -= GEAR_FRAME * cutter
    body -= GEAR_FRAME * axial_cylinder(7.2, INTERMEDIATE_BOTTOM - 2, INTERMEDIATE_TOP - 11.5)
    body -= b.Pos(DRIVE_X, 90, 72) * b.Rot(0, 90, 0) * b.Cylinder(20.1, 18)
    for support in pump_mount_supports():
        body += support
    return body


def pickup_tube():
    start = (PUMP_FRAME * b.Vertex(-34, 0, 5)).center()
    path = b.Spline(start, (60, 48, -130), (-100, 41, -210),
                    (-190, 41, -245), tangents=[(-1, 0, 0), (-1, 0, 0)])
    plane = b.Plane(origin=path @ 0, x_dir=(0, 1, 0), z_dir=(-1, 0, 0))
    return b.sweep(plane * (b.Circle(6) - b.Circle(4.8)), path=path, is_frenet=True)


def candidate_parts(manifest, definitions):
    locations = transforms(manifest)
    placed = {}
    old_distributor = b.Pos(200, 190, 145)
    old_pump = b.Pos(210, 56, -112)
    for occurrence in manifest['occurrences']:
        identifier = occurrence['id']
        if identifier.startswith('distributor-'):
            shape = definitions[occurrence['definition']]
            if identifier == 'distributor-shaft':
                shape = distributor_shaft_interface(shape)
            elif identifier == 'distributor-housing':
                shape = distributor_housing_interface(shape)
            elif identifier == 'distributor-drive-gear':
                shape = b.Pos(0, 0, -85) * distributor_gear()
            elif identifier not in ('distributor-drive-gear', 'distributor-drive-pin', 'distributor-thrust-washer',
                                     'distributor-hold-down-clamp', 'distributor-hold-down-bolt',
                                     'distributor-o-ring', 'distributor-bushing-1'):
                shape = b.Pos(0, 0, UPPER_LIFT) * shape
            placed[identifier] = DISTRIBUTOR_FRAME * old_distributor.inverse() * locations[identifier] * shape
        if identifier.startswith('oil-pump-'):
            shape = definitions[occurrence['definition']]
            if identifier == 'oil-pump-housing':
                shape = pump_housing_interface(shape)
            if identifier == 'oil-pump-rotor-shaft':
                shape = rotor_shaft_interface(shape)
            placed[identifier] = PUMP_FRAME * old_pump.inverse() * locations[identifier] * shape
    placed['block'] = block_interface(definitions['block'])
    placed['camshaft'] = b.Pos(0, 90, 72) * cam_interface(definitions['camshaft'])
    placed['oil-pump-intermediate-shaft'] = GEAR_FRAME * b.Pos(0, 0, INTERMEDIATE_BOTTOM) * intermediate_shaft()
    placed['oil-pump-drive-retainer'] = GEAR_FRAME * b.Pos(0, 0, INTERMEDIATE_BOTTOM) * retainer()
    placed['oil-pickup-tube'] = pickup_tube()
    for index, station in enumerate((-28, 28), 1):
        placed[f'oil-pump-mount-bolt-{index}'] = PUMP_FRAME * b.Pos(station, 28, 0) * pump_mount_bolt()
    return placed


def distributor_definition(identifier, shape):
    if identifier == 'distributor-shaft':
        return distributor_shaft_interface(shape)
    if identifier == 'distributor-housing':
        return distributor_housing_interface(shape)
    if identifier == 'distributor-drive-gear':
        return b.Pos(0, 0, -85) * distributor_gear()
    if identifier == 'distributor-cap':
        from ignition_leads import cap_interface
        return cap_interface(b.Pos(0, 0, UPPER_LIFT) * shape)
    lower = {'distributor-drive-pin', 'distributor-thrust-washer', 'distributor-hold-down-clamp',
             'distributor-hold-down-bolt', 'distributor-o-ring', 'distributor-bushing'}
    return shape if identifier in lower else b.Pos(0, 0, UPPER_LIFT) * shape


def distributor_api(api, include_root=True):
    define, add, group = api

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), claims=()):
        if identifier == 'distributor-cap':
            from ignition_leads import SOURCES as lead_sources, GAPS as lead_gaps
            sources = list(sources) + lead_sources
            gaps = list(gaps) + lead_gaps
        define(identifier, distributor_definition(identifier, shape), name, function, system, color,
               list(dict.fromkeys(list(sources) + SOURCES)), list(gaps) + GAPS, claims)

    def add_part(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
        if identifier == 'distributor-bushing-2':
            pos = (pos[0], pos[1], pos[2] + UPPER_LIFT)
        add(identifier, definition, parent, pos, explode, rotation, name=name)

    def add_group(identifier, name, parent='engine', **kwargs):
        if identifier == 'ignition' and not include_root:
            return
        if identifier == 'distributor-assembly':
            kwargs['position'] = tuple(DISTRIBUTOR_FRAME.position)
            kwargs['rotation'] = (-TILT, 0, 0)
        group(identifier, name, parent, **kwargs)

    return define_part, add_part, add_group


def pump_api(api):
    define, add, group, cylinder_x, spring = api

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), claims=()):
        if identifier == 'oil-pump-housing':
            shape = pump_housing_interface(shape)
        elif identifier == 'oil-pump-rotor-shaft':
            shape = rotor_shaft_interface(shape)
            function = 'Receives the intermediate hex shaft in a matching socket and drives the inner rotor. Upper shaft diameter and interface clearances are provisional.'
        elif identifier == 'oil-pickup-tube':
            shape = b.Pos(210, 56, -112).inverse() * pickup_tube()
        define(identifier, shape, name, function, system, color,
               list(dict.fromkeys(list(sources) + SOURCES)), list(gaps) + GAPS, claims)

    def add_group(identifier, name, parent='engine', **kwargs):
        if identifier == 'oil-pump-assembly':
            kwargs['position'] = tuple(PUMP_FRAME.position)
            kwargs['rotation'] = (-TILT, 0, 0)
        group(identifier, name, parent, **kwargs)

    return define_part, add, add_group, cylinder_x, spring


def build(api):
    define, add, group = api
    group('oil-drive-assembly', 'Oil pump intermediate drive · constrained study', 'lubrication',
          position=tuple(GEAR_FRAME.position), rotation=(-TILT, 0, 0))
    for identifier, shape, name, function in [
        ('oil-pump-intermediate-shaft', intermediate_shaft(), 'Oil pump intermediate shaft · IS-74 study',
         'Connects the distributor lower hex socket to the pump rotor shaft. Sourced overall length and hex size are preserved; installed datums and engagement depths are provisional.'),
        ('oil-pump-drive-retainer', retainer(), 'Intermediate shaft retaining ring · envelope',
         'Sits below the modeled block shoulder. Split-ring geometry, gripping construction and working retention remain unverified.')]:
        define(identifier, shape, name, function, 'lubrication', '#a0aab0', SOURCES, GAPS)
        add(identifier, identifier, 'oil-drive-assembly', pos=(0, 0, INTERMEDIATE_BOTTOM), explode=(0, 0, 100))
    define('oil-pump-mount-bolt', pump_mount_bolt(), 'Oil pump mounting bolt · provisional',
           'Clamps an illustrative mounting foot against an outboard pump ear. Count, thread, strength and production mounting architecture remain unresolved.',
           'lubrication', '#929ba1', SOURCES, GAPS)
    for index, station in enumerate((-28, 28), 1):
        add(f'oil-pump-mount-bolt-{index}', 'oil-pump-mount-bolt', 'oil-pump-assembly',
            pos=(station, 28, 0), explode=(0, 0, 80))
