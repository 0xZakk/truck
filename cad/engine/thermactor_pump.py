"""Thermactor exterior and support study; pumping cartridge remains unresolved."""
import math

import build123d as cad

from accessory_brackets import axial, boss, web, engine_foot, bolt

POSITION = (473.56, -280, 100)
ROTATION = (0, 90, 0)
SOURCES = ['ford-thermactor-study', 'ford-accessory-routing', 'ford-accessory-brackets']
GAPS = [
    'Ford identifies a belt-driven positive-displacement vane pump and illustrates its body, inlet, outlet and three-hole pulley hub. This interim model reconstructs the exterior interfaces, not the full internal pumping mechanism.',
    'The generic Ford truck description covers 19 and 22 cubic-inch pumps without assigning one to this installed engine. Neither displacement nor vane count is claimed. The pumping cartridge is one explicitly unresolved envelope.',
    'All dimensions, rotor-envelope form, bearing cartridges, shaft, pulley diameter/profile, six grooves, case fastener count and mounting-ear positions are illustrative. No aftermarket part identity or published generic comparison dimensions are treated as verified installed geometry.',
    'Station (473.56,-280,100) follows the labeled lower-RH A/P topology and provisional belt plane, not measured engine datums. Inlet filter, hoses, bypass/diverter valves and air-injection manifold connections remain unfinished.',
    'A separate assumed support connects the current pump ears to dry blind front-block bosses. Bracket casting, two mount bolts, two engine bolts and 14 mm smooth engagement envelopes are not factory dimensional evidence.',
    'No threads, bearing rolling elements, dynamic vane contact, pressure/flow, pump speed ratio or thermal/friction simulation. Collision-free geometry does not verify an emissions-system repair or production fit.'
]
CASE_BOLTS = [(53 * math.cos(math.radians(angle)), 53 * math.sin(math.radians(angle))) for angle in (30, 150, 270)]


def cylinder(radius, width, axial_position):
    return cad.Pos(0, 0, axial_position) * cad.Cylinder(radius, width)


def ring(outer, inner, width, axial_position):
    return cylinder(outer, width, axial_position) - cylinder(inner, width + 2, axial_position)


def case_holes(shape):
    for horizontal, vertical in CASE_BOLTS:
        shape -= cad.Pos(horizontal, vertical, 0) * cylinder(3.3, 106, -76)
    return shape


def housing():
    shape = ring(58, 50, 95, -80)
    shape += cad.Pos(0, -62, -92) * cad.Rot(90, 0, 0) * cad.Cylinder(13, 28)
    shape += cad.Pos(-62, 0, -55) * cad.Rot(0, 90, 0) * cad.Cylinder(10, 28)
    shape -= cad.Pos(0, -60, -92) * cad.Rot(90, 0, 0) * cad.Cylinder(10, 40)
    shape -= cad.Pos(-60, 0, -55) * cad.Rot(0, 90, 0) * cad.Cylinder(7, 40)
    return case_holes(shape)


def front_plate():
    shape = ring(58, 15, 8, -28.5) + ring(20, 15, 12.3, -18.35)
    for direction in (-1, 1):
        shape += cad.Pos(0, direction * 70, -28.5) * cad.Box(20, 40, 8)
        shape += cad.Pos(0, direction * 85, 0) * cylinder(11, 8, -28.5)
        shape -= cad.Pos(0, direction * 85, 0) * cylinder(5.5, 12, -28.5)
    return case_holes(shape)


def rear_plate():
    shape = cylinder(58, 6, -130.5) + cylinder(20, 12, -122.5)
    shape -= cylinder(15, 17, -120.5)
    return case_holes(shape)


def pulley():
    shape = ring(70, 64, 24, 0) + ring(65, 8.2, 4, -2)
    for index in range(6):
        center = (index - 2.5) * 3.6
        profile = cad.Plane.XZ * cad.Polygon((68.2, center), (71, center - 1), (71, center + 1), align=None)
        shape -= cad.revolve(profile, axis=cad.Axis.Z)
    for angle in (0, 120, 240):
        radians = math.radians(angle)
        shape -= cad.Pos(24 * math.cos(radians), 24 * math.sin(radians), 0) * cylinder(3.5, 8, -2)
    return shape


def hub():
    shape = ring(32, 7.9, 8, -8)
    for angle in (0, 120, 240):
        radians = math.radians(angle)
        shape -= cad.Pos(24 * math.cos(radians), 24 * math.sin(radians), 0) * cylinder(3.2, 10, -8)
    return shape


def components():
    result = {
        'thermactor-housing': housing(),
        'thermactor-front-plate': front_plate(),
        'thermactor-rear-plate': rear_plate(),
        'thermactor-shaft': cylinder(7.8, 119.5, -67.75),
        'thermactor-front-bearing': ring(14.9, 7.9, 14, -25),
        'thermactor-rear-bearing': ring(14.9, 7.9, 12, -121.5),
        'thermactor-pumping-cartridge': ring(43, 8, 70, -77.5),
        'thermactor-pulley-hub': hub(),
        'thermactor-pulley': pulley()
    }
    for index, angle in enumerate((0, 120, 240), 1):
        radians = math.radians(angle)
        shape = cylinder(2.9, 11, -5.5) + cad.extrude(cad.RegularPolygon(5.5, 6), amount=4)
        result[f'thermactor-pulley-bolt-{index}'] = cad.Pos(24 * math.cos(radians), 24 * math.sin(radians), 0) * shape
    for index, (horizontal, vertical) in enumerate(CASE_BOLTS, 1):
        shape = cylinder(3, 103, -76) + cad.Pos(0, 0, -24.5) * cad.extrude(cad.RegularPolygon(5.5, 6), amount=5)
        result[f'thermactor-case-bolt-{index}'] = cad.Pos(horizontal, vertical, 0) * shape
    return result


def support():
    face = POSITION[0] - 24.5
    shape = boss(face, -280, 100, 98, 78)
    for horizontal in (-195, -365):
        shape += boss(face, horizontal, 100, 11, 5.5)
    shape += web(face, (-190, 100), (-175, 100), 18)
    shape += web(face, (-175, 90), (-175, 180), 18)
    for vertical in (90, 180):
        shape += engine_foot(-100, vertical, face + 5, -175)
    for horizontal in (-195, -365):
        shape -= axial(5.5, 14, (face + 5, horizontal, 100))
    return shape


def block_interface(shape):
    for vertical in (90, 180):
        shape += axial(12, 24, (361, -100, vertical))
        shape -= axial(5.2, 17, (365.5, -100, vertical))
    return shape


def parts():
    mount = cad.Pos(*POSITION) * cad.Rot(*ROTATION)
    result = {identifier: mount * shape for identifier, shape in components().items()}
    result['thermactor-support-bracket'] = support()
    for index, horizontal in enumerate((-195, -365), 1):
        result[f'thermactor-mount-bolt-{index}'] = bolt(441.26, 459.06, horizontal, 100, 4.9)
    for index, vertical in enumerate((90, 180), 1):
        result[f'thermactor-engine-bolt-{index}'] = bolt(359, 385, -100, vertical, 4.9)
    return result


def build(api):
    define, add, group = api
    group('thermactor-pump-assembly', 'Thermactor pump · unresolved cartridge', 'accessory-drive')
    for index, (identifier, shape) in enumerate(parts().items()):
        name = identifier.replace('-', ' ').title()
        function = 'Belt-driven secondary-air pump component. Exterior architecture follows Ford; geometry and fitted interfaces remain provisional.'
        if identifier == 'thermactor-pumping-cartridge':
            name = 'Thermactor pumping cartridge · unresolved envelope'
            function = 'Reserved envelope for the untraced rotor, carbon vanes and internal pumping interfaces. This is not a single identified production part and does not establish vane count or displacement.'
        elif 'bracket' in identifier:
            function = 'Illustrates a separate engine support with dry blind block attachments. Exact casting and load path dimensions remain assumed.'
        elif 'bearing' in identifier:
            function = 'Unresolved bearing cartridge supports the shaft; races, rolling elements, fit and identity remain unknown.'
        define(identifier, shape, name, function, 'accessory-drive', '#484d50' if 'pulley' in identifier else '#98a2a4', SOURCES, GAPS)
        add(identifier, identifier, 'thermactor-pump-assembly', (0, 0, 0), (100 + index * 15, -50, 0))
