"""Service-source-informed water pump study; all dimensional geometry provisional.

Local +X points toward fan. Internal separation is educational, not a rebuild
procedure: Ford specifies replacing the sealed pump assembly.
"""
import math
import build123d as b

def build(api):
    define, add, group, cx = api
    sources=['system-7b01cf423275','system-628ac5b60213','gates-water-pumps-2011']
    gaps=[
        'F6TZ8501KB / Gates 44009 application is sourced; no pump dimensions or installed datums are established.',
        'Casting outline, ports, mounting pattern, vane count/profile and all internal dimensions are illustrative. Bearing is represented as a sealed cartridge, not individual races/rolling elements.',
        'Engine-side heater return, pulley and fan-clutch connections are provisional interface studies. Vehicle hoses, block coolant interface and pump attaching hardware remain outstanding. No belt ratio or coolant-flow simulation is implemented.'
    ]
    group('cooling','Cooling system')
    group('water-pump-assembly','Water pump · internal study','cooling',position=(440,0,170))
    def ring(ro,ri,w): return cx(ro,w)-cx(ri,w+2)
    # Hollow rear chamber with closed front wall and a bearing-support nose.
    housing=ring(66,59,36)+b.Pos(22,0,0)*ring(66,24,8)+b.Pos(48,0,0)*ring(29,24,46)
    # Weep passage below the cavity separating coolant seal from bearing.
    housing-=b.Pos(30,0,-27)*b.Cylinder(2.5,18)
    from cooling_connections import pump_housing_interface, SOURCES as cooling_sources, GAPS as cooling_gaps
    housing=pump_housing_interface(housing)
    gasket=b.Pos(-19,0,0)*ring(65,59,2)
    shaft=b.Pos(27,0,0)*cx(8,104)
    bearing=b.Pos(51,0,0)*ring(23.9,8.05,34)
    seal=b.Pos(16,0,0)*ring(23.8,8.05,10)
    slinger=b.Pos(29,0,0)*ring(17,8.05,1.2)
    hub=b.Pos(78,0,0)*ring(35,8.05,8)
    for a in range(0,360,90):
        y,z=25*math.cos(math.radians(a)),25*math.sin(math.radians(a))
        hub-=b.Pos(78,y,z)*cx(3.5,10)
    from fan_clutch import hub_interface, SOURCES as fan_sources, GAPS as fan_gaps
    hub=hub_interface(hub)
    # Single cast/stamped impeller: vanes joined to backing disk, clear of seal.
    impeller=b.Pos(-10,0,0)*ring(51,8.05,4)
    for a in range(0,360,60):
        vane=b.Pos(-3,30,0)*b.Box(12,37,3)
        impeller+=b.Rot(a,0,0)*vane
    pieces=[
        ('water-pump-housing',housing,'Water pump housing','Contains the coolant chamber and supports the sealed bearing. The small lower passage represents the weep hole described by Ford.','#8c999b',-90),
        ('water-pump-gasket',gasket,'Water pump mounting gasket','Seals the pump mounting joint; the actual block opening and gasket outline still need reconstruction.','#bfa77c',-150),
        ('water-pump-impeller',impeller,'Water pump impeller','Transfers shaft power to coolant. This six-vane study illustrates the mechanism; production vane shape and rotation direction are not verified.','#a0a9ac',-220),
        ('water-pump-shaft',shaft,'Water pump shaft','Carries the drive hub and impeller. The shaft and sealed bearing are serviced together as part of the replacement pump.','#b5bec4',170),
        ('water-pump-seal',seal,'Water pump coolant seal · envelope','Separates the coolant chamber from the bearing area. Mechanical seal faces, spring and elastomer are not yet individually represented.','#535c63',230),
        ('water-pump-slinger',slinger,'Water pump slinger','Throws seal leakage toward the housing bleed passage before it reaches the bearing.','#adb6b9',290),
        ('water-pump-bearing',bearing,'Water pump sealed bearing · cartridge','Supports radial and axial shaft loads; Ford describes a sealed bearing requiring no lubrication. Internal rolling elements remain unmodeled.','#657880',350),
        ('water-pump-drive-hub',hub,'Water pump drive hub','Provides a mounting interface for the pulley. Bolt circle and fan-clutch connection need measurement.','#839397',410)
    ]
    for id,shape,name,function,color,offset in pieces:
        part_sources=sources + (cooling_sources if id=='water-pump-housing' else fan_sources if id=='water-pump-drive-hub' else [])
        part_gaps=gaps + (cooling_gaps if id=='water-pump-housing' else fan_gaps if id=='water-pump-drive-hub' else [])
        define(id,shape,name,function,'cooling',color,part_sources,part_gaps)
        add(id,id,'water-pump-assembly',explode=(offset,0,0))
