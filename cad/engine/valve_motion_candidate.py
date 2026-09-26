"""Isolated cam-envelope and rocker-datum CAD candidates; never modifies atlas.

First run node scripts/check-valve-motion-candidate.mjs to generate the sampled
flat-tappet envelope. The rocker is a datum/contour candidate, NOT yet the rigid
linkage geometry used by the pedagogic solver: its three-dimensional cup/pad
contacts must be reconciled before applying solver transforms to this STEP.
"""
from pathlib import Path
import json
import math
import build123d as b

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT/'cad/engine/candidates/valve-motion'
PIVOT_Y = (1.6*90-16)/2.6


def lobe_shape(profile):
    # Profile uses actual Y,Z dimensions; extrusion centred on the X shaft.
    # Periodic interpolating curve avoids1440 planar side faces while retaining
    # every sampled support-envelope point. Exact follower checks validate it.
    edge=b.Edge.make_spline([b.Vector(-7.5,y,z) for y,z in profile],periodic=True)
    wire=b.Wire(edge)
    return b.Solid.extrude(b.Face(wire), b.Vector(15,0,0))


def rocker_shape():
    # Keep old overall end extent [-23.5,95.5], change pivot and cup coordinates.
    shape = b.Pos(0,36-PIVOT_Y,0)*b.Box(17,119,11)
    shape -= b.Pos(0,0,8)*b.Sphere(15)
    shape -= b.Pos(0,90-PIVOT_Y,-8)*b.Sphere(4)
    shape -= b.Cylinder(5,30)
    return shape


def main():
    data = json.loads((OUTPUT/'profile.json').read_text())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    lobe = lobe_shape(data['profile'])
    rocker = rocker_shape()
    roundtrips=[]
    for name,shape in [('catalog-constrained-cam-lobe',lobe),('asymmetric-rocker-datum',rocker)]:
        assert shape.is_valid and len(shape.solids()) == 1
        path=OUTPUT/(name+'.step')
        b.export_step(shape,path)
        restored=b.import_step(path)
        error=abs(restored.volume-shape.volume)
        assert restored.is_valid and error<1e-5
        roundtrips.append({'part':name,'volume_mm3':shape.volume,'roundtrip_volume_error_mm3':error})
    # A flat follower with 11.1mm radius samples every5 cam degrees. This radius is
    # an explicit study envelope; the installed factory-range radius is not assumed.
    overlap_checks=[]
    profile=data['profile']
    for degrees in range(-180,181,5):
        angle=math.radians(degrees)
        # Max projection gives the true support of saved polygon geometry; contact
        # is on the follower's plane, rather than guessed radial lift.
        support=max(y*math.sin(angle)+z*math.cos(angle) for y,z in profile)
        # Rotation -degrees moves sampled outward normal to +Z.
        moved=b.Rot(degrees,0,0)*lobe
        follower=b.Pos(0,0,support+10)*b.Cylinder(11.1,20)
        intersection=moved & follower
        volume=intersection.volume if intersection else 0
        assert volume<1e-5,(degrees,volume)
        overlap_checks.append({'cam_deg':degrees,'overlap_mm3':volume})
    report={'status':'PASS isolated CAD candidates; not installed engine clearance',
      'roundtrips':roundtrips,'flat_follower_poses':len(overlap_checks),
      'max_follower_overlap_mm3':max(x['overlap_mm3'] for x in overlap_checks),
      'candidate_pivot_y_mm':PIVOT_Y,'candidate_pivot_shift_mm':PIVOT_Y-36,
      'exports':str(OUTPUT),'unresolved':[
      'Follower uses11.1mm study radius; no tappet crown, lobe taper or wear simulation.',
      'Rocker pad/cup Z offsets are not reconciled with the coplanar ideal linkage solver.',
      'Head pedestal and bolt socket atY36 must move13.23077mm; cover and neighbors need full sweep checks.',
      'Cam journal/retention/drive integrations and twelve lobe phases require separate adapters.',
      'All lobe-profile intermediates and base-circle radius are assumptions, not a measured Ford profile.'],
      'failures':[]}
    (ROOT/'inventory/engine/valve-motion-candidate-cad-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
