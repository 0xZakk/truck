"""Inserted flexed dipstick display pose; no elastic or oil-calibration claim.

Issue #17/#78 interface study. Retains the existing pilot's approximate AXIAL
692.15mm datum. Near-stop waves add material centerline length, reported apart.
All section/handle/wave dimensions remain estimates inherited from that pilot.
"""
from dataclasses import replace
import importlib.util
import math
from pathlib import Path
import sys
import build123d as b
from dipstick_tube_candidate import SEAT, AXIS

PILOT_PATH=Path(__file__).parent/'pilot/dipstick/dipstick.py'
spec=importlib.util.spec_from_file_location('dipstick_inserted_pilot',PILOT_PATH)
pilot=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=pilot
spec.loader.exec_module(pilot)
P=pilot.P
MOUTH=b.Vector(-285,170,500)


def route():
    """Reconstruct the frozen tube's exact guide, without editing its module."""
    lower=SEAT-AXIS*76
    a=SEAT+AXIS*9
    upper=b.Vector(-285,170,155)
    curve=b.Spline(a,(-310,150,80),(-295,168,120),upper,
                   tangents=(AXIS,b.Vector(0,0,1)))
    guide=b.Wire([b.Line(lower,a),curve,b.Line(upper,MOUTH)])
    free=P.blade_axial_length-guide.length
    return lower,a,upper,curve,guide,free


def parts(stamp=True):
    lower,a,upper,curve,guide,free=route()
    # Pilot wave profile is preserved in the straight expanded-mouth region.
    stations=sorted(set([0,5,53]+list(range(6,53,2))))
    centers=[(P.wave_amplitude*math.sin(2*math.pi*(s-5)/24) if 5<s<53 else 0,s) for s in stations]
    polygon=[(x-P.stem_width/2,-s) for x,s in centers]+[(x+P.stem_width/2,-s) for x,s in reversed(centers)]
    wave=b.Pos(*MOUTH)*b.extrude(b.Plane.XZ*b.Polygon(*polygon,align=None),amount=P.blade_thickness/2,both=True)
    transition_start=P.blade_axial_length-P.tip_length-15
    stem_end=lower-AXIS*(transition_start-guide.length)
    start=MOUTH-b.Vector(0,0,53)
    stem_path=b.Wire([b.Line(start,upper),curve.reversed(),b.Line(a,stem_end)])
    section=b.Plane(origin=start,x_dir=(1,0,0),z_dir=(0,0,-1))
    stem=b.sweep(section*b.Rectangle(P.stem_width,P.blade_thickness),path=stem_path,is_frenet=False)
    # Read the transported sweep's actual end rectangle to attach the free tip
    # without a guessed roll discontinuity.
    end_face=min(stem.faces(),key=lambda f:(f.center()-stem_end).length)
    edge=max(end_face.edges(),key=lambda e:e.length)
    width_dir=(edge@1-edge@0).normalized()
    tip_frame=b.Plane(origin=stem_end,x_dir=width_dir,z_dir=-AXIS)
    tip=b.loft([tip_frame.location*b.Pos(0,0,s)*b.Rectangle(w,P.blade_thickness)
                for s,w in [(0,P.stem_width),(15,P.tip_width),(102,P.tip_width),(105,1.3)]],ruled=True)
    if stamp:
        lettering=tip_frame.location*(b.Plane(origin=(0,-P.blade_thickness/2-.01,635-transition_start),
                       x_dir=(0,0,1),z_dir=(0,-1,0))*b.Text('E9TE-6750-DA  M',font_size=1.7))
        tip-=b.extrude(lettering,amount=-.16)
    blade=wave+stem+tip
    # Pilot stop bottom is localZ=-0.5. Raise handle alone0.5mm so its bottom
    # bears on the mouth plane while blade datum remains exactly at that plane.
    handle=b.Pos(MOUTH.X,MOUTH.Y,MOUTH.Z+.5)*pilot.parts(replace(P,stamp=False))['engine-oil-dipstick-handle']
    wave_length=sum(math.hypot(x2-x1,s2-s1) for (x1,s1),(x2,s2) in zip(centers,centers[1:]))
    metadata={'guide_centerline_length_mm':guide.length,'free_axial_route_length_mm':free,
              'route_sum_mm':guide.length+free,'pilot_axial_length_mm':P.blade_axial_length,
              'wave_axial_length_mm':53,'wave_polyline_material_length_mm':wave_length,
              'blade_material_centerline_length_mm':P.blade_axial_length+wave_length-53,
              'mouth_mm':list(MOUTH),'tip_mm':list(lower-AXIS*free),
              'stem_end_mm':list(stem_end),'stop_bottom_correction_mm':.5,
              'reading_marks':'UNKNOWN; no ADD/FULL/oil-level marks added',
              'stamp':'E9TE-6750-DA M specimen comparison; not owner identification'}
    return {'engine-oil-dipstick-blade-inserted':blade,
            'engine-oil-dipstick-handle-inserted':handle},metadata
