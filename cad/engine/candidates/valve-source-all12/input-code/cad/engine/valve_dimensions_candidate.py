"""Replacement-envelope comparison solids, separate from installed teaching layout."""
from pathlib import Path
import json,hashlib,math
import build123d as b
from valve_layout_candidate import OUT as FIRST
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cad/engine/candidates/valve-dimensions'
LENGTHS={'intake':4.749*25.4,'exhaust':4.750*25.4}
STEM_D=.342*25.4;PUSHROD_D=.312*25.4;PUSHROD_OVERALL=10.14*25.4
BALL_R=PUSHROD_D/2;OIL_R=1.2
END_AXIAL=math.sqrt(BALL_R**2-OIL_R**2)
PUSHROD_CENTERS=PUSHROD_OVERALL-2*END_AXIAL


def valve(old,kind):
    """Add sourced length in plain stem, preserving assumed head/groove profile."""
    delta=LENGTHS[kind]-109
    lower=old & (b.Pos(0,0,-25)*b.Box(60,60,150)) # topZ50
    upper=old & (b.Pos(0,0,100)*b.Box(60,60,100)) # bottomZ50
    bridge=b.Pos(0,0,50+delta/2)*b.Cylinder(4.49,delta+.2)
    fused=bridge.fuse(*lower.solids(),*(b.Pos(0,0,delta)*upper).solids())
    s=b.Compound(children=list(fused)) if isinstance(fused,b.ShapeList) else fused
    shell=b.Cylinder(5,LENGTHS[kind]+10)-b.Cylinder(STEM_D/2,LENGTHS[kind]+12)
    return s-b.Pos(0,0,3.2+(LENGTHS[kind]+10)/2)*shell


def pushrod():
    s=b.Cylinder(BALL_R,PUSHROD_CENTERS)
    for z in [-PUSHROD_CENTERS/2,PUSHROD_CENTERS/2]:s+=b.Pos(0,0,z)*b.Sphere(BALL_R)
    return s-b.Cylinder(OIL_R,PUSHROD_OVERALL+10)


def main():
    OUT.mkdir(parents=True,exist_ok=True);shapes={'pushrod':pushrod()};inputs={}
    for kind in LENGTHS:
        p=FIRST/(kind+'-valve.step');inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
        shapes[kind+'-valve']=valve(b.import_step(p),kind)
    measures={}
    for name,s in shapes.items():
        assert s.is_valid and len(s.solids())==1,name
        b.export_step(s,OUT/(name+'.step'));reload=b.import_step(OUT/(name+'.step'));box=reload.bounding_box()
        desired=PUSHROD_OVERALL if name=='pushrod' else LENGTHS[name.split('-')[0]]
        assert abs(box.size.Z-desired)<1e-4,(name,box.size.Z,desired)
        measures[name]={'height_mm':box.size.Z,'width_mm':box.size.X,'volume_mm3':reload.volume,'valid':reload.is_valid}
    # Conditional datum solutions; no geometry installation implied.
    solutions=[]
    for source,height_in in [('Crower66015J-12 comparison',1.715),('Howards91211-12 alternative',2.018)]:
      for kind,length in LENGTHS.items():
        tip=261+length;pivot=tip+13.5
        # This scenario assumes published seat-height is the socket bottom.
        lower=72+18+height_in*25.4+BALL_R
        upper=lower+PUSHROD_CENTERS
        solutions.append({'source':source,'kind':kind,'valve_tip_z':tip,'pivot_z_assumed_pad':pivot,'lower_ball_center_z':lower,'upper_ball_center_z':upper,'required_rocker_cup_offset_z':upper-pivot})
    report={'status':'PASS replacement-envelope STEP roundtrip; no assembled fit approval','source_inputs':inputs,
      'sources':['kb/sources/melling-valve-progressive-size-chart-2025.md','kb/sources/melling-pushrod-specifications.md'],
      'constraints':{'valve_lengths_mm':LENGTHS,'stem_diameter_mm':STEM_D,'pushrod_overall_mm':PUSHROD_OVERALL,'pushrod_diameter_mm':PUSHROD_D,'assumed_ball_radius_mm':BALL_R,'end_axial_material_extent_mm':END_AXIAL,'derived_ball_centers_mm':PUSHROD_CENTERS},
      'measured_step':measures,'conditional_datum_solutions':solutions,
      'limitations':['These are replacement comparisons, not owner-part identification.','Valve groove location and head contours retain prior assumptions; overall and stem dimensions now sourced.','Pushrod ball radius equated to tube radius and1.2mm oil bore remain assumed; center spacing includes loss of spherical apex from oil drilling.','Conditional seat-height scenarios assume seat height is socket bottom, not ball center; manufacturer convention and actual part unresolved.','No coordinated rocker,head,lifter,cover or timing fit approval.']}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
