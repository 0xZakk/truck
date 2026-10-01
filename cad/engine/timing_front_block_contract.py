"""Research masks only: declared source-derived stepped front boundaries.
No geometry candidate is cut or unioned here. Dimensions remain estimates.
"""
import build123d as b
import timing_cover_front_joint_candidate as front
import timing_cover_joint_candidate as outline
MAIN_PLANE=373.
LOWER_PLANE=365.
STEP_TOP=front.PLANE+10. # existing front-upper clamp structure top, -14.5mm

def proposed_regions():
 points=[front.c.yz(q,front.P) for q in outline.OUTLINE_NORMALIZED]
 outer=front.face(points[:45]+[(front.RIGHT,front.PLANE),(front.RIGHT,-70),(front.LEFT,-70),(front.LEFT,front.PLANE)])
 main=front.c.extrude_x(outer,MAIN_PLANE,420-MAIN_PLANE)-front.c.extrude_x(front.band_profile(-150,0),372,50)
 # Source-defined lower pan seating surface; diagnostic cut ends on the
 # established upper clamp-structure elevation, rather than an arbitrary box.
 a=(front.RADIUS**2-front.PLANE**2)**.5
 ys=[front.LEFT]+[-a+2*a*i/96 for i in range(97)]+[front.RIGHT]
 lower=[(y,front.top(y)) for y in ys]
 lower_face=b.Plane.YZ*b.Polygon(*(lower+[(front.RIGHT,STEP_TOP),(front.LEFT,STEP_TOP)]),align=None)
 lower_prism=front.c.extrude_x(lower_face,LOWER_PLANE,MAIN_PLANE-LOWER_PLANE)
 # Narrow band is an alternate diagnostic, not an applied neighbor cut.
 upper_band=front.clip_x(front.front_blank(0,10)[0],LOWER_PLANE,MAIN_PLANE)
 return {'main-plane-only':main,'source-upper-band-supplement':upper_band,'stepped-lower-region':lower_prism}
