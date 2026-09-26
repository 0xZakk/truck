#!/usr/bin/env python3
"""Stage dipstick integration through the shared exporter; --apply is explicit.

Default is a write-free plan. --stage writes only an ignored isolated directory.
Canonical installation remains the integration owner's action after review.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import dipstick_integration as integration


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def validate_candidates(manifest,allow_installed=False):
    tr=ROOT/'inventory/engine/dipstick-tube-candidate-validation.json'
    br=ROOT/'inventory/engine/dipstick-inserted-candidate-validation.json'
    tube=json.loads(tr.read_text());blade=json.loads(br.read_text())
    assert tube['isolated_candidate']['status']=='PASS bounded educational geometry'
    assert blade['status']=='PASS bounded geometry'
    # The old tube report's whole-manifest/static-neighbor hash is historical:
    # the inserted report supplies the later relevant dependency contract.
    for p,h in blade['frozen_relevant_inputs_sha256'].items():
        assert sha(ROOT/p)==h, f'Stale inserted dependency: {p}'
    for key in ['cad/engine/dipstick_tube_candidate.py','cad/engine/generated/pushrod-cover-bolt.step','cad/engine/pushrod_cover.py']:
        assert sha(ROOT/key)==tube['inputs_sha256'][key],key
    if not allow_installed:
        key='cad/engine/generated/block.step'
        assert sha(ROOT/key)==tube['inputs_sha256'][key],'Block changed since receiver study'
    spec=importlib.util.spec_from_file_location('dipstick_inserted_check',ROOT/'scripts/check-dipstick-inserted-candidate.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    selected=set(blade['relevant_manifest_subset']['occurrences'])
    assert mod.dependency_summary(manifest,selected)==blade['relevant_manifest_subset'],'Relevant pose/motion changed'
    for p,h in tube['exports'].items():assert sha(ROOT/p)==h,p
    for p,h in blade['outputs_sha256'].items():assert sha(ROOT/p)==h,p
    return {'tube_report_sha256':sha(tr),'blade_report_sha256':sha(br)}


def assert_scope(before,after,changed):
    allowed={'definitions':integration.CHANGED_IDS,'occurrences':set(changed['changed_occurrences']),
             'assemblies':{integration.GROUP}}
    for kind,ids in allowed.items():
        a={r['id']:r for r in before[kind] if r['id'] not in ids}
        c={r['id']:r for r in after[kind] if r['id'] not in ids}
        assert a==c, f'Unrelated {kind} changed'
        all_ids=[r['id'] for r in after[kind]]
        assert len(all_ids)==len(set(all_ids)),f'Duplicate {kind}'
    old={o['id']:o for o in before['occurrences']};new={o['id']:o for o in after['occurrences']}
    for n in range(2,7):assert old[f'pushrod-cover-bolt-{n}']==new[f'pushrod-cover-bolt-{n}']
    for key in ['parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:
        assert old['pushrod-cover-bolt-1'].get(key)==new['pushrod-cover-bolt-1'].get(key),key


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--stage',action='store_true');mode.add_argument('--apply',action='store_true')
    parser.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/dipstick-integration-stage')
    args=parser.parse_args()
    if not(args.stage or args.apply):
        print('Plan: replace block, rebind only rear cover bolt, upsert four tube parts and two dipstick materials. No writes.')
        return
    import full_engine as engine
    from cad_metrics import support_bounds
    import numpy as np
    import trimesh
    target=ROOT/'inventory/engine/full-assembly.json';raw=target.read_bytes();manifest=json.loads(raw);before=copy.deepcopy(manifest)
    already=any(d['id']==integration.RETAINER for d in manifest['definitions'])
    evidence=validate_candidates(manifest,allow_installed=already)
    if already:
        # Reinstall requires proof the current changed artifacts match the last
        # installation. A new block must never bypass the original-block guard.
        record=json.loads((ROOT/'inventory/engine/dipstick-installation.json').read_text())
        assert record['after_manifest_sha256']==sha(target),'Installed manifest has moved; revalidate installed study first'
        for p,h in record['canonical_artifact_sha256'].items():assert sha(ROOT/p)==h,p
    out=args.stage_dir.resolve()
    if out==ROOT or ROOT not in out.parents or 'generated' not in out.parts:raise ValueError('Stage directory must be inside repository generated artifacts')
    out.mkdir(parents=True,exist_ok=True)
    engine.STEP=out/'step';engine.OUT=out/'models';engine.STEP.mkdir(exist_ok=True);engine.OUT.mkdir(exist_ok=True)
    engine.defs[:]=manifest['definitions'];engine.occurrences[:]=manifest['occurrences'];engine.assemblies[:]=manifest['assemblies'];engine.shapes.clear()
    changed=integration.install(engine.define,engine.add,engine.group,engine.defs,engine.occurrences,engine.assemblies,engine.shapes)
    for d in engine.defs:
        if d['id'] in integration.CHANGED_IDS:
            shape=engine.shapes[d['id']];bounds=shape.bounding_box();size=bounds.size
            mesh=trimesh.load(engine.OUT/(d['id']+'.glb'),force='mesh')
            if np.max(np.abs(mesh.extents*1000-np.array([size.X,size.Z,size.Y])))>=.2:
                bounds=support_bounds(shape);size=bounds.size
            d['model_bounds_mm']=[size.X,size.Y,size.Z]
    manifest.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies)
    manifest['sources'].update(integration.sources())
    manifest['coverage'].update(modeled_definitions=len(engine.defs),modeled_occurrences=len(engine.occurrences))
    assert_scope(before,manifest,changed)
    stage_manifest=out/'full-assembly.json';stage_manifest.write_text(json.dumps(manifest,indent=2)+'\n')
    report={'status':'STAGED; installed acceptance pending','before_manifest_sha256':hashlib.sha256(raw).hexdigest(),
        'staged_manifest_sha256':sha(stage_manifest),'candidate_evidence':evidence,**changed,
        'changed_assemblies':[integration.GROUP],'before_occurrences':[o for o in before['occurrences'] if o['id'] in changed['changed_occurrences']],
        'unrelated_inventory_unchanged':True,'canonical_modified':False,
        'installer_sha256':sha(Path(__file__)),'checker_sha256':sha(ROOT/'scripts/check-dipstick-integration.py'),
        'adapter_sha256':sha(ROOT/'cad/engine/dipstick_integration.py'),'learning_sha256':sha(ROOT/'inventory/engine/dipstick-learning.json'),
        'staged_artifact_sha256':{str(p.relative_to(out)):sha(p) for folder in ['step','models'] for p in (out/folder).iterdir()}}
    (out/'installation.json').write_text(json.dumps(report,indent=2)+'\n')
    assert target.read_bytes()==raw,'Canonical manifest changed during staging'
    validate_candidates(before,allow_installed=already)
    if args.apply:
        subprocess.run([sys.executable,str(ROOT/'scripts/check-dipstick-integration.py'),'--stage-dir',str(out)],check=True)
        assert target.read_bytes()==raw,'Canonical manifest changed during preflight checks'
        validate_candidates(before,allow_installed=already)
        report['stage_validation_sha256']=sha(out/'validation.json')
        writes={target:stage_manifest.read_bytes()}
        for ident in integration.CHANGED_IDS:
            writes[ROOT/f'cad/engine/generated/{ident}.step']=(engine.STEP/f'{ident}.step').read_bytes()
            writes[ROOT/f'models/engine/{ident}.glb']=(engine.OUT/f'{ident}.glb').read_bytes()
        record_path=ROOT/'inventory/engine/dipstick-installation.json'
        report.update(status='INSTALLED; installed checks/browser acceptance pending',canonical_modified=True,
                      after_manifest_sha256=sha(stage_manifest),
                      canonical_artifact_sha256={str(p.relative_to(ROOT)):hashlib.sha256(data).hexdigest() for p,data in writes.items() if p!=target})
        writes[record_path]=(json.dumps(report,indent=2)+'\n').encode()
        backups={p:p.read_bytes() if p.exists() else None for p in writes}
        try:
            for p,data in writes.items():
                pending=p.with_suffix(p.suffix+'.pending');pending.write_bytes(data);pending.replace(p)
        except Exception:
            for p,data in backups.items():
                if data is None:p.unlink(missing_ok=True)
                else:p.write_bytes(data)
            raise
    print(json.dumps({'status':report['status'],'stage_dir':str(out),'changed':changed,'definitions':len(engine.defs),'occurrences':len(engine.occurrences)},indent=2))

if __name__=='__main__':main()
