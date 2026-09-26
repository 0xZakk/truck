"""EVR exterior and ports from Ford illustration and Standard VS52 catalog.

Dimensions and mounting datum are provisional. No internal decomposition is
claimed without a section or teardown; cap and terminals are externally distinct.
"""
import build123d as b
POSITION=(-420,-65,395)
MOUNT=b.Pos(*POSITION)*b.Rot(0,0,90)
SOURCES=['ford-evr-factory','standard-vs52','truck-egr-evtm']
GAPS=['Exterior dimensions, mounting ears, hose diameters and installed datum are provisional. Factory EVTM locates the unit below EVP at the left rear of the engine.',
 'Solenoid winding, magnetic circuit, moving valve, atmospheric bleed/filter, terminal straps and seals remain unmodeled; this is an exterior reconstruction, not a complete internal replica.',
 'Port routing is source-supported. No calibrated vacuum response or electrical simulation is claimed. Mounting bracket and fasteners remain unfinished.']

def cyl(r,h,z=0):
 return b.Pos(0,0,z)*b.Cylinder(r,h,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))

def body():
 s=cyl(16,42)+cyl(12,8,-8)
 # Molded connector housing, open at its outboard face.
 s+=b.Pos(21,0,31)*b.Box(24,18,15)
 s-=b.Pos(26,0,31)*b.Box(22,14,11)
 for z in (1,15):
  s+=b.Pos(12,0,z)*b.Rot(0,90,0)*cyl(3.4,18)
  for x in (22,26):s+=b.Pos(x,0,z)*b.Rot(0,90,0)*b.Cone(4.1,3.4,2,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
  s-=b.Pos(8,0,z)*b.Rot(0,90,0)*cyl(2,24)
 for y in (-3,3):s-=b.Pos(22,y,31)*b.Box(20,.8,3)
 # Two ear openings, constrained only by the catalog count.
 for y in (-23,23):
  ear=b.Pos(0,y,27)*b.Box(5,22,14)
  ear-=b.Pos(0,y,27)*b.Rot(0,90,0)*b.Cylinder(3.3,8)
  s+=ear
 return s

def cap():
 s=cyl(18,7,42)+cyl(15,10,49)
 s-=cyl(13,16,41)
 for angle in range(0,360,45):
  s+=b.Rot(0,0,angle)*(b.Pos(17.8,0,45.5)*b.Box(1.5,2,7))
 return s

def parts():
 return {'evr-body':(body(),'EVR body and hose ports','Receives manifold vacuum at the lower nipple and delivers controlled vacuum from the upper nipple to the EGR valve. Internal valve and magnetic components remain unmodeled.'),
 'evr-cap':(cap(),'EVR upper cap','Externally distinct upper cap. Hidden vent and filter construction remains unresolved.'),
 'evr-terminal-supply':(b.Pos(22,-3,31)*b.Box(20,.8,3),'EVR power terminal','C180 receives switched EEC power on circuit 361, red. Physical cavity assignment and internal strap routing are unverified.'),
 'evr-terminal-control':(b.Pos(22,3,31)*b.Box(20,.8,3),'EVR control terminal','C180 connects to the PCM control on circuit 360, brown/pink, PCM pin 33. Physical cavity assignment remains unverified.')}

def build(api):
 define,add,group=api
 group('egr-vacuum-regulator','EGR vacuum regulator','egr')
 for i,(id,(s,name,function)) in enumerate(parts().items()):
  define(id,s,name,function,'induction','#343936' if id in ('evr-body','evr-cap') else '#b5a278',SOURCES,GAPS)
  add(id,id,'egr-vacuum-regulator',POSITION,(-70,0,20*i),(0,0,90))
