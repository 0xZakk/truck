"""Carbon-core ignition leads and a provisional supported coil installation."""
import math
import build123d as b
from oil_drive_layout import DISTRIBUTOR_FRAME, UPPER_LIFT
from plug_mounts import PLUG_Y, PLUG_LOCAL_Z, PLUG_ANGLE, HEAD_WORLD_Z

FIRING_ORDER = (1, 5, 3, 6, 2, 4)
TOWER_BY_CYLINDER = {1: 1, 5: 6, 3: 5, 6: 4, 2: 3, 4: 2}
LANE_Y = {1: 200, 2: 245, 3: 155, 4: 270, 5: 180, 6: 220}
CYLINDER_X = [(2.5 - index) * 113.792 for index in range(6)]
COIL_FRAME = b.Pos(-40, 210, 235)
SOURCES = ['fsm-be886ffa4807', 'fsm-2f144bda5e08', 'system-f1571449160a', 'system-2ea2c28d7cca']
GAPS = [
    'Firing sequence and clockwise distributor sweep follow Ford references. Tower 1 at local +X is an explicit model phase; surveyed cap clocking and absolute ignition timing are unverified.',
    'Ford describes a carbon-impregnated multifilament synthetic-fiber core and heat-resistant rubber insulation. The 7 mm jacket, 2 mm aggregate core and all boot/contact dimensions are illustrative; individual fibers and electrical resistance are not simulated.',
    'Lead lengths, bends, terminal clip construction, seal compression and support arrangement are provisional. These routes are not an installation guide.',
    'Coil bracket geometry, two head mounting bosses and fasteners are a fit study. Four coil screws follow existing provisional core holes, not a verified factory screw count.',
    'Electrical paths and firing order are represented; ignition voltage, dielectric breakdown, spark timing, flexing and thermal behavior are not simulated.'
]


def cylinder(radius, lower, upper):
    return b.Pos(0, 0, (lower + upper) / 2) * b.Cylinder(radius, upper - lower)


def cap_frame(tower=None):
    angle = 0 if tower is None else math.radians((tower - 1) * 60)
    radius = 0 if tower is None else 33
    return DISTRIBUTOR_FRAME * b.Pos(radius * math.cos(angle), radius * math.sin(angle), UPPER_LIFT)


def plug_frame(cylinder_number):
    return b.Pos(CYLINDER_X[cylinder_number - 1], PLUG_Y, HEAD_WORLD_Z + PLUG_LOCAL_Z) * b.Rot(PLUG_ANGLE, 0, 0)


def point(frame, height):
    return (frame * b.Vertex(0, 0, height)).center()


def direction(frame):
    return point(frame, 1) - point(frame, 0)


def cap_interface(shape):
    for tower in (None, 1, 2, 3, 4, 5, 6):
        angle = 0 if tower is None else math.radians((tower - 1) * 60)
        radius = 0 if tower is None else 33
        shape -= b.Pos(radius * math.cos(angle), radius * math.sin(angle), UPPER_LIFT) * cylinder(3.8, 105, 115)
    return shape


def cap_boot():
    outer = cylinder(8, 100, 116) + b.Pos(0, 0, 119.5) * b.Cone(8, 5.2, 7)
    outer += cylinder(5.2, 123, 128)
    return outer - cylinder(6.1, 99, 113) - cylinder(3.6, 112.8, 129)


def cap_contact():
    cup = cylinder(3.7, 106, 112) - cylinder(3, 105, 111)
    return cup + b.Pos(0, 0, 114) * b.Cone(3.7, 1.2, 4)


def plug_boot():
    outer = cylinder(8.2, 20, 48) + cylinder(5.2, 48, 68)
    return outer - cylinder(6.25, 19, 45) - cylinder(4.3, 44, 46) - cylinder(3.6, 46, 69)


def plug_contact():
    return cylinder(4.1, 38, 46) - cylinder(3.5, 37, 44)


def coil_boot():
    outer = cylinder(10, 40, 58) + b.Pos(0, 0, 65) * b.Cone(10, 5.2, 14) + cylinder(5.2, 72, 80)
    return outer - cylinder(8.1, 39, 52) - cylinder(5.1, 51.8, 60) - cylinder(3.6, 59.8, 81)


def coil_contact():
    cup = cylinder(5, 52.5, 58) - cylinder(4.5, 52, 55.5)
    return cup + b.Pos(0, 0, 60) * b.Cone(5, 1.2, 4)


def cable(path, frame):
    transverse = (0, 1, 0) if abs(direction(frame).X) > .9 else (1, 0, 0)
    plane = b.Plane(origin=path @ 0, x_dir=transverse, z_dir=direction(frame))
    frenet = abs(direction(frame).X) <= .9
    jacket = b.sweep(plane * (b.Circle(3.5) - b.Circle(1.05)), path=path, is_frenet=frenet)
    core = b.sweep(plane * b.Circle(1), path=path, is_frenet=frenet)
    return jacket, core


def plug_path(cylinder_number):
    tower = TOWER_BY_CYLINDER[cylinder_number]
    start_frame, end_frame = cap_frame(tower), plug_frame(cylinder_number)
    start, exit_point = point(start_frame, 116), point(start_frame, 145)
    approach, end = point(end_frame, 80), point(end_frame, 46)
    lane = b.Vector((exit_point.X + approach.X) / 2, LANE_Y[cylinder_number], 340 + cylinder_number * 12)
    travel = b.Vector(math.copysign(min(60, abs(exit_point.X - approach.X) / 4), approach.X - exit_point.X), 0, 0)
    first = b.Bezier(exit_point, exit_point + direction(start_frame) * 20, lane - travel, lane)
    second = b.Bezier(lane, lane + travel, approach + direction(end_frame) * 50, approach)
    return b.Wire([b.Line(start, exit_point), first, second, b.Line(approach, end)])


def coil_frame():
    return COIL_FRAME * b.Pos(0, 0, 22) * b.Rot(0, 90, 0)


def coil_path():
    start_frame, end_frame = coil_frame(), cap_frame()
    start, exit_point = point(start_frame, 62), point(start_frame, 92)
    approach, end = point(end_frame, 175), point(end_frame, 116)
    lane = b.Vector(130, 300, 400)
    first = b.Bezier(exit_point, exit_point + b.Vector(50, 0, 0), lane - b.Vector(20, 0, 0), lane)
    second = b.Bezier(lane, lane + b.Vector(20, 0, 0), approach + direction(end_frame) * 50, approach)
    return b.Wire([b.Line(start, exit_point), first, second, b.Line(approach, end)])


def coil_bracket():
    bracket = b.Pos(-39.9, 254, 222.5) * b.Box(88.2, 8, 3)
    for station in (-78, -1.8):
        bracket += b.Pos(station, 210, 222.5) * b.Box(10, 90, 3)
        bracket += b.Pos(station, 254, 271.25) * b.Box(10, 3, 100.5)
        bracket += b.Pos(station, 186, 320) * b.Box(10, 139, 3)
        for lateral in (177, 243):
            bracket -= b.Pos(station, lateral, 223) * b.Cylinder(2.8, 8)
    bracket += b.Pos(-50, 116.5, 320) * b.Box(120, 3, 22)
    for station in (-95, -20):
        bracket -= b.Solid.make_cylinder(3.2, 12, b.Plane(origin=(station, 111, 320), z_dir=(0, 1, 0)))
    return bracket


def head_interface(shape):
    for station in (-95, -20):
        frame = b.Plane(origin=(station, 105, 320 - HEAD_WORLD_Z), z_dir=(0, 1, 0))
        shape += b.Solid.make_cylinder(9, 10, frame)
        shape -= b.Solid.make_cylinder(3.15, 20, b.Plane(origin=(station, 96, 320 - HEAD_WORLD_Z), z_dir=(0, 1, 0)))
    return shape


def fastener(radius, lower, upper, head_radius, head_height):
    return cylinder(radius, lower, upper) + b.Pos(0, 0, upper) * b.extrude(b.RegularPolygon(head_radius, 6), amount=head_height)


def parts():
    result = {}
    for cylinder_number in range(1, 7):
        prefix = f'ignition-lead-{cylinder_number}'
        start_frame, end_frame = cap_frame(TOWER_BY_CYLINDER[cylinder_number]), plug_frame(cylinder_number)
        jacket, core = cable(plug_path(cylinder_number), start_frame)
        result[prefix + '-jacket'] = jacket
        result[prefix + '-carbon-core'] = core
        result[prefix + '-cap-boot'] = start_frame * cap_boot()
        result[prefix + '-cap-contact'] = start_frame * cap_contact()
        result[prefix + '-plug-boot'] = end_frame * plug_boot()
        result[prefix + '-plug-contact'] = end_frame * plug_contact()
    jacket, core = cable(coil_path(), coil_frame())
    result['ignition-coil-lead-jacket'] = jacket
    result['ignition-coil-lead-carbon-core'] = core
    result['ignition-coil-lead-cap-boot'] = cap_frame() * cap_boot()
    result['ignition-coil-lead-cap-contact'] = cap_frame() * cap_contact()
    result['ignition-coil-lead-coil-boot'] = coil_frame() * coil_boot()
    result['ignition-coil-lead-coil-contact'] = coil_frame() * coil_contact()
    result['ignition-coil-bracket'] = coil_bracket()
    for index, (station, lateral) in enumerate([(station, lateral) for station in (-78, -1.8) for lateral in (177, 243)], 1):
        result[f'ignition-coil-bracket-screw-{index}'] = b.Pos(station, lateral, 0) * fastener(2.5, 219, 246, 4.25, 3)
    for index, station in enumerate((-95, -20), 1):
        frame = b.Pos(station, 0, 320) * b.Rot(-90, 0, 0)
        result[f'ignition-coil-bracket-head-bolt-{index}'] = frame * fastener(3, 100, 118, 5.5, 4.5)
    return result


def build(api):
    define, add, group = api
    group('ignition-leads', 'Secondary ignition leads · routed study', 'ignition')
    group('ignition-coil-mount', 'Ignition coil mounting bracket · provisional', 'ignition')
    for cylinder_number in range(1, 7):
        group(f'ignition-lead-{cylinder_number}-assembly', f'Cylinder {cylinder_number} ignition lead', 'ignition-leads')
    group('ignition-coil-lead-assembly', 'Coil-to-distributor lead', 'ignition-leads')
    for identifier, shape in parts().items():
        mounting = 'bracket' in identifier
        name = identifier.replace('-', ' ').capitalize()
        if identifier.endswith('carbon-core'):
            function, color = 'Aggregate carbon-impregnated fiber conductor carries the secondary ignition signal. Individual fibers, resistance and voltage are not simulated.', '#45423c'
        elif identifier.endswith('jacket'):
            function, color = 'Hollow rubber insulation surrounds the separate carbon core. Route and diameter are provisional.', '#343c45'
        elif identifier.endswith('boot'):
            function, color = 'Separate insulating boot encloses the terminal and cable entry. Production contour and sealing compression remain unverified.', '#343c45'
        elif identifier.endswith('contact'):
            function, color = 'Conductive terminal cup joins the cable core to its coil, cap or plug contact. Clip construction and dimensions are provisional.', '#b9a576'
        else:
            function, color = 'Supports the ignition coil on modeled head bosses. Geometry, fasteners and production mounting architecture are provisional.', '#82949b'
        define(identifier, shape, name, function, 'ignition', color, SOURCES, GAPS)
        parent = 'ignition-coil-mount' if mounting else 'ignition-coil-lead-assembly' if identifier.startswith('ignition-coil-lead-') else '-'.join(identifier.split('-')[:3]) + '-assembly'
        if mounting:
            explode=(0,100,30 if identifier=='ignition-coil-bracket' else 100)
        elif identifier.endswith('carbon-core'):
            explode=(0,280,30)
        elif identifier.endswith('cap-boot'):
            explode=(0,180,100)
        elif identifier.endswith('cap-contact'):
            explode=(0,180,170)
        elif identifier.endswith('boot'):
            explode=(0,180,-100)
        elif identifier.endswith('contact'):
            explode=(0,180,-170)
        else:
            explode=(0,180,30)
        add(identifier, identifier, parent, explode=explode)
