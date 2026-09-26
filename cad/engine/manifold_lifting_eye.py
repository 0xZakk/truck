"""Two-point front manifold lifting-eye construction comparison."""
import build123d as cad

STATIONS = {'stud13': (350, 315), 'bolt14': (49, 315)}
SOURCES = ['ford-manifold-fastener-topology', 'ford-1996-manifold-comparison', 'ford-1996-manifold-fastener-table']
GAPS = [
    'Ford 1994 identifies front stud13 and bolt14 before intake installation; the recovered 1996 factory figure shows a two-foot spanning eye.',
    'All station coordinates, lug sections, eye outline, socket depths and clearances are provisional adaptations to current castings, not production dimensions.',
    'Stud total axial length90.678 mm and bolt underhead length33.274 mm compare the 1996 labels3/8-16x3.57 and3/8-16x1.31; 1994 identity is not established.',
    'Smooth nominal thread envelopes do not simulate thread engagement, preload, lifting strength or fatigue. The projecting stud end has no invented downstream retaining nut.',
    'Remaining fourteen manifold fastener stations and shared clamping details are not completed by this subset.',
    'The provisional bolt axes are above the intake gasket strip. The casting webs lie outside its sealing plane instead of cutting the gasket into disconnected pieces.',
    'Bolt14 and its eye foot use assumed X49 mm, revised from X45 after the whole-engine audit found1.7265 mm3 overlap with injector3 connector. This clearance-driven adaptation is not a recovered Ford station.',
    'The simplified head needs explicit8 mm radius internal mounting bosses ending at worldY-109 to surround the provisional blind sockets. These assumed bosses are not traced production castings or verified against recovered coolant-gallery geometry.'
]


def axis_y(radius, first, last, horizontal, vertical):
    return cad.Pos(horizontal, (first + last) / 2, vertical) * cad.Rot(90, 0, 0) * cad.Cylinder(radius, last - first)


def plate(points, first, last):
    return cad.Pos(0, last, 0) * cad.Rot(90, 0, 0) * cad.extrude(cad.Polygon(*points, align=None), amount=last - first)


def hexagon(horizontal, vertical, first, last, radius=8.25):
    return cad.Pos(horizontal, last, vertical) * cad.Rot(90, 0, 0) * cad.extrude(cad.RegularPolygon(radius, 6), amount=last - first)


def head_interface(shape):
    for horizontal, vertical in STATIONS.values():
        shape += axis_y(8, -133, -109, horizontal, vertical - 255.5)
        shape -= axis_y(4.8125, -134, -111, horizontal, vertical - 255.5)
    return shape


def lug_material():
    result = None
    for identifier, branch_x in [('stud13', 309.48), ('bolt14', 81.896)]:
        horizontal, vertical = STATIONS[identifier]
        piece = axis_y(8.5, -143, -133, horizontal, vertical)
        piece += plate([(branch_x - 4, 277.5), (branch_x + 4, 277.5),
                        (horizontal + 4, vertical), (horizontal - 4, vertical)], -143, -135.6)
        piece -= axis_y(15, -144, -132, branch_x, 277.5)
        piece -= axis_y(5.2, -144, -132, horizontal, vertical)
        result = piece if result is None else result + piece
    return result


def front_interface(shape):
    lugs = lug_material()
    with cad.SkipClean():
        return shape.fuse(*lugs)


def lower_interface(shape):
    for horizontal, vertical in STATIONS.values():
        shape -= axis_y(9, -146, -132.5, horizontal, vertical)
    shape -= lug_material()
    return shape


def gasket_interface(shape):
    for horizontal, vertical in STATIONS.values():
        shape -= axis_y(9, -136, -132.5, horizontal, vertical)
    return shape


ADAPTERS = {
    'cylinder-head': head_interface,
    'efi-lower-intake': lower_interface,
    'efi-head-intake-gasket': gasket_interface,
    'exhaust-front': front_interface
}


def parts():
    outline = [(39, 289), (59, 289), (59, 307), (200, 307), (266, 348), (280, 348), (340, 307), (340, 289), (360, 289), (360, 317), (284, 370), (259, 370), (195, 321), (49, 321), (39, 313)]
    eye = cad.Pos(0, 0, 17) * plate(outline, -147, -143)
    eye -= axis_y(8, -148, -142, 271, 375)
    for horizontal, vertical in STATIONS.values():
        eye -= axis_y(5.2, -148, -142, horizontal, vertical)
    stud_x, stud_z = STATIONS['stud13']
    bolt_x, bolt_z = STATIONS['bolt14']
    stud = axis_y(4.7625, -204.404, -113.726, stud_x, stud_z)
    stud += hexagon(stud_x, stud_z, -153, -147)
    bolt = axis_y(4.7625, -147, -113.726, bolt_x, bolt_z)
    bolt += hexagon(bolt_x, bolt_z, -153, -147)
    return {'front-manifold-lifting-eye': eye, 'front-manifold-stud13': stud, 'front-manifold-bolt14': bolt}


def build(api):
    define, add, group = api
    group('front-manifold-eye', 'Front manifold lifting eye · construction comparison', 'exhaust')
    functions = {
        'front-manifold-lifting-eye': 'Spans two separate front-manifold mounting regions; each foot is clamped against a casting lug. This geometric load path does not establish a safe lifting rating.',
        'front-manifold-stud13': 'Its integral shoulder clamps one eye foot and the front casting against the head. The external extension represents the compared long stud, not a completed downstream attachment.',
        'front-manifold-bolt14': 'Clamps the second eye foot and front casting into a separate blind head socket before the intake is installed.'
    }
    offsets = {
        'front-manifold-lifting-eye': (0, -350, -100),
        'front-manifold-stud13': (0, -440, -100),
        'front-manifold-bolt14': (0, -500, -100)
    }
    for identifier, shape in parts().items():
        define(identifier, shape, identifier.replace('-', ' ').title(), functions[identifier], 'exhaust', '#858a8e', SOURCES, GAPS)
        add(identifier, identifier, 'front-manifold-eye', explode=offsets[identifier])
