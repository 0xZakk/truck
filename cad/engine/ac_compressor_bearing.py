"""Dimensioned FS10 clutch-bearing envelope and provisional mating-seat revision."""
from functools import lru_cache
import build123d as b
import ac_compressor_motion as accepted

POSITION = accepted.POSITION
SOURCES = accepted.SOURCES + ['nsk-fs10-clutch-bearing', 'nachi-magnetic-clutch-bearing-construction']
GAPS = accepted.GAPS + [
    'NSK30BD40/NACHI30BG05S5G-2DS provides a30mm bore,55mm outside diameter and23mm width for the FS10 comparison. The bearing remains one explicitly unresolved internal cartridge; no ball, roller or cage count is invented.',
    'Front-head nose, pulley seat, retaining ring, coil carrier and armature neck are reconciled to the sourced bearing envelope. Their diameters, shoulders, clearances and axial stations remain provisional.',
    'The double-row angular-contact architecture and NACHI polyamide cage material are sourced, but raceways, balls, cages, seals and grease are not individually reconstructed. This revision does not complete bearing internals.'
]


def ring(outer, inner, length, center):
    return b.Rot(0, 90, 0) * accepted.base.ring(outer, inner, length, center)


@lru_cache(maxsize=1)
def replacements():
    original = accepted.home_components()
    head = original['ac-compressor-front-head']
    head -= b.Rot(0, 90, 0) * accepted.base.cylinder(24.01, 15, 92.5)
    shoulder = accepted.base.ring(24, 10.2, 3.2, 86.6)
    shoulder -= accepted.base.cylinder(17, 3, 86.45)
    head += b.Rot(0, 90, 0) * shoulder
    head += ring(14.9, 10.2, 23.1, 99.55)
    pulley = original['ac-compressor-clutch-pulley'] + ring(36, 27.55, 4, 110)
    pulley += ring(31, 27.55, 24, 100)
    carrier = ring(36, 24.1, 2, 86) + ring(36, 35, 4, 88)
    snap = ring(18, 14.95, .8, 111.7) - b.Pos(111.7, 18, 0) * b.Box(2, 12, 3)
    return {
        'ac-compressor-front-head': head,
        'ac-compressor-pulley-bearing': ring(27.5, 15, 23, 99.7),
        'ac-compressor-shaft-seal': ring(16.8, 10.1, 6, 84),
        'ac-compressor-seal-retainer': ring(16.8, 10.2, .8, 87.5),
        'ac-compressor-clutch-pulley': pulley,
        'ac-compressor-clutch-coil-carrier': carrier,
        'ac-compressor-pulley-snap-ring': snap,
        'ac-compressor-armature-hub': ring(64, 10.1, 3, 114.1) + ring(14.8, 10.1, 1.8, 112.2)
    }


def home_components():
    return {**accepted.home_components(), **replacements()}


def components(phase=0, engaged=True):
    result = {}
    for identifier, shape in home_components().items():
        motion = accepted.descriptor(identifier)
        if motion:
            center = accepted.group_center(identifier)
            shape = b.Pos(*center) * accepted.motion_pose(motion, phase, engaged) * b.Pos(*(-value for value in center)) * shape
        result[identifier] = shape
    return result


def parts(phase=0, engaged=True):
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in components(phase, engaged).items()}


def build(api):
    define, add, group = api
    revised = replacements()

    def bearing_define(identifier, shape, name, description, system, color, sources, gaps):
        if identifier in revised:
            shape = revised[identifier]
            sources = list(dict.fromkeys(sources + SOURCES))
            gaps = list(dict.fromkeys(gaps + GAPS))
            description += ' Mating geometry is revised around the sourced30×55×23mm clutch-bearing envelope; seat dimensions remain provisional.'
        if identifier == 'ac-compressor-pulley-bearing':
            name = 'FS10 clutch bearing ·30×55×23mm unresolved cartridge'
            description = 'Manufacturer-sized NSK30BD40/NACHI30BG05S5G-2DS comparison cartridge. Double-row angular-contact architecture is supported; individual races, balls, cage counts and seal profiles remain unresolved, not fabricated.'
        define(identifier, shape, name, description, system, color, sources, gaps)

    accepted.build((bearing_define, add, group))
