"""Replacement damper envelope with explicitly illustrative internal decomposition."""
import json
import math
import build123d as b
from first_assembly import ROOT

def build(api):
    define,add,group,cx=api
    ledger=json.loads((ROOT/'inventory/engine/replacement-specs-2026-09-23.json').read_text())
    spec=next(c['values'] for c in ledger['claims'] if c['part_number']=='594-152')
    radius=spec['diameter_mm_converted']/2
    width=spec['width_mm_converted']
    # Catalog measures overall replacement envelope, not these internal sections.
    bore=21.05; hub_radius=55; rubber_radius=60; ring_width=24
    def ring(ro,ri,w):return cx(ro,w)-cx(ri,w+2)
    sources=['dorman-2006-oes-catalog','dorman-594-152']
    gaps=['Only the 6.42-inch overall diameter and 2.8-inch overall width are catalog dimensions for Dorman 594-152. Internal diameters, section widths, keyway and grooves are not dimensioned.',
          'Axial placement follows the provisional crank snout. It is not an established engine datum or verified installed OE part.',
          'Bonded internal decomposition is an educational interpretation, not a service disassembly. Key and retaining hardware are represented by a provisional joint study. Integrated pulley grooves are now represented; their production profile and belt plane remain unverified.']
    group('damper-assembly','Crankshaft vibration damper','crank-motion',position=(454.56,0,0))
    hub=ring(27,bore,width)+b.Pos(20,0,0)*ring(hub_radius,bore,ring_width)
    from damper_attachment import hub_interface
    hub=hub_interface(hub)
    # Front recessed web follows the replacement photo; depth is provisional.
    hub-=b.Pos(23.5,0,0)*ring(53,27,19)
    rubber=b.Pos(20,0,0)*ring(rubber_radius,hub_radius+.03,ring_width)
    inertia=b.Pos(20,0,0)*ring(radius,rubber_radius+.03,ring_width)
    # Six provisional V grooves across the integrated belt rim. The profile,
    # spacing and depth are comparison geometry, not a pulley production trace.
    for i in range(6):
        x=10.1+i*3.56;half=1.7*math.tan(math.radians(20))
        cutter=b.revolve(b.Polygon((x-half,radius+.01),(x,radius-1.7),(x+half,radius+.01),align=None),axis=b.Axis.X)
        inertia-=cutter
    gaps.append('Front web recess and six integrated pulley grooves follow replacement appearance, but groove count, pitch, depth, root radius and web thickness remain provisional.')
    pieces=[('damper-hub',hub,'Damper hub','Connects the damper assembly to the crankshaft. The modeled keyway and retaining joint illustrate the attachment; production dimensions remain unverified.','#7b8990',180),
            ('damper-elastomer',rubber,'Damper elastomer','An elastic layer couples the hub to the inertia ring; deformation dissipates torsional vibration energy. This section is illustrative.','#393e40',260),
            ('damper-inertia-ring',inertia,'Damper inertia ring','The outer mass responds to crankshaft torsional oscillation through the elastic coupling. Rigid viewer rotation does not simulate vibration or damping.','#919b9c',340)]
    for id,shape,name,function,color,explode in pieces:
        define(id,shape,name,function,'rotating',color,sources,gaps)
        add(id,id,'damper-assembly',explode=(explode,0,0))
