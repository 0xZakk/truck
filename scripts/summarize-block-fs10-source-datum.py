from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];s=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[R/'inventory/engine/block-fs10-source-onset.json',R/'docs/components/block-fs10-source-datum-investigation.md',R/'scripts/render-block-fs10-source-datum.py',Path(__file__)]
paths+=list((R/'cad/engine/generated/block-fs10-source-datum-investigation').glob('*'))
paths += [R/p for p in ['reference/engine/timing-cover-front-joint-review.json','reference/engine/timing-cover-registration-review.json','reference/engine/timing-cover-joint-review.json','reference/engine/accessory-layout-source-review.json','reference/engine/ford-tsb-94-10-19-accessory-reviewed.json','reference/engine/uac-fs10-replacement.html','cad/engine/ac_compressor.py','cad/engine/accessory_carrier_1994.py','cad/engine/timing_cover_front_joint_candidate.py']]
a=json.loads(paths[0].read_text());assert len(a['rows'])==42;assert not any('adaptive_error' in x for x in a['rows']);assert all(x['default_mm3']<.1 for x in a['rows'][:12])
out={'status':'COMPLETE source onset study; no repair accepted','checks':42,'adaptive_errors':0,'canonical_and_prefront_clear_checks':12,'actual_sections_reviewed':True,'visual_findings':'X360 shows new boss entering piston; X368 shows original rail through shaft and cylinder. Front/rear orientation follow-up is separate.','input_sha256':{str(p.relative_to(R)):s(p) for p in paths},'source_onset_bound_inputs_verified':all(s(R/p)==h for p,h in a['input_sha256'].items())}
assert out['source_onset_bound_inputs_verified'];(R/'inventory/engine/block-fs10-source-datum-delivery.json').write_text(json.dumps(out,indent=2)+'\n')
