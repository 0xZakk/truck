#!/usr/bin/env python3
"""Bind the exterior promotion and exercise isolated installed-check negatives."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
    promoter=load('exterior_promoter',ROOT/'scripts/install-intake-exterior.py');stage=promoter.STAGE
    report=promoter.read(stage/'validation.json');assert report['status'].startswith('PASS')
    assert sha(ROOT/'inventory/engine/full-assembly.json')==report['before_manifest_sha256']
    # The original actor is still the previously installed coordinated casting.
    # This separate record binds its bytes without rewriting the staged audit.
    cap_record_path=ROOT/'inventory/engine/intake-cap-coordination-installation.json';cap_record=promoter.read(cap_record_path)
    actor={}
    for p in ('cad/engine/generated/efi-upper-intake.step','models/engine/efi-upper-intake.glb'):
        assert sha(ROOT/p)==cap_record['canonical_artifact_sha256'][p],'Original actor changed since coordinated installation'
        actor[p]=sha(ROOT/p)
    record={'status':'PASS promotion actor/source binding','stage_validation_sha256':sha(stage/'validation.json'),'baseline_actor_sha256':actor,
            'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'scripts/install-intake-exterior.py',cap_record_path]}}
    proof_path=ROOT/'inventory/engine/intake-exterior-promotion-validation.json';proof_path.write_text(json.dumps(record,indent=2)+'\n')
    promoter.validate()
    # Isolated mirror: source/neighbor references are individual symlinks;
    # modified installed assets and manifest are copies, never canonical links.
    mirror=ROOT/'cad/engine/generated/intake-exterior-promotion-mirror';mirror.mkdir(exist_ok=True)
    candidate=promoter.read(ROOT/'inventory/engine/intake-exterior-candidate-validation.json')
    files=set(report['current_neighbor_sha256'])|set(report['source_sha256'])|set(record['source_sha256'])
    files.update(p for p in candidate['input_sha256'] if not Path(p).is_absolute())
    files.update(['inventory/engine/intake-exterior-candidate-validation.json','inventory/engine/intake-exterior-promotion-validation.json','inventory/engine/intake-cap-promotion-transaction-validation.json','scripts/install-intake-cap-coordination.py'])
    for p in files:
        dest=mirror/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.unlink(missing_ok=True);dest.symlink_to(ROOT/p)
    for relative,source in [('cad/engine/generated/efi-upper-intake.step',stage/'step/efi-upper-intake.step'),('models/engine/efi-upper-intake.glb',stage/'models/efi-upper-intake.glb'),('inventory/engine/full-assembly.json',stage/'full-assembly.json')]:
        dest=mirror/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.unlink(missing_ok=True);shutil.copy2(source,dest)
    installed_record=mirror/'inventory/engine/intake-exterior-installation.json';installed_record.write_text(json.dumps({'stage_validation_sha256':sha(stage/'validation.json'),'promotion_source_sha256':{p:sha(ROOT/p) for p in ['scripts/install-intake-exterior.py','scripts/install-intake-cap-coordination.py']}}))
    promoter.ROOT=mirror;promoter.RECORD=installed_record;promoter.HELPER=mirror/'scripts/install-intake-cap-coordination.py'
    success=promoter.validate(True);cases=[{'case':'installed mirror','status':success['status']}]
    mesh=mirror/'models/engine/efi-upper-intake.glb';saved=mesh.read_bytes();mesh.write_bytes(saved+b'corrupt')
    try:promoter.validate(True)
    except AssertionError as e:cases.append({'case':'corrupt installed GLB','status':'PASS rejected','reason':str(e)})
    else:raise AssertionError('Corrupt mesh accepted')
    mesh.write_bytes(saved)
    manifest=mirror/'inventory/engine/full-assembly.json';m=json.loads(manifest.read_text());next(o for o in m['occurrences'] if o['id']=='efi-upper-intake')['position_cad_mm'][0]+=1;manifest.write_text(json.dumps(m))
    try:promoter.validate(True)
    except AssertionError as e:cases.append({'case':'shifted casting frame','status':'PASS rejected','reason':str(e)})
    else:raise AssertionError('Shifted casting accepted')
    shutil.copy2(stage/'full-assembly.json',manifest)
    result={'status':'PASS isolated exterior installed-binding controls','canonical_modified':False,'stage_validation_sha256':sha(stage/'validation.json'),'promotion_validation_sha256':sha(proof_path),'cases':cases,'checker_sha256':sha(Path(__file__))}
    (ROOT/'inventory/engine/intake-exterior-promotion-controls-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
