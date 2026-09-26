"""Source-counted FS10 rear manifold interface with provisional seats and routing."""
from functools import lru_cache
import math
import build123d as b
import ac_compressor_bearing as accepted

POSITION = accepted.POSITION
PORTS = {'suction': (-20, 20), 'discharge': (24, 38)}
SEAL_ID = .796 * 25.4
SEAL_SECTION = .139 * 25.4
FACE = -95
BOLT_CENTER = (2, 29)
SOURCES = ['summit-fs10-port-seals', 'uac-fs10-rear-port-photo', 'uac-fs10-port-seals', 'ford-compressor-manifold-diagnosis']
GAPS = [
    'Two rear-facing port seals follow the UAC CO101220C application photo and Summit FS10 construction illustration. Summit lists 211C70 suction/discharge seals; its size table supplies the nominal .796 inch bore and .139 inch section. Installed seal identity remains unverified.',
    'Rear-head pads, manifold contour, port pitch, passage bore, axial stations and bolt geometry remain provisional. The original study port axes are retained; no photograph is treated as a dimensional drawing.',
    'Nominal undeformed toroidal seals sit in matching illustrative two-sided seats. This is not a production gland, seal squeeze, pressure rating or leak-tightness calculation.',
    'The single fastener follows the 1994 factory manifold-bolt description. Its diameter, length and head are assumed; threads, engagement and clamp loads are not reconstructed.',
    'The manifold contains two separate open through passages. Vehicle refrigerant tubes, hose crimps and complete installed routing are absent; no shipping plate is included as an operating component.'
]
NAMES = {
    'ac-compressor-rear-manifold': 'FS10 rear refrigerant manifold · provisional interface',
    'ac-compressor-manifold-suction-seal': 'FS10 suction port O-ring · size 211 comparison',
    'ac-compressor-manifold-discharge-seal': 'FS10 discharge port O-ring · size 211 comparison',
    'ac-compressor-manifold-bolt': 'FS10 manifold retaining bolt · provisional geometry'
}
FUNCTIONS = {
    'ac-compressor-rear-manifold': 'A single manifold block connects two independent rear ports to the vehicle suction and discharge lines. Separate open study passages preserve their isolation; the vehicle lines are not yet modeled.',
    'ac-compressor-manifold-suction-seal': 'A separate nominal size 211 toroidal seal surrounds the suction passage at the rear-head/manifold interface. Its sourced comparison dimensions do not establish production gland fit or installed identity.',
    'ac-compressor-manifold-discharge-seal': 'A second nominal size 211 seal surrounds the discharge passage independently of the suction seal and compressor case seal. This geometry does not simulate elastomer compression or pressure sealing.',
    'ac-compressor-manifold-bolt': 'One retaining bolt bears against the manifold and enters a blind study socket in the rear head. The factory procedure identifies this fastener separately from the compressor through-bolts; its thread and clamp load remain unresolved.'
}


def axial(radius, length, center, horizontal=0, vertical=0):
    return b.Pos(horizontal, vertical, center) * b.Cylinder(radius, length)


def seal(horizontal, vertical):
    return b.Pos(horizontal, vertical, FACE) * b.Torus((SEAL_ID + SEAL_SECTION) / 2, SEAL_SECTION / 2)


@lru_cache(maxsize=1)
def local_parts():
    rear = b.Rot(0, -90, 0) * accepted.home_components()['ac-compressor-rear-head']
    midpoint_horizontal, midpoint_vertical = BOLT_CENTER
    angle = math.degrees(math.atan2(18, 44))
    span = math.hypot(44, 18)
    manifold = b.Pos(midpoint_horizontal, midpoint_vertical, -101) * b.Rot(0, 0, angle) * b.Box(span, 32, 12)
    result = {}
    for role, (horizontal, vertical) in PORTS.items():
        rear += axial(15, 12, -89, horizontal, vertical)
        manifold += axial(16, 12, -101, horizontal, vertical)
        result[f'ac-compressor-manifold-{role}-seal'] = seal(horizontal, vertical)
    rear += axial(8, 12, -89, *BOLT_CENTER)
    for role, (horizontal, vertical) in PORTS.items():
        passage = axial(6, 40, -93, horizontal, vertical)
        rear -= passage
        manifold -= passage
        gland = result[f'ac-compressor-manifold-{role}-seal']
        rear -= gland
        manifold -= gland
    rear -= axial(3.2, 14, -89, *BOLT_CENTER)
    manifold -= axial(3.2, 16, -101, *BOLT_CENTER)
    shaft = axial(3, 18, -98, *BOLT_CENTER)
    head = b.Pos(*BOLT_CENTER, -110) * b.extrude(b.RegularPolygon(6, 6), amount=3)
    result['ac-compressor-manifold-bolt'] = shaft + head
    result['ac-compressor-rear-manifold'] = manifold
    result['ac-compressor-rear-head'] = rear
    return result


def replacements():
    return {identifier: b.Rot(0, 90, 0) * shape for identifier, shape in local_parts().items()}


def changed_parts():
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in replacements().items()}


def home_components():
    return {**accepted.home_components(), **replacements()}


def components(phase=0, engaged=True):
    return {**accepted.components(phase, engaged), **replacements()}


def parts(phase=0, engaged=True):
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in components(phase, engaged).items()}


def passage_probes():
    return {role: b.Pos(*POSITION) * b.Rot(0, 90, 0) * axial(5.5, 35, -91.5, *center) for role, center in PORTS.items()}


def build(api):
    define, add, group = api
    revised = replacements()

    def manifold_define(identifier, shape, name, description, system, color, sources, gaps):
        if identifier == 'ac-compressor-rear-head':
            shape = revised[identifier]
            description += ' Rear port lands and a blind retaining-bolt socket accommodate the separate provisional manifold and two size 211 comparison seals.'
            sources = list(dict.fromkeys(sources + SOURCES))
            gaps = list(dict.fromkeys(gaps + GAPS))
        define(identifier, shape, name, description, system, color, sources, gaps)

    accepted.build((manifold_define, add, group))
    for index, identifier in enumerate(NAMES):
        color = '#416b49' if 'seal' in identifier else '#a1a8af'
        define(identifier, revised[identifier], NAMES[identifier], FUNCTIONS[identifier], 'accessory-drive', color, SOURCES, GAPS)
        add(identifier, identifier, 'ac-compressor', (0, 0, 0), (-180 - 45 * index, 80, 50))
