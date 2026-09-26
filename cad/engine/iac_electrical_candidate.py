"""Source-supported two-terminal topology, estimated insulating construction.

IAC-local mm. Coil is a winding envelope, not a computed conductor. The diode is
kept in the circuit explanation; no unsupported package is fabricated.
"""
import build123d as b
PARAMS=dict(coil_inner_radius=4.4,coil_outer_radius=9.3,coil_start=26.5,coil_end=65.5,
            carrier_inner_radius=4.,carrier_outer_radius=9.6,terminal_z=2.,tail_radius=.3)
TERMINALS={'iac-terminal-control-estimated':(2.,6.),'iac-terminal-vpwr-estimated':(-2.,-6.)}
def cx(r,left,right):return b.Pos((left+right)/2,0,0)*b.Rot(0,90,0)*b.Cylinder(r,right-left)
def terminal(z,y):
 blade=b.Pos(75.5,0,z)*b.Box(7,.6,1.6)
 shoulder=b.Pos(72.5,0,z)*b.Box(1,1.6,2.2)
 path=b.Bezier((72,0,z),(68.5,0,z),(68.5,y,z),(65.5,y,z))
 tail=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(.3),path)
 return blade+shoulder+tail

def build():
 # Rounded shroud with one asymmetric upper guide rib. This is a controlled
 # polarity witness, not a reproduced latch or a dimensional connector claim.
 outer=b.Pos(70,0,0)*b.extrude(b.Plane.YZ*b.RectangleRounded(14,12,1.5),amount=10)
 opening=b.Pos(74,0,0)*b.extrude(b.Plane.YZ*b.RectangleRounded(10,8,1),amount=8)
 cap=cx(12,68,70)-cx(2,67,71)+outer-opening
 cap+=b.Pos(77,0,3.5)*b.Box(6,1.2,1)
 carrier=(cx(9.6,24,26.5)+cx(4.4,26.5,65.5)+cx(9.6,65.5,68))-cx(4,23,69)
 coil=cx(9.3,26.5,65.5)-cx(4.4,26,66)
 parts={ident:terminal(z,y) for ident,(z,y) in TERMINALS.items()}
 # Embedded exact-contact envelopes hold the terminal shoulders and isolate
 # conductors from case. Production molding or crimp method is unknown.
 for t in parts.values():cap-=t;carrier-=t
 parts.update({'iac-connector-cap':cap,'iac-coil':coil,'iac-coil-carrier-estimated':carrier})
 return parts

def mating_witness():
 """Unexported positive/negative key gauge; not a vehicle harness part."""
 gauge=b.Pos(75,0,0)*b.extrude(b.Plane.YZ*b.RectangleRounded(9.6,7.6,.8),amount=4)
 gauge-=b.Pos(77,0,3.3)*b.Box(5,1.6,1.4)
 # Contact cavities only provide clearance around the two header pins.
 for z in [-2,2]:gauge-=b.Pos(77,0,z)*b.Box(5,1,2)
 return gauge
