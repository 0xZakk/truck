"""Provisional Thermactor support relocation for source-constrained pump flange.

Old upperfoot(-100,180) conflicts with the newly reconstructed pump left lug.
The complete upper load path moves to(-125,140); lowerfoot and pump ears stay.
This is packaging geometry, not a traced Ford accessory casting.
"""
from accessory_brackets import boss,web,engine_foot,axial,bolt
UPPER=(-125,140)
def support():
 face=449.06
 shape=boss(face,-280,100,98,78)
 for y in (-195,-365):shape+=boss(face,y,100,11,5.5)
 shape+=web(face,(-190,100),(-175,100),18)
 shape+=web(face,(-175,90),(-175,140),18)
 shape+=engine_foot(-100,90,face+5,-175)
 shape+=engine_foot(*UPPER,face+5,-175)
 for y in (-195,-365):shape-=axial(5.5,14,(face+5,y,100))
 return shape

def upper_bolt():return bolt(359,385,*UPPER,4.9)
def block_interface(shape):
 # Close now-unused original dry socket before new pump holes are machined.
 shape+=axial(5.2,16,(365,-100,180))
 shape+=axial(12,24,(361,*UPPER))
 shape-=axial(5.2,17,(365.5,*UPPER))
 return shape
GAPS=['Upper Thermactor support foot relocates from(-100,180) to(-125,140) in the front Y/Z plane to respect the photo-derived pump flange; all support casting, dry socket and fastener dimensions are unverified. Lower mount/pump ears are retained. No factory bracket part identity, strength or belt-load claim.']
