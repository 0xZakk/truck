"""FS10 double-acting construction study, not an installed-unit reproduction."""
import math
import build123d as b

POSITION = (373.56, 280, 100)
PULLEY_POSITION = (473.56, 280, 100)
TILT = 18
PITCH = 37
SOURCES = ['denso-fs10-application', 'ford-fs10-construction-comparison',
           'fs10-dissection-comparison', 'fs10-separated-parts-photo', 'ford-ac-clutch-gap', 'uac-fs10-101220c', 'fs10-piston-ring-photo']
GAPS = [
    'DENSO identifies FS10 471-8130 for the 1990–95 F-150 4.9 factory-A/C branch. Owner photos show A/C, but installed identity and factory/dealer branch are unresolved.',
    'Five double-ended pistons, ten shoes, swashplate/shaft, two cylinder halves and valve/reed stacks follow Ford FS10 architecture and a 1998 Crown Victoria dissection. This is not truck-specific teardown evidence.',
    'UAC CO101220C supplies a 145 mm clutch diameter and six grooves for 1990–95 F-series 4.9. Diameter is used as an outside envelope, not a verified belt pitch diameter. Its 93 mm tangent mount width lacks a diagrammed datum and is not yet applied. Case diameter, cylinder pitch/bore, 18 degree swash angle, groove profile, axial lengths, mount ears and manifold ports remain provisional.',
    'Clutch static gap is 0.6 mm, within the Ford 1994 specification 0.4572–0.8382 mm. Friction, electromagnetics, refrigerant, oil and thermodynamics are not simulated.',
    'Piston displacement and shoe face orientation are analytic swashplate relationships; checked discrete poses do not prove production motion, pressure sealing or continuous clearance.',
    'Thrust rolling elements and pulley bearing are envelope cartridges, not counted rollers. Reed flexure, shaft splines, seals, fastener threads, piston coatings and manufacturing fits are simplified.',
    'Ten separate piston seal rings follow the PTFE rings identified in the comparison teardown; ring profiles and grooves are provisional. Head suction/discharge annuli are separated, but longitudinal refrigerant passages between heads are not reconstructed; no closed fluid network is claimed.',
    'Mount ears at X432.56, Y210/350, Z60/140 and the X473.56 belt center are shared provisional accessory-bracket interfaces, not measured truck locations. Vehicle refrigerant lines are omitted.'
]


def cylinder(radius, length, center=0):
    return b.Pos(0, 0, center) * b.Cylinder(radius, length)


def ring(outer, inner, length, center=0):
    return cylinder(outer, length, center) - cylinder(inner, length + 2, center)


def axis_position(index):
    angle = math.radians(index * 72)
    return PITCH * math.cos(angle), PITCH * math.sin(angle)


def displacement(index, phase):
    horizontal, vertical = axis_position(index)
    rotation = math.radians(phase)
    return -math.tan(math.radians(TILT)) * (horizontal * math.cos(rotation) + vertical * math.sin(rotation))


def case(front):
    direction = 1 if front else -1
    shape = ring(65, 10.2, 69.5, direction * 34.85)
    shape -= cylinder(54, 45, 0)
    shape -= cylinder(23.2, 66, 0)
    for index in range(5):
        horizontal, vertical = axis_position(index)
        shape -= b.Pos(horizontal, vertical) * cylinder(13, 145)
    if front:
        for horizontal in (-40, 40):
            for vertical in (-70, 70):
                shape += b.Pos(horizontal, vertical / 70 * 55, 53) * b.Box(22, 35, 12)
                shape += b.Pos(horizontal, vertical) * cylinder(11, 12, 53)
                shape -= b.Pos(horizontal, vertical) * cylinder(5.5, 16, 53)
    return bolt_holes(shape)


def bolt_holes(shape):
    for index in range(5):
        angle = math.radians(index * 72 + 36)
        shape -= b.Pos(59 * math.cos(angle), 59 * math.sin(angle)) * cylinder(3.1, 190)
    return shape


def valve_plate(direction):
    shape = ring(65, 10.2, 2, direction * 71)
    for index in range(5):
        angle = math.radians(index * 72)
        for radius in (31, 43):
            shape -= b.Pos(radius * math.cos(angle), radius * math.sin(angle)) * cylinder(3, 150)
    return bolt_holes(shape)


def reed(direction, outer):
    height = direction * (72.2 if outer else 69.8)
    shape = ring(64, 56, .2, height)
    for index in range(5):
        finger = b.Pos(44 if outer else 41, 0, height) * b.Box(28 if outer else 34, 7, .2)
        shape += b.Rot(0, 0, index * 72) * finger
    for index in range(5):
        angle = math.radians(index * 72)
        radius = 31 if outer else 43
        shape -= b.Pos(radius * math.cos(angle), radius * math.sin(angle)) * cylinder(3.2, 150)
    return bolt_holes(shape)


def head(direction):
    shape = ring(65, 10.2, 12, direction * 79)
    shape -= ring(35.5, 17, 10, direction * 74)
    shape -= ring(53, 38.5, 10, direction * 74)
    if direction > 0:
        shape += ring(24, 10.2, 14, 92)
        shape -= cylinder(17, 10, 85)
    else:
        shape += cylinder(17, 2, -86)
        for horizontal, vertical in ((-20, 20), (24, 38)):
            shape += b.Pos(horizontal, vertical, -89) * b.Box(24, 28, 12)
            shape -= b.Pos(horizontal, vertical) * cylinder(6, 25, -85)
    return bolt_holes(shape)


def piston(index, phase):
    horizontal, vertical = axis_position(index)
    offset = displacement(index, phase)
    shape = cylinder(12.8, 35, 25.5) + cylinder(12.8, 35, -25.5)
    shape += b.Rot(0, 0, index * 72) * b.Pos(11, 0, 0) * b.Box(2, 8, 80)
    for direction in (-1, 1):
        shape -= ring(14, 12.25, 4.2, direction * 31)
    for direction in (-1, 1):
        center = (direction * 3.2 * math.sin(math.radians(TILT)) * math.cos(math.radians(phase)),
                  direction * 3.2 * math.sin(math.radians(TILT)) * math.sin(math.radians(phase)),
                  direction * 3.2 * math.cos(math.radians(TILT)))
        shape -= b.Pos(*center) * b.Sphere(6.1)
    return b.Pos(horizontal, vertical, offset) * shape


def shoe(index, phase, direction):
    horizontal, vertical = axis_position(index)
    offset = displacement(index, phase)
    shape = b.Solid.make_sphere(6, angle1=0, angle2=90)
    if direction < 0:
        shape = b.Rot(180, 0, 0) * shape
    return b.Pos(horizontal, vertical, offset) * b.Rot(0, 0, phase) * b.Rot(0, TILT, 0) * b.Pos(0, 0, direction * 3.2) * shape


def pulley():
    shape = ring(72.5, 65, 24, 100) + ring(72.5, 35.2, 4, 110)
    for index in range(6):
        shape -= ring(74, 70.5, 2, 90 + index * 4)
    return shape


def components(phase=0):
    shapes = {}
    for direction, label in ((-1, 'rear'), (1, 'front')):
        shapes[f'ac-compressor-{label}-cylinder'] = case(direction > 0)
        shapes[f'ac-compressor-{label}-valve-plate'] = valve_plate(direction)
        shapes[f'ac-compressor-{label}-suction-reed'] = reed(direction, False)
        shapes[f'ac-compressor-{label}-discharge-reed'] = reed(direction, True)
        shapes[f'ac-compressor-{label}-head'] = head(direction)
        shapes[f'ac-compressor-{label}-head-seal'] = ring(55.8, 54.2, .6, direction * 72.65)
        shapes[f'ac-compressor-{label}-plenum-seal'] = ring(38, 36, .68, direction * 72.65)
        for index, (center, length) in enumerate(((24, 1), (26.1, 3), (28.2, 1))):
            shapes[f'ac-compressor-{label}-thrust-{index + 1}'] = ring(23, 10.1, length, direction * center)
    shapes['ac-compressor-case-seal'] = ring(55.8, 54.2, .18)
    shaft = cylinder(10, 190, 20)
    shaft += b.Rot(0, 0, phase) * b.Rot(0, TILT, 0) * cylinder(45.5, 6)
    shaft -= cylinder(3, 10, 113)
    shapes['ac-compressor-swashplate-shaft'] = shaft
    for index in range(5):
        shapes[f'ac-compressor-piston-{index + 1}'] = piston(index, phase)
        for direction, label in ((-1, 'rear'), (1, 'front')):
            shapes[f'ac-compressor-shoe-{index + 1}-{label}'] = shoe(index, phase, direction)
            horizontal, vertical = axis_position(index)
            shapes[f'ac-compressor-piston-{index + 1}-{label}-seal'] = b.Pos(horizontal, vertical, displacement(index, phase)) * ring(12.9, 12.3, 4, direction * 31)
        angle = math.radians(index * 72 + 36)
        bolt = cylinder(3, 168, 1) + b.Pos(0, 0, 85) * b.extrude(b.RegularPolygon(5, 6), amount=4)
        shapes[f'ac-compressor-case-bolt-{index + 1}'] = b.Pos(59 * math.cos(angle), 59 * math.sin(angle)) * bolt
    shapes['ac-compressor-shaft-seal'] = ring(16.8, 10.1, 6, 85)
    shapes['ac-compressor-seal-retainer'] = ring(16.8, 10.2, .8, 89)
    shapes['ac-compressor-pulley-bearing'] = ring(35, 24.1, 12, 102)
    shapes['ac-compressor-clutch-coil'] = ring(62, 36, 14, 96)
    shapes['ac-compressor-clutch-coil-carrier'] = ring(36, 24.1, 2, 90)
    shapes['ac-compressor-clutch-pulley'] = pulley()
    shapes['ac-compressor-pulley-snap-ring'] = ring(35, 24.1, .8, 108.6) - b.Pos(0, 35, 108.6) * b.Box(4, 25, 3)
    shapes['ac-compressor-armature-hub'] = ring(64, 10.1, 3, 114.1) + ring(18, 10.1, 3.8, 111)
    shapes['ac-compressor-hub-bolt'] = cylinder(2.9, 7, 112.5) + b.Pos(0, 0, 116) * b.extrude(b.RegularPolygon(5, 6), amount=3)
    return {identifier: b.Rot(0, 90, 0) * shape for identifier, shape in shapes.items()}


def parts(phase=0):
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in components(phase).items()}


def description(identifier):
    if 'piston' in identifier and 'seal' in identifier:
        return 'Circumferential PTFE piston seal ring, one on each end of a double-acting piston. Separate from the aluminum piston; profile, groove and running clearance are provisional.'
    if 'piston' in identifier:
        return 'Double-ended sliding piston. One head compresses while the other takes in refrigerant; the bridge receives two spherical shoes. Bore, stroke, bridge and socket geometry are illustrative.'
    if 'shoe' in identifier:
        return 'Spherical sliding shoe between one piston socket and one swashplate face. Its flat face follows the inclined plate while its curved back accommodates the piston motion; oil film and contact forces are not simulated.'
    if 'swashplate-shaft' in identifier:
        return 'Shaft and fixed inclined swashplate transmit clutch torque into reciprocating piston motion through ten shoes. The comparison supports the architecture, not the selected 18 degree angle or shaft dimensions.'
    if 'cylinder' in identifier:
        return 'One cylinder/case half guides five piston ends, surrounds the swash chamber and reacts bearing loads. The front half includes provisional bracket ears; connecting longitudinal refrigerant galleries remain unfinished.'
    if 'suction-reed' in identifier:
        return 'Thin suction reed sheet on the cylinder side of the valve plate. Five illustrative fingers cover inlet holes while discharge holes remain open; actual reed flexure and stop geometry are not simulated.'
    if 'discharge-reed' in identifier:
        return 'Thin discharge reed sheet on the head side of the valve plate. Five illustrative fingers cover outlet holes while inlet holes remain open; pressure-operated bending is explained rather than animated.'
    if 'valve-plate' in identifier:
        return 'Rigid end plate closes five cylinder bores and provides separate inlet and outlet holes beneath the reed sheets. Hole sizes, circular spacing and sealing lands are provisional.'
    if 'plenum-seal' in identifier:
        return 'Illustrative concentric divider seal between the head and valve stack, separating modeled suction and discharge annuli. It is not a sourced gasket profile or a validated pressure seal.'
    if 'head-seal' in identifier:
        return 'Outer head-to-valve-stack refrigerant seal envelope. Actual groove section, elastomer, squeeze and factory sealing detail remain unmeasured.'
    if identifier.endswith('-head'):
        return 'End head contains separate illustrative suction and discharge annuli. The rear head carries two open manifold stubs; the front head carries the shaft nose. Longitudinal communication between heads remains absent.'
    if 'thrust' in identifier:
        return 'Axial thrust rolling-element cartridge between separate races; individual rollers, cage and element count are unresolved.' if identifier.endswith('-2') else 'Separate thrust-bearing race transfers axial load between the rotating swash assembly and its rolling-element cartridge. Material, thickness and seating are provisional.'
    if 'case-bolt' in identifier:
        return 'Illustrative long case bolt holds the cylinder halves and end stacks together. Five-bolt layout, engagement and head geometry are provisional; thread helices and preload are omitted.'
    details = {
        'case-seal': 'Mid-case sealing ring between the two cylinder halves. The continuous envelope marks the case joint; actual O-ring section and compression are not reconstructed.',
        'shaft-seal': 'Front rotating-shaft refrigerant seal envelope. It separates the compressor interior from the clutch nose; actual lip construction, contact pressure and oil film are unresolved.',
        'seal-retainer': 'Separate front shaft-seal retaining ring envelope. Factory retention section and installation method are not reproduced.',
        'pulley-bearing': 'Bearing cartridge allows the belt pulley to rotate on the stationary nose when the clutch is disengaged. Individual rolling elements and exact bearing specification remain unresolved.',
        'clutch-coil': 'Stationary electromagnetic coil envelope. Energizing the real coil attracts the armature across the clutch air gap; windings, connector, magnetic field and current are not simulated.',
        'clutch-coil-carrier': 'Stationary carrier supports the coil around the compressor nose. This separate support envelope is not the rotating pulley or the armature hub.',
        'clutch-pulley': 'Belt-driven rotor and six-groove pulley supported on its own bearing. UAC supplies the 145 mm clutch diameter and six grooves; groove profile, pitch diameter and axial belt position remain provisional.',
        'pulley-snap-ring': 'Split retaining-ring envelope locates the pulley-bearing stack on the nose. Groove dimensions and spring action are provisional.',
        'armature-hub': 'Separate clutch armature and shaft hub receive torque when attracted against the pulley friction face. The static 0.6 mm face gap falls within Ford specification; splines and compliant links are simplified.',
        'hub-bolt': 'Central retaining bolt envelope secures the armature hub to the shaft. Bolt diameter, head, threads, shim stack and torque are not established by this model.'
    }
    return details[identifier.removeprefix('ac-compressor-')]


def build(api):
    define, add, group = api
    group('ac-compressor', 'FS10 A/C compressor · provisional construction study', 'accessory-drive')
    for index, (identifier, shape) in enumerate(components().items()):
        title = identifier.removeprefix('ac-compressor-').replace('-', ' ').title()
        color = '#b9bec2' if any(word in identifier for word in ('cylinder', 'head', 'piston')) else '#626b73'
        if any(word in identifier for word in ('seal', 'coil')):
            color = '#383b3c'
        if 'piston' in identifier and 'seal' in identifier:
            color = '#b6a57d'
        define(identifier, shape, 'FS10 ' + title, description(identifier), 'accessory-drive', color, SOURCES, GAPS)
        add(identifier, identifier, 'ac-compressor', POSITION, (100 + index * 5, 200, 50))
