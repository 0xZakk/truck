"""Isolated DR375A-photo-compared rotor leaf; all dimensions are estimates.

The cap center contact remains the existing unverified envelope. No invented
cap coil spring, material identification, electrical or preload certification.
"""
import build123d as b

def baseline_parts():
    """Reviewed existing inferred rotor geometry after oil-drive +50mm lift.

    Kept parametric so repeat/partial builds need no original temporary STEP.
    Checker compares these reference solids with the pre-promotion baseline.
    """
    rotor=b.Pos(0,0,75)*(b.Cylinder(10,12)-b.Cylinder(6.05,14))
    rotor+=b.Pos(17,0,81.5)*b.Box(34,10,3)
    rotor-=b.Pos(0,0,81.5)*b.Cylinder(2.1,5)
    return {'distributor-rotor':b.Pos(0,0,50)*rotor,
            'distributor-rotor-contact':b.Pos(16,0,133.75)*b.Box(34,6,1.5)}

def parts(original_rotor=None, original_contact=None):
    if original_rotor is None and original_contact is None:
        base=baseline_parts()
        original_rotor,original_contact=base['distributor-rotor'],base['distributor-rotor-contact']
    if original_rotor is None or original_contact is None:
        raise ValueError('Supply both baseline solids or neither')
    z_shift=original_contact.bounding_box().min.Z-83
    original_rotor=b.Pos(0,0,-z_shift)*original_rotor
    original_contact=b.Pos(0,0,-z_shift)*original_contact
    # Preserve shaft seating material and the original peripheral-tip region.
    rotor=original_rotor
    rotor+=b.Pos(0,0,82)*b.Cylinder(10,2)
    collar=b.Pos(0,0,84.5)*(b.Cylinder(10,3)-b.Cylinder(8,5))
    collar-=b.Pos(8,0,84.5)*b.Box(12,8,5)
    rotor+=collar
    # Flat leaf/contact seating surface; all values inferred within existing
    # center-transfer and outer-tip datums, not scaled factory measurements.
    rotor+=b.Pos(17,0,82.5)*b.Cylinder(6,1)
    # Visible photo recess lets the leaf fold below the old flat deck. A thin
    # estimated floor above the existing shaft end preserves the shaft seat.
    rotor+=b.Pos(0,0,80.75)*b.Cylinder(10,.5)
    pocket=b.Pos(0,0,82.1)*b.Cylinder(7.5,2.2)
    pocket+=b.Pos(9,0,82.1)*b.Box(10,7,2.2)
    rotor-=pocket
    # Rounded free contact end and tangent-continuous folded leaf silhouette.
    # Ford photo establishes a curved raised tongue, not bend radii/preload.
    leaf=b.Pos(-1,0,84.1)*b.extrude(b.RectangleRounded(8,6,1.8),amount=.4)
    path=b.Spline((2.8,0,84.3),(5,0,83.3),(7.5,0,81.7),(10,0,82),(14,0,83.2),
                  tangents=((1,0,0),(1,0,0)))
    section=b.Plane(origin=path@0,x_dir=(0,1,0),z_dir=path%0)*b.Rectangle(6,.4)
    leaf+=b.sweep(section,path=path)
    leaf+=b.Pos(15.9,0,83.2)*b.Box(4.2,6,.4)
    leaf+=b.Pos(18,0,83.2)*b.Cylinder(4,0.4)
    hole=b.Pos(18,0,84)*b.Cylinder(1.5,5)
    leaf-=hole
    # Distinct captured conductor maintains exact old peripheral-tip geometry.
    conductor=original_contact & (b.Pos(30,0,84)*b.Box(12,20,5))
    conductor+=b.Pos(21,0,83.95)*b.Box(6,6,1.1)
    conductor+=b.Pos(18,0,83.95)*b.Cylinder(4,1.1)
    conductor-=hole
    # Illustrative molded stake follows visible photo topology, not known
    # factory fastening process. Its underside seats on the conductor.
    rotor+=b.Pos(18,0,83.75)*b.Cylinder(1.5,1.5)
    rotor+=b.Pos(18,0,84.8)*b.Cylinder(2.4,.6)
    return {key:b.Pos(0,0,z_shift)*shape for key,shape in
            {'distributor-rotor':rotor,'distributor-rotor-contact':conductor,
             'distributor-rotor-center-leaf':leaf}.items()}
