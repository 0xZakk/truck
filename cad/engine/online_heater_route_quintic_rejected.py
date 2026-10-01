"""New manufacturer-view axial hypothesis; all dimensions remain inferred."""
import numpy as np
import build123d as b
import waterpump_heater_source_candidate as old
R=old.R
O=R/'cad/engine/generated/online-heater-route-candidate'
ROOT=old.ROOT.copy();DIR=old.DIR.copy();START=old.START.copy()
NOMINAL_X=410-(438-360)*143/180
END_X={'nominal':NOMINAL_X,'rear-limit':410-(442-356)*143/176,'front-limit':410-(434-364)*143/184}
# Terminal slope is a side-photo proxy; preserved radial direction, no neighbors.
radial_span=np.linalg.norm(old.END[1:]-ROOT[1:])
axial_per_radial=(76/100)*(143/180)/(radial_span/178)
ENDDIR=np.array([-axial_per_radial,* (old.ENDDIR[1:]/np.linalg.norm(old.ENDDIR[1:]))]);ENDDIR/=np.linalg.norm(ENDDIR)
def controls(variant='nominal'):
 end=old.END.copy();end[0]=END_X[variant]
 p0=ROOT+25*DIR;p1=ROOT+70*DIR;p1[0]=425
 p3=end-25*ENDDIR;p2=p3-65*ENDDIR
 return p0,p1,p2,p3,end
def path(variant='nominal'):
 p0,p1,p2,p3,end=controls(variant)
 # A raised inner Bezier control changes only axial curvature; root tangent
 # must remain radial: preserve p1.x=p0.x and use an extra quintic control.
 q1=p0+25*DIR
 q2=p1
 q3=p2
 return b.Wire([b.Edge.make_line(tuple(START),tuple(p0)),b.Edge.make_bezier(*map(tuple,[p0,q1,q2,q3,p3-20*ENDDIR,p3])),b.Edge.make_line(tuple(p3),tuple(end))])
def sweep(radius,variant='nominal'):
 return b.sweep(b.Plane(origin=tuple(START),z_dir=tuple(DIR))*b.Circle(radius),path(variant))
def tube(variant='nominal'):
 end=controls(variant)[-1]
 return (sweep(8,variant)+old.segment(8.5,end-5*ENDDIR,end-3*ENDDIR))-sweep(6.5,variant)
