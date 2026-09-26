"""Two source-counted shaft-support cartridges with explicitly assumed envelopes."""
from functools import lru_cache
import build123d as b
import ac_compressor_manifold as accepted

POSITION = accepted.POSITION
SHAFT_RADIUS = 10
SEAT_RADIUS = 14
BEARING_WIDTH = 12
BEARING_STATION = 42
SOURCES = ['summit-fs10-shaft-supports']
GAPS = [
    'Summit FS10 illustration identifies one shaft bearing in each cylinder half, distinct from the adjacent thrust stack. This establishes the comparison support count, not the installed truck bearing identity.',
    'The 20 mm bore, 28 mm outside diameter, 12 mm width and axial stations at plus/minus 42 mm are assumed to match the existing study shaft and cylinder envelope. No catalog bearing number or production fit is asserted.',
    'Each radial bearing is one unresolved cartridge envelope. Rolling elements, cage, cup, raceways, lubrication details and manufacturing tolerances are not reconstructed or counted.',
    'Matched nominal shaft and housing contact surfaces describe a load-path interface only. Zero-clearance CAD contact is not a press-fit, running-clearance, wear or bearing-load calculation.'
]


def axial(radius, width, station):
    return b.Pos(station, 0, 0) * b.Rot(0, 90, 0) * b.Cylinder(radius, width)


@lru_cache(maxsize=1)
def replacements():
    result = {}
    original = accepted.home_components()
    for label, direction in (('front', 1), ('rear', -1)):
        station = direction * BEARING_STATION
        envelope = axial(SEAT_RADIUS, BEARING_WIDTH, station) - axial(SHAFT_RADIUS, BEARING_WIDTH + 2, station)
        identifier = f'ac-compressor-{label}-cylinder'
        result[identifier] = original[identifier] - axial(SEAT_RADIUS, BEARING_WIDTH, station)
        result[f'ac-compressor-{label}-shaft-bearing'] = envelope
    return result


def home_components():
    return {**accepted.home_components(), **replacements()}


def components(phase=0, engaged=True):
    return {**accepted.components(phase, engaged), **replacements()}


def parts(phase=0, engaged=True):
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in components(phase, engaged).items()}


def changed_parts():
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in replacements().items()}


def build(api):
    define, add, group = api
    revised = replacements()

    def support_define(identifier, shape, name, description, system, color, sources, gaps):
        if identifier in revised:
            shape = revised[identifier]
            description += ' A nominal stepped bore seats the separate unresolved radial shaft-bearing cartridge; bearing dimensions and housing fits remain provisional.'
            sources = list(dict.fromkeys(sources + SOURCES))
            gaps = list(dict.fromkeys(gaps + GAPS))
        define(identifier, shape, name, description, system, color, sources, gaps)

    accepted.build((support_define, add, group))
    for label, direction in (('front', 1), ('rear', -1)):
        identifier = f'ac-compressor-{label}-shaft-bearing'
        name = f'FS10 {label} radial shaft bearing · unresolved cartridge'
        text = f'The {label} radial support locates the rotating compressor shaft inside its stationary cylinder half. It is separate from the thrust washers and thrust-bearing cartridge, which address axial loading. Internal construction and all envelope dimensions remain unresolved comparison geometry.'
        define(identifier, revised[identifier], name, text, 'accessory-drive', '#776e60', SOURCES, GAPS)
        add(identifier, identifier, 'ac-compressor', (0, 0, 0), (direction * 200, 140, direction * 110))
