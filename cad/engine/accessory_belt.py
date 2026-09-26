"""Analytic with-A/C serpentine routing, not a verified catalog-length installation."""
import math

import build123d as cad

from accessory_belt_profile import BELT_PLANE_X, CONTACT_CLEARANCE, CORD_ABOVE_RIB_ROOT, BACK_ABOVE_CORD, NOMINAL_EFFECTIVE_LENGTH, belt_section_points, SOURCES as PROFILE_SOURCES, GAPS as PROFILE_GAPS

SOURCES = ['ford-accessory-routing', 'gates-1994-drive'] + PROFILE_SOURCES
GAPS = PROFILE_GAPS + [
    'Loop order ALT, TENS, P/S, A/C, W/P, C/S, A/P follows the reviewed Ford with-A/C diagram. Tensioner and water pump contact the smooth belt back; all other wheels engage the ribbed face.',
    'Analytic common tangents and signed wrap arcs use current provisional pulley stations. A closed collision-free loop does not prove correct catalog length, tensioner working range, belt traction, accessory speed or load capacity.',
    'No center is moved to force the nominal belt length. The geometric path and residual expose the unresolved engine accessory layout rather than concealing it.'
]
PULLEYS = [
    {'id': 'ALT', 'center': (-325, 410), 'radius': 35, 'side': 1},
    {'id': 'TENS', 'center': (0, 435), 'radius': 45, 'side': -1},
    {'id': 'PS', 'center': (280, 410), 'radius': 5.17 * 25.4 / 2, 'side': 1},
    {'id': 'AC', 'center': (280, 100), 'radius': 72.5, 'side': 1},
    {'id': 'WP', 'center': (0, 170), 'radius': 75, 'side': -1},
    {'id': 'CS', 'center': (0, 0), 'radius': 6.42 * 25.4 / 2, 'side': 1},
    {'id': 'AP', 'center': (-280, 100), 'radius': 70, 'side': 1},
]


def solve(pulleys=None, cord_path=True):
    nodes = [dict(node) for node in (PULLEYS if pulleys is None else pulleys)]
    for node in nodes:
        offset = CONTACT_CLEARANCE + (CORD_ABOVE_RIB_ROOT if node['side'] == 1 else BACK_ABOVE_CORD) if cord_path else 0
        node['path_radius'] = node['radius'] + offset
    spans = []
    for first, second in zip(nodes, nodes[1:] + nodes[:1]):
        delta = tuple(second['center'][index] - first['center'][index] for index in range(2))
        distance = math.hypot(*delta)
        radius_delta = first['side'] * first['path_radius'] - second['side'] * second['path_radius']
        cosine = radius_delta / distance
        assert abs(cosine) < 1, (first['id'], second['id'], 'no common tangent')
        sine = math.sqrt(1 - cosine * cosine)
        normal = ((cosine * delta[0] - sine * delta[1]) / distance,
                  (cosine * delta[1] + sine * delta[0]) / distance)
        points = [tuple(node['center'][index] + node['side'] * node['path_radius'] * normal[index] for index in range(2)) for node in (first, second)]
        length = math.dist(*points)
        spans.append({'from': first['id'], 'to': second['id'], 'start': points[0], 'end': points[1], 'normal': normal, 'length': length})
    arcs = []
    for index, node in enumerate(nodes):
        start, end = spans[index - 1]['end'], spans[index]['start']
        start_angle = math.atan2(start[1] - node['center'][1], start[0] - node['center'][0])
        end_angle = math.atan2(end[1] - node['center'][1], end[0] - node['center'][0])
        sweep = ((start_angle - end_angle) if node['side'] == 1 else (end_angle - start_angle)) % math.tau
        middle_angle = start_angle - node['side'] * sweep / 2
        middle = tuple(node['center'][coordinate] + node['path_radius'] * (math.cos(middle_angle), math.sin(middle_angle))[coordinate] for coordinate in range(2))
        arcs.append({'pulley': node['id'], 'start': start, 'middle': middle, 'end': end, 'wrap_degrees': math.degrees(sweep), 'length': sweep * node['path_radius'], 'side': node['side'], 'path_radius': node['path_radius']})
    return {'nodes': nodes, 'spans': spans, 'arcs': arcs, 'length': sum(span['length'] for span in spans) + sum(arc['length'] for arc in arcs)}


def world(point):
    return (BELT_PLANE_X, point[0], point[1])


def path(solution=None):
    solution = solve() if solution is None else solution
    edges = []
    for index, span in enumerate(solution['spans']):
        edges.append(cad.Edge.make_line(world(span['start']), world(span['end'])))
        arc = solution['arcs'][(index + 1) % len(solution['arcs'])]
        edges.append(cad.Edge.make_three_point_arc(world(arc['start']), world(arc['middle']), world(arc['end'])))
    return cad.Wire(edges)


def belt():
    solution = solve()
    first = solution['spans'][0]
    direction = (0, (first['end'][0] - first['start'][0]) / first['length'], (first['end'][1] - first['start'][1]) / first['length'])
    section_plane = cad.Plane(origin=world(first['start']), x_dir=(-1, 0, 0), z_dir=direction)
    section = section_plane * cad.Polygon(*belt_section_points(), align=None)
    return cad.sweep(section, path(solution), is_frenet=False)


def parts():
    return {'accessory-serpentine-belt': belt()}


def routing_report():
    cord = solve()
    effective = solve(cord_path=False)
    return {
        'verified_nominal_belt_fit': False,
        'catalog_effective_length_mm': NOMINAL_EFFECTIVE_LENGTH,
        'outside_radius_as_effective_assumption_length_mm': effective['length'],
        'assumed_effective_length_residual_mm': effective['length'] - NOMINAL_EFFECTIVE_LENGTH,
        'illustrative_cord_path_length_mm': cord['length'],
        'cord_path_not_directly_equal_to_catalog_effective_length': True,
        'solution': cord,
        'limits': GAPS
    }


def build(api):
    define, add, group = api
    group('accessory-belt-assembly', 'Accessory belt · unresolved nominal-length fit', 'accessory-drive')
    define('accessory-serpentine-belt', belt(), 'Six-rib accessory belt · routing study',
           'One continuous ribbed belt follows analytic tangents and pulley wraps. Smooth backside contacts the tensioner and water pump; the current geometric loop is longer than the sourced nominal belt and is not a verified installation.',
           'accessory-drive', '#292d2d', SOURCES, GAPS)
    add('accessory-serpentine-belt', 'accessory-serpentine-belt', 'accessory-belt-assembly', (0, 0, 0), (180, 0, 0))
