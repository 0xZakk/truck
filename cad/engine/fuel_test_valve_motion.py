"""Replacement-state adapter for the existing illustrative diagnostic valve."""
from functools import lru_cache

import build123d as cad

import fuel_test_valve

POSITION = fuel_test_valve.POSITION
MAX_ILLUSTRATIVE_TRAVEL = .12
SOURCES = ['fsm-4840fb38c793', 'schrader-core-construction']
GAPS = [
    'Preserves existing eight component identities, dimensions and rail datum; no installed core identity or production travel is established.',
    'The pin and its soft seating washer move together. The existing four-turn spring shortens over an illustrative0..0.12 mm interval; no spring rate, preload or real stroke is implied.',
    'Opening states require cap and cap seal removed. Gauge/tool attachment and external fuel collection are outside this geometry study.',
    'Existing static-seal inner radius2.61 mm versus groove radius2.60 mm leaves0.01 mm radial clearance. This uncompressed geometry does not prove a pressure-tight secondary bypass seal.',
    'Fluid probes demonstrate geometric passage connectivity only, not leak rate, pressure rating, material compatibility or safe servicing.'
]


def spring(radius, wire, height, turns):
    path = cad.Helix(height / turns, height, radius)
    return cad.sweep(cad.Plane(origin=path @ 0, z_dir=path % 0) * cad.Circle(wire), path=path)


@lru_cache(maxsize=1)
def baseline():
    definitions = {}
    def define(identifier, shape, *metadata):
        definitions[identifier] = (shape, metadata)
    fuel_test_valve.build((define, lambda *args, **kwargs: None, lambda *args, **kwargs: None, spring))
    return definitions


def components(travel=0, cap_removed=False):
    if not 0 <= travel <= MAX_ILLUSTRATIVE_TRAVEL:
        raise ValueError('Travel exceeds the illustrative non-binding interval')
    if travel and not cap_removed:
        raise ValueError('Remove the cap before depicting diagnostic actuation')
    result = {identifier: shape for identifier, (shape, metadata) in baseline().items()}
    if cap_removed:
        for identifier in ('fuel-test-cap', 'fuel-test-cap-seal'):
            result.pop(identifier)
    if travel:
        for identifier in ('fuel-test-pin', 'fuel-test-seat-seal'):
            result[identifier] = cad.Pos(0, 0, -travel) * result[identifier]
        result['fuel-test-spring'] = cad.Pos(0, 0, 1.2) * spring(1.6, .18, 1.62 - travel, 4)
    return result


def parts(travel=0, cap_removed=False):
    return {identifier: cad.Pos(*POSITION) * shape for identifier, shape in components(travel, cap_removed).items()}


def passage_probe(travel, radius=.003):
    crossing_height = 4.5 - travel / 2
    points = [(-.7, 0, -.5), (-.7, 0, 1.05), (-2.2, 0, 1.05),
              (-2.2, 0, crossing_height), (-1.05, 0, crossing_height), (-1.05, 0, 14.5)]
    segments = []
    for start, end in zip(points, points[1:]):
        direction = cad.Vector(end) - cad.Vector(start)
        segments.append(cad.Plane(origin=(cad.Vector(start) + cad.Vector(end)) * .5, z_dir=direction) * cad.Cylinder(radius, direction.length))
    return segments


def build(api, travel=0, cap_removed=False):
    define, add, group = api
    group('fuel-test-valve', 'Fuel pressure test valve · geometric actuation study', 'fuel-rail-assembly', position=POSITION)
    for identifier, shape in components(travel, cap_removed).items():
        metadata = baseline()[identifier][1]
        name, function, system, color, sources, gaps = metadata
        define(identifier, shape, name, function, system, color, SOURCES, GAPS)
        add(identifier, identifier, 'fuel-test-valve')
