"""Dimensioned IS-74 candidate; installation is blocked by existing drive datums."""
import math
import build123d as b

LENGTH = 4.520 * 25.4
ACROSS_FLATS = .312 * 25.4
POSITION = (213.5, 56, -95)
RETAINER_STATION = LENGTH - 12
SOURCES = ['fsm-a3698a10af15', 'melling-1994-49-applications',
           'melling-intermediate-shaft-dimensions', 'ford-industrial-csg649']
GAPS = [
    'Uninstalled candidate. Existing distributor and pump axes are separated laterally; this shaft must not be stretched or tilted to bridge them.',
    'Melling IS-74 establishes 4.520 inch length, .312 inch hex section and L & M ends. End profiles, orientation, chamfers and tolerances remain unverified.',
    'The older Melling chart uses nominal 5/16 inch, while the current chart lists .312 inch; the 0.0127 mm difference is not a manufacturing tolerance.',
    'Retainer is a separate illustrative split washer. Truck-specific retention architecture, dimensions, interference, axial station and block retaining shoulder remain unverified.',
    'Pump-side candidate origin and 9 mm insertion are provisional. Existing pump socket is undersized and distributor lower socket is absent; no installed fit or motion is claimed.'
]


def shaft():
    radius = ACROSS_FLATS / math.sqrt(3)
    sections = [b.Pos(0, 0, station) * b.RegularPolygon(section_radius, 6)
                for station, section_radius in [(0, radius - .5), (1, radius),
                                                 (LENGTH - 1, radius), (LENGTH, radius - .5)]]
    return b.loft(sections, ruled=True)


def retainer():
    washer = b.Cylinder(7, .7)
    washer -= b.extrude(b.RegularPolygon((ACROSS_FLATS + .06) / math.sqrt(3), 6), amount=1, both=True)
    washer -= b.Pos(5.5, 0, 0) * b.Box(6, .45, 2)
    return b.Pos(0, 0, RETAINER_STATION) * washer


def parts():
    return {'oil-pump-intermediate-shaft': shaft(), 'oil-pump-drive-retainer': retainer()}


def build(api):
    define, add, group = api
    group('oil-pump-drive-study', 'Oil pump intermediate drive · uninstalled candidate',
          'lubrication', position=POSITION)
    descriptions = {
        'oil-pump-intermediate-shaft': ('Oil pump intermediate shaft · IS-74 study',
            'Transfers distributor torque to the oil pump through a separate hexagonal shaft. Manufacturer length and hex section are dimensioned; ends and installation remain provisional.'),
        'oil-pump-drive-retainer': ('Intermediate shaft retainer · envelope',
            'Illustrates a separate shaft retention component. Exact truck construction, gripping geometry and block stop are unverified; the modeled clearance is not a working retention fit.')}
    for identifier, shape in parts().items():
        name, description = descriptions[identifier]
        define(identifier, shape, name, description, 'lubrication', '#a0aab0', SOURCES, GAPS)
        add(identifier, identifier, 'oil-pump-drive-study', explode=(0, 0, 100 if identifier.endswith('shaft') else 140))
