#!/usr/bin/env python3
"""Read-only numeric scope proposal; never changes or exports neighbor CAD."""
from pathlib import Path
import hashlib,json,sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_valvetrain_inclined_hypothesis as c
import timing_axis_kinematic_candidate as k
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']}
files=[Path(__file__),Path(c.__file__),Path(k.__file__),ROOT/'inventory/engine/full-assembly.json',ROOT/'inventory/engine/timing-valvetrain-inclined-hypothesis-validation.json']
files += [ROOT/'cad/engine'/name for name in ['timing_valvetrain_contract.py','timing_coupled_core_candidate.py','valve_source_layout.py','valve_dimensions_candidate.py']]
lifter=[]
for o in m['occurrences']:
 if o['id'].startswith('c1-intake-lifter-'):
  p=ROOT/defs[o['definition']]['step'].lstrip('/');files.append(p)
  bounds=b.import_step(p).bounding_box()
  lifter.append({'id':o['id'],'local_z_bounds_mm':[bounds.min.Z,bounds.max.Z], 'rest_world_top_mm':o['position_cad_mm'][2]+c.DELTA[1]+bounds.max.Z,'peak_world_top_mm':o['position_cad_mm'][2]+c.DELTA[1]+bounds.max.Z+k.MAX_CAM_LIFT})
h=c.layout(90);rest=h['solve'](0);zlo,zhi=244.,304.;radius=5.
def axis(z):return c.section_y(rest,z)[0]
minimum={'gap_mm':float('inf')};oldmin={'gap_mm':float('inf')}
for i in range(1,7):
 for kind in ['intake','exhaust']:
  for theta in range(721):
   for axial in [0,-.1]:
    s=c.state(h,theta,i,kind,axial)
    # Difference of two straight axes is affine in Z; maximum absolute offset
    # on this interval occurs at an endpoint. R5 is an inscribed circle of
    # the proposed oblique cylinder's horizontal ellipse, a sufficient bound.
    for z in [zlo,zhi]:
     y,half=c.section_y(s,z);gap=radius-abs(y-axis(z))-half
     if gap<minimum['gap_mm']:minimum={'gap_mm':gap,'branch':f'c{i}-{kind}','theta':theta,'axial':axial,'z_mm':z}
    y,half=c.section_y(s,304.);gap=6-abs(y-90)-half
    if gap<oldmin['gap_mm']:oldmin={'gap_mm':gap,'branch':f'c{i}-{kind}','theta':theta,'axial':axial}
peak=max(x['peak_world_top_mm'] for x in lifter)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r={'status':'SCOPE PROPOSAL ONLY; no neighbor CAD changes','inputs':{str(p.relative_to(ROOT)):sha(p) for p in files},'lifter_bound':lifter,'maximum_lifter_top_over_bounded_lift_mm':peak,'proposed_backing_z_mm':[244,254],'minimum_backing_to_lifter_z_gap_mm':244-peak,'proposed_oblique_passage_radius_mm':radius,'proposed_passage_axis_y_at_z_mm':{str(z):axis(z) for z in [244,254,255.5,304]},'minimum_sampled_new_passage_sufficient_gap':minimum,'minimum_sampled_unchanged_upper_passage_gap_at_304':oldmin,'negative_controls':{'R3_passage_gap_mm':minimum['gap_mm']-2,'backing_bottom_at150_lifter_z_gap_mm':150-peak},'limits':['Actual lifter STEP bounds plus analytic profile maximum bound lift continuously; rod clearance is sampled in crank/axial endpoints, not continuous phase proof.','Lower head and gasket would retain existingR6/Y90 hole and union an inclinedR5 aperture. Block support must clear this union, not solelyR5.','R5 aperture and244–254 backing are estimated study choices, not factory dimensions.','No CAD fit, support continuity, fluid preservation, export, source shape, or browser acceptance claimed.']}
assert minimum['gap_mm']>0 and oldmin['gap_mm']>0 and peak<244
assert r['negative_controls']['R3_passage_gap_mm']<0 and r['negative_controls']['backing_bottom_at150_lifter_z_gap_mm']<0
out=ROOT/'inventory/engine/timing-valvetrain-inclined-scope-validation.json';out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['inputs','lifter_bound','limits']},indent=2))
