"""Pressure-switch teaching assembly; EVTM behavior, provisional internal geometry."""
import build123d as b
POSITION=(-245,165,115)
ROTATION=(-90,0,0)
SOURCES=['truck-oil-pressure-evtm','standard-ps238-switch']
GAPS=['Exterior follows a Standard PS-238 comparison photograph; exact installed part, dimensions, thread and contact construction are unverified. The factory catalog identifies E9TZ9278A.', 'Internal diaphragm, carrier, contact and spring geometry is a functional teaching arrangement, not a measured PS-238 or Ford cutaway. No switching pressure, hysteresis or diaphragm deformation is simulated.', 'Staged on the lower rear cam side according to the EVTM location index. Block boss, oil passage and connector are not yet reconstructed; placement is not verified installed fit.']

def build(api):
    define,add,group,spring=api
    group('oil-pressure-switch-assembly','Oil-pressure switch study','lubrication',position=POSITION)
    def cz(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
    def ring(ro,ri,a,z):return cz(ro,a,z)-cz(ri,a-1,z+1)
    body=cz(6.5,0,12)+b.Pos(0,0,16)*b.Cone(6.5,13,8)
    body+=b.Pos(0,0,20)*b.extrude(b.RegularPolygon(14,6),amount=4)
    body-=cz(2,-1,19)
    body-=cz(11,18,25)
    diaphragm=cz(11,20,20.3)
    carrier=cz(9,20.3,22.6)
    moving=ring(6,3,22.6,22.9)
    terminal=cz(7,23.9,24.2)+cz(1.5,24.2,44)
    cap=cz(12,24,38)-cz(10,23,35)-cz(1.7,34,39)
    rim=ring(14,12,24,25.5)
    coil=b.Pos(0,0,23)*spring(8,.4,11.6,6)
    # Illustrative grounded flexible contact bridge, separate from the carrier.
    # It touches the moving contact at x=-5.8 and the metal-body inner wall.
    bridge=b.Pos(-8.4,0,22.75)*b.Box(5.2,1,.3)
    bridge-=moving
    rows=[('body',body,'Pressure switch metal body','Admits oil through the inlet and provides the grounded housing. The inlet thread is a nominal envelope with unverified dimensions.','#a8adb0'),('diaphragm',diaphragm,'Pressure switch diaphragm','Separates oil from the electrical chamber and transmits pressure force. Manufacturer material description supports a diaphragm; this flat pose does not simulate deformation.','#ac8557'),('carrier',carrier,'Pressure switch contact carrier','Illustrative insulated carrier transfers diaphragm displacement to the moving contact. Internal construction is not established by the exterior photograph.','#c6b795'),('moving-contact',moving,'Pressure switch moving contact','In this illustrative normally-open arrangement, upward displacement meets the fixed contact and grounds the terminal. The factory EVTM establishes the switching behavior, not this contact shape.','#b5b9bc'),('terminal',terminal,'Pressure switch terminal and fixed contact','Connects the external single stud to the fixed contact. Contact flange and stud dimensions are provisional.','#bac0c2'),('insulator',cap,'Pressure switch terminal insulator','Insulates the terminal from the grounded metal housing. Blue exterior follows the manufacturer photograph.','#3279ad'),('rim',rim,'Pressure switch retaining rim','Illustrates the metal crimp retaining the insulating cap. Manufacturing seam and forming details remain unverified.','#a4a9a9'),('spring',coil,'Pressure switch return spring','Illustrative spring opposes pressure force and returns the contacts to their open state. No threshold or spring rate is assigned.','#87969d'),('ground-bridge',bridge,'Pressure switch ground contact bridge','Illustrates the electrical connection from the moving contact to the grounded body. Its flexible construction is hypothetical, not a documented production part.','#b7a474')]
    for i,(key,shape,name,fn,color) in enumerate(rows):
        ident='oil-pressure-'+key
        define(ident,shape,name,fn,'lubrication',color,SOURCES,GAPS)
        add(ident,ident,'oil-pressure-switch-assembly',rotation=ROTATION,explode=((i%3-1)*30,-i*12,0))
