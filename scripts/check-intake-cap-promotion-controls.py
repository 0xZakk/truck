#!/usr/bin/env python3
"""Exercise promotion rollback and installed binding in an isolated file mirror."""
from pathlib import Path
import hashlib,importlib.util,json,shutil
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    installer=module('promotion',ROOT/'scripts/install-intake-cap-coordination.py')
    checker=module('installed_check',ROOT/'scripts/check-intake-cap-coordination-installed.py')
    stage=checker.STAGE;proof=checker.read(ROOT/'cad/engine/generated/upper-intake-clearance-study/validation.json');report=checker.read(stage/'validation.json')
    folder=ROOT/'cad/engine/generated/intake-cap-promotion-controls';folder.mkdir(exist_ok=True)
    old=folder/'existing';new=folder/'new';old.write_bytes(b'original');new.unlink(missing_ok=True)
    cases=[]
    for name,fail,post in [('mid-write failure',2,lambda:None),('postcheck failure',None,lambda:(_ for _ in ()).throw(ValueError('injected postcheck failure')))]:
        try:installer.promote({old:b'changed',new:b'created'},post,fail_after=fail)
        except (RuntimeError,ValueError):pass
        else:raise AssertionError('Fault not detected: '+name)
        assert old.read_bytes()==b'original' and not new.exists()
        cases.append({'case':name,'status':'PASS rollback restores old bytes and removes new files'})
    installer.promote({old:b'changed',new:b'created'},lambda:None);assert old.read_bytes()==b'changed' and new.read_bytes()==b'created'
    cases.append({'case':'successful transaction','status':'PASS'})
    mirror=folder/'mirror';mirror.mkdir(exist_ok=True)
    contract=checker.read(ROOT/'reference/engine/intake-cap-frame-contract.json')
    paths=set(proof['input_hashes'])|set(report['source_sha256'])|set(contract['artifacts_sha256'])|set(contract['geometry_sources_sha256'])
    paths.update(['cad/engine/generated/upper-intake-clearance-study/validation.json','reference/engine/intake-cap-frame-contract.json','reference/engine/upper-intake-topology-review.json','inventory/engine/intake-cap-replay-validation.json','inventory/engine/intake-cap-promotion-transaction-validation.json','scripts/install-intake-cap-coordination.py','scripts/check-intake-cap-coordination-installed.py','scripts/check-intake-cap-replay.py'])
    # Individual read-only-reference symlinks; mutable installed targets below
    # are copies. No directory symlink permits a write into canonical folders.
    for path in paths:
        dest=mirror/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.unlink(missing_ok=True);dest.symlink_to(ROOT/path)
    artifacts={}
    for ident in report['changed_definitions']:
        for relative,source in [(f'cad/engine/generated/{ident}.step',stage/'step'/(ident+'.step')),(f'models/engine/{ident}.glb',stage/'models'/(ident+'.glb'))]:
            dest=mirror/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.unlink(missing_ok=True);shutil.copy2(source,dest);artifacts[relative]=sha(dest)
    manifest=mirror/'inventory/engine/full-assembly.json';manifest.unlink(missing_ok=True);shutil.copy2(stage/'full-assembly.json',manifest)
    record={'stage_validation_sha256':sha(stage/'validation.json'),'promotion_source_sha256':{p:sha(ROOT/p) for p in ['scripts/install-intake-cap-coordination.py','scripts/check-intake-cap-coordination-installed.py']},'canonical_artifact_sha256':artifacts}
    installed_record=mirror/'inventory/engine/intake-cap-coordination-installation.json';installed_record.write_text(json.dumps(record))
    checker.ROOT=mirror;checker.RECORD=installed_record
    good=checker.validate(stage,installed=True);assert len(good['solids'])==8 and len(good['bound_moved_frames'])==67
    cases.append({'case':'staged assets as installed mirror','status':'PASS eight valid solids and67 frame bindings'})
    target=mirror/'models/engine/oil-filler-cap-seal.glb';saved=target.read_bytes();target.write_bytes(saved+b'corrupt')
    try:checker.validate(stage,installed=True)
    except AssertionError as error:cases.append({'case':'corrupted installed asset','status':'PASS rejected','reason':str(error)})
    else:raise AssertionError('Corrupt asset was accepted')
    target.write_bytes(saved)
    m=json.loads(manifest.read_text());next(o for o in m['occurrences'] if o['id']=='oil-filler-cap')['position_cad_mm'][0]+=1;manifest.write_text(json.dumps(m))
    try:checker.validate(stage,installed=True)
    except AssertionError as error:cases.append({'case':'shifted installed cap frame','status':'PASS rejected','reason':str(error)})
    else:raise AssertionError('Shifted frame was accepted')
    shutil.copy2(stage/'full-assembly.json',manifest)
    result={'status':'PASS isolated promotion and installed-checker controls','canonical_modified':False,'cases':cases,'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'scripts/install-intake-cap-coordination.py',ROOT/'scripts/check-intake-cap-coordination-installed.py']},'stage_validation_sha256':sha(stage/'validation.json')}
    (ROOT/'inventory/engine/intake-cap-promotion-controls-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
