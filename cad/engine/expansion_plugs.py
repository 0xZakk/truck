"""Replacement-envelope studies; cast seats and stamped sections are provisional."""
import build123d as b

# Melling MPC-147: listed OD2.194in, height.343in. Neither is a bore size.
CAM_OD=2.194*25.4
CAM_HEIGHT=.343*25.4
WALL=1.0  # not published; uniform sheet section is an illustration
REAR_FACE=-373.0
SEAT_DEPTH=CAM_HEIGHT+.5  # assumed recessed installation
SEAT_RADIUS=CAM_OD/2+.025  # display clearance; no press-fit deformation
MOUNT=b.Pos(REAR_FACE+SEAT_DEPTH,90,72)*b.Rot(0,-90,0)

def cam_plug_shape():
    """Local+Z toward open rim/outside of engine; closed floor faces camshaft."""
    outer=b.Cylinder(CAM_OD/2,CAM_HEIGHT,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    inner=b.Pos(0,0,WALL)*b.Cylinder(CAM_OD/2-WALL,CAM_HEIGHT,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    return outer-inner

def machine_block_seat(block, cam_bore_radius):
    # Add support around the seat because the simplified cam tunnel was too thin.
    # This boss is an interface study, not a measured cast feature.
    boss=b.Pos(REAR_FACE+6,90,72)*b.Rot(0,90,0)*b.Cylinder(32,12)
    tunnel=b.Pos(REAR_FACE+7,90,72)*b.Rot(0,90,0)*b.Cylinder(cam_bore_radius,16)
    seat=MOUNT*(b.Pos(0,0,-.025)*b.Cylinder(SEAT_RADIUS,SEAT_DEPTH+1,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN)))
    return (block+boss)-tunnel-seat

def build(api):
    define,add,group=api
    group('block-plugs','Block plugs','structure')
    define('rear-cam-plug',cam_plug_shape(),'Rear camshaft bore plug',
        'Closes the rear access opening of the camshaft tunnel. The cup is a separate stationary seal; it does not support or retain the rotating camshaft.',
        'structure','#b0a895',['melling-expansion-plug-guide','ford-industrial-parts'],
        ['Melling MPC-147 replacement envelope: OD2.194in and height.343in; kit identifies its camshaft application. Installed identity is not verified.',
         'Uniform1mm cup wall, square internal corner, supporting boss, .5mm recess and clearance-fit seat are assumptions. Actual press fit, stamp radii and bore size remain unresolved.'])
    add('rear-cam-plug','rear-cam-plug','block-plugs',(REAR_FACE+SEAT_DEPTH,90,72),(-125,0,0),(0,-90,0))
