"""Ford TSB94-10-19 Fig4 attachment topology; every coordinate is provisional."""
import math
import build123d as cad
import accessory_brackets as old
import tensioner_arm
import tensioner_pulley
from tensioner_engine_support import mount_bolt_local

SOURCES=['ford-tsb-94-10-19-accessory','ford-accessory-routing']
GAPS=[
 'Ford Fig4 establishes a shared P/S–A/C–tensioner carrier, front-head bolt#1, side-head bolt#2 and two side-block nuts#3. It does not dimension any modeled hole, web, casting, stud or fastening fit.',
 'PS and A/C stations stay unchanged. The tensioner wheel is provisionally at(473.56,167,350) with its75mm assumed arm below the pivot; source drawings establish relative arrangement only.',
 'Smooth shafts and nut bores represent stud engagement without production thread pitches, grades, preload or load analysis.',
 'Adapters add dry external side bosses. Passage proximity, casting wall thickness and original old front block boss cleanup require independent source work.',
 'The original separate tensioner engine support must not be installed. This candidate replaces the PS/AC carrier and its two provisional front-axis attachment bolts.',
 'Catalog belt fit and moving tensioner travel remain unresolved. This architecture correction does not match centers to a target belt length.'
]
TENSIONER_POSITION=(473.56,167,350)
TENSIONER_ROTATION=cad.Rot(-90,0,0)*cad.Rot(*tensioner_arm.ROTATION)
REPLACE_IDS=['ps-ac-support-bracket','ps-ac-engine-bracket-bolt-1','ps-ac-engine-bracket-bolt-2']
BLOCK_STATIONS=[(292,110),(340,110)]
HEAD_SIDE=(340,310)


def sideways(radius,length,x,y,z):
 return cad.Pos(x,y,z)*cad.Rot(-90,0,0)*cad.Cylinder(radius,length)

def bridge(start,end,width=12):
 delta=tuple(b-a for a,b in zip(start,end));length=math.sqrt(sum(v*v for v in delta))
 return cad.Plane(origin=tuple((a+b)/2 for a,b in zip(start,end)),z_dir=delta)*cad.Box(width,width,length)

def carrier():
 shape=old.boss(old.PS_FACE,*old.PS_CENTER,79,68)
 for y,z in old.PS_EARS:
  dy,dz=y-280,z-410
  shape+=old.web(old.PS_FACE,(y,z),(280+dy*75/62,410+dz*75/62))
  shape+=old.boss(old.PS_FACE,y,z,10,4.8)
 for y in (205,355):shape+=old.web(old.PS_FACE,(y,410),(y,55),18)
 shape+=old.web(old.PS_FACE,(205,50),(355,50),18)
 for y,z in old.AC_EARS:shape+=old.boss(old.PS_FACE,y,z,11,5.5)
 shape-=old.axial(68,14,(old.PS_FACE+5,*old.AC_CENTER))
 shape+=old.engine_foot(90,300,old.PS_FACE+5,205)
 for y,z in old.PS_EARS:shape-=old.axial(4.8,14,(old.PS_FACE+5,y,z))
 for y,z in old.AC_EARS:shape-=old.axial(5.5,14,(old.PS_FACE+5,y,z))
 # The front-head foot atY90/Z300 is retained as Ford bolt#1.
 for x,z in [*BLOCK_STATIONS,HEAD_SIDE]:
  shape+=sideways(16,28,x,149,z)
 for start,end in [((292,155,110),(340,155,110)),((340,155,110),(340,155,310)),((292,155,110),(340,155,310)),((340,155,110),(437.56,205,180)),((340,155,310),(437.56,205,300))]:
  shape+=bridge(start,end)
 for x,z in [*BLOCK_STATIONS,HEAD_SIDE]:
  shape-=sideways(5.5,40,x,155,z)
  shape-=sideways(12,18,x,172,z)
 # Spring cartridge seats directly on the shared carrier; locator atY187/Z425.
 shape+=old.axial(32,20,(390.56,167,425))
 shape+=old.web(380.56,(167,425),(220,450),18,20)
 shape+=old.axial(9,43,(421.5,220,450))
 shape-=old.axial(5.8,17,(393.06,167,425))
 shape-=old.axial(6.35,13,(395.06,187,425))
 if isinstance(shape,list):shape=shape[0].fuse(*shape[1:])
 if isinstance(shape,list):raise RuntimeError('Carrier remains disconnected after union')
 for x,z in [*BLOCK_STATIONS,HEAD_SIDE]:
  shape-=sideways(5.5,40,x,155,z)
  shape-=sideways(12,18,x,172,z)
 shape-=old.axial(5.8,17,(393.06,167,425))
 shape-=old.axial(6.35,13,(395.06,187,425))
 return shape

def block_interface(shape):
 for x,z in BLOCK_STATIONS:
  shape+=sideways(14,31,x,119.5,z)
  shape-=sideways(5.2,25,x,123.5,z)
 return shape

def head_interface(shape):
 x,z=HEAD_SIDE;z-=255.5
 shape+=sideways(14,35,x,117.5,z)
 return shape-sideways(5.2,25,x,123.5,z)

def stud(x,z):return sideways(4.9,61,x,145.5,z)
def washer(x,z):return sideways(11,2,x,164,z)-sideways(5.2,4,x,164,z)
def nut(x,z):
 shape=cad.Pos(x,165,z)*cad.Rot(-90,0,0)*cad.extrude(cad.RegularPolygon(9.8,6),amount=9)
 return shape-sideways(5.05,11,x,169.5,z)

def head_side_bolt():
 x,z=HEAD_SIDE
 return sideways(4.9,48,x,139,z)+cad.Pos(x,163,z)*cad.Rot(-90,0,0)*cad.extrude(cad.RegularPolygon(9.8,6),amount=6)

def tensioner_parts():
 mount=cad.Pos(*TENSIONER_POSITION)*TENSIONER_ROTATION
 pieces=tensioner_arm.components();pieces['tensioner-mounting-bolt']=mount_bolt_local()
 result={k:mount*s for k,s in pieces.items()}
 wheel_mount=cad.Pos(*TENSIONER_POSITION)*cad.Rot(0,90,0)
 result.update({k:wheel_mount*s for k,s in tensioner_pulley.components().items()})
 return result

def parts():
 result={'ps-ac-support-bracket':carrier(),
         'carrier-front-head-bolt-1':old.bolt(359,385,90,300,4.9),
         'carrier-side-head-bolt-2':head_side_bolt(),**tensioner_parts()}
 for i,(x,z) in enumerate(BLOCK_STATIONS,1):
  result[f'carrier-block-stud-{i}']=stud(x,z)
  result[f'carrier-block-washer-{i}']=washer(x,z)
  result[f'carrier-block-nut-{i}']=nut(x,z)
 return result
