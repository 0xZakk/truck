"""Source-proportioned TCS45829 main gasket study, not an installed joint.
Manual outline transcription from actual manufacturer image at 1600px display.
Scale, thickness and exact hole circles are estimates; no engine registration.
"""
import build123d as b
ILLUSTRATIVE_IMAGE_EDGE_MM=320.0
THICKNESS=.8
ORIGIN_NORMALIZED=(.5,.64375)
# Centers ±3 reference-view pixels; hand-traced edge ±8 pixels.
CENTER_UNCERTAINTY_NORMALIZED=3/1600
EDGE_UNCERTAINTY_NORMALIZED=8/1600
# Follow outer edge from left lower terminal around crown to right terminal,
# then return along the inner edge. The bottom is intentionally OPEN.
OUTLINE_NORMALIZED=[(0.03125,0.64125),
(0.04875,0.590625),
(0.071875,0.566875),
(0.2525,0.48375),
(0.328125,0.36875),
(0.330625,0.344375),
(0.336875,0.330625),
(0.353125,0.32125),
(0.37125,0.311875),
(0.3875,0.284375),
(0.4175,0.270625),
(0.45,0.24375),
(0.465625,0.21875),
(0.484375,0.183125),
(0.506875,0.15375),
(0.54125,0.130625),
(0.57,0.11125),
(0.578125,0.0925),
(0.5975,0.0825),
(0.62125,0.094375),
(0.6875,0.091875),
(0.75,0.10375),
(0.80625,0.12875),
(0.85,0.15625),
(0.88125,0.174375),
(0.90625,0.176875),
(0.92125,0.193125),
(0.9225,0.2175),
(0.94375,0.254375),
(0.963125,0.308125),
(0.976875,0.37125),
(0.985,0.38125),
(0.99375,0.3975),
(0.9925,0.41625),
(0.98,0.42875),
(0.97375,0.475),
(0.953125,0.53125),
(0.9075,0.58375),
(0.91,0.60625),
(0.896875,0.624375),
(0.875,0.626875),
(0.85625,0.641875),
(0.8,0.64375),
(0.78,0.640625),
(0.75625,0.64375),
(0.7625,0.635),
(0.7925,0.62125),
(0.81375,0.623125),
(0.83125,0.61125),
(0.85,0.594375),
(0.88125,0.568125),
(0.90875,0.5375),
(0.925,0.49125),
(0.93875,0.4425),
(0.94,0.396875),
(0.93375,0.338125),
(0.90875,0.270625),
(0.875,0.22125),
(0.83125,0.1825),
(0.7875,0.155625),
(0.7375,0.1375),
(0.68125,0.1275),
(0.6375,0.130625),
(0.586875,0.140625),
(0.553125,0.15625),
(0.52375,0.178125),
(0.505,0.2025),
(0.48625,0.240625),
(0.463125,0.26625),
(0.436875,0.288125),
(0.419375,0.306875),
(0.4075,0.325),
(0.386875,0.3525),
(0.360625,0.39375),
(0.326875,0.445625),
(0.281875,0.515625),
(0.255625,0.553125),
(0.2325,0.57125),
(0.13875,0.608125),
(0.126875,0.61875),
(0.12,0.6425),
(0.1,0.645625),
(0.08125,0.640625),
(0.068125,0.644375),
(0.05,0.64375)]
HOLES_NORMALIZED=[(0.08375,0.598125),
(0.224375,0.53625),
(0.351875,0.345625),
(0.6,0.108125),
(0.89875,0.20375),
(0.968125,0.40375),
(0.885625,0.6)]
def yz(p):return ((p[0]-ORIGIN_NORMALIZED[0])*ILLUSTRATIVE_IMAGE_EDGE_MM,(ORIGIN_NORMALIZED[1]-p[1])*ILLUSTRATIVE_IMAGE_EDGE_MM)
def axial_cylinder(radius,y,z,start=-1,length=3):
 return b.Pos(start,y,z)*b.Rot(0,90,0)*b.Cylinder(radius,length,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def build():
 profile=b.Plane.YZ*b.Polygon(*[yz(p) for p in OUTLINE_NORMALIZED],align=None)
 shape=b.extrude(profile,amount=THICKNESS)
 for p in HOLES_NORMALIZED:
  y,z=yz(p);shape-=axial_cylinder(4.2,y,z)
 return {'timing-cover-main-gasket-topology-candidate':shape}
