"""Uninstalled Fel-Pro13816 topology study. Photo frame, NOT engine orientation.

One existing pump gasket is to be replaced eventually; this is not an added seal.
The manufacturer catalog supports application; exact product photo supports four
small mounting apertures and a larger fifth peripheral opening. No dimensions
or function of the fifth opening are asserted. No block coolant tunnel invented.
"""
import build123d as b
SOURCE='water-pump-mounting-topology'
# Approximate photo ratios scaled to existing provisional59mm central radius.
# Coordinates use photo-right as+Y, photo-up as+Z, extrusion alongX.
MOUNTING=((-7.7,66.5),(-66.3,-6.3),(66.2,-5.3),(-17.,-64.9))
EXTRA=(10.9,-69.)
GAPS=[
 'All millimeter dimensions and installed orientation are provisional; these approximate the exact replacement photo silhouette, not a tracing or measured drawing.',
 'Four small mounting apertures are distinct from the larger fifth opening; the latter function is unidentified and no fifth bolt is inferred.',
 'Existing pump rear-face/block datum mismatch remains unresolved. This candidate is intentionally uninstalled and does not complete the engine coolant jacket or pump mounting joint.',
]
def disk(radius,y,z):
    return b.Pos(0,y,z)*b.Rot(0,90,0)*b.Cylinder(radius,2)
def gasket_shape():
    shape=disk(65,0,0)
    for y,z in MOUNTING:shape+=disk(9.5,y,z)
    shape+=disk(11.5,*EXTRA)
    shape-=disk(59,0,0)
    for y,z in MOUNTING:shape-=disk(5.2,y,z)
    shape-=disk(6.5,*EXTRA)
    return shape
