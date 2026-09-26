"""Photograph-informed cast surfaces on provisional retained mounting stations.

The F4TE-10239-AC photos show broad webs, recessed panels, raised perimeter ribs
and a narrow asymmetric extension. Their hole correspondence and dimensions are
not measured. This candidate improves those visible features without claiming a
production trace, changing hardware, or tuning any station to belt length.
"""
import math
import build123d as cad
import accessory_brackets as base
import alternator_carrier_1994_candidate as alt
import water_pump_thermactor_foot_candidate as ap
SOURCES=['ford-alt-thermactor-shared-carrier','ford-accessory-routing']
NEW_ID='alternator-thermactor-common-carrier'
REMOVE_IDS=['alternator-support-bracket','thermactor-support-bracket']
GAPS=[
 'F4TE-10239-AC photographs support a broad ribbed casting, recessed panels and narrow asymmetric fork extension. Exact photo-hole mapping and installed orientation remain unverified.',
 'Upper arched web is assigned to alternator and lower extended arm to Thermactor provisionally. All accessory stations, ears, four engine feet, axial faces and hardware are retained assumptions, not factory datums.',
 'The visible casting silhouette is reconstructed with a107mm outer upper arc,70mm opening, recessed panels and angular fork. Radii, pocket depth, perimeter rib widths, draft, fillets and load capacity are unverified; this is not an OEM manufacturing replica.',
 'Medial wall stops outboard of the existing heater-return tube; lower wall clears the Thermactor front-plate ear. Those boundaries are provisional packaging constraints rather than production measurements.',
 'No station has been moved to match catalog belt length. Existing belt/outlet interference and the unresolved effective-gauge comparison remain independent blockers.'
]
def prism(points,x,depth):return cad.Pos(x,0,0)*cad.extrude(cad.Plane.YZ*cad.Polygon(*points,align=None),amount=depth,dir=(1,0,0))
def carrier():
 # Keep the four demonstrated model seat/ear interfaces, replacing thin closed
 # loops and rods only in their free spans. These are assumed interfaces.
 upper=alt.bracket()
 upper-=base.boss(base.ALT_FACE,-325,320,89,69) & cad.Pos(444,-325,252)*cad.Box(16,200,112)
 lower=ap.support()
 lower-=base.boss(449.06,-280,100,99,77) & cad.Pos(454,-280,100)*cad.Box(16,220,240)
 # Restore the two mounting-ear collars after removing the old annular support.
 collars=[base.boss(449.06,y,100,11,5.5) for y in (-195,-365)]
 # Broad curved upper web with shallow recessed panels and radial stiffeners.
 arch=base.boss(base.ALT_FACE,-325,320,107,70) & cad.Pos(444,-325,379)*cad.Box(20,240,118)
 pockets=base.boss(base.ALT_FACE+4,-325,320,100,77,width=7) & cad.Pos(448,-325,379)*cad.Box(20,240,118)
 for degrees in (0,45,90,135,180):
  t=math.radians(degrees)
  p0=(-325+72*math.cos(t),320+72*math.sin(t));p1=(-325+108*math.cos(t),320+108*math.sin(t))
  pockets-=base.web(base.ALT_FACE+3,p0,p1,5,9)
 arch-=pockets
 # Broad central casting wall, with perimeter left after front pocket cuts.
 body_points=[(-220,326),(-155,308),(-153,237),(-153,161),(-163,128),(-195,125),(-213,158),(-231,225)]
 body=prism(body_points,435,14)
 body=cad.fillet(body.edges().filter_by(cad.Axis.X),3)
 for points in [[(-212,307),(-163,294),(-162,247),(-215,243)],[(-215,230),(-162,233),(-163,174),(-200,168)]]:
  body-=prism(points,442,8)
 # Narrow lower extension follows the photographed arm/fork construction rather
 # than wrapping a second circular ring. Its route is still a packaging inference.
 arm_points=[(-194,108),(-207,181),(-350,183),(-378,104),(-358,96),(-337,159),(-228,159),(-217,102)]
 arm=prism(arm_points,449.06,10)
 arm=cad.fillet(arm.edges().filter_by(cad.Axis.X),2)
 recess=[(-214,175),(-345,176),(-367,112),(-363,110),(-339,166),(-222,166)]
 arm-=prism(recess,453.06,7)
 # Axial transition joins the broad upper wall and lower fork smoothly.
 transition=cad.loft([cad.Plane(origin=(442,-195,160),z_dir=(0,0,1))*cad.Rectangle(14,42),cad.Plane(origin=(454,-195,130),z_dir=(0,0,1))*cad.Rectangle(10,30)],ruled=True)
 chunks=[]
 for item in (upper,lower,arch,body,arm,transition,*collars):
  if isinstance(item,cad.ShapeList):
   for piece in item: chunks.extend(piece.solids())
  else: chunks.extend(item.solids())
 shape=chunks[0].fuse(*chunks[1:])
 if isinstance(shape,cad.ShapeList):shape=cad.Compound(children=list(shape))
 # Retain all fastener clearance after overlapping web construction.
 for y,z,front in [(-248,320,438.56),(-402,320,438.56),(-195,100,449.06),(-365,100,449.06)]:shape-=base.axial(5.5,18,(front+5,y,z))
 return shape
