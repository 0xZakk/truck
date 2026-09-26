"""Conjugate four/five gerotor study; production dimensions remain unverified."""
import math
import build123d as b

ECCENTRICITY = 3.5
INNER_TEETH = 4
OUTER_TEETH = 5
CUTTER_ORBIT = 26.0
CUTTER_RADIUS = 8.0
ROOT_RADIUS = 26.5
OUTER_RADIUS = 29.3
PROFILE_CLEARANCE = .025
SOURCES = ['fsm-6f023139b5f8', 'fsm-59c6d1fb5ae3', 'gerotor-conjugate-profile-liu-2015']
GAPS = ['The four/five tooth interpretation, all rotor dimensions, 3.5 mm eccentricity, D-flat coupling and running clearances remain provisional, not production measurements.',
        'The inner profile is the inward normal offset of the circular-cutter center trochoid; its periodic spline is a numerical approximation of the analytic conjugate envelope.',
        'Coordinated rigid-body kinematics do not simulate oil pressure, leakage, elastic tooth contact, friction or hydrodynamic lubrication.']


def inner_points(count=720):
    points = []
    for index in range(count):
        angle = math.tau * index / count
        center_x = CUTTER_ORBIT * math.cos(angle) - ECCENTRICITY * math.cos(OUTER_TEETH * angle)
        center_y = CUTTER_ORBIT * math.sin(angle) - ECCENTRICITY * math.sin(OUTER_TEETH * angle)
        tangent_x = -CUTTER_ORBIT * math.sin(angle) + ECCENTRICITY * OUTER_TEETH * math.sin(OUTER_TEETH * angle)
        tangent_y = CUTTER_ORBIT * math.cos(angle) - ECCENTRICITY * OUTER_TEETH * math.cos(OUTER_TEETH * angle)
        speed = math.hypot(tangent_x, tangent_y)
        offset = CUTTER_RADIUS + PROFILE_CLEARANCE
        points.append((center_x - offset * tangent_y / speed, center_y + offset * tangent_x / speed))
    return points


def d_bore(radius=4.78, flat=3.73, height=30):
    return b.Cylinder(radius, height) & b.Pos(flat - 20, 0, 0) * b.Box(40, 40, height)


def inner_rotor():
    edge = b.Spline(*inner_points(), periodic=True)
    return b.extrude(b.Face(b.Wire(edge)), amount=12, both=True) - d_bore()


def outer_cavity():
    cavity = b.Cylinder(ROOT_RADIUS, 30)
    for index in range(OUTER_TEETH):
        angle = math.tau * index / OUTER_TEETH
        cavity -= b.Pos(CUTTER_ORBIT * math.cos(angle), CUTTER_ORBIT * math.sin(angle), 0) * b.Cylinder(CUTTER_RADIUS, 32)
    return cavity


def outer_rotor():
    return b.Cylinder(OUTER_RADIUS, 24) - outer_cavity()


def shaft_interface(shape):
    return shape - b.Pos(13.7, 0, -8.5) * b.Box(20, 30, 25)


def motion_descriptors():
    return {
        'oil-pump-intermediate-rotation': {'type': 'rotary', 'axis': 'z', 'ratio': -.5},
        'oil-pump-inner-rotation': {'type': 'rotary', 'axis': 'z', 'ratio': -.5},
        'oil-pump-outer-rotation': {'type': 'rotary', 'axis': 'z', 'ratio': -.4},
    }


def rotor_poses(crank_degrees):
    return (b.Pos(ECCENTRICITY, 0, -3.85) * b.Rot(0, 0, -crank_degrees / 2),
            b.Pos(0, 0, -3.85) * b.Rot(0, 0, -crank_degrees * INNER_TEETH / OUTER_TEETH / 2))


def pump_api(api):
    define, add, group, cylinder_x, spring = api

    def define_part(identifier, shape, name, function, system, color='#8498a3', sources=(), gaps=(), claims=()):
        gaps = [gap for gap in gaps if 'illustrative profiles' not in gap]
        if identifier == 'oil-pump-inner-rotor':
            shape = inner_rotor()
            function = 'Four-lobe conjugate-envelope rotor turns at distributor speed around the eccentric pump shaft. A provisional D-flat transmits torque; no pressure simulation is performed.'
        elif identifier == 'oil-pump-outer-rotor':
            shape = outer_rotor()
            function = 'Five circular-arc teeth mesh with the generated inner profile; this rotor turns in the same direction at four-fifths inner speed.'
        elif identifier == 'oil-pump-rotor-shaft':
            shape = shaft_interface(shape)
            function = 'Co-rotates with the distributor and intermediate shaft. A matching upper hex socket and provisional lower D-flat couple the shaft to the inner rotor.'
        if identifier in ('oil-pump-inner-rotor', 'oil-pump-outer-rotor', 'oil-pump-rotor-shaft'):
            sources = list(dict.fromkeys(list(sources) + SOURCES))
            gaps = list(gaps) + GAPS
        define(identifier, shape, name, function, system, color, sources, gaps, claims)

    def add_part(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
        if identifier in ('oil-pump-inner-rotor', 'oil-pump-rotor-shaft'):
            parent, pos = 'oil-pump-inner-rotation', (pos[0] - ECCENTRICITY, pos[1], pos[2])
        elif identifier == 'oil-pump-outer-rotor':
            parent = 'oil-pump-outer-rotation'
        add(identifier, definition, parent, pos, explode, rotation, name=name)

    def add_group(identifier, name, parent='engine', **kwargs):
        group(identifier, name, parent, **kwargs)
        if identifier == 'oil-pump-rotors':
            group('oil-pump-inner-rotation', 'Inner rotor and drive shaft', identifier,
                  position=(ECCENTRICITY, 0, 0), motion=motion_descriptors()['oil-pump-inner-rotation'])
            group('oil-pump-outer-rotation', 'Conjugate outer rotor', identifier,
                  motion=motion_descriptors()['oil-pump-outer-rotation'])

    return define_part, add_part, add_group, cylinder_x, spring


def drive_api(api):
    define, add, group = api

    def add_part(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0), name=None):
        if identifier in ('oil-pump-intermediate-shaft', 'oil-pump-drive-retainer'):
            parent = 'oil-pump-intermediate-rotation'
        add(identifier, definition, parent, pos, explode, rotation, name=name)

    def add_group(identifier, name, parent='engine', **kwargs):
        group(identifier, name, parent, **kwargs)
        if identifier == 'oil-drive-assembly':
            group('oil-pump-intermediate-rotation', 'Intermediate hex shaft and retainer', identifier,
                  motion=motion_descriptors()['oil-pump-intermediate-rotation'])

    return define, add_part, add_group
