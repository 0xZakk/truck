"""Uninstalled pump/block joint reconstruction, constrained by exact part photos.

Preserves the provisional pump hub/bearing/heater-return frame. Moves only the
rear casting flange/gasket/impeller toward the demonstrated block mounting face.
All dimensions, bolt diameter/length and internal pump chamber profile are
assumptions; source photos establish topology, not a production drawing.
"""
import math
import build123d as b
from water_pump_gasket_topology_candidate import gasket_shape as photo_gasket, MOUNTING as PHOTO_MOUNTING,EXTRA as PHOTO_EXTRA
MOUNTING=tuple((-y,-z) for y,z in PHOTO_MOUNTING)
EXTRA=tuple(-v for v in PHOTO_EXTRA)
PUMP_POSITION=(440,-32,170)
SOURCES=['water-pump-mounting-topology','gates-water-pumps-2011','fel-pro-vin-y-gaskets']
GAPS=[
 'ATK DFF8 automotive block-front photo supports pump flange directly on block face, four mounting holes and a larger fifth opening; exact hole coordinates and installed lateral axis offset remain unmeasured.',
 'The casting now reaches modeled blockfrontX373 through its rear flange and2mmgasket; tapered chamber depth83mm is assumed to preserve the existing provisional hub/bearing/heater-return datums. This is not a verified Gates44009 dimension.',
 'All four fasteners are unthreaded8mm×31.75mm illustrative envelopes with13mmhex heads. Production bolt thread, length, head, washer construction and socket depth are unverified; these are not replacement specifications.',
 'The receiver cuts only the demonstrated front opening into the existing modeled cavity while retaining the front cylinder wall. Deeper coolant jacket, fifth-opening function, circulation and hydraulic performance remain unresolved.',
 'The larger gasket opening is retained as an unidentified passage with a provisional short pump-chamber connection; its actual cast routing is unverified. Radiator inlet neck remains a separate missing reconstruction.',
 'Impeller, mechanical seal, bearing cartridge and internal shaft geometry remain simplified. Existing belt plane and pumpY−32/Z170 coordinates are not factory dimensions.'
]
def cx(radius,start,end,y=0,z=0):
    return b.Pos((start+end)/2,y,z)*b.Rot(0,90,0)*b.Cylinder(radius,end-start)
def ring(ro,ri,start,end):return cx(ro,start,end)-cx(ri,start-1,end+1)
def gasket_shape():return b.Pos(-66,0,0)*b.Rot(180,0,0)*photo_gasket()
def housing_interface(old):
    # Retain original front wall, bearing nose and weep feature. Longer cast
    # rear chamber replaces floating rear envelope; this is pump, not block.
    shape=old & (b.Pos(110,0,0)*b.Box(168,500,500)) # localX26..194
    def section(x,r):return b.Pos(x,0,0)*b.Rot(0,90,0)*b.Circle(r)
    outer=b.loft([section(x,r) for x,r in [(-65,66),(-57,66),(-51,55),(18,29)]],ruled=True)
    inner=b.loft([section(x,r) for x,r in [(-66,59),(-57,59),(-51,51),(18,24),(27,24)]],ruled=True)
    shape+=(outer+cx(29,18,26))-inner
    # Casting boss attaches retained formed heater tube to tapered chamber.
    from cooling_connections import cylinder
    shape+=cylinder(12,32,(-2,-45,15),(0,1,0))
    shape-=cylinder(8.1,39,(-2,-44.5,15),(0,1,0))
    for y,z in MOUNTING:shape+=cx(11.5,-65,-51,y,z)
    shape+=cx(11.5,-65,-46,*EXTRA)
    for y,z in MOUNTING:shape-=cx(4.3,-66,-50,y,z)
    shape-=cx(6.5,-66,-51,*EXTRA)
    # Short illustrative connection from the unidentified fifth aperture to
    # chamber, kept explicitly provisional rather than naming its function.
    y,z=EXTRA
    inward=(y*.78,z*.78)
    channel=b.Solid.make_cylinder(6.5,math.hypot(y-inward[0],z-inward[1]),b.Plane(origin=(-54,y,z),z_dir=(0,inward[0]-y,inward[1]-z)))
    shape-=channel
    from cooling_connections import pump_housing_interface
    return pump_housing_interface(shape)
def impeller_interface(old):return b.Pos(-59,0,0)*old
# Disk centerold430→371; backing disk at369..373, vanes372..384.
def shaft_shape():return cx(8,-75,79)
def screw_shape():
    # Smooth envelope deliberately avoids inventing a sourced thread pitch.
    return cx(4,-31.75,0)+(b.Rot(0,90,0)*b.extrude(b.RegularPolygon(13/math.sqrt(3),6),amount=5.3))
def block_interface(shape):
    # Reinforce front casting around source-observed mounting holes, with dry
    # sockets that stop before cylinder1's retained outer wall (~X342.3).
    for y,z in MOUNTING:shape+=cx(10,350,373,y-32,z+170)
    shape-=cx(59,359.5,374,-32,170)
    shape-=cx(6.5,359.5,374,EXTRA[0]-32,EXTRA[1]+170)
    for y,z in MOUNTING:shape-=cx(4.3,356,374,y-32,z+170)
    return shape

def adapt_api(api):
    define,add,group,cx_original=api
    def adapted(key,shape,*args,**kwargs):
        if key=='water-pump-housing':shape=housing_interface(shape)
        elif key=='water-pump-gasket':shape=gasket_shape()
        elif key=='water-pump-impeller':shape=impeller_interface(shape)
        elif key=='water-pump-shaft':shape=shaft_shape()
        return define(key,shape,*args,**kwargs)
    return adapted,add,group,cx_original

def shifted_manifest(manifest):
    import copy
    candidate=copy.deepcopy(manifest)
    for a in candidate['assemblies']:
        if a['id'] in ('water-pump-assembly','fan-clutch-assembly'):a['position_cad_mm'][1]-=32
    for o in candidate['occurrences']:
        if o['id']=='heater-pump-return-elbow':o['position_cad_mm'][1]-=32
    return candidate

def build_hardware(api):
    define,add,group=api
    define('water-pump-mounting-screw',screw_shape(),'Water-pump mounting screw · provisional envelope','One of four fasteners clamping the pump flange; dimensions and thread are unverified.','cooling','#9ca6ad',SOURCES,GAPS)
    for n,(y,z) in enumerate(MOUNTING,1):add(f'water-pump-mounting-screw-{n}','water-pump-mounting-screw','water-pump-assembly',position=(-51,y,z),explode=(120,0,0))
