#!/usr/bin/env python3
"""Rebind the exact exterior audit across the recorded source-only registration."""
from pathlib import Path
import copy,hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1];STAGE=ROOT/'cad/engine/generated/intake-exterior-integration-stage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    report=read(STAGE/'validation.json');current=read(ROOT/'inventory/engine/full-assembly.json');staged=read(STAGE/'full-assembly.json')
    registration=read(ROOT/'inventory/engine/source-capture-registration.json')
    assert report['before_manifest_sha256']==registration['before_manifest_sha256']
    assert sha(ROOT/'inventory/engine/full-assembly.json')==registration['after_manifest_sha256']
    assert registration['geometry_placements_learning_unchanged']
    # Recover the exact pre-stage manifest using the unchanged original actor.
    prior=copy.deepcopy(staged)
    for key in ('definitions','occurrences'):
        old=next(x for x in current[key] if x['id']=='efi-upper-intake')
        indexed={x['id']:x for x in prior[key]}
        prior[key]=[old if x['id']=='efi-upper-intake' else indexed[x['id']] for x in current[key]]
    prior['sources'].pop('upper-intake-exterior-study')
    encoded=(json.dumps(prior,indent=2)+'\n').encode()
    assert hashlib.sha256(encoded).hexdigest()==report['before_manifest_sha256'],'Cannot recover exact historical baseline'
    assert {k:v for k,v in prior.items() if k!='sources'}=={k:v for k,v in current.items() if k!='sources'}
    changed=[k for k in prior['sources'].keys()|current['sources'].keys() if prior['sources'].get(k)!=current['sources'].get(k)]
    assert set(changed)<=set(registration['updated_sources'])
    for p,h in report['current_neighbor_sha256'].items():assert sha(ROOT/p)==h,p
    historical=STAGE/'historical-source-context';historical.mkdir(exist_ok=True)
    for name in ('full-assembly.json','validation.json'):shutil.copy2(STAGE/name,historical/name)
    (historical/'before-full-assembly.json').write_bytes(encoded)
    staged['sources']={**current['sources'],'upper-intake-exterior-study':staged['sources']['upper-intake-exterior-study']}
    (STAGE/'full-assembly.json').write_text(json.dumps(staged,indent=2)+'\n')
    report['source_only_rebind']={'historical_validation_sha256':sha(historical/'validation.json'),'historical_before_manifest_sha256':report['before_manifest_sha256'],'changed_source_ids':changed,'non_source_manifest_exactly_equal':True,'geometry_rechecks':'Reused unchanged exact audit; every current neighbor hash reverified.'}
    report['before_manifest_sha256']=registration['after_manifest_sha256'];report['staged_manifest_sha256']=sha(STAGE/'full-assembly.json')
    for p in [Path(__file__),ROOT/'inventory/engine/source-capture-registration.json']:report['source_sha256'][str(p.relative_to(ROOT))]=sha(p)
    for p in [STAGE/'validation.json',ROOT/'inventory/engine/intake-exterior-stage-validation.json']:p.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS source-only rebind; original context preserved')
if __name__=='__main__':main()
