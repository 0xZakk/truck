"""Uninstalled E7TE visual topology study; all numeric geometry is estimated.
See docs/components/online-airbox-duct-specimen.md before reuse.
"""
from pathlib import Path
import numpy as np
import build123d as b
R=Path(__file__).resolve().parents[2]
O=Path(__file__).parent/'generated/online-airbox-duct-specimen'
WALL=3.0
PARAMETERS={'long_length_mm':559,'short_length_mm':533,'large_outer_radius_mm':42.5,'small_outer_radius_mm':28.5,'radial_wall_mm':WALL,'corrugation_rise_mm':5,'pitch_mm':12,'section':'estimated circular','frame':'local specimen only; X large-to-small cuff; Y tube separation; Z up'}
def stations(short=False):
 start=26 if short else 0
 end=559
 first=110 if short else 86
 last=290 if short else 254
 xs=[start,start+16,first]
 for x in np.arange(first+3,last,3): xs.append(float(x))
 xs.extend([last,320,440,543,end])
 out=[]
 for x in sorted(set(xs)):
  t=np.clip((x-first)/(last-first),0,1)
  rad=42.5-14*t
  if first<x<last:rad+=5*(1-np.cos(2*np.pi*(x-first)/12))/2
  if short:y=float(np.interp(x,[start,first,last,440,end],[-48,-48,-72,-66,-66]))
  else:y=float(np.interp(x,[start,first,last,440,end],[60,60,20,20,20]))
  out.append((x,y,rad))
 return out

def sections(rows,inner=False):
 return [b.Plane(origin=(x,y,0),x_dir=(0,1,0),z_dir=(1,0,0))*b.Circle(r-WALL if inner else r) for x,y,r in rows]

def tube(short=False):
 rows=stations(short)
 return b.loft(sections(rows),ruled=True)-b.loft(sections(rows,True),ruled=True)

def ring(x,y,r,width,thick):
 return b.extrude(b.Plane(origin=(x,y,0),x_dir=(0,1,0),z_dir=(1,0,0))*(b.Circle(r+thick)-b.Circle(r)),amount=width)

def build():
 parts={'online-airbox-duct-long':tube(),'online-airbox-duct-short':tube(True)}
 # External linking web: trim against the actual tube exteriors, preserving tangency.
 web=b.Pos(378,-23,0)*b.Box(54,60,7)
 for short in (False,True):web=web-b.loft(sections(stations(short)),ruled=True)
 parts['online-airbox-joining-web']=web
 # Estimated saddle and two open retainer fingers; no specific retained item asserted.
 saddle=ring(280,20,28.5,18,2)
 for xx in (282,294):
  saddle=saddle+b.Pos(xx,20,36)*b.Box(4,16,16)
 # Trim finger undersides against the actual duct exterior; external saddle contact only.
 saddle=saddle-b.loft(sections(stations()),ruled=True)
 parts['online-airbox-retainer']=saddle
 for i,(x,y,r) in enumerate([(8,60,42.5),(34,-48,42.5),(546,20,28.5),(546,-66,28.5)],1):
  band=ring(x,y,r,10,0.7)
  band=band+b.Pos(x+5,y,r+2.5)*b.Box(12,10,5)
  band=band-b.Pos(x+5,y,r+3)*b.Rot(90,0,0)*b.Cylinder(2.2,20)
  parts[f'online-airbox-clamp-{i}-band']=band
  parts[f'online-airbox-clamp-{i}-screw']=b.Pos(x+5,y,r+3)*b.Rot(90,0,0)*b.Cylinder(2.1,18)
 return parts
