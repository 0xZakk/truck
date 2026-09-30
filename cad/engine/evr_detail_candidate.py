"""Illustrative filtered atmospheric passage only; not a complete EVR valve.
Exact1994 supports filter/vent existence, not these estimated dimensions.
Lower/source nipple remains unfinished. No coil, disc or calibration claimed.
"""
import build123d as b
import evr

def cz(r,h,z):return evr.cyl(r,h,z)
def cx(r,x,length,z):return b.Pos(x,0,z)*b.Rot(0,90,0)*cz(r,length,0)
def pores():
 return [(x,y) for x in range(-8,9,2) for y in range(-8,9,2) if x*x+y*y<81]
def build():
 body=evr.body()+cz(13,6,42)
 # Remove inherited tangent-only lower nipple root; preserve mouth/barbs.
 body+=cx(3.4,11.5,1,1)
 body-=cx(2,8,24,1)
 body-=cz(10,11,38)+cz(2,25,15)+cx(2,0,9,15)
 cap=evr.cap()+(cz(13,7,50)-cz(10,7,50))
 cap-=cx(1.5,-20,40,54)
 filt=cz(13,2,48)
 for x,y in pores():filt-=b.Pos(x,y,0)*cz(.45,2,48)
 return {'evr-body':body,'evr-cap':cap,'evr-vent-filter-illustrative':filt}
