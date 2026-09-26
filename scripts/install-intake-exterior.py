#!/usr/bin/env python3
"""Read-only exterior preflight by default; explicit--apply or--check-installed."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
STAGE=ROOT/'cad/engine/generated/intake-exterior-integration-stage'
RECORD=ROOT/'inventory/engine/intake-exterior-installation.json'
HELPER=ROOT/'scripts/install-intake-cap-coordination.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def validate(installed=False):
    report=read(STAGE/'validation.json');assert report['status'].startswith('PASS')
    for p,h in report['source_sha256'].items():assert sha(ROOT/p)==h,'Stage source/evidence changed: '+p
    for p,h in report['staged_artifact_sha256'].items():assert sha(STAGE/p)==h,'Stage asset changed: '+p
    assert sha(STAGE/'full-assembly.json')==report['staged_manifest_sha256']
    proofpath=ROOT/'inventory/engine/intake-exterior-candidate-validation.json';proof=read(proofpath)
    assert sha(proofpath)==report['candidate_report_sha256'] and proof['status'].startswith('PASS') and proof['input_guard_pass']
    for p,h in proof['input_sha256'].items():
        path=Path(p) if Path(p).is_absolute() else ROOT/p
        assert sha(path)==h,'Candidate source/frozen fixture changed: '+p
    expected_assets={'cad/engine/generated/efi-upper-intake.step':STAGE/'step/efi-upper-intake.step','models/engine/efi-upper-intake.glb':STAGE/'models/efi-upper-intake.glb'}
    promotion=read(ROOT/'inventory/engine/intake-exterior-promotion-validation.json')
    assert promotion['status'].startswith('PASS') and promotion['stage_validation_sha256']==sha(STAGE/'validation.json')
    for p,h in promotion['source_sha256'].items():assert sha(ROOT/p)==h,'Promotion source changed: '+p
    for p,h in {**report['current_neighbor_sha256'],**promotion['baseline_actor_sha256']}.items():
        expected=sha(expected_assets[p]) if installed and p in expected_assets else h
        assert sha(ROOT/p)==expected,'Current actor/neighbor changed: '+p
    manifest=ROOT/'inventory/engine/full-assembly.json';expected_manifest=report['staged_manifest_sha256'] if installed else report['before_manifest_sha256']
    assert sha(manifest)==expected_manifest,'Manifest no longer matches reviewed stage context'
    transaction=read(ROOT/'inventory/engine/intake-cap-promotion-transaction-validation.json')
    assert transaction['status'].startswith('PASS') and transaction['installer_sha256']==sha(HELPER)
    assert not any(p['new_or_worsened'] for p in report['static']['pairs']) and not report['current_throttle_motion']['failures']
    if installed:
        record=read(RECORD);assert record['stage_validation_sha256']==sha(STAGE/'validation.json')
        for p,h in record['promotion_source_sha256'].items():assert sha(ROOT/p)==h,p
        import build123d as b
        s=b.import_step(ROOT/'cad/engine/generated/efi-upper-intake.step');assert s.is_valid and len(s.solids())==1
    return {'status':'PASS installed exterior binding; browser acceptance pending' if installed else 'PASS exterior promotion preflight; no writes','manifest_sha256':sha(manifest),'stage_validation_sha256':sha(STAGE/'validation.json'),'candidate_report_sha256':sha(proofpath),'definitions':report['definitions'],'occurrences':report['occurrences'],'static_pairs':report['static']['exact_pairs'],'current_throttle_motion':report['current_throttle_motion'],'frame_changes':False}
def main():
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group();mode.add_argument('--apply',action='store_true');mode.add_argument('--check-installed',action='store_true');args=parser.parse_args()
    if args.check_installed:
        result=validate(True);(ROOT/'inventory/engine/intake-exterior-installed-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return
    preflight=validate()
    if not args.apply:print(json.dumps(preflight,indent=2));return
    spec=importlib.util.spec_from_file_location('reviewed_promotion_helper',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    writes={ROOT/'cad/engine/generated/efi-upper-intake.step':(STAGE/'step/efi-upper-intake.step').read_bytes(),ROOT/'models/engine/efi-upper-intake.glb':(STAGE/'models/efi-upper-intake.glb').read_bytes(),ROOT/'inventory/engine/full-assembly.json':(STAGE/'full-assembly.json').read_bytes()}
    record={**preflight,'status':'INSTALLED exterior; independent browser acceptance pending','promotion_source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),HELPER]},'after_manifest_sha256':sha(STAGE/'full-assembly.json')}
    writes[RECORD]=(json.dumps(record,indent=2)+'\n').encode();validation_path=ROOT/'inventory/engine/intake-exterior-installed-validation.json';writes[validation_path]=b''
    result={}
    def postcheck():
        result.update(validate(True));helper.replace(validation_path,(json.dumps(result,indent=2)+'\n').encode())
    validate();helper.promote(writes,postcheck);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
