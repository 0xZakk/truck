"""Isolated FS10 passage and rigid-motion revision; accepted base stays immutable."""
from functools import lru_cache
import math
import build123d as b
import ac_compressor as base
from accessory_belt_profile import regroove_x, SOURCES as BELT_PROFILE_SOURCES

POSITION = base.POSITION
PITCH = base.PITCH
TILT = base.TILT
AMPLITUDE = PITCH * math.tan(math.radians(TILT))
BALL_HEIGHT = 3.2 / math.cos(math.radians(TILT))
SOURCES = base.SOURCES + ['fs10-cylinder-passage-comparison'] + BELT_PROFILE_SOURCES
GAPS = [gap for gap in base.GAPS if 'Ten separate piston seal rings' not in gap]
GAPS += [
    'Ford describes gas-tight passages through the cylinder connecting both heads to rear suction/discharge ports. The two 4 mm longitudinal galleries, radial head-cap drillings, concentric plenums and full reed sheets are an illustrative connected topology, not traced production passages.',
    'Two fixed spherical sockets per piston allow rigid piston translation and shoe rotation without geometry morphing. The socket spacing and 18 degree swash inclination remain provisional.',
    'Independent compressor angle and engagement controls are not coupled to crank angle or a claimed belt pitch ratio. Engagement gates motion only; this simplified combined hub/armature does not flex or close its static gap.',
    'Disengagement resets the mechanism to its reference pose; it does not simulate physical run-down. Shared illustrative PK groove normalization uses 3.56 mm pitch and 40 degree flanks, not a traced Ford pulley section.',
    'Open-channel probes and seated-reed obstruction checks establish selected geometric routes, not a pressure-tight fluid simulation. Piston-ring clearances, oil films, reed lift and leakage are not solved.'
]


def axial(radius, length, center, direction=(0, 0, 1)):
    start = tuple(center[index] - direction[index] * length / 2 for index in range(3))
    return b.Part() + b.Solid.make_cylinder(radius, length, b.Plane(origin=start, z_dir=direction))


def galleries(radius=2):
    return [axial(radius, 164, (0, vertical, 0)) for vertical in (59, -59)]


def head_branches(direction, radius=2):
    passages = []
    for inner, outer in ((28, 59), (-45, -59)):
        passages.append(axial(radius, abs(outer - inner), (0, (inner + outer) / 2, direction * 82), (0, 1, 0)))
        passages.append(axial(radius, 6, (0, inner, direction * 79)))
    return passages


def cut_galleries(shape):
    for passage in galleries():
        shape -= passage
    return shape


def cylinder_half(direction):
    face = base.ring(65, 10.2, .2, direction * 69.7)
    for index in range(5):
        horizontal, vertical = base.axis_position(index)
        face -= b.Pos(horizontal, vertical) * base.cylinder(13, 145)
    return cut_galleries(base.case(direction > 0) + base.bolt_holes(face))


def reed(direction, outer):
    height = direction * (72.1 if outer else 69.9)
    shape = base.ring(65, 10.2, .2, height)
    for index in range(5):
        rotation = b.Rot(0, 0, index * 72)
        open_port = 31 if outer else 43
        shape -= rotation * b.Pos(open_port, 0) * base.cylinder(3.2, 150)
        midpoint = 42 if outer else 32.5
        endpoint = 47 if outer else 27
        for tangent in (-3.6, 3.6):
            shape -= rotation * b.Pos(midpoint, tangent, height) * b.Box(10 if outer else 11, .2, 1)
        shape -= rotation * b.Pos(endpoint, 0, height) * b.Box(.2, 7.4, 1)
    return cut_galleries(base.bolt_holes(shape))


def piston(index):
    horizontal, vertical = base.axis_position(index)
    shape = base.cylinder(12.8, 35, 25.5) + base.cylinder(12.8, 35, -25.5)
    shape += b.Rot(0, 0, index * 72) * b.Pos(11, 0, 0) * b.Box(2, 8, 80)
    for direction in (-1, 1):
        shape -= base.ring(14, 12.25, 4.2, direction * 31)
        shape -= b.Pos(0, 0, direction * BALL_HEIGHT) * b.Sphere(6.1)
    return b.Pos(horizontal, vertical, base.displacement(index, 0)) * shape


def shoe(index, direction):
    horizontal, vertical = base.axis_position(index)
    shape = b.Solid.make_sphere(6, angle1=0, angle2=90)
    if direction < 0:
        shape = b.Rot(180, 0, 0) * shape
    return b.Pos(horizontal, vertical, base.displacement(index, 0) + direction * BALL_HEIGHT) * b.Rot(0, TILT, 0) * shape


@lru_cache(maxsize=1)
def home_components():
    shapes = base.components(0)
    replacements = {}
    for direction, label in ((-1, 'rear'), (1, 'front')):
        replacements[f'ac-compressor-{label}-cylinder'] = cylinder_half(direction)
        replacements[f'ac-compressor-{label}-valve-plate'] = cut_galleries(base.valve_plate(direction))
        replacements[f'ac-compressor-{label}-suction-reed'] = reed(direction, False)
        replacements[f'ac-compressor-{label}-discharge-reed'] = reed(direction, True)
        head = cut_galleries(base.head(direction))
        for passage in head_branches(direction):
            head -= passage
        replacements[f'ac-compressor-{label}-head'] = head
        replacements[f'ac-compressor-{label}-head-seal'] = cut_galleries(base.bolt_holes(base.ring(65, 54.2, .8, direction * 72.6)))
        replacements[f'ac-compressor-{label}-plenum-seal'] = base.ring(38.5, 35.5, .8, direction * 72.6)
    replacements['ac-compressor-case-seal'] = cut_galleries(base.bolt_holes(base.ring(65, 54, .2)))
    for index in range(5):
        replacements[f'ac-compressor-piston-{index + 1}'] = piston(index)
        for direction, label in ((-1, 'rear'), (1, 'front')):
            replacements[f'ac-compressor-shoe-{index + 1}-{label}'] = shoe(index, direction)
    shapes.update({identifier: b.Rot(0, 90, 0) * shape for identifier, shape in replacements.items()})
    shapes['ac-compressor-clutch-pulley'] = regroove_x(shapes['ac-compressor-clutch-pulley'], 72.5, (100, 0, 0))
    assert len(shapes) == 61
    return shapes


def descriptor(identifier):
    if 'piston-' in identifier or 'shoe-' in identifier:
        index = int(identifier.split('-')[3]) - 1
        return {'type': 'fs10', 'role': 'shoe' if 'shoe-' in identifier else 'piston',
                'cylinder_phase_deg': index * 72, 'stroke_amplitude_mm': AMPLITUDE}
    if identifier in ('ac-compressor-swashplate-shaft', 'ac-compressor-armature-hub', 'ac-compressor-hub-bolt'):
        return {'type': 'fs10', 'role': 'shaft'}
    if identifier == 'ac-compressor-clutch-pulley':
        return {'type': 'fs10', 'role': 'pulley'}
    return None


def motion_pose(motion, compressor_degrees=0, compressor_engaged=False):
    role = motion['role']
    phase = compressor_degrees if role == 'pulley' or compressor_engaged else 0
    if not math.isfinite(phase):
        raise ValueError('FS10 control angle must be finite')
    if role in ('shaft', 'pulley'):
        return b.Rot(phase, 0, 0)
    angle = math.radians(motion['cylinder_phase_deg'])
    displacement = motion['stroke_amplitude_mm'] * (math.cos(angle) - math.cos(angle - math.radians(phase)))
    if role == 'piston':
        return b.Pos(displacement, 0, 0)
    if role == 'shoe':
        return b.Pos(displacement, 0, 0) * b.Rot(phase, 0, 0)
    raise ValueError('Unknown FS10 motion role')


def group_center(identifier):
    if 'shoe-' not in identifier:
        return (0, 0, 0)
    index = int(identifier.split('-')[3]) - 1
    direction = -1 if identifier.endswith('-rear') else 1
    horizontal, vertical = base.axis_position(index)
    return (base.displacement(index, 0) + direction * BALL_HEIGHT, vertical, -horizontal)


def components(phase=0, engaged=True):
    result = {}
    for identifier, shape in home_components().items():
        motion = descriptor(identifier)
        if motion:
            center = group_center(identifier)
            shape = b.Pos(*center) * motion_pose(motion, phase, engaged) * b.Pos(*(-value for value in center)) * shape
        result[identifier] = shape
    return result


def parts(phase=0, engaged=True):
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in components(phase, engaged).items()}


def flow_networks():
    networks = {}
    for label, inner, outer, gallery_y, branch_y, port in (
            ('suction', 17.3, 35.2, 59, 28, (-20, 20)),
            ('discharge', 38.8, 52.7, -59, -45, (24, 38))):
        shape = axial(1.4, 164, (0, gallery_y, 0))
        for direction in (-1, 1):
            shape += axial(1.4, abs(gallery_y - branch_y), (0, (gallery_y + branch_y) / 2, direction * 82), (0, 1, 0))
            shape += axial(1.4, 6, (0, branch_y, direction * 79))
            shape += base.ring(outer, inner, 5.6, direction * 76)
        shape += axial(5.2, 20, (port[0], port[1], -86.5))
        networks[label] = b.Pos(*POSITION) * b.Rot(0, 90, 0) * shape
    return networks


def valve_probes():
    probes = {}
    for direction, end in ((-1, 'rear'), (1, 'front')):
        for index in range(5):
            angle = math.radians(index * 72)
            for label, radius in (('suction', 31), ('discharge', 43)):
                local = axial(1, 4, (radius * math.cos(angle), radius * math.sin(angle), direction * 71))
                probes[f'{end}-{label}-{index + 1}'] = (f'ac-compressor-{end}-{label}-reed', b.Pos(*POSITION) * b.Rot(0, 90, 0) * local)
    return probes


def explode_vector(identifier):
    if 'piston-' in identifier or 'shoe-' in identifier:
        index = int(identifier.split('-')[3]) - 1
        angle = math.radians(index * 72)
        radius = 140 if 'shoe-' in identifier else 95
        axial_offset = 0
        if 'shoe-' in identifier or identifier.endswith('-seal'):
            axial_offset = -45 if '-rear' in identifier else 45
        return (axial_offset, radius * math.sin(angle), -radius * math.cos(angle))
    if '-front-' in identifier or '-rear-' in identifier:
        direction = -1 if '-rear-' in identifier else 1
        offset = 240
        if 'cylinder' in identifier:
            offset = 100
        elif 'suction-reed' in identifier:
            offset = 160
        elif 'valve-plate' in identifier:
            offset = 190
        elif 'discharge-reed' in identifier:
            offset = 220
        elif 'head-seal' in identifier:
            return (direction * 250, 0, 70)
        elif 'plenum-seal' in identifier:
            return (direction * 250, 0, -70)
        elif 'thrust' in identifier:
            offset = 40 + 15 * int(identifier[-1])
        elif identifier.endswith('-head'):
            offset = 285
        return (direction * offset, 0, 0)
    if 'case-bolt-' in identifier:
        angle = math.radians((int(identifier[-1]) - 1) * 72 + 36)
        return (0, 150 * math.sin(angle), -150 * math.cos(angle))
    if identifier.endswith('case-seal'):
        return (0, 0, 170)
    if identifier.endswith('swashplate-shaft'):
        return (0, 0, 0)
    clutch_order = ['shaft-seal', 'seal-retainer', 'clutch-coil-carrier', 'clutch-coil',
                    'pulley-bearing', 'clutch-pulley', 'pulley-snap-ring', 'armature-hub', 'hub-bolt']
    return (330 + 30 * clutch_order.index(identifier.removeprefix('ac-compressor-')), 0, 0)


def build(api):
    define, add, group = api
    group('ac-compressor', 'FS10 A/C compressor · connected passage and rigid-motion study', 'accessory-drive', position=POSITION)
    created = set()
    for index, (identifier, shape) in enumerate(home_components().items()):
        motion = descriptor(identifier)
        parent = 'ac-compressor'
        if motion:
            if motion['role'] == 'piston':
                parent = '-'.join(identifier.split('-')[:4]) + '-motion'
            elif motion['role'] == 'shoe':
                parent = identifier + '-motion'
            else:
                parent = 'ac-compressor-' + motion['role'] + '-motion'
            center = group_center(identifier)
            shape = b.Pos(*(-value for value in center)) * shape
            if parent not in created:
                group(parent, parent.replace('-', ' ').title(), 'ac-compressor', motion, center)
                created.add(parent)
        title = identifier.removeprefix('ac-compressor-').replace('-', ' ').title()
        color = '#b9bec2' if any(word in identifier for word in ('cylinder', 'head', 'piston')) else '#626b73'
        if any(word in identifier for word in ('seal', 'coil')):
            color = '#383b3c'
        if 'piston' in identifier and 'seal' in identifier:
            color = '#b6a57d'
        text = base.description(identifier).replace('connecting longitudinal refrigerant galleries remain unfinished', 'two provisional longitudinal galleries connect the head plenums').replace('Longitudinal communication between heads remains absent.', 'Provisional isolated longitudinal galleries connect both heads.')
        define(identifier, shape, 'FS10 ' + title, text, 'accessory-drive', color, SOURCES, GAPS)
        add(identifier, identifier, parent, (0, 0, 0), explode_vector(identifier))
