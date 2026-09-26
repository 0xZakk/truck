#!/usr/bin/env python3
"""Verify the reviewed stage; --apply explicitly promotes with rollback on failure."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[1]
CHECK=ROOT/'scripts/check-intake-cap-coordination-installed.py'
spec=importlib.util.spec_from_file_location('intake_cap_installed_check',CHECK);check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace(path,data):
    pending=path.with_suffix(path.suffix+'.pending');pending.write_bytes(data);pending.replace(path)
def promote(writes,postcheck,fail_after=None):
    """Per-file atomic replacement with full rollback on any write/check error."""
    backup={p:p.read_bytes() if p.exists() else None for p in writes}
    try:
        for number,(p,data) in enumerate(writes.items(),1):
            replace(p,data)
            if number==fail_after:raise RuntimeError('Injected transaction failure')
        postcheck()
    except BaseException:
        for p,data in backup.items():
            p.with_suffix(p.suffix+'.pending').unlink(missing_ok=True)
            if data is None:p.unlink(missing_ok=True)
            else:replace(p,data)
        raise

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    preflight=check.validate();stage=check.STAGE;report=check.read(stage/'validation.json')
    if not args.apply:
        print(json.dumps({'status':preflight['status'],'definitions':len(report['changed_definitions']),'added_occurrences':report['new_occurrences'],'moved_frames':len(report['frame_checks'])},indent=2));return
    canonical=ROOT/'inventory/engine/full-assembly.json';before=canonical.read_bytes()
    writes={}
    for ident in report['changed_definitions']:
        writes[ROOT/f'cad/engine/generated/{ident}.step']=(stage/'step'/(ident+'.step')).read_bytes()
        writes[ROOT/f'models/engine/{ident}.glb']=(stage/'models'/(ident+'.glb')).read_bytes()
    writes[canonical]=(stage/'full-assembly.json').read_bytes()
    record={**preflight,'status':'INSTALLED; independent browser acceptance pending','before_manifest_sha256':sha(canonical),
            'after_manifest_sha256':report['staged_manifest_sha256'],'promotion_source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),CHECK]},
            'canonical_artifact_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(data).hexdigest() for p,data in writes.items() if p!=canonical}}
    writes[check.RECORD]=(json.dumps(record,indent=2)+'\n').encode()
    assert canonical.read_bytes()==before;check.validate()
    post={};validation_path=ROOT/'inventory/engine/intake-cap-coordination-installed-validation.json'
    writes[validation_path]=b''  # Include the final report in rollback coverage.
    def postcheck():
        post.update(check.validate(installed=True))
        replace(validation_path,(json.dumps(post,indent=2)+'\n').encode())
    promote(writes,postcheck)
    print(post['status'])
if __name__=='__main__':main()
