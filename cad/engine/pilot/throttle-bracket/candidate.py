"""Photo-informed teaching candidate; all dimensions assumed except baseline datums."""
import build123d as b
PARAMS=dict(thickness=2.0,mount_x=378.5,mount_y=74.,mount_z=(464.,516.),hole_r=4.4,web_y=93.,tip_x=465.,cable_y=110.)
SOURCES=['pilot-throttle-bracket-factory','pilot-throttle-bracket-photo']
GAPS=['Photo-informed teaching candidate only; every bracket dimension and installed handedness is assumed. Exact 1994 manual-transmission variant is unconfirmed.','Preserves accepted stud axes. Educational stack requires positive-Y nuts shifted +2 mm X and explicitly inferred 34 mm stud envelopes centered X373. Threads, material and installed anchorage remain unverified.','Sharp bend intersections replace production bend radii; cable clips, linkage, load strength and motion sweep are not validated.']
def shape(p=None):
 p=PARAMS| (p or {});t=p['thickness'];x=p['mount_x'];y=p['mount_y'];wy=p['web_y'];tip=p['tip_x']
 s=None
 for z in p['mount_z']:
  ear=b.Pos(x+t/2,(y+wy)/2,z)*b.Box(t,wy-y+t,16)
  ear-=b.Pos(x+t/2,y,z)*b.Rot(0,90,0)*b.Cylinder(p['hole_r'],t+2)
  ear-=b.Pos(x+t/2,y-5,z)*b.Box(t+2,10,5)
  s=ear if s is None else s+ear
 # Tapered formed web with oval lightening aperture.
 poly=b.Plane.XZ*b.Polygon((x,456),(tip,456),(tip,500),(x,524),align=None)
 web=b.Pos(0,wy+t/2,0)*b.extrude(poly,amount=t)
 aperture=b.Pos(418,wy,484)*b.Rot(90,0,0)*b.Cylinder(9,t+4)
 aperture+=b.Pos(427,wy,484)*b.Rot(90,0,0)*b.Cylinder(9,t+4)
 aperture+=b.Pos(422.5,wy,484)*b.Box(9,t+4,18)
 s+=web-aperture
 face=b.Pos(tip-t/2,(wy+124)/2,478)*b.Box(t,124-wy,44)
 face-=b.Pos(tip,p['cable_y'],467)*b.Rot(0,90,0)*b.Cylinder(5.5,t+4)
 face-=b.Pos(tip,p['cable_y'],488)*b.Box(t+4,11,12)
 s+=face
 return s.clean()
def build(api):
 define,add,group,rounded_box,cx=api
 define('accelerator-cable-bracket',shape(),'Accelerator cable mounting bracket','Holds the cable outer housing so cable pull rotates the throttle linkage. Photo-informed provisional mounting study.','induction','#879297',SOURCES,GAPS)
 add('accelerator-cable-bracket','accelerator-cable-bracket','throttle-assembly',explode=(130,100,0))

# Estimated mounting envelope only: not a verified Ford service part or thread model.
STACK = dict(stud_length_mm=34., stud_radius_mm=4., stud_center_x_mm=373.,
             inward_end_x_mm=356., nut_center_x_mm=383.5, nut_height_mm=6.,
             assumed_pitch_mm=1.25, minimum_protrusion_mm=2.5)
def mounting_stud_shape():
 return b.Rot(0,90,0)*b.Cylinder(STACK['stud_radius_mm'], STACK['stud_length_mm'])
