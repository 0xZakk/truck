"""Non-unique, uninstalled datum hypothesis constrained by the Gates belt length."""
import math

import build123d as cad

import accessory_belt
import accessory_belt_profile

CASE_NAME = 'clearance-constrained'
TARGETS = {'ALT': (-325, 350), 'TENS': (-160, 420), 'PS': (190, 350), 'AC': (245, 100), 'AP': (-235, 100)}
PREFIXES = {'ALT': ('alternator-',), 'TENS': ('tensioner-',), 'PS': ('ps-pump-',), 'AC': ('ac-compressor-',), 'AP': ('thermactor-',)}
DEPENDENT_BRACKETS = ('ps-ac-support-bracket', 'alternator-support-bracket', 'thermactor-support-bracket', 'tensioner-engine-bracket')
DEPENDENT_PREFIXES = ('ps-bracket-bolt-', 'ac-bracket-bolt-', 'alt-bracket-bolt-', 'ps-ac-engine-bracket-bolt-', 'alt-engine-bracket-bolt-', 'thermactor-engine-bolt-', 'tensioner-bracket-')
LIMITS = [
    'This is a non-unique analytical layout hypothesis, not measured Ford accessory coordinates or an accepted installation.',
    'The root engine, water pump, crankshaft and pulley diameters are fixed. Translated accessory bodies preserve all internal geometry; brackets and engine attachments must be redesigned before installation.',
    'Current outside radii are only an assumed effective-radius diagnostic. A near-zero nominal length residual does not prove actual Gates belt fit.',
    'The exploratory plus/minus ten-degree tensioner sweep is not a sourced working-angle range. Factory stops, spring preload, arm force, available take-up and installed index remain unknown.',
    'Low air-pump and tensioner wraps require traction, load and travel review. No minimum safe wrap, belt tension or accessory-power capacity is established.',
    'Oblique owner photographs support component identity and broad topology but are not calibrated front-view center measurements.'
]


def pulleys(tensioner_angle=0):
    result = [dict(node) for node in accessory_belt.PULLEYS]
    for node in result:
        if node['id'] in TARGETS:
            node['center'] = TARGETS[node['id']]
        if node['id'] == 'TENS':
            angle = math.radians(tensioner_angle)
            node['center'] = (TARGETS['TENS'][0] - 75 + 75 * math.cos(angle), TARGETS['TENS'][1] + 75 * math.sin(angle))
    return result


def dependent(identifier):
    return identifier in DEPENDENT_BRACKETS or identifier.startswith(DEPENDENT_PREFIXES) or identifier == 'accessory-serpentine-belt'


def assembly(identifier):
    if dependent(identifier):
        return None
    return next((name for name, prefixes in PREFIXES.items() if identifier.startswith(prefixes)), None)


def move(identifier, shape, tensioner_angle=0):
    name = assembly(identifier)
    if name is None:
        return shape
    old = next(node['center'] for node in accessory_belt.PULLEYS if node['id'] == name)
    new = TARGETS[name]
    shape = cad.Pos(0, new[0] - old[0], new[1] - old[1]) * shape
    if identifier in ('tensioner-moving-arm', 'tensioner-pulley-bolt', 'tensioner-pulley-wheel', 'tensioner-pulley-bearing'):
        pivot_y, pivot_z = TARGETS['TENS'][0] - 75, TARGETS['TENS'][1]
        shape = cad.Pos(0, pivot_y, pivot_z) * cad.Rot(tensioner_angle, 0, 0) * cad.Pos(0, -pivot_y, -pivot_z) * shape
    return shape


def belt(tensioner_angle=0):
    solution = accessory_belt.solve(pulleys(tensioner_angle))
    first = solution['spans'][0]
    direction = (0, (first['end'][0] - first['start'][0]) / first['length'], (first['end'][1] - first['start'][1]) / first['length'])
    section_plane = cad.Plane(origin=accessory_belt.world(first['start']), x_dir=(-1, 0, 0), z_dir=direction)
    section = section_plane * cad.Polygon(*accessory_belt_profile.belt_section_points(), align=None)
    return cad.sweep(section, accessory_belt.path(solution), is_frenet=False)


def numerical_report():
    reports = []
    for angle in (-10, 0, 10):
        effective = accessory_belt.solve(pulleys(angle), cord_path=False)
        cord = accessory_belt.solve(pulleys(angle))
        reports.append({'exploratory_arm_angle_degrees': angle,
                        'assumed_effective_length_mm': effective['length'],
                        'assumed_effective_length_residual_mm': effective['length'] - accessory_belt_profile.NOMINAL_EFFECTIVE_LENGTH,
                        'illustrative_cord_path_length_mm': cord['length'],
                        'modeled_rib_root_reference_length_mm': cord['length'] - math.tau * accessory_belt_profile.CORD_ABOVE_RIB_ROOT,
                        'modeled_rib_root_residual_mm': cord['length'] - math.tau * accessory_belt_profile.CORD_ABOVE_RIB_ROOT - accessory_belt_profile.NOMINAL_EFFECTIVE_LENGTH,
                        'rib_root_reference_not_verified_catalog_gauge_line': True,
                        'wrap_degrees': {arc['pulley']: arc['wrap_degrees'] for arc in cord['arcs']}})
    return reports
