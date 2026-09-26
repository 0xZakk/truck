"""One-piece ALT/Thermactor carrier topology study, not an OEM dimensional replica.

F4TE-10239-AC photographs establish a common ribbed casting with open cradles.
Existing accessory ears and four engine seats are preserved provisionally. Which
photographed bore maps to each modeled seat is not established by available views.
"""
import build123d as cad
import accessory_brackets as base
import alternator_carrier_1994_candidate as alt
import water_pump_thermactor_foot_candidate as ap
SOURCES=['ford-alt-thermactor-shared-carrier','ford-accessory-routing']
GAPS=[
 'Ford F4TE-10239-AC stamp and one-piece ribbed casting topology are photographed. US used-part records identify alternator/Thermactor application; Brazilian photographer application label conflicts and is not adopted.',
 'The upper open cradle is assigned to ALT and lower arm/cradle to Thermactor provisionally. Exact photograph-hole correspondence, bolt count, installed orientation and AB/AC interchange remain unverified.',
 'All existing accessory stations, ears and four engine seats are retained. Their dimensions remain assumed; no station moves or belt-length fitting occur.',
 'Open cradle contours, linking plate, ribs, section widths and axial transition are approximate packaging construction. This does not certify OEM casting fidelity, strength, stiffness, fatigue, thread engagement or belt fit.'
]
REMOVE_IDS=['alternator-support-bracket','thermactor-support-bracket']
NEW_ID='alternator-thermactor-common-carrier'
def ring_section(front,y,z,ro,ri):return base.boss(front,y,z,ro,ri)
def carrier():
 # Remove the unsupported closed-loop half of each prior study cradle. Keep
 # its ear neighborhoods and existing engine load paths for interface stability.
 upper=alt.bracket()
 lower=ap.support()
 alt_opening=ring_section(base.ALT_FACE,-325,320,89,69) & cad.Pos(444,-325,252)*cad.Box(16,200,112)
 ap_opening=ring_section(449.06,-280,100,99,77) & cad.Pos(454,-280,163)*cad.Box(16,200,102)
 # Trim only ring halves; untouched engine feet and ribs are outside these zones.
 upper-=alt_opening;lower-=ap_opening
 # A broad cast spine bridges the two former load paths. Axial thickness grows
 # continuously between their retained face planes instead of unrelated plates.
 sections=[]
 for z,x,y,width in [(132,454.06,-175,24),(180,449,-187.5,30),(235,443.56,-200,24)]:
  sections.append(cad.Plane(origin=(x,y,z),z_dir=(0,0,1))*cad.Rectangle(10,width))
 spine=cad.loft(sections,ruled=True)
 # Front reinforcing bead follows the same load path; all values assumed.
 ribs=[]
 for z,x,y,width in [(135,460,-175,7),(180,455,-187.5,7),(232,449.5,-200,7)]:
  ribs.append(cad.Plane(origin=(x,y,z),z_dir=(0,0,1))*cad.Rectangle(4,width))
 rib=cad.loft(ribs,ruled=True)
 shape=upper.fuse(lower,spine,rib)
 if isinstance(shape,cad.ShapeList):shape=cad.Compound(children=list(shape))
 return shape
