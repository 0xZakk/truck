#!/usr/bin/env python3
"""One explicit additive-ledger rebind; preserve the failed stability guard."""
from pathlib import Path
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-gear-backlash-candidate'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
ledger=ROOT/'reference/engine/timing-gear-backlash-review.json';current=read(ledger)
assert 'crank_key_followup' in current
original={k:v for k,v in current.items() if k!='crank_key_followup'}
raw=(json.dumps(original,indent=2)+'\n').encode();oldhash=hashlib.sha256(raw).hexdigest()
assert oldhash=='58c9cfbc225a5b576993a94c6ff233a69b33284a8b85ac567b347722cb794419'
build=read(OUT/'build-report.json');watched=build['input_sha256'];rel=str(ledger.relative_to(ROOT));assert watched[rel]==oldhash
assert (OUT/'original-backlash-review.json').read_bytes()==raw
for p,h in watched.items():
 if p!=rel:assert sha(ROOT/p)==h,p
assert build['status']=='PASS isolated core and exports' and build['base_globals_unchanged']
assert build['core_fault_detected_mm3']>.4
for k,e in build['exports'].items():
 assert all(e[x] for x in ['valid','watertight']) and e['solids']==1
 assert e['bounds_error_mm']<.15 and e['roundtrip_volume_error_mm3']<.001
 for ext in ['step','glb']:assert sha(OUT/(k+'.'+ext))==e[ext+'_sha256']
 g=build['protected_core'][k];assert g['core_difference_mm3']<1e-5 and g['outside_tooth_envelope_mm3']<1e-5
contact=read(OUT/'contact-progress.json');rows=read(OUT/'sweep-progress.json');sign=read(OUT/'axial-sign-witnesses.json');radius=81.2
assert len(contact)==8 and len(rows)==50
brackets=[]
for theta in [0.,180/29]:
 sides=[]
 for s in [-1,1]:
  q=[r for r in contact if abs(r['crank_degrees']-theta)<1e-10 and s*r['cam_extra_degrees']>0];assert len(q)==2
  free=[abs(r['cam_extra_degrees']) for r in q if r['overlap_mm3']<1e-5 and r['gap_mm']>1e-6]
  hit=[abs(r['cam_extra_degrees']) for r in q if r['overlap_mm3']>1e-5];assert free and hit
  sides.append([max(free),min(hit)])
 play=[math.radians(sum(s[i] for s in sides))*radius for i in [0,1]];assert .0508<=play[0]<=play[1]<=.1016
 brackets.append(dict(crank_degrees=theta,pitch_circle_play_mm=play))
k=-math.tan(math.radians(25))/81.2
for i in range(25):
 for d in [0.,-.1]:
  q=[r for r in rows if abs(r['crank_degrees']-(360/29)*i/24)<1e-10 and r['axial_mm']==d];assert len(q)==1
  r=q[0];assert abs(r['cam_extra_degrees']-math.degrees(k*d))<1e-10
  assert r['overlap_mm3']<1e-5 and r['gap_mm']>1e-6
assert sign['fixed_phase']['overlap_mm3']>1e-5 and sign['opposite_sign']['overlap_mm3']>1e-5
assert sign['correct_sign']['overlap_mm3']<1e-5 and sign['correct_sign']['gap_mm']>1e-6
render=read(OUT/'render-record.json')
for key in ['crank','cam']:assert render['mesh_sha256'][key]==build['exports'][key]['glb_sha256']
rebind=dict(reason='Root added only independent crank_key_followup metadata after numerical sweep began. Removing exactly that key reconstructs original bytes/hash; backlash evidence and all numerical inputs unchanged.',original_ledger_sha256=oldhash,current_ledger_sha256=sha(ledger),removed_key='crank_key_followup',original_run_final_guard='FAILED as intended on ledger hash change; all 50 numerical rows preserved, no original successful exit claimed',checker_sha256=sha(Path(__file__)),witness_sha256={n:sha(OUT/n) for n in ['build-report.json','contact-progress.json','sweep-progress.json','axial-sign-witnesses.json','motion.log','original-backlash-review.json','render-record.json']})
r=dict(status='PASS isolated candidate after explicit additive metadata rebind; fixed-phase axial hypothesis FAIL; UNINSTALLED',input_sha256={**watched,rel:sha(ledger)},original_run_input_sha256=watched,metadata_rebind=rebind,build=build,contact_rows=contact,two_sided_brackets=brackets,service_range_mm=[.0508,.1016],service_interpretation='Tangential pitch-circle indicator assumed; source radius/direction unspecified',axial_sign_witnesses=sign,cam_k_rad_per_mm=k,sweep=rows,continuous_axial_argument='At each sampled crank phase: cam hand=-1 produces phase k*x. Translation delta plus rotation k*delta preserves cross-section phase at world X. The shared axial slab is a subset of the neutral slab for delta in[-0.1,0]. This is an analytic construction-level no-intersection certificate at the 25 checked rotations, independently supported by endpoint CAD checks; not continuous rotation or loaded dynamics.',limits=['The keyed camshaft/key/spacer/gear and retaining bolt must rotate together; gear must not slip on its key.','Existing fixed-phase core/thrust proofs do not validate rotated non-axisymmetric neighbors, valve linkage or distributor/pump drive coupling.','No production calibration: source dial indicator radius/direction unspecified; profile/helix/axes and thrust land retain estimated status.','Coupled law is one feasible unloaded path, not a prediction of loaded engine motion.'])
(ROOT/'inventory/engine/timing-gear-backlash-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
