"""Illustrative four plate screws; neither count nor dimensions Ford-verified.

Preserve current shaft/key and both plate poses. Heads seat directly on plates;
rear shaft pads bridge the inherited0.2 mm gap. Explicit mating helical threads
provide an educational retention path, not a thread/load/locking specification.
"""
import build123d as b
PARAMS=dict(head_side_x=-1,screws_per_plate=2,offset_y=8.,plate_hole_radius=1.15,head_radius=1.8,head_height=1.,front_pocket_radius=1.9,back_pad_radius=2.,core_radius=.85,thread_major_radius=1.1,thread_pitch=.5,thread_length=2.7,thread_start_x=-3.2,tap_radial_clearance=.02,tap_axial_clearance=.02)
def cx(r,h):return b.Rot(0,90,0)*b.Cylinder(r,h)
def screw():
 p=PARAMS
 core=b.Cylinder(p['core_radius'],p['thread_length'],align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 helix=b.Pos(0,0,.18)*b.Helix(p['thread_pitch'],p['thread_length']-.36,.9)
 triangle=b.Pos(0,0,.18)*(b.Plane.XZ*b.Polygon((.8,-.18),(p['thread_major_radius'],0),(.8,.18),align=None))
 ridge=b.sweep(triangle,path=helix,is_frenet=True)
 thread=(b.Pos(p['thread_start_x'],0,0)*b.Rot(0,90,0)*(core+ridge)).clean()
 shank=cx(p['core_radius'],1.)
 head=b.Pos(1.,0,0)*cx(p['head_radius'],p['head_height'])
 # Shallow cross drive is illustrative; actual head/drive is unresolved.
 head-=b.Pos(1.45,0,0)*b.Box(.3,2.6,.45)
 head-=b.Pos(1.45,0,0)*b.Box(.3,.45,2.6)
 return (b.Rot(0,180,0)*(thread+shank+head)).clean()
def thread_tap():
 """Phase-matched cutter extends beyond both shaft faces; no finite runout."""
 p=PARAMS;extra=1.5;start=.18-extra
 core=b.Pos(0,0,-extra)*b.Cylinder(p['core_radius']+p['tap_radial_clearance'],p['thread_length']+2*extra,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 helix=b.Pos(0,0,start)*b.Helix(p['thread_pitch'],p['thread_length']-.36+2*extra,.9)
 triangle=b.Pos(0,0,start)*(b.Plane.XZ*b.Polygon((.8,-.18-p['tap_axial_clearance']),(p['thread_major_radius']+p['tap_radial_clearance'],0),(.8,.18+p['tap_axial_clearance']),align=None))
 ridge=b.sweep(triangle,path=helix,is_frenet=True)
 return b.Rot(0,180,0)*b.Pos(p['thread_start_x'],0,0)*b.Rot(0,90,0)*(core+ridge)

def parts(current_shaft,current_plate,finite_thread_cutter=False):
 p=PARAMS;fastener=screw();tap=fastener if finite_thread_cutter else thread_tap();shaft=current_shaft;plate=current_plate
 for y in [-p['offset_y'],p['offset_y']]:plate-=b.Pos(0,y,0)*cx(p['plate_hole_radius'],4)
 screws={}
 for plate_index,center in enumerate([-27,27],1):
  for index,dy in enumerate([-p['offset_y'],p['offset_y']],1):
   y=center+dy
   shaft+=b.Pos(.6,y,0)*cx(p['back_pad_radius'],.2)
   shaft-=b.Pos(-2.25,y,0)*cx(p['front_pocket_radius'],3.5)
   # Female helix uses a longer phase-matched tap, avoiding artificial
   # finite-screw runout interference during unscrewing.
   placed=b.Pos(0,y,0)*fastener
   shaft-=b.Pos(0,y,0)*tap
   screws[f'throttle-plate-screw-{plate_index}-{index}-illustrative']=placed
 return {'throttle-shaft-plate-retention-illustrative':shaft.clean(),'throttle-plate-drilled-illustrative':plate.clean()},screws
