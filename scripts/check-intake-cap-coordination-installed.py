#!/usr/bin/env python3
"""Bind reviewed staged/installed solids, frames, inputs and evidence by hashes."""
from pathlib import Path
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
STAGE=ROOT/'cad/engine/generated/intake-cap-integration-stage'
RECORD=ROOT/'inventory/engine/intake-cap-coordination-installation.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def validate(stage=STAGE,installed=False):
    report=read(stage/'validation.json');target=read(stage/'full-assembly.json')
    assert report['status'].startswith('PASS staged')
    assert sha(stage/'full-assembly.json')==report['staged_manifest_sha256']
    for p,h in report['source_sha256'].items():assert sha(ROOT/p)==h,'Changed stage source/evidence: '+p
    for p,h in report['staged_artifact_sha256'].items():assert sha(stage/p)==h,'Changed staged asset: '+p
    assert len(report['geometry_checks'])==8 and all(r['world_symmetric_difference_mm3']<.1 for r in report['geometry_checks'])
    assert len(report['frame_checks'])==67 and all(r['frame_error_mm']<1e-6 for r in report['frame_checks'])
    candidate=ROOT/'cad/engine/generated/upper-intake-clearance-study/validation.json';proof=read(candidate)
    assert sha(candidate)==report['candidate_report_sha256'] and all(proof['gate_summary'].values()) and proof['input_guard_pass']
    replay=read(ROOT/'inventory/engine/intake-cap-replay-validation.json')
    assert replay['status'].startswith('PASS')
    for p,h in replay['input_sha256'].items():
        # Replay's initial staged manifest is a historical fixture. Its target
        # solids are independently compared again by the current staging pass.
        if p.endswith('full-assembly.json'):continue
        assert sha(ROOT/p)==h,'Replay source stale: '+p
    transaction=read(ROOT/'inventory/engine/intake-cap-promotion-transaction-validation.json')
    assert transaction['status'].startswith('PASS') and transaction['installer_sha256']==sha(ROOT/'scripts/install-intake-cap-coordination.py')
    contract_path=ROOT/'reference/engine/intake-cap-frame-contract.json';contract=read(contract_path)
    assert report['frame_contract_sha256']==sha(contract_path)
    for p,h in {**contract['artifacts_sha256'],**contract['geometry_sources_sha256']}.items():assert sha(ROOT/p)==h,'Changed frame contract input: '+p
    source=target['sources']['upper-intake-topology-study'];assert sha(ROOT/source['path'].lstrip('/'))==source['sha256']
    canonical=ROOT/'inventory/engine/full-assembly.json'
    expected_manifest=report['staged_manifest_sha256'] if installed else report['before_manifest_sha256']
    assert sha(canonical)==expected_manifest,'Canonical manifest differs from reviewed '+('installation' if installed else 'baseline')
    replacements={f'cad/engine/generated/{i}.step':stage/'step'/(i+'.step') for i in report['changed_definitions']}
    replacements.update({f'models/engine/{i}.glb':stage/'models'/(i+'.glb') for i in report['changed_definitions']})
    for p,h in proof['input_hashes'].items():
        expected=sha(replacements[p]) if installed and p in replacements else expected_manifest if p=='inventory/engine/full-assembly.json' else h
        assert sha(ROOT/p)==expected,'Candidate dependency changed: '+p
    if installed:
        record=read(RECORD)
        assert record['stage_validation_sha256']==sha(stage/'validation.json')
        for p,h in record['promotion_source_sha256'].items():assert sha(ROOT/p)==h,'Changed promotion source: '+p
        for p,h in record['canonical_artifact_sha256'].items():assert sha(ROOT/p)==h,'Installed asset differs: '+p
        import build123d as b
        solids=[]
        for ident in report['changed_definitions']:
            path=ROOT/f'cad/engine/generated/{ident}.step';shape=b.import_step(path)
            assert shape.is_valid and len(shape.solids())==1,(ident,'Invalid installed STEP')
            solids.append({'id':ident,'valid':True,'solid_count':1,'sha256':sha(path)})
    else:solids=report['geometry_checks']
    return {'status':'PASS installed binding; browser acceptance pending' if installed else 'PASS promotion preflight; no writes',
            'manifest_sha256':sha(canonical),'stage_validation_sha256':sha(stage/'validation.json'),
            'solids':solids,'bound_moved_frames':report['frame_checks'],'frame_contract_sha256':sha(contract_path),
            'source_ledger_sha256':source['sha256'],'candidate_report_sha256':sha(candidate),'replay_report_sha256':sha(ROOT/'inventory/engine/intake-cap-replay-validation.json')}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',action='store_true');args=parser.parse_args()
    result=validate(installed=not args.stage)
    if not args.stage:(ROOT/'inventory/engine/intake-cap-coordination-installed-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'solids':len(result['solids']),'moved_frames':len(result['bound_moved_frames'])},indent=2))
if __name__=='__main__':main()
