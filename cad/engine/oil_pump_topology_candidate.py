"""Uninstalled topology study; explicit display estimates, no production outlet/mount."""
from pathlib import Path
import build123d as b
ROOT=Path(__file__).resolve().parents[2]
# Existing illustrative pump-local frame, not a new surveyed Ford datum.
DISPLAY_ESTIMATES={'neck_radius':13.,'neck_top':44.,'mount_blank_width':60.,'mount_blank_depth':32.,'mount_blank_bottom':40.,'mount_blank_top':46.,'pickup_flange_width_y':40.,'pickup_flange_height_z':26.,'pickup_bolt_y':13.,'pickup_bolt_radius':3.2,'pickup_gasket_thickness':.5}
DRIVE_X=3.5;DRIVE_CLEARANCE=6.15;INLET_RADIUS=6.
def axial(radius,z0,z1):return b.Pos(DRIVE_X,0,(z0+z1)/2)*b.Cylinder(radius,z1-z0)
def flange(x0,x1):
 q=b.Pos((x0+x1)/2,0,5)*b.Box(x1-x0,40,26)
 for y,r in [(0,INLET_RADIUS),(-13,3.2),(13,3.2)]:q-=b.Solid.make_cylinder(r,x1-x0+2,b.Plane(origin=(x0-1,y,5),z_dir=(1,0,0)))
 return q
def build():
 old=b.import_step(ROOT/'cad/engine/generated/oil-pump-housing.step')
 # Existing drive-interface bore retained; no outlet drilling is inferred.
 base=old-axial(DRIVE_CLEARANCE,-25,30)
 neck=axial(13,15,44)-axial(DRIVE_CLEARANCE,14,47)
 blank=b.Pos(DRIVE_X,0,43)*b.Box(60,32,6)-axial(DRIVE_CLEARANCE,39,47)
 # Integral body-side inlet flange, separate gasket and tube-side flange.
 housing=base+neck+blank+flange(-39,-30)
 return {'oil-pump-topology-housing':housing,'oil-pump-topology-pickup-gasket':flange(-39.5,-39),'oil-pump-topology-pickup-tube-flange':flange(-44.5,-39.5)}
