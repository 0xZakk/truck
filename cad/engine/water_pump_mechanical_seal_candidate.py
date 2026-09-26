"""Illustrative axial-face pump seal; not Gates44009 production internals.

Fits the inherited localX11..21 seal space. Generic Gates description establishes
stationary spring-loaded face and rotating shaft face; GMB generic section shows
spring/carrier/elastomer support. Materials, sections and dimensions unverified.
No inference of the truck's bearing rolling-element arrangement is made here.
"""
import build123d as b
from water_pump_joint_candidate import cx
SOURCES=['water-pump-internal-construction']
GAPS=[
 'This six-component seal is a generic axial-face construction study, not a verified Gates44009 bill of materials. No real replacement seal number is established.',
 'All face diameters,10mm stack length, carrier shape, elastomer sections, spring wire/turn count and installed compression are illustrative. Face material pairing is not established for this truck.',
 'Carrier contact at localX18..21 uses radius24 to meet the modeled housing throat; it replaces the former radius23.8 floating envelope. Housing, shaft, mounting and drive poses are unchanged.',
 'Exact bearing row count/type, rolling-element count, cages and raceway dimensions remain unknown. The existing bearing cartridge is not claimed to be a measured production bearing.',
 'Exploded geometry explains interfaces, not a pump rebuild procedure. Ford services the sealed pump as an assembly. No elastic, thermal, pressure, leakage or coolant-film simulation is included.'
]
def ring(ro,ri,start,end):return cx(ro,start,end)-cx(ri,start-1,end+1)
def spring():
 path=b.Helix(1.4,5.6,15.5)
 s=b.Pos(14.95,0,0)*b.Rot(0,90,0)*b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(.4),path=path)
 return s&(b.Pos(17.75,0,0)*b.Box(4.5,50,50))
def components():
 bellows=ring(11,9,14,20)
 for start in (16,18):bellows-=ring(11.1,10,start,start+.5)
 return {
 'water-pump-seal-carrier':ring(24,22,18,21)+ring(22,9,20,21),
 'water-pump-seal-stationary-face':ring(18,11,13.5,15.5),
 'water-pump-seal-rotating-face':ring(18,9,11,13.5),
 'water-pump-seal-shaft-collar':ring(9,8,11,13.5),
 'water-pump-seal-bellows':bellows,
 'water-pump-seal-spring':spring()
 }
LABELS={
 'water-pump-seal-carrier':('Mechanical-seal carrier · illustrative','Stationary cup fixes the seal support to the pump housing.','#a1adb5'),
 'water-pump-seal-stationary-face':('Stationary sealing face · illustrative','Spring-loaded face remains stationary while its mating face rotates.','#424d52'),
 'water-pump-seal-rotating-face':('Rotating sealing face · illustrative','Shaft-driven face meets the stationary ring across a lubricating coolant film.','#d8d5c8'),
 'water-pump-seal-shaft-collar':('Rotating seal collar · illustrative','Illustrative elastomer collar seals and couples the rotating face to the shaft.','#393a3d'),
 'water-pump-seal-bellows':('Stationary seal bellows · illustrative','Flexible secondary seal joins the stationary face to its carrier while permitting axial compliance.','#494a4d'),
 'water-pump-seal-spring':('Seal face-loading spring · illustrative','Applies axial force to hold the sealing faces together.','#b0a781')
}
EXPLODE_X={
 'water-pump-seal-carrier':285, 'water-pump-seal-stationary-face':230,
 'water-pump-seal-rotating-face':200, 'water-pump-seal-shaft-collar':180,
 'water-pump-seal-bellows':250, 'water-pump-seal-spring':270
}
def build(api):
 define,add,group=api
 group('water-pump-mechanical-seal-assembly','Mechanical face seal · illustrative construction','water-pump-assembly')
 for index,(key,shape) in enumerate(components().items()):
  label,function,color=LABELS[key];define(key,shape,label,function,'cooling',color,SOURCES,GAPS)
  add(key,key,'water-pump-mechanical-seal-assembly',explode=(EXPLODE_X[key],0,0))
