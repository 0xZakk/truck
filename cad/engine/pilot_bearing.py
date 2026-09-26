"""FC65662 pilot-bearing construction study; internal layout is illustrative."""
import math
import build123d as b
POSITION=(-381,0,0)
ROTATION=(0,-90,0)
MOUNT=b.Pos(*POSITION)*b.Rot(*ROTATION)
OD=1.44*25.4;BORE=.6721*25.4;WIDTH=.67*25.4
N=16;RR=1.5;PITCH=BORE/2+RR
SOURCES=['timken-pilot-application','timken-pilot-dimensions']
GAPS=['Timken application catalog specifies FC65662 for 1990–2002 six-cylinder truck applications including 300/4.9L. Installed identity is not inspected.',
 'Needle-bearing table gives 1.4400 inch OD, 0.6721 inch shaft diameter and 0.6700 inch width. The same guide pilot table gives 1.450/0.671/0.669 inch; this discrepancy is preserved, not treated as manufacturing tolerance.',
 'Sixteen needles, needle size, cage, race section, seal and axial seating depth are illustrative. SPCL catalog type lacks a production section drawing. No rolling/contact/friction simulation or production interference fit.']
def cyl(r,h,z=0):return b.Pos(0,0,z)*b.Cylinder(r,h,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def ring(ro,ri,h,z=0):return cyl(ro,h,z)-cyl(ri,h+2,z-1)
def case():return ring(OD/2,PITCH+RR,WIDTH)+ring(PITCH+RR,8.8,1.4)
def cage():
 s=ring(PITCH+1.15,PITCH-1.15,13.6,1.6)
 for i in range(N):
  a=i*math.tau/N;s-=b.Pos(PITCH*math.cos(a),PITCH*math.sin(a),0)*cyl(1.65,11.4,2.8)
 return s

def needle():return cyl(RR,11,3)
def seal():return ring(PITCH+RR-.03,8.65,1.5,WIDTH-1.5)
def crank_interface(crank):
 return crank-MOUNT*cyl(OD/2+.025,WIDTH+.2)
def parts():
 out={'pilot-bearing-case':MOUNT*case(),'pilot-bearing-cage':MOUNT*cage(),'pilot-bearing-seal':MOUNT*seal()}
 for i in range(N):
  a=i*math.tau/N
  out[f'pilot-bearing-needle-{i+1}']=MOUNT*b.Pos(PITCH*math.cos(a),PITCH*math.sin(a),0)*needle()
 return out

def build(api):
 define,add,group=api
 group('pilot-bearing-assembly','Clutch pilot bearing','crank-motion')
 for id,shape,name,desc,color in [
 ('pilot-bearing-case',case(),'Pilot bearing outer case','Locates the needle bearing in the crankshaft recess and supports its rolling race. The section and press fit are provisional.','#8e969c'),
 ('pilot-bearing-cage',cage(),'Pilot bearing cage','Spaces the needles around the transmission input-shaft pilot. Pocket count and cage construction are illustrative.','#bb9c60'),
 ('pilot-bearing-needle',needle(),'Pilot bearing needle','Rolls between the input-shaft pilot and outer race when shaft speeds differ. Sixteen needles illustrate the mechanism; actual count and dimensions are unverified.','#b2b9bf'),
 ('pilot-bearing-seal',seal(),'Pilot bearing seal','Illustrates the bearing closure around the shaft. Exact installed seal architecture and lip geometry remain unverified.','#343b3b')]:
  define(id,shape,name,desc,'rotating',color,SOURCES,GAPS)
 for id in ['pilot-bearing-case','pilot-bearing-cage','pilot-bearing-seal']:
  add(id,id,'pilot-bearing-assembly',POSITION,(-80 if id.endswith('case') else -140 if id.endswith('cage') else -200,0,0),ROTATION)
 for i in range(N):
  a=i*math.tau/N;x=PITCH*math.cos(a);y=PITCH*math.sin(a)
  add(f'pilot-bearing-needle-{i+1}','pilot-bearing-needle','pilot-bearing-assembly',(-381,y,x),(-140,30*math.sin(a),30*math.cos(a)),ROTATION)
