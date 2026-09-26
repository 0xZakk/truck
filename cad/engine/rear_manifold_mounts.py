"""Rear bolts 15/16: factory topology with explicitly provisional interfaces.

Not integrated until all saved-neighbor and positive-material checks pass.
"""
import build123d as cad
from manifold_lifting_eye import axis_y, plate, hexagon

STATIONS = {'rear-manifold-bolt15': (-65.0, 315.0, -31.896),
            'rear-manifold-bolt16': (-292.0, 315.0, -259.48)}
SOURCES = ['ford-manifold-fastener-topology', 'ford-1996-manifold-comparison',
           'ford-1996-manifold-fastener-table']
GAPS = [
    'Ford1994 explicitly installs rear bolts15/16 before the intake; these two fasteners do not complete the remaining shared manifold clamps.',
    'Nominal3/8-16 diameter and1.31in underhead length are1996 comparison dimensions, not established1994 installed identity.',
    'All mounting stations, casting webs, head bosses, clearance holes, socket depths and hex-head dimensions are provisional adaptations to the existing reconstruction.',
    'Smooth envelopes do not model female threads, preload, thermal expansion or retention. Added head bosses are not verified against production coolant jackets.'
]


def lug_material():
    pieces = []
    for horizontal, vertical, branch_x in STATIONS.values():
        lug = axis_y(8.5, -143, -133, horizontal, vertical)
        lug += plate([(branch_x-4,277.5),(branch_x+4,277.5),
                      (horizontal+4,vertical),(horizontal-4,vertical)], -143, -135.6)
        lug -= axis_y(15, -144, -132, branch_x, 277.5)
        lug -= axis_y(5.2, -144, -132, horizontal, vertical)
        pieces.extend(lug.solids())
    return cad.Compound(children=pieces)


def rear_interface(shape):
    return shape.fuse(*lug_material().solids())


def head_interface(shape):
    for horizontal, vertical, _ in STATIONS.values():
        shape += axis_y(8, -133, -105, horizontal, vertical-255.5)
        shape -= axis_y(4.8125, -134, -107, horizontal, vertical-255.5)
    return shape


def lower_interface(shape):
    for horizontal, vertical, _ in STATIONS.values():
        shape -= axis_y(9, -151, -132.5, horizontal, vertical)
    return shape - lug_material()


def gasket_interface(shape):
    for horizontal, vertical, _ in STATIONS.values():
        shape -= axis_y(9, -136, -132.5, horizontal, vertical)
    return shape


ADAPTERS = {'exhaust-rear': rear_interface, 'cylinder-head': head_interface,
            'efi-lower-intake': lower_interface, 'efi-head-intake-gasket': gasket_interface}


def parts():
    return {identifier: axis_y(4.7625,-143,-109.726,x,z)+hexagon(x,z,-149,-143)
            for identifier,(x,z,_) in STATIONS.items()}


def build(api):
    define, add, group = api
    group('rear-manifold-mounts','Rear manifold bolts15/16 · mounting study','exhaust')
    for index,(identifier,shape) in enumerate(parts().items()):
        define(identifier,shape,identifier.replace('-',' ').title(),
               'Clamps a rear manifold mounting land to a blind head socket before intake installation; geometry and retention remain provisional.',
               'exhaust','#858a8e',SOURCES,GAPS)
        add(identifier,identifier,'rear-manifold-mounts',explode=(0,-440-index*60,-100))
