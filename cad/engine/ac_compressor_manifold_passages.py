"""Restore original cap drillings after manifold-seat additions without venting the bolt socket."""
from functools import lru_cache
import build123d as b
import ac_compressor_shaft_support as accepted
import ac_compressor_motion as motion
import ac_compressor_manifold as manifold

POSITION = accepted.POSITION
SOURCES = ['fs10-cylinder-passage-comparison', 'ford-compressor-manifold-diagnosis']
GAPS = [
    'Original provisional suction/discharge cap drillings are restored through the added manifold mounting boss. This preserves the complete accepted diagnostic flow paths, not just the two external port probes.',
    'The manifold retaining-bolt socket is blind at local axial station -86 mm, leaving an illustrative 2 mm wall to the nearest suction cap drilling. Thread engagement, pressure wall adequacy and production geometry remain unverified.'
]


@lru_cache(maxsize=1)
def replacements():
    head = b.Rot(0, -90, 0) * accepted.home_components()['ac-compressor-rear-head']
    head += manifold.axial(3.2, 4, -84, *manifold.BOLT_CENTER)
    for passage in motion.head_branches(-1):
        head -= passage
    return {'ac-compressor-rear-head': b.Rot(0, 90, 0) * head}


def home_components():
    return {**accepted.home_components(), **replacements()}


def components(phase=0, engaged=True):
    return {**accepted.components(phase, engaged), **replacements()}


def parts(phase=0, engaged=True):
    return {identifier: b.Pos(*POSITION) * shape for identifier, shape in components(phase, engaged).items()}


def build(api):
    define, add, group = api

    def passage_define(identifier, shape, name, description, system, color, sources, gaps):
        if identifier == 'ac-compressor-rear-head':
            shape = replacements()[identifier]
            description += ' The manifold-boss revision retains the original cap drillings and a separate blind bolt socket; all dimensions remain illustrative.'
            sources = list(dict.fromkeys(sources + SOURCES))
            gaps = list(dict.fromkeys(gaps + GAPS))
        define(identifier, shape, name, description, system, color, sources, gaps)

    accepted.build((passage_define, add, group))
