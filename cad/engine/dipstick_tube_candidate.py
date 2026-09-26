"""Fail-closed dipstick tube feasibility tools; no production dimensions inferred.

Issue #78. Existing receiver identification precedes any tube route. Diagnostic
probe radii are test inputs, never proposed tube diameters or machining sizes.
"""
import build123d as b


def straight_probe(start, end, radius):
    path = b.Line(start, end)
    return b.sweep(b.Plane(origin=start, z_dir=path % 0) * b.Circle(radius), path=path)


def passage_evidence(solid, start, end, radius, tolerance_mm3=0.001):
    probe = straight_probe(start, end, radius)
    common = solid.intersect(probe)
    intrusion = sum(s.volume for s in common.solids()) if common is not None else 0.0
    return {"start_mm": list(start), "end_mm": list(end), "diagnostic_radius_mm": radius,
            "intrusion_mm3": intrusion, "clear": intrusion <= tolerance_mm3,
            "tolerance_mm3": tolerance_mm3}


# Educational estimates, independently selected from block section/cover datums.
SEAT = b.Vector(-315,129,18*3**.5)
AXIS = b.Vector(0,.5,3**.5/2)
FRAME = b.Plane(origin=SEAT,z_dir=AXIS).location
SUPPORT = b.Vector(-285,144.292,185)
TUBE_OUTER_RADIUS = 4.5
TUBE_INNER_RADIUS = 3.5


def axial_cylinder(radius, low, high):
    return FRAME * (b.Pos(0,0,(low+high)/2) * b.Cylinder(radius,high-low))


def candidate(block, installed_bolt):
    """Return isolated estimated parts and probes in installed CAD coordinates.

    Lower/upper threads are clearance envelopes in this first feasibility study;
    no thread size, clamp load, factory routing or oil calibration is claimed.
    """
    boss = axial_cylinder(10,-50,0) + axial_cylinder(8,0,8.5)
    cutter = axial_cylinder(5,-116,16)
    modified_block = (block + boss) - cutter
    lower = SEAT - AXIS*76
    # Straight seated leg, tangent curved transition, then vertical upper leg.
    a = SEAT + AXIS*9
    upper = b.Vector(-285,170,155)
    curve = b.Spline(a,(-310,150,80),(-295,168,120),upper,
                     tangents=(AXIS,b.Vector(0,0,1)))
    path = b.Wire([b.Line(lower,a),curve,b.Line(upper,(-285,170,500))])
    section = b.Plane(origin=lower,z_dir=AXIS)
    tube = b.sweep(section*(b.Circle(4.5)-b.Circle(3.5)),path=path)
    tube += axial_cylinder(6.5,8.5,9.5)-axial_cylinder(3.5,8,10)
    tube += b.Pos(-285,170,470)*b.Cylinder(5.25,60)
    tube -= b.Pos(-285,170,470.5)*b.Cylinder(4.25,61)
    nut = FRAME*(b.Pos(0,0,0)*b.extrude(b.RegularPolygon(11,6),amount=12))
    nut -= axial_cylinder(8.2,-1,9.5)
    nut -= axial_cylinder(4.7,9.5,13)
    # Existing hex is retained as a lower cover-clamp envelope; exposed stud added.
    stud = installed_bolt + b.Pos(-285,150.292,185)*b.Rot(-90,0,0)*b.Cylinder(4,12)
    # Plate bears against existing head, tongue reaches the guide tube collar.
    plate = b.Pos(-285,145.292,185)*b.Box(20,2,20)
    plate -= b.Pos(-285,145.292,185)*b.Rot(-90,0,0)*b.Cylinder(4.2,4)
    tongue = b.Pos(-285,157.646,176)*b.Box(16,26.708,2)
    collar = b.Pos(-285,170,176)*b.Cylinder(8,2)
    bracket = (plate+tongue+collar)-b.Pos(-285,170,176)*b.Cylinder(4.5,4)
    support_nut = b.Pos(-285,146.292,185)*b.Rot(-90,0,0)*b.extrude(b.RegularPolygon(7,6),amount=5)
    support_nut -= b.Pos(-285,148.792,185)*b.Rot(-90,0,0)*b.Cylinder(4.1,7)
    # Flexible-blade insertion clearance surrogate, no calibration or elastic claim.
    guide_probe = b.sweep(section*b.Circle((6.5**2+.8**2)**.5/2),path=path)
    free_length=692.15-path.length
    if free_length<=0: raise ValueError('Guide longer than comparison blade')
    free_tip = straight_probe(tuple(lower),tuple(lower-AXIS*free_length),(6.5**2+.8**2)**.5/2)
    wave_probe=b.Pos(-285,170,473.5)*b.Cylinder((4.1**2+.4**2)**.5,53)
    return {'block-candidate':modified_block,'engine-oil-dipstick-tube':tube,
            'engine-oil-dipstick-tube-retaining-nut':nut,
            'pushrod-cover-retainer-candidate':stud,
            'engine-oil-dipstick-tube-bracket':bracket,
            'engine-oil-dipstick-tube-support-nut':support_nut}, {
            'receiver-cutter':cutter,'added-boss':boss,'blade-guide-probe':guide_probe,
            'blade-free-tip-probe':free_tip,'blade-wave-probe':wave_probe}


def render_review(parts, out):
    """Regenerate a review PNG; requires system python3 with matplotlib/numpy."""
    import json
    import subprocess
    items=[]
    for name,shape in parts.items():
        if name=='block-candidate':
            shape=shape.intersect(b.Pos(-307.5,30,25)*b.Box(85,250,140))
        vertices,faces=shape.tessellate(.4)
        items.append({'name':name,'vertices':[list(v) for v in vertices],
                      'faces':[list(f) for f in faces]})
    (out/'render-mesh.json').write_text(json.dumps(items))
    subprocess.run(['python3','-c',REVIEW_PLOT,str(out)],check=True)

REVIEW_PLOT = "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nfrom mpl_toolkits.mplot3d.art3d import Poly3DCollection\nimport json,numpy as np,pathlib\nimport sys\nout=pathlib.Path(sys.argv[1]);items=json.loads((out/'render-mesh.json').read_text())\nfig=plt.figure(figsize=(12,9),facecolor='#f4f6f8')\ncolors=['#557085','#e4aa45','#a7adb5','#b8bcc4','#63798e','#b8bcc4']\nfor i in [1,2]:\n ax=fig.add_subplot(1,2,i,projection='3d');ax.set_facecolor('#f4f6f8')\n for item,col in zip(items,colors):\n  v=np.array(item['vertices']);f=np.array(item['faces']);p=Poly3DCollection(v[f],facecolor=col,edgecolor='none',alpha=.18 if item['name']=='block-candidate' else 1)\n  ax.add_collection3d(p)\n if i==1:\n  ax.set(xlim=(-360,-240),ylim=(40,210),zlim=(-70,515));ax.set_box_aspect((120,170,585));ax.set_title('Estimated route and rear cover support')\n else:\n  ax.set(xlim=(-345,-285),ylim=(65,155),zlim=(-65,75));ax.set_box_aspect((60,90,140));ax.set_title('Lower seat and sectioned casting')\n ax.view_init(elev=20,azim=35);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')\nfig.suptitle('Dipstick tube — isolated educational feasibility study',fontsize=16)\nfig.text(.5,.035,'New dimensions are estimates. Threads use clearance envelopes. Not installed; oil calibration unresolved.',ha='center',fontsize=10)\nplt.tight_layout(rect=(0,.07,1,.94));fig.savefig(out/'candidate-review.png',dpi=150)\n"
