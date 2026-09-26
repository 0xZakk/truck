"""Integral-regulator alternator construction study, not verified installed geometry."""
import math

import build123d as cad

POSITION = (473.56, -325, 410)
ROTATION = (0, 90, 0)
SOURCES = ['ford-alternator-study', 'denso-alternator-construction', 'gates-1994-drive']
GAPS = [
    'The 1994 vehicle service archive lists 75, 95 and 130 amp variants; the installed rating and 2G/3G identity have not been verified. This is a 95-amp-oriented integral-regulator construction study, not an identified replacement part.',
    'Ford establishes a field coil, rotor, stator, brushes, internal rectifier, regulator and two mounting bolts. DENSO conventional-alternator cutaway is a generic construction comparison only, not evidence of a DENSO alternator on this truck.',
    'All dimensions, case vents, mounting-ear angles, four through-bolts, twelve claw poles, ten fan blades and six pulley grooves are illustrative. External fan configuration remains provisional pending installed alternator identification.',
    'The stator winding and rotor coil are volume envelopes, not individual winding turns; rectifier and regulator electronics are unresolved packages without invented diode or transistor arrangements.',
    'Bearings are unresolved cartridges. Fits, bearing identity, threads, materials, spring-loaded brush detail, wiring, terminals and electrical insulation clearances are not production reconstructions.',
    'Pulley center (473.56,-325,410) follows the current illustrative belt plane and Ford RH-front location only; lateral clearance is chosen against the current provisional intake. Bracket, belt routing, belt ratio and installed centers remain unresolved.',
]


def cylinder(radius, length, axial):
    return cad.Pos(0, 0, axial) * cad.Cylinder(radius, length)


def ring(outer, inner, length, axial):
    return cylinder(outer, length, axial) - cylinder(inner, length + 2, axial)


def case(front):
    axial, width, plate, bore = (-49, 31, -35.5, 20) if front else (-126, 35, -141.5, 17)
    shape = ring(64, 60, width, axial) + ring(64, bore, 4, plate)
    shape += ring(bore + 4, bore, 24 if front else 15, -47.5 if front else -134)
    for index in range(8):
        shape -= cad.Rot(0, 0, index * 45) * cad.Pos(40, 0, plate) * cad.Box(22, 8, 7)
    if front:
        for direction in (-1, 1):
            shape += cad.Pos(0, direction * 63, -45) * cad.Box(22, 25, 20)
            shape += cad.Pos(0, direction * 77, 0) * cylinder(12, 20, -45)
            shape -= cad.Pos(0, direction * 77, 0) * cylinder(5.5, 24, -45)
    for index in range(4):
        angle = math.radians(45 + index * 90)
        shape -= cad.Pos(62 * math.cos(angle), 62 * math.sin(angle), 0) * cylinder(2.6, 150, -87)
    return shape


def claw_pole(front):
    cap = -65 if front else -107
    shape = ring(42, 10, 5, cap)
    if not front:
        shape += ring(12.8, 10, 39.5, -87.25)
    for index in range(6):
        angle = math.radians(index * 60 + (30 if front else 0))
        half = math.radians(10)
        profile = cad.Polygon(
            (33 * math.cos(angle - half), 33 * math.sin(angle - half)),
            (42 * math.cos(angle - half), 42 * math.sin(angle - half)),
            (42 * math.cos(angle + half), 42 * math.sin(angle + half)),
            (33 * math.cos(angle + half), 33 * math.sin(angle + half)), align=None)
        shape += cad.Pos(0, 0, -102.5 if front else -104.5) * cad.extrude(profile, amount=35)
    return shape


def fan():
    shape = ring(50, 10, 2, -23)
    for index in range(10):
        shape += cad.Rot(0, 0, index * 36) * cad.Pos(35, 0, -26) * cad.Box(28, 1.5, 8)
    return shape


def pulley():
    shape = ring(35, 10, 24, 0)
    for index in range(6):
        axial = (index - 2.5) * 3.6
        profile = cad.Plane.XZ * cad.Polygon((33.4, axial), (36, axial - 1), (36, axial + 1), align=None)
        shape -= cad.revolve(profile, axis=cad.Axis.Z)
    return shape


def components():
    winding = ring(53.5, 44, 42, -86)
    winding += ring(58, 44, 8, -111) + ring(58, 44, 8, -61)
    holder = cad.Pos(0, 20, -155.5) * cad.Box(20, 15, 21)
    holder -= cylinder(13.2, 24, -155.5)
    for axial in (-151, -160):
        holder -= cad.Pos(0, 16.5, axial) * cad.Box(5.2, 8.2, 5.2)
    nut = cad.Pos(0, 0, 12) * cad.extrude(cad.RegularPolygon(15, 6), amount=7)
    nut -= cylinder(9.9, 9, 15.5)
    shapes = {
        'alternator-drive-housing': case(True),
        'alternator-rear-housing': case(False),
        'alternator-stator-core': ring(59, 54, 42, -86),
        'alternator-stator-winding': winding,
        'alternator-rotor-front-pole': claw_pole(True),
        'alternator-rotor-rear-pole': claw_pole(False),
        'alternator-field-coil': ring(30, 13, 30, -86),
        'alternator-shaft': cylinder(9.8, 186, -75),
        'alternator-front-bearing': ring(19.9, 10, 12, -49),
        'alternator-rear-bearing': ring(16.9, 10, 10, -133),
        'alternator-fan': fan(),
        'alternator-pulley-spacer': ring(14, 10, 9, -16.5),
        'alternator-pulley': pulley(),
        'alternator-pulley-nut': nut,
        'alternator-slip-ring-insulator': ring(11.7, 10, 18, -156),
        'alternator-brush-holder': holder,
        'alternator-regulator': cad.Pos(-32, 24, -150) * cad.Box(30, 30, 12),
        'alternator-rectifier': ring(56, 26, 7, -121),
    }
    for index, axial in enumerate((-151, -160), 1):
        shapes[f'alternator-slip-ring-{index}'] = ring(13, 11.8, 5, axial)
        shapes[f'alternator-brush-{index}'] = cad.Pos(0, 16, axial) * cad.Box(5, 6, 5)
    bolt = cylinder(2.2, 110, -87)
    bolt += cad.Pos(0, 0, -32) * cad.extrude(cad.RegularPolygon(4.2, 6), amount=4)
    for index in range(4):
        angle = math.radians(45 + index * 90)
        shapes[f'alternator-case-bolt-{index + 1}'] = cad.Pos(62 * math.cos(angle), 62 * math.sin(angle), 0) * bolt
    return shapes


def parts():
    mount = cad.Pos(*POSITION) * cad.Rot(*ROTATION)
    return {identifier: mount * shape for identifier, shape in components().items()}


def descriptions():
    result = {
        'alternator-drive-housing': ('Alternator drive housing', 'Supports the pulley-side bearing and two mounting ears. Vent, ear and bearing-seat geometry is illustrative; engine bracket remains unresolved.', '#a9adb0'),
        'alternator-rear-housing': ('Alternator rear housing', 'Supports the rear bearing and encloses the rectifier. Openings and bolt pattern are provisional.', '#a9adb0'),
        'alternator-stator-core': ('Alternator stator iron core', 'Provides the magnetic path around the rotating claw poles. Laminations and slot geometry are not individually reconstructed.', '#626a71'),
        'alternator-stator-winding': ('Alternator stator winding envelope', 'Stationary windings produce AC as rotor poles pass. Copper-colored volume shows the active winding and end-turn regions without claiming exact wire paths or turns.', '#b66d38'),
        'alternator-rotor-front-pole': ('Alternator rotor front claw pole', 'Interleaves with the opposite pole around the field coil. Six illustrative fingers per half are not a verified Ford pole count.', '#727b84'),
        'alternator-rotor-rear-pole': ('Alternator rotor rear claw pole and core', 'Carries the field-coil core and opposing magnetic fingers. The combined core and pole are an illustrative magnetic construction.', '#727b84'),
        'alternator-field-coil': ('Alternator rotor field-coil envelope', 'Field current magnetizes the rotor pole pieces. This is a coil-volume envelope; winding turns and leads remain unresolved.', '#c27a43'),
        'alternator-shaft': ('Alternator rotor shaft', 'Carries the pulley, rotor and slip rings. Diameters, shoulders, press fits and end threads remain provisional.', '#9da5ad'),
        'alternator-front-bearing': ('Alternator front bearing cartridge', 'Supports the pulley side of the rotor. Races, rolling elements, seals and production bearing identity remain unresolved.', '#84939f'),
        'alternator-rear-bearing': ('Alternator rear bearing cartridge', 'Supports the rear of the rotor shaft. Internal bearing construction and fit are not reconstructed.', '#84939f'),
        'alternator-fan': ('Alternator external cooling fan · provisional', 'Illustrates conventional-alternator cooling airflow through housing vents. External versus internal fan variant and blade geometry remain unverified for the installed unit.', '#777f85'),
        'alternator-pulley-spacer': ('Alternator pulley spacer · illustrative', 'Separates pulley and fan in the study stack. Production spacer identity and clamping stack remain unresolved.', '#9aa4ab'),
        'alternator-pulley': ('Alternator six-groove pulley · provisional', 'Transfers accessory-belt torque to the rotor. The 70 mm diameter, six-groove profile and ratio are illustrative; the belt plane is shared only as a modeling datum.', '#343c43'),
        'alternator-pulley-nut': ('Alternator pulley nut · illustrative', 'Represents axial retention of the pulley stack. Thread and torque specification are not modeled.', '#a4adb3'),
        'alternator-slip-ring-insulator': ('Alternator slip-ring insulating sleeve', 'Separates the rotating field-current contacts from the shaft. Geometry and electrical clearance are illustrative.', '#c7a15d'),
        'alternator-brush-holder': ('Alternator brush holder · illustrative', 'Locates two stationary brushes at the slip rings. Brush springs, guides and fixing screws remain unresolved.', '#363e45'),
        'alternator-regulator': ('Alternator regulator · unresolved electronics', 'Controls rotor field current to regulate charging voltage. Package is an envelope, without invented circuitry or connector pin placement.', '#35434d'),
        'alternator-rectifier': ('Alternator rectifier · unresolved electronics', 'Converts stator AC to DC. Annular volume locates the assembly; semiconductor count, heat sink, insulation and terminals remain unresolved.', '#586872'),
    }
    for index in (1, 2):
        result[f'alternator-slip-ring-{index}'] = (f'Alternator slip ring {index}', 'Provides a rotating contact for rotor field current. Ring section and electrical connections are illustrative.', '#d39a52')
        result[f'alternator-brush-{index}'] = (f'Alternator brush {index}', 'Contacts a slip ring to feed the rotor field. The carbon block is modeled; spring force and wire lead are unresolved.', '#30363a')
    for index in range(1, 5):
        result[f'alternator-case-bolt-{index}'] = (f'Alternator housing through-bolt {index} · illustrative', 'Shows housing retention through cleared bores. Count, dimensions, thread and production clamping fit remain provisional.', '#929ba1')
    return result


def build(api):
    define, add, group = api
    group('alternator-assembly', 'Alternator · construction study', 'accessory-drive')
    labels = descriptions()
    for index, (identifier, shape) in enumerate(components().items()):
        name, function, color = labels[identifier]
        define(identifier, shape, name, function, 'accessory-drive', color, SOURCES, GAPS)
        axial = shape.bounding_box().center().Z
        explode = (250 + 2.2 * (axial + 163), -100, 80 + index * 2)
        add(identifier, identifier, 'alternator-assembly', POSITION, explode, ROTATION)
