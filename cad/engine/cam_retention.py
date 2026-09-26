"""Ford industrial cam-retention comparison integrated at provisional datums.

Published comparison: C5AZ6269A plate ID1-5/8in, thickness13/64in;
C5AZ6265A spacer OD1-1/2in, ID1-1/4in; two5/16-18x3/4in screws.
Plate outline, bolt stations, washer section and spacer length are assumed.
Local+Z points toward the timing gear; MOUNT locates the plate at the block face.
"""
import build123d as b
from pushrod_cover import bolt_shape

PLATE_THICKNESS=25.4*13/64
PLATE_BORE=25.4*1.625
SPACER_OD=25.4*1.5
SPACER_ID=25.4*1.25
ENDPLAY=.1  # illustrative, within published1994 .001-.007inch range
SPACER_LENGTH=PLATE_THICKNESS+ENDPLAY
BOLT_STATIONS=(-35,35)
BLOCK_FACE=373.0
GEAR_CENTER=BLOCK_FACE+SPACER_LENGTH+7
MOUNT=b.Pos(BLOCK_FACE,90,72)*b.Rot(0,90,0)


def key_shape(clearance=0):
    """Woodruff-form study; key width/diameter and seat height are assumed."""
    disk=b.Pos(GEAR_CENTER,0,17.5)*b.Rot(90,0,0)*b.Cylinder(6.35+clearance,3.175+2*clearance)
    return disk & b.Pos(GEAR_CENTER,0,7.5)*b.Box(20,10,20)


def connect_cam_nose(cam):
    """Extend the provisional cam nose through the spacer and timing-gear hub."""
    end=GEAR_CENTER+7
    cam+=b.Pos((371+end)/2,0,0)*b.Rot(0,90,0)*b.Cylinder(SPACER_ID/2,end-371)
    return cam-key_shape(.025)


def machine_gear_back(gear):
    """Gear-centered coordinates; annular relief clears stationary screw heads."""
    recess=b.Rot(0,90,0)*(b.Cylinder(47,8)-b.Cylinder(19.15,10))
    gear-=b.Pos(-3,0,0)*recess
    # The study key's flat face projects beyond the nose into this hub keyway.
    gear-=b.Pos(0,0,16.5)*b.Box(18,3.225,2.1)
    return gear


def machine_block_bolts(block):
    for x in BOLT_STATIONS:
        block-=MOUNT*(b.Pos(x,0,-6)*b.Cylinder(4.05,12.2))
    return block


def plate_shape():
    profile=b.Circle(28)+b.Rectangle(70,18)
    for x in BOLT_STATIONS:profile+=b.Pos(x,0)*b.Circle(9)
    profile-=b.Circle(PLATE_BORE/2)
    for x in BOLT_STATIONS:profile-=b.Pos(x,0)*b.Circle(4.2)
    return b.extrude(profile,amount=PLATE_THICKNESS)


def spacer_shape():
    return b.extrude(b.Circle(SPACER_OD/2)-b.Circle(SPACER_ID/2),amount=SPACER_LENGTH)


def washer_shape():
    # Unloaded spring shape is not established by the industrial illustration.
    profile=b.Circle(7.5)-b.Circle(4.2)-b.Pos(0,6)*b.Rectangle(1.5,6)
    return b.extrude(profile,amount=2)


def candidate_parts():
    parts={'cam-thrust-plate':plate_shape(),'cam-gear-spacer':spacer_shape()}
    screw=bolt_shape(25.4*.75);washer=washer_shape()
    for i,x in enumerate(BOLT_STATIONS,1):
        parts[f'cam-thrust-washer-{i}']=b.Pos(x,0,PLATE_THICKNESS)*washer
        parts[f'cam-thrust-bolt-{i}']=b.Pos(x,0,PLATE_THICKNESS+2-25.4*.75)*screw
    return parts


def build(api):
    define,add,group=api
    parent='cam-retention-assembly'
    group(parent,'Camshaft thrust plate, spacer & key','closures')
    sources=['ford-industrial-parts','fsm-33bfe47109d5','fsm-2e5473b2bf99']
    gaps=['Plate bore/thickness and spacer bore/OD follow an industrial comparison, not verified installed identities.',
          'Plate outline, bolt stations, washer section, key size, nose/hub profile and axial stations remain assumed. Female threads and press fits are not represented.',
          'The spacer provides an illustrative0.1mm axial allowance; no wear or thrust-load simulation is performed.']
    components=[
        ('cam-thrust-plate',plate_shape(),'Camshaft thrust plate','Fixed to the block, this plate limits axial camshaft movement between the shaft shoulder and timing-gear hub.'),
        ('cam-gear-spacer',spacer_shape(),'Cam timing-gear spacer','Sets the shoulder-to-hub distance around the thrust plate, allowing controlled axial clearance rather than clamping the plate rigidly.'),
        ('cam-thrust-bolt',bolt_shape(25.4*.75),'Cam thrust-plate bolt','Fastens the stationary thrust plate to the block. The industrial comparison specifies5/16-18 ×3/4-inch.'),
        ('cam-thrust-washer',washer_shape(),'Cam thrust-plate washer','Separate washer shown under each retaining bolt in the industrial exploded drawing; its section is provisional.'),
        ('cam-timing-key',key_shape(),'Camshaft timing-gear key','Registers the gear to the cam nose through matching shaft and hub seats. The woodruff-form dimensions remain provisional.')]
    for id,s,name,function in components:define(id,s,name,function,'closures','#a3adb3',sources,gaps)
    add('cam-thrust-plate','cam-thrust-plate',parent,(BLOCK_FACE,90,72),(125,0,0),(0,90,0))
    add('cam-gear-spacer','cam-gear-spacer','cam-motion',(BLOCK_FACE,0,0),(155,0,0),(0,90,0))
    add('cam-timing-key','cam-timing-key','cam-motion',(0,0,0),(0,0,70))
    for i,x in enumerate(BOLT_STATIONS,1):
        add(f'cam-thrust-washer-{i}','cam-thrust-washer',parent,(BLOCK_FACE+PLATE_THICKNESS,90,72-x),(170,0,0),(0,90,0))
        add(f'cam-thrust-bolt-{i}','cam-thrust-bolt',parent,(BLOCK_FACE+PLATE_THICKNESS+2-25.4*.75,90,72-x),(210,0,0),(0,90,0))
