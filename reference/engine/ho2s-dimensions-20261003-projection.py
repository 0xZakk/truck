"""Replay authored pixel spans; no source pixels or CAD required.
Conditional sensitivity envelopes, not metrology confidence intervals.
"""
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[2]
P=R/'reference/engine/ho2s-dimensions-20261003-landmarks.json'
d=json.loads(P.read_text());a=d['assumptions'];af=a['hex_across_flats_mm'];anchor=a['hex_projected_span_px'];err=a['hex_span_pick_error_px']
slo=af/(anchor+err);shi=(af/math.cos(math.pi/6))/(anchor-err);snom=(af+af/math.cos(math.pi/6))/2/anchor
rows=[]
for f in d['features']:
 span=f['span_px'];pe=f['pick_error_px'];depth=a[f['family']+'_relative_scale_factor'];alpha=a[f['family']+'_axis_out_of_plane_degrees_max'] if f['direction']=='axial' else 0
 lo=(span-pe)*slo*depth[0];hi=(span+pe)*shi*depth[1]/math.cos(math.radians(alpha));nom=span*snom
 rows.append(dict(f,projection_center_mm=round(nom,3),conditional_sensitivity_mm=[round(lo,3),round(hi,3)],candidate_choice_within_sensitivity=lo<=f['proposed_candidate_mm']<=hi))
assert all(r['candidate_choice_within_sensitivity'] for r in rows)
# Sensitivity controls: gross double scale and a 3mm thread pitch must fail.
assert not rows[0]['conditional_sensitivity_mm'][0]<=rows[0]['proposed_candidate_mm']*2<=rows[0]['conditional_sensitivity_mm'][1]
pitch=next(r for r in rows if r['id']=='pitch');assert not pitch['conditional_sensitivity_mm'][0]<=3<=pitch['conditional_sensitivity_mm'][1]
report={'schema_version':1,'status':'PASS arithmetic and declared sensitivity only; not physical-fit validation','scale_mm_per_pixel':{'nominal':snom,'hex_roll_pick_only':[slo,shi]},'assumptions':a,'features':rows,'controls':{'double_scale_rejected':True,'pitch3mm_rejected':True,'pitch1_25_vs1_5_discriminated':False},'inputs':{str(P.relative_to(R)):hashlib.sha256(P.read_bytes()).hexdigest(),str(Path(__file__).relative_to(R)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'limitations':['Scale assumes uniform image sampling and chosen camera/depth ranges; not calibrated or guaranteed bounds','No CAD/host/collision/connector-fit acceptance','Default dimensions are declared modeling choices within ranges, not measurements']}
(R/'reference/engine/ho2s-dimensions-20261003-projection.json').write_text(json.dumps(report,indent=2)+'\n')
for r in rows:print(r['id'],r['projection_center_mm'],r['conditional_sensitivity_mm'],'candidate',r['proposed_candidate_mm'])
