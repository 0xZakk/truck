"""Illustrative positive-gain EVR; dimensions/calibration/identity unverified.
Exact1994 supports filtered vent + coil/armature/disc mechanism. Complete
arrangement is comparative (EP0124399A2 Fig2), not a factory section replica.
Original evr_detail_candidate stays frozen. Units mm, EVR-local coordinates.
"""
import math
import build123d as b
import evr
from evr_detail_candidate import cz,cx,pores
TRAVEL=.8

def ring(ro,ri,h,z):return cz(ro,h,z)-cz(ri,h,z)
def spring(travel=0):
 lo=-3;hi=16.3-travel;length=hi-lo
 helix=b.Pos(0,0,lo+.6)*b.Helix((length-1.2)/7.25,length-1.2,3)
 s=b.sweep(b.Plane(origin=helix@0,z_dir=helix%0)*b.Circle(.35),helix)
 # End rings provide explicit ground seating; no force or rate asserted.
 for z in [lo,hi-.8]:s+=ring(3.5,2.5,.8,z)
 return s
def moving(travel=0):
 return {'evr-disc-illustrative':cz(5.5,.7,16.3-travel),'evr-disc-spring-illustrative':spring(travel)}
def build(travel=0):
 body=evr.body()+cz(13,6,42)+cx(3.4,11.5,1,1)
 body-=cx(2,8,24,1)
 body-=cz(8,20,-3)+cz(10,22,19)+cz(3,25,17)+cz(10,7,41)
 body-=cx(2,7,5,15)
 # Source restriction atX8..9, source mouth geometry preserved.
 body+=cx(2.1,8,1,1)
 body-=cx(2,9,4,1)+cx(.5,7,3,1)
 body-=ring(13.1,12.5,1.4,43.8)
 cap=evr.cap()+ring(13,10,7,50)+ring(13.05,12.6,1,44)
 cap-=cx(1.5,-20,40,54)
 for angle in range(0,360,90):
  cap-=b.Rot(0,0,angle)*(b.Pos(16,0,44.5)*b.Box(8,1,5))
 filt=cz(13,2,48)
 for x,y in pores():filt-=b.Pos(x,y,0)*cz(.45,2,48)
 core=ring(3,1.5,25,17)
 bobbin=ring(4.05,3.2,20,20)+ring(9.3,3.2,2,20)+ring(9.3,3.2,2,38)
 # Continuous illustrative 15-turn conductor, not a resistance-derived winding.
 helix=b.Pos(0,0,22.4)*b.Helix(15.2/15,15.2,4.25)
 first=helix@0;last=helix@1;ta=helix%0;tb=helix%1
 lower=b.Bezier((12,-3,31),(10,-3,31),(8,-3,26),first-ta*2,first)
 upper=b.Bezier(last,last+tb*2,(8,3,36),(10,3,31),(12,3,31))
 path=b.Wire([lower,helix,upper])
 coil=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(.25),path)
 clearance=b.Compound(children=[b.sweep(b.Plane(origin=e@0,z_dir=e%0)*b.Circle(.6),e) for e in [lower,upper]])
 yoke=ring(10,9.3,20,20)+ring(10,3,1,19)+ring(10,3,1,40)
 yoke-=clearance;bobbin-=clearance;bobbin-=coil;body-=coil
 parts={}
 for y,key in [(-3,'supply'),(3,'control')]:
  parts['evr-terminal-'+key]=b.Pos(22,y,31)*b.Box(20,.8,3)
 parts.update({'evr-body':body,'evr-cap':cap,'evr-vent-filter-illustrative':filt,'evr-core-illustrative':core,'evr-bobbin-illustrative':bobbin,'evr-winding-illustrative':coil,'evr-magnetic-shell-illustrative':yoke})
 parts.update(moving(travel));return parts
