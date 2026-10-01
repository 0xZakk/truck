#!/usr/bin/env python3
"""Continuous hub/seal rotation and bounded axial sensitivity; no part edits."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import front_seal_2692_candidate as c
OUT=ROOT/'cad/engine/generated/front-seal-2692-candidate';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();names=['cover','damper-hub','seal-case-installed','seal-elastomer','seal-garter-spring'];paths={n:OUT/(n+'.step') for n in names}
q={n:b.import_step(p) for n,p in paths.items()}
def vol(s):return sum(abs(solid_volume(x,'adaptive')) for x in s.solids()) if s else 0.
source=ROOT/'reference/engine/front-seal-2692-motion-source-review.json';ledger=json.loads(source.read_text());watch=[Path(__file__),Path(c.__file__),Path(c.e.__file__),ROOT/'cad/engine/cad_metrics.py',ROOT/'viewer/atlas.js',ROOT/'inventory/engine/full-assembly.json',ROOT/'inventory/engine/front-seal-2692-delivery-validation.json',source,ROOT/'docs/components/front-seal-2692-motion-study.md']+list(paths.values())
watch.extend(ROOT/s['path'] for s in ledger['sources'] if 'path' in s)
r={'status':'RUNNING','inputs':{str(p.relative_to(ROOT)):sha(p) for p in watch},'continuous_proofs':{},'sample_controls':[]}
# Before relying on annular symmetry, compare exported track in both directions.
near=q['damper-hub'].intersect(c.cx(200,418,435.5));ideal=c.ring(c.TRACK_R,21.05,419,435.5);missing=vol(ideal.cut(near));excess=vol(near.cut(ideal));assert missing<1e-5 and excess<1e-5
r['continuous_proofs']['actual_track_annulus']={'domain_x_mm':[419,435.5],'inner_radius_mm':21.05,'outer_radius_mm':c.TRACK_R,'ideal_volume_mm3':vol(ideal),'missing_mm3':missing,'excess_mm3':excess}
assert vol(ideal)>6000 and len(near.solids())==1 and near.is_valid
# Independent strict interior material witnesses guard Boolean false emptiness.
witnesses=[]
for x in [419.01,420,427.9,428.2,435.49]:
 for angle in [0,31,79,141,217,293]:
  t=math.radians(angle);p=(x,22.5*math.cos(t),22.5*math.sin(t));inside=any(s.is_inside(p,1e-6) for s in q['damper-hub'].solids());assert inside;witnesses.append({'x':x,'angle_deg':angle,'inside':inside})
r['track_material_witnesses']=witnesses
# No off-axis remainder can enter the stationary assembly in the entire range.
e=.008*25.4;far=q['damper-hub'].cut(near);far_min=far.bounding_box().min.X;fixed_max=max(q[n].bounding_box().max.X for n in names if n!='damper-hub');axial_gap=far_min-e-fixed_max;assert far_min>=435.5-1e-5 and axial_gap>1
r['continuous_proofs']['remaining_hub_axial_separation']={'remaining_hub_min_x':far_min,'stationary_max_x':fixed_max,'offset_range_mm':[-e,e],'minimum_axial_gap_mm':axial_gap,'reason':'Rotation about X preserves every X coordinate; translation extrema bound the entire interval.'}
# Rotating near-hub has invariant outer cylinder, continuously clear of cover.
local_domain=c.cx(24,419-e,435.5+e);v=vol(q['cover'].intersect(local_domain));assert v<1e-5
r['continuous_proofs']['cover_radial_clearance']={'cover_inside_R24_mm3':v,'axial_domain_mm':[419-e,435.5+e],'minimum_clearance_mm':24-c.TRACK_R}
# The union of all required contact support bands, expressed in hub coordinates.
probe=c.ring(c.TRACK_R-.001,c.TRACK_R-.01,427.9-e,428.2+e);v=vol(probe);missing=vol(probe.cut(q['damper-hub']));assert v>.5 and missing<1e-5
r['continuous_proofs']['lip_track_support']={'lip_x_mm':[427.9,428.2],'relative_track_required_x_mm':[427.9-e,428.2+e],'probe_mm3':v,'missing_mm3':missing,'rear_margin_mm':427.9-(419+e),'front_margin_mm':435.5-e-428.2,'source_width_rear_margin_mm':420-(419+e),'source_width_front_margin_mm':435.5-e-c.AIR}
# Every seal component stays entirely inside the common axial track interval.
# There the hub equals the same annulus at every angle and every translation,
# so the already checked nominal contact/non-contact relation is invariant.
common=[419+e,435.5-e];covered={}
for n in ['seal-case-installed','seal-elastomer','seal-garter-spring']:
 bb=q[n].bounding_box();assert bb.min.X>common[0] and bb.max.X<common[1]
 covered[n]={'actual_axial_bounds_mm':[bb.min.X,bb.max.X],'rear_margin_mm':bb.min.X-common[0],'front_margin_mm':common[1]-bb.max.X}
r['continuous_proofs']['stationary_seal_invariant_track_relation']={'common_track_interval_mm':common,'parts':covered,'proof':'Actual annular hub equality and full stationary-part containment make relative radial contact/clearance independent of angle and every offset in the interval.'}
# Case and garter radial clearances use a slightly inflated continuous spring
# envelope, as in the separate frozen internal-clearance proof.
envelope=b.Pos(c.SPRING_X,0,0)*b.Rot(0,90,0)*b.Torus(c.SPRING_R,c.COIL_R+c.WIRE_R+.001)
for n,s in [('seal-case-installed',q['seal-case-installed']),('spring-conservative-envelope',envelope)]:
 v=vol(s.intersect(c.cx(c.TRACK_R,419-e,435.5+e)));assert v<1e-5;r['continuous_proofs'][n]={'intersection_with_full_rotational_axial_envelope_mm3':v}
# Endpoint rotations are diagnostic samples supplementing the symmetry proof.
for shift,angle in [(-e,0),(-e,137),(e,0),(e,223)]:
 h=b.Pos(shift,0,0)*b.Rot(angle,0,0)*q['damper-hub']
 for n in ['cover','seal-case-installed','seal-elastomer']:
  v=vol(h.intersect(q[n]));gap=h.distance_to(q[n]);assert v<.1
  if n=='seal-elastomer':assert gap<.002
  r['sample_controls'].append({'offset_mm':shift,'angle_deg':angle,'stationary_part':n,'overlap_mm3':v,'gap_mm':gap})
# A meaningful material-removal control and axial off-track fault must fail.
notch=b.Pos(428,22.5,0)*b.Box(.8,8,2);bad=q['damper-hub'].cut(notch);fault_missing=vol(probe.cut(bad));assert fault_missing>.01
bad_margin=435.5-10-428.2;assert bad_margin<0
r['negative_controls']={'notched_track_missing_probe_mm3':fault_missing,'rearward10mm_forward_track_margin_mm':bad_margin}
# Independent sign calculation for a top marker seen from front/+X.
t=math.radians(1);marker=(0,-math.sin(t),math.cos(t));assert marker[1]<0
viewer=(ROOT/'viewer/atlas.js').read_text();assert "g.rotateX(angle*Math.PI/180)" in viewer and "angle=(angle+dt*30)%720" in viewer and "new THREE.Vector3(a[0],a[2],-a[1])" in viewer
r['viewer_direction']={'front_observer':'+X looking toward -X; Z up; Y right','positive1deg_top_marker_cad':marker,'screen_direction':'counterclockwise','basis_determinant':1,'source_compatibility':'UNKNOWN exact-year crank direction and2692 spiral viewing convention'}
r['endplay_interpretation']={'source_total_range_mm':[.1016,.2032],'checked_sensitivity_offset_mm':[-e,e],'centered_interpretation_offset_mm':[-e/2,e/2],'nominal_registration':'estimated; neither thrust stop nor midpoint sourced','does_not_claim_total_endplay_mm':2*e}
r['limits']=['Only candidate hub moved mathematically; no exported geometry, canonical or timing-gear pose changed.','A real crank shift carries rigid crank-group parts and crank gear; coupled helical engagement, thrust stack, clutch/rod/rear-seal/belt effects remain unchecked.','Fixed seal support reused from frozen delivery; axial range is a sensitivity about estimated registration.','No source-level rotation handedness acceptance or hydrodynamic pumping claim.']
assert all(sha(ROOT/p)==h for p,h in r['inputs'].items());r['status']='PASS continuous declared hub/seal geometry and conservative axial sensitivity; handedness compatibility UNKNOWN';(ROOT/'inventory/engine/front-seal-2692-motion-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
