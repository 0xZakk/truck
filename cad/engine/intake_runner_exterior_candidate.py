"""Exterior-only broad runner-face trial; dimensions inferred, datums protected."""
import build123d as b
import upper_intake_clearance_candidate as core

def paths():
 out=[]
 for x in core.PORTS:
  terminal=-150+(x+core.PORTS[0])/(2*core.PORTS[0])*300
  out.append(b.Bezier((x,-228,366.5),(x,-228,490),(terminal,-145,490),(terminal,-20,490)))
 return out

def shoulder(path):
 sections=[]
 # End profiles lie inside existing envelopes. Mid-arch broad surfaces follow
 # visible casting topology; numerical ratios/radii are not source dimensions.
 for t,w,h,r in ((.025,34,34,9),(.14,50,44,9),(.32,56,44,9),(.56,56,44,9),(.74,54,46,9),(.90,34,34,9)):
  tangent=path%t;transverse=b.Vector(1,0,0)-tangent*tangent.dot(b.Vector(1,0,0))
  plane=b.Plane(origin=path@t,x_dir=transverse,z_dir=tangent)
  sections.append(plane*b.RectangleRounded(w,h,r))
 return b.loft(sections)

def parts(base):
 curves=paths();air=b.Pos(0,25,490)*core.rounded_box(392,137,82,21)
 for x,path in zip(core.PORTS,curves):
  wire=b.Wire([b.Line((x,-228,354),path@0),path]);air+=b.sweep(b.Plane(origin=wire@0,z_dir=wire%0)*b.Circle(16.5),path=wire)
 # New skins overlap outer metal by0.5mm but leave the bore faces untouched.
 protected_core=b.Pos(0,25,490)*core.rounded_box(392,137,82,21)
 for path in curves:
  protected_core+=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(21.5),path=path)
 exterior=[shoulder(path) for path in curves]
 result=base
 for s in exterior:result+=s-protected_core
 return result,exterior,air,curves
