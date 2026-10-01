#!/usr/bin/env python3
"""Bounded results acceptance; does not rerun or reinterpret failed CAD metrics."""
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1]
p=R/'inventory/engine/crossed-oil-drive-endplay-review.json';r=json.loads(p.read_text())
for name,h in r['input_sha256'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h,name
rows=r['rows'];nominal=[x for x in rows if x['label']=='nominal'];bad=[x for x in rows if x['label'].startswith('phase-')];omitted=next(x for x in rows if x['label']=='omitted-endplay')
assert len(nominal)==9 and len(bad)==2
assert all(x['metric_error'] is None and x['overlap_mm3']==0 and x['distance_mm']>1e-7 and abs(x['registration_residual_rad'])<1e-12 for x in nominal)
assert all(x['metric_error'] is None and x['overlap_mm3']>.1 and x['distance_mm']<1e-7 for x in bad)
assert abs(math.degrees(omitted['registration_residual_rad'])-.3512131629903308)<1e-10
edges=r['actual_cam_edge_translation_fit'];assert len(edges)==304
assert max(abs(x['intercept_change_at_minus_0p1_mm']-.1/18)for x in edges)<1e-6
assert all(r['invalid_input_rejected'])
files=[p,Path(__file__),R/'docs/components/crossed-oil-drive-endplay-coupling.md']
s={'nominal_sampled_clearance':'PASS','nominal_samples':len(nominal),'minimum_separation_mm':min(x['distance_mm']for x in nominal),'wrong_phase_penetration_controls_mm3':[x['overlap_mm3']for x in bad],'omitted_correction':omitted,'actual_edge_translation_phase_fit':'PASS','scope_limits':['Only nine axial/event samples; prior zero-endplay17 samples remain separate','Finite backlash means nominal registration error need not cause collision','No pressure/contact force, factory identity, continuous solid sweep, installed motion or browser claim'],'sha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest()for f in files}}
(R/'inventory/engine/crossed-oil-drive-endplay-summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
