"""Ford accessory attachment topology with explicitly illustrative support castings."""
import math

import build123d as cad

SOURCES = ['ford-accessory-brackets', 'ford-accessory-routing', 'ford-cii-pump-study', 'ford-alternator-study']
GAPS = [
    'Ford identifies a shared power-steering/A/C bracket attached to block and head and a separate alternator bracket. These castings reconstruct that load-path topology, not a measured production casting.',
    'All boss coordinates, bolt counts, web sections, material colors, hole sizes and mounting-face locations are illustrative interfaces to the current component studies. Casting ribs, part numbers, dowels and factory contours remain unknown.',
    'Engine feet touch provisional front-face seats. Explicit interface adapters add isolated blind support bosses and 16 mm deep smooth thread-envelope bores; 14 mm bolt engagement is illustrative, not a verified thread specification. These are dry blind attachments, not coolant or oil passages.',
    'Accessory bolt shanks use clearance through the candidate mounting ears. Threads, grades, preload, bracket stiffness and belt-load deflection are not simulated.',
    'The Thermactor and tensioner engine brackets remain separate unresolved load paths. No unsupported air-pump attachment is added to these castings.'
]
PS_CENTER = (280, 410)
AC_CENTER = (280, 100)
ALT_CENTER = (-325, 410)
PS_FACE = 432.56
ALT_FACE = 438.56
PS_EARS = [(280 + 62 * math.sin(math.radians(angle)), 410 - 62 * math.cos(math.radians(angle)))
           for angle in (45, 165, 285)]
AC_EARS = [(horizontal, vertical) for horizontal in (210, 350) for vertical in (60, 140)]
ALT_EARS = [(-248, 410), (-402, 410)]


def axial(radius, length, center):
    return cad.Pos(*center) * cad.Rot(0, 90, 0) * cad.Cylinder(radius, length)


def boss(front, horizontal, vertical, outer, inner, width=10):
    center = (front + width / 2, horizontal, vertical)
    return axial(outer, width, center) - axial(inner, width + 2, center)


def web(front, start, end, width=14, depth=10):
    delta_y, delta_z = end[0] - start[0], end[1] - start[1]
    length = math.hypot(delta_y, delta_z)
    normal_y, normal_z = -delta_z / length * width / 2, delta_y / length * width / 2
    points = [(start[0] + normal_y, start[1] + normal_z),
              (end[0] + normal_y, end[1] + normal_z),
              (end[0] - normal_y, end[1] - normal_z),
              (start[0] - normal_y, start[1] - normal_z)]
    return cad.Pos(front, 0, 0) * cad.extrude(cad.Plane.YZ * cad.Polygon(*points, align=None), amount=depth, dir=(1, 0, 0))


def engine_foot(horizontal, vertical, target_x, target_y):
    shape = axial(16, 12, (379, horizontal, vertical))
    delta_x, delta_y = target_x - 379, target_y - horizontal
    length = math.hypot(delta_x, delta_y)
    normal_x, normal_y = -delta_y / length * 7, delta_x / length * 7
    profile = cad.Polygon((379 + normal_x, horizontal + normal_y),
                          (target_x + normal_x, target_y + normal_y),
                          (target_x - normal_x, target_y - normal_y),
                          (379 - normal_x, horizontal - normal_y), align=None)
    shape += cad.Pos(0, 0, vertical - 10) * cad.extrude(profile, amount=20, dir=(0, 0, 1))
    shape -= axial(5.5, 22, (379, horizontal, vertical))
    shape -= axial(11, 20, (395, horizontal, vertical))
    return shape & cad.Pos(673, 0, 0) * cad.Box(600, 2000, 2000)


def block_interface(shape):
    for horizontal in (90, -100):
        shape += axial(12, 24, (361, horizontal, 220))
        shape -= axial(5.2, 17, (365.5, horizontal, 220))
    return shape


def head_interface(shape):
    for horizontal, vertical in ((90, 300 - 255.5), (-100, 310 - 255.5)):
        shape += axial(12, 24, (361, horizontal, vertical))
        shape -= axial(5.2, 17, (365.5, horizontal, vertical))
    return shape


def power_steering_ac_bracket():
    shape = boss(PS_FACE, *PS_CENTER, 79, 68)
    for horizontal, vertical in PS_EARS:
        direction_y, direction_z = horizontal - 280, vertical - 410
        shape += web(PS_FACE, (horizontal, vertical), (280 + direction_y * 75 / 62, 410 + direction_z * 75 / 62))
        shape += boss(PS_FACE, horizontal, vertical, 10, 4.8)
    shape += web(PS_FACE, (205, 410), (205, 55), 18)
    shape += web(PS_FACE, (355, 410), (355, 55), 18)
    shape += web(PS_FACE, (205, 50), (355, 50), 18)
    for horizontal, vertical in AC_EARS:
        shape += boss(PS_FACE, horizontal, vertical, 11, 5.5)
    shape -= axial(68, 14, (PS_FACE + 5, *AC_CENTER))
    for vertical in (220, 300):
        shape += engine_foot(90, vertical, PS_FACE + 5, 205)
    for horizontal, vertical in PS_EARS:
        shape -= axial(4.8, 14, (PS_FACE + 5, horizontal, vertical))
    for horizontal, vertical in AC_EARS:
        shape -= axial(5.5, 14, (PS_FACE + 5, horizontal, vertical))
    return shape


def alternator_bracket():
    shape = boss(ALT_FACE, *ALT_CENTER, 88, 70)
    for horizontal, vertical in ALT_EARS:
        shape += boss(ALT_FACE, horizontal, vertical, 11, 5.5)
    shape += web(ALT_FACE, (-243, 410), (-200, 310), 18)
    shape += web(ALT_FACE, (-200, 310), (-200, 220), 18)
    for vertical in (220, 310):
        shape += engine_foot(-100, vertical, ALT_FACE + 5, -200)
    for horizontal, vertical in ALT_EARS:
        shape -= axial(5.5, 14, (ALT_FACE + 5, horizontal, vertical))
    return shape


def bolt(start, end, horizontal, vertical, radius):
    shape = axial(radius, end - start, ((start + end) / 2, horizontal, vertical))
    head = cad.extrude(cad.RegularPolygon(radius * 1.85, 6), amount=6)
    return shape + cad.Pos(end, horizontal, vertical) * cad.Rot(0, 90, 0) * head


def parts():
    result = {'ps-ac-support-bracket': power_steering_ac_bracket(), 'alternator-support-bracket': alternator_bracket()}
    for index, (horizontal, vertical) in enumerate(PS_EARS, 1):
        result[f'ps-bracket-bolt-{index}'] = bolt(424.76, 442.56, horizontal, vertical, 4.2)
    for index, (horizontal, vertical) in enumerate(AC_EARS, 1):
        result[f'ac-bracket-bolt-{index}'] = bolt(420.76, 442.56, horizontal, vertical, 4.9)
    for index, (horizontal, vertical) in enumerate(ALT_EARS, 1):
        result[f'alt-bracket-bolt-{index}'] = bolt(418.76, 448.56, horizontal, vertical, 4.9)
    for name, horizontal, levels in [('ps-ac', 90, (220, 300)), ('alt', -100, (220, 310))]:
        for index, vertical in enumerate(levels, 1):
            result[f'{name}-engine-bracket-bolt-{index}'] = bolt(359, 385, horizontal, vertical, 4.9)
    return result


def build(api):
    define, add, group = api
    group('accessory-support-brackets', 'Accessory brackets · provisional load paths', 'accessory-drive')
    for index, (identifier, shape) in enumerate(parts().items()):
        casting = identifier.endswith('support-bracket')
        name = ('Power-steering/A/C shared support' if identifier.startswith('ps-ac') else 'Alternator support') if casting else identifier.replace('-', ' ').title()
        function = 'Transfers accessory loads through separate feet to the provisional engine front faces. Factory attachment topology is sourced; the casting shape and interfaces are assumed.' if casting else 'Illustrates a clearance-fit clamp fastener. Smooth shank omits thread engagement, grade and production preload.'
        define(identifier, shape, name, function, 'accessory-drive', '#8b9598' if casting else '#a9afb2', SOURCES, GAPS)
        add(identifier, identifier, 'accessory-support-brackets', (0, 0, 0), (90 + index * 15, 0, 0))
