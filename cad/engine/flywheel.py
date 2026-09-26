"""LFW132-family flywheel study constrained by HICENGINE FFM68 dimensions.

Replacement dimensional comparison, not verified installed Ford geometry.
Local +Z points rearward; front mounting face is Z=0.
"""
import math
import build123d as b
POSITION=(-393,0,0)
ROTATION=(0,-90,0)
MOUNT=b.Pos(*POSITION)*b.Rot(*ROTATION)
SOURCES=['luk-flywheel','hicengine-ffm68']
GAPS=['HICENGINE FFM68 is a replacement cross-reference to LFW132, not an inspected OEM flywheel or proof of installed identity.',
 'Catalog constrains 362 mm OD, 44.5 mm bore, 25 mm thickness, six 11 mm crank holes on 76 mm PCD, 295 mm cover PCD and 164 teeth. Axial datums, recesses, cover hole count/threads and angular indexing remain provisional.',
 'Ring width, shrink fit, tooth pressure angle/profile, balance drilling, dowels and fastener thread/grade are unverified. Clutch diameter remains unresolved between catalog options; pilot bearing and clutch internals remain unfinished.']
HOLES=[(38*math.cos(i*math.tau/6),38*math.sin(i*math.tau/6)) for i in range(6)]
def cyl(r,h,z=0):return b.Pos(0,0,z)*b.Cylinder(r,h,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def body():
 s=cyl(170,25)-cyl(22.25,27,-1)
 # Front recess and ring seat are assumed section geometry.
 s-=cyl(145,12)-cyl(55,14,-1)
 for x,y in HOLES:s-=b.Pos(x,y,-1)*cyl(5.5,27)
 for i in range(6):
  a=i*math.tau/6+math.pi/6
  s-=b.Pos(147.5*math.cos(a),147.5*math.sin(a),15)*cyl(4.2,12)
 return s

def ring_gear():
 # Involute construction uses assumed standard pressure angle; exact production
 # tooth form remains unverified, while outside diameter/count are catalog data.
 n=164;module=362/(n+2);pitch=n*module/2
 base=pitch*math.cos(math.radians(20));root=pitch-1.25*module;tip=181
 def inv(r):
  t=math.sqrt(max(0,(r/base)**2-1));return t-math.atan(t)
 half=math.pi/(2*n)-.12/(2*pitch)
 points=[]
 for i in range(n):
  a=i*math.tau/n
  points.append((root*math.cos(a-math.pi/n),root*math.sin(a-math.pi/n)))
  for r in [root+(tip-root)*j/8 for j in range(9)]:
   t=a-half-inv(pitch)+inv(r);points.append((r*math.cos(t),r*math.sin(t)))
  for r in [root+(tip-root)*j/8 for j in reversed(range(9))]:
   t=a+half+inv(pitch)-inv(r);points.append((r*math.cos(t),r*math.sin(t)))
 return b.Pos(0,0,5)*b.extrude(b.Polygon(*points,align=None)-b.Circle(170),amount=10)

def bolt():
 return cyl(5,37,-12)+b.Pos(0,0,25)*b.extrude(b.RegularPolygon(9,6),amount=5)

def crank_interface(crank):
 # Common provisional rear-flange datum, with a close-clearance register.
 crank+=MOUNT*cyl(22.2,5)
 for x,y in HOLES:crank-=MOUNT*(b.Pos(x,y,-14)*cyl(5.1,15))
 return crank

def build(api):
 define,add,group=api
 group('flywheel-assembly','Flywheel & starter ring gear','crank-motion')
 define('flywheel-body',body(),'Flywheel body','Stores rotational energy and provides the clutch friction face and mounting pattern. Replacement dimensions constrain this study; installed profile and clutch variant remain unverified.','rotating','#8b9193',SOURCES,GAPS)
 define('flywheel-ring-gear',ring_gear(),'Starter ring gear','Its 164 teeth provide the starter engagement around the flywheel. Exact tooth profile, ring width and interference fit remain provisional.','rotating','#8c8f88',SOURCES,GAPS)
 define('flywheel-crank-bolt',bolt(),'Flywheel crankshaft bolt','One of six fasteners clamping the flywheel to the crankshaft. Smooth shank and assumed head represent attachment; production thread, grade and engagement remain unverified.','rotating','#a4a9ab',SOURCES,GAPS)
 for id in ['flywheel-body','flywheel-ring-gear']:add(id,id,'flywheel-assembly',POSITION,(-100 if id=='flywheel-body' else -170,0,0),ROTATION)
 for i,(x,y) in enumerate(HOLES,1):
  p=b.Vector(-393,y,x)
  add(f'flywheel-crank-bolt-{i}','flywheel-crank-bolt','flywheel-assembly',tuple(p),(-220,0,0),ROTATION)
