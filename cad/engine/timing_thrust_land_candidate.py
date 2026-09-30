"""Estimated rear thrust land only; no production backside evidence or install."""
import build123d as b
PARAMS={'inner_radius_mm':20.65,'outer_radius_mm':26.,'local_x_min_mm':-7.,'local_x_max_mm':1.02}
def cylinder(radius,length):return b.Rot(0,90,0)*b.Cylinder(radius,length)
def revise(local_cam):
 p=PARAMS;length=p['local_x_max_mm']-p['local_x_min_mm'];mid=(p['local_x_min_mm']+p['local_x_max_mm'])/2
 return local_cam+(b.Pos(mid,0,0)*(cylinder(p['outer_radius_mm'],length)-cylinder(p['inner_radius_mm'],length+2)))
