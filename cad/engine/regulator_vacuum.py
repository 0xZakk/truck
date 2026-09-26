"""Factory-supported regulator vacuum connection with provisional routing."""
import build123d as cad

SOURCES = ['system-750bd1047639', 'system-73d3dd2d32e7']
GAPS = [
    'Ford establishes an intake-manifold vacuum connection to the regulator spring chamber. It does not dimension the hose or identify this modeled dedicated fitting.',
    'Hose routing, 12 mm outside diameter, 8.2 mm main bore, 8.3 mm straight regulator socket, fitting dimensions and plenum port station are provisional; production routing may use a shared vacuum harness.',
    'The fitting uses an unthreaded seat with clearance; thread sealing, hose compression, clamps and actual installed variant remain unresolved. No pressure response is simulated.'
]


def cylinder(radius, start, end):
    vector = cad.Vector(end) - cad.Vector(start)
    return cad.Plane(origin=(cad.Vector(start) + cad.Vector(end)) * .5,
                     z_dir=vector) * cad.Cylinder(radius, vector.length)


def intake_interface(shape):
    return shape - cylinder(4.05, (0, -55, 460), (0, -39, 460))


def fitting():
    shape = cylinder(4, (0, -73, 460), (0, -43, 460))
    shape += cylinder(6, (0, -53, 460), (0, -47.5, 460))
    return shape - cylinder(2.5, (0, -74, 460), (0, -42, 460))


def hose():
    route = cad.Bezier((0, -163, 420), (0, -163, 440),
                       (0, -163, 455), (0, -120, 460),
                       (0, -95, 460), (0, -55, 460))
    plane = cad.Plane(origin=route @ 0, z_dir=route % 0)
    shape = (cad.sweep(plane * cad.Circle(6), path=route, is_frenet=True) -
             cad.sweep(plane * cad.Circle(4.1), path=route, is_frenet=True))
    return shape - cylinder(4.15, (0, -163, 419), (0, -163, 430))


def parts():
    return {'regulator-vacuum-hose': hose(), 'regulator-vacuum-fitting': fitting()}


def build(api):
    define, add, group = api
    group('regulator-vacuum-line', 'Fuel regulator vacuum reference', 'fuel-system')
    descriptions = {
        'regulator-vacuum-hose': ('Fuel regulator vacuum hose',
            'Connects the regulator spring chamber to intake manifold pressure so fuel pressure is referenced to the injector outlet pressure. The route is provisional.', '#353c3a'),
        'regulator-vacuum-fitting': ('Regulator manifold vacuum fitting · provisional',
            'Provides an open connection through the modeled plenum wall. A dedicated fitting is a construction assumption; the production vacuum harness and port identity remain unresolved.', '#a49772')
    }
    for identifier, shape in parts().items():
        name, function, color = descriptions[identifier]
        define(identifier, shape, name, function, 'induction', color, SOURCES, GAPS)
        add(identifier, identifier, 'regulator-vacuum-line', explode=(0, -100, 60))
