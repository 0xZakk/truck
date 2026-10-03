"""Bosch15718 comparison exterior; only AF22 primary, every other size estimated.
No host transform, installed route, target internals or manufacturing thread claim.
"""
from pathlib import Path
import math
import build123d as b
from pan_fastener_thread_candidate import solid, cz
O=Path(__file__).parent/'generated/ho2s-specimen-20261003'
P={'hex_af_primary':22.,'body_od_est':20.,'body_wall_est':1.,'thread_major_est':18.,'thread_root_est':16.2,'pitch_est':1.5,'thread_length_est':7.5,'crest_halfwidth_est':.08,'profile_halfwidth_est':.65,'cap_od_est':11.5,'cap_wall_est':.8,'cap_tip_z_est':25.,'slot_count_est':4,'slot_width_est':.7,'slot_z_start_est':8.5,'slot_z_end_est':21.5,'wire_od_est':1.3,'connector_od_est':17.,'connector_length_est':44.,'pin_od_est':1.6,'pin_square_est':6.}
SENSOR_XY=[(-1.8,-1.8),(1.8,-1.8),(-1.8,1.8),(1.8,1.8)]
CONNECTOR_XY=[(-3,-3),(3,-3),(-3,3),(3,3)]
COLORS={'metal':(.50,.46,.34,1),'silver':(.63,.65,.66,1),'cap':(.32,.34,.31,1),'white':(.85,.85,.76,1),'black':(.075,.085,.085,1),'gray':(.38,.42,.42,1),'red':(.52,.12,.055,1),'gold':(.61,.47,.23,1)}
def cone(r1,r2,a,z):return b.Pos(0,0,a)*b.Cone(r1,r2,z-a,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def box(x,y,z,at):return b.Pos(*at)*b.Box(x,y,z)
def rounded_rect(w,h,r,a,z):return b.Pos(0,0,a)*b.extrude(b.RectangleRounded(w,h,r),amount=z-a)
def drill(shape,points,r,a,z):
 for x,y in points:shape=shape-b.Pos(x,y,0)*cz(r,a,z)
 return solid(shape)
def threaded_mount(smooth=False):
 root=P['thread_root_est']/2;pitch=P['pitch_est'];length=P['thread_length_est']
 neck=cz(9.5,-8.5,0)
 hexagon=b.Pos(0,0,-7.8)*b.extrude(b.RegularPolygon(22/math.sqrt(3),6),amount=5.2)
 if smooth:thread=cz(9,0,length)
 else:
  profile=b.Plane.XZ*b.Polygon((root-.15,-.65),(9,-.08),(9,.08),(root-.15,.65),align=None)
  loop=solid(b.loft([b.Pos(0,0,pitch*i/24)*b.Rot(0,0,360*i/24)*profile for i in range(25)]))
  turns=[b.Pos(0,0,k*pitch)*loop for k in range(-1,6)]
  thread=solid(cz(root,-pitch,length+pitch).fuse(*turns)) & cz(9.1,0,length)
 return solid((neck+hexagon+thread)-cz(4.95,-9,8))
def protective_cap(blocked=False):
 # Hollow hemisphere and tube. Slots extend through the wall, not markings.
 outer=cz(5.75,7.5,19.25)+(b.Pos(0,0,19.25)*b.Sphere(5.75)&cz(6,19.25,25.1))
 inner=cz(4.95,7.4,19.25)+(b.Pos(0,0,19.25)*b.Sphere(4.95)&cz(5,19.25,24.3))
 cap=outer-inner
 if not blocked:
  # Capsule slot cutter points radially along +X, then repeats around axis.
  cut=box(7,.7,12.3,(3.5,0,15))
  for z in [8.85,21.15]:cut=cut+b.Pos(3.5,0,z)*b.Rot(0,90,0)*b.Cylinder(.35,7)
  for angle in range(0,360,90):cap=cap-b.Rot(0,0,angle)*cut
 return solid(cap)
def rear_closure():
 outer=cz(6.25,-65,-55.5)+cone(6.25,8.25,-55.5,-55)+cz(8.25,-55,-45.5)+cone(8.25,10.25,-45.5,-45)+cz(10.25,-45,-38.5)
 void=cz(5.25,-65.1,-54.5)+cz(7.25,-54.5,-44.5)+cz(9.25,-44.5,-38.4)
 return solid(outer-void)
def connector_housing(blocked=False):
 outer=rounded_rect(17,14,3,0,25)+cz(8.5,23,44)
 shell=outer-(rounded_rect(14,11,2,-.1,31)+cz(7,26,44.1))
 # Latch rails sink into outer wall; open window remains between them.
 rails=[box(1.2,4,17,(x,9,30.5)) for x in [-3,3]]
 bridges=[box(7.2,1.2,1.2,(0,10.4,z)) for z in [22.6,38.4]]
 shell=shell.fuse(*rails,*bridges)
 if blocked:shell=shell+cz(7,42,44)
 return solid(shell)
def build():
 rows={}
 def add(name,shape,frame,color,meaning):
  rows[name]={'shape':solid(shape),'frame':frame,'color':COLORS[color],'meaning':meaning}
 add('main-shell',cz(10,-38.5,-8.5)-cz(9,-38.6,-8.4),'sensor','metal','Hollow outer shell; internal ceramic/heater omitted')
 add('mounting-shell',threaded_mount(),'sensor','metal','Hex/neck and estimated visible right-hand thread')
 # Ring fits outside neck radius9.5: prior ID18 was inadequate for this neck.
 add('seat-ring',cz(10.75,-2,0)-cz(9.5,-2.1,.1),'sensor','silver','Visible annulus, not compressed sealing proof')
 add('slotted-protective-cap',protective_cap(),'sensor','cap','Rounded hollow four-slot educational cap')
 add('rear-stepped-closure',rear_closure(),'sensor','silver','Metal collar/reducer/wire exit')
 add('exit-insulator',drill(cz(5.25,-66,-64),SENSOR_XY,.65,-66.1,-63.9),'sensor','white','Visible pale face; hidden thickness estimated')
 wirecolors=['white','white','black','gray']
 for i,((x,y),color) in enumerate(zip(SENSOR_XY,wirecolors),1):
  add(f'exit-collar-{i}',b.Pos(x,y,0)*(cz(1.2,-66.2,-66)-cz(.65,-66.3,-65.9)),'sensor','red','Visible wire collar; material and seal performance unverified')
  add(f'sensor-lead-{i}',b.Pos(x,y,0)*cz(.65,-78,-64),'sensor',color,'Cut insulated lead stub; no pin mapping or conductor')
 add('connector-housing',connector_housing(),'connector','white','Open mouth and open latch; no mating fit')
 add('connector-support-face',drill(cz(7,32,35),CONNECTOR_XY,.8,31.9,35.1),'connector','gold','Estimated contact carrier face')
 add('connector-mouth-seal',cz(7,35,36)-cz(6.25,34.9,36.1),'connector','red','Visible colored ring; no sealing guarantee')
 add('connector-divider',box(.9,12,5,(0,0,37.5)),'connector','red','Visible central colored feature; function unconfirmed')
 # Actual rear photograph supports black insert; exact geometry declared amendment.
 add('connector-rear-insert',drill(rounded_rect(14,11,2,0,2),CONNECTOR_XY,.65,-.1,2.1),'connector','black','Estimated rear lead carrier, hidden thickness unknown')
 for i,((x,y),color) in enumerate(zip(CONNECTOR_XY,wirecolors),1):
  pin=cz(.8,34,41)
  pin=b.fillet(pin.edges().filter_by(b.GeomType.CIRCLE).sort_by(b.Axis.Z)[-1:],.2)
  add(f'connector-contact-{i}',b.Pos(x,y,0)*pin,'connector','gold','Estimated round-ended male contact, cut hidden termination')
  add(f'connector-lead-{i}',b.Pos(x,y,0)*cz(.65,-10,2),'connector',color,'Cut lead stub, not electrical continuity')
 return rows
