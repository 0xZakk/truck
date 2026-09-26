"""MotoRad 244-192 replacement-envelope thermostat; internal profiles illustrative."""
import build123d as b

def build(api):
    define,add,group,cx,spring=api
    group('thermostat-assembly','Thermostat · wax-element study','coolant-outlet-assembly')
    sources=['motorad-244-192','system-b852e150201f','system-44801c5452af']
    gaps=['Replacement cross-reference, not identification of the installed thermostat. Flange diameter 53.85 mm, flange thickness 1.27 mm and overall height 37.85 mm are manufacturer values.',
          'Internal shapes, spring, valve travel, wax volume and support dimensions are illustrative. Placement is provisional; coolant outlet and head interfaces remain unfinished.',
          'Manufacturer part suffix says 192 while opening-temperature field says 190 F; temperature calibration is unresolved. No temperature-to-lift simulation is claimed.']
    def ring(ro,ri,w):return cx(ro,w)-cx(ri,w+2)
    frame=ring(53.85/2,13.5,1.27)
    # Front bridge reaches +21.76; rear cage reaches -16.09: 37.85 total.
    for y in [-20,20]:frame+=b.Pos(10.88,y,0)*b.Box(21.76,1.27,5)
    frame+=b.Pos(21.125,0,0)*b.Box(1.27,41.27,5)
    frame-=b.Pos(0,23,0)*cx(1.2,5)
    cage=b.Pos(-15.455,0,0)*ring(19,6,1.27)
    for y in [-18,18]:cage+=b.Pos(-8.36,y,0)*b.Box(14.19,1.27,5)
    valve=b.Pos(-1.635,0,0)*ring(1.15*25.4/2,5.1,2)
    cup=b.Pos(-8.5,0,0)*cx(5,13)
    cup-=b.Pos(-7.4,0,0)*cx(4.2,13)
    wax=b.Pos(-9,0,0)*cx(4.1,9)
    diaphragm=b.Pos(-3.7,0,0)*ring(4.1,1.55,1.5)
    piston=b.Pos(8.5,0,0)*cx(1.5,24)
    coil=b.Pos(-14,0,0)*b.Rot(0,90,0)*spring(9,.7,10,4)
    jiggle=b.Pos(0,23,0)*cx(.8,4)+b.Pos(2,23,0)*cx(1.65,1)
    pieces=[('thermostat-frame',frame,'Thermostat flange and bridge','Seats in the coolant outlet and supports the actuator reaction point.','#aab6bd',80),
      ('thermostat-cage',cage,'Thermostat spring cage','Retains and supports the return spring behind the valve.','#92a4ad',-100),
      ('thermostat-poppet',valve,'Thermostat poppet valve','Controls the radiator flow opening; a closed seat restricts that path during warm-up.','#aebdc1',-160),
      ('thermostat-capsule',cup,'Thermostat actuator capsule','Copper enclosure transfers coolant heat to the wax element.','#ba8050',-220),
      ('thermostat-wax',wax,'Thermostat wax charge','Thermally expanding material supplies actuator displacement. Composition and response curve are not established.','#dbb869',-280),
      ('thermostat-diaphragm',diaphragm,'Thermostat actuator seal · interpretation','Illustrates separation of the wax charge from the moving piston; exact production seal construction is unverified.','#40484b',160),
      ('thermostat-piston',piston,'Thermostat actuator piston','Reacts against the bridge as expansion moves the capsule and valve.','#c3ced0',220),
      ('thermostat-spring',coil,'Thermostat return spring','Returns the valve toward its seat as the actuator cools. Rate and preload are unknown.','#849ba6',-340),
      ('thermostat-jiggle-pin',jiggle,'Thermostat air-bleed jiggle pin','The manufacturer lists one jiggle-pin check valve. Its detailed geometry and orientation remain provisional.','#b6a775',280)]
    for id,shape,name,function,color,ex in pieces:
        define(id,shape,name,function,'cooling',color,sources,gaps)
        add(id,id,'thermostat-assembly',explode=(ex,0,0))
