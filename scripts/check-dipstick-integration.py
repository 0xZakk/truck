#!/usr/bin/env python3
"""Validate staged or installed dipstick artifacts, frames, sources and replay.

Default checks the isolated stage and writes only its validation.json. Use
--installed after the integration owner applies the installer.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys
import build123d as b
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import dipstick_integration as integration
from assembly_math import transforms
from cad_metrics import support_bounds


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(q.volume for q in s.solids()) if s is not None else 0.
def difference(a,c):return vol(a-c)+vol(c-a)

def replay(manifest,shapes,legacy_pose=False):
    """Exercise adapter semantics without writing any export or canonical file."""
    data=copy.deepcopy(manifest);defs=data['definitions'];occs=data['occurrences'];assemblies=data['assemblies']
    if legacy_pose:
        for o in occs:
            if o['definition'] in (integration.BLADE,integration.HANDLE):
                o.update(parent='lubrication',position_cad_mm=[-120,170,445],rotation_cad_deg=[-8.5,0,0])
    old={d['id']:d for d in defs};captured={}
    def define(ident,shape,name,function,system,color,sources,gaps,claims,prepared=False):
        assert prepared
        row=copy.deepcopy(old[ident])
        assert row['name']==name and row['function']==function and row['sources']==sources
        assert row['system']==system and row['color']==color
        assert row['unresolved']==gaps and row['dimension_claims']==claims
        defs.append(row);captured[ident]=shape
    def add(ident,definition,parent,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
        d=next(d for d in defs if d['id']==definition)
        occs.append(dict(id=ident,definition=definition,parent=parent,name=name or d['name'],function=d['function'],
                         position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode)))
    def group(ident,name,parent='engine',motion=None,position=(0,0,0),rotation=(0,0,0)):
        assemblies.append(dict(id=ident,name=name,parent=parent,motion=motion,position_cad_mm=list(position),rotation_cad_deg=list(rotation)))
    integration.install(define,add,group,defs,occs,assemblies,shapes)
    for key in ['definitions','occurrences','assemblies']:
        assert data[key]==manifest[key],f'Replay changed {key}'
    return captured


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installed',action='store_true')
    parser.add_argument('--stage-dir',type=Path,default=ROOT/'cad/engine/generated/dipstick-integration-stage')
    args=parser.parse_args();stage=args.stage_dir.resolve()
    mp=ROOT/'inventory/engine/full-assembly.json' if args.installed else stage/'full-assembly.json'
    record_path=ROOT/'inventory/engine/dipstick-installation.json' if args.installed else stage/'installation.json'
    raw=mp.read_bytes();m=json.loads(raw);record=json.loads(record_path.read_text())
    expected_hash=record['after_manifest_sha256'] if args.installed else record['staged_manifest_sha256']
    assert sha(mp)==expected_hash
    assert sha(ROOT/'scripts/install-dipstick.py')==record['installer_sha256']
    assert sha(Path(__file__))==record['checker_sha256']
    assert sha(ROOT/'cad/engine/dipstick_integration.py')==record['adapter_sha256']
    assert sha(ROOT/'inventory/engine/dipstick-learning.json')==record['learning_sha256']
    spec=importlib.util.spec_from_file_location('dipstick_installer_check',ROOT/'scripts/install-dipstick.py')
    installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
    assert installer.validate_candidates(m,allow_installed=True)==record['candidate_evidence']
    defs={d['id']:d for d in m['definitions']};occs={o['id']:o for o in m['occurrences']};poses=transforms(m)
    tube_root=ROOT/'cad/engine/generated/dipstick-tube-feasibility'
    blade_root=ROOT/'cad/engine/generated/dipstick-inserted-feasibility'
    expected={ident:tube_root/(ident+'.step') for ident in integration.TUBE_IDS}
    expected.update({'block':tube_root/'block-candidate.step',integration.RETAINER:tube_root/'pushrod-cover-retainer-candidate.step',
                     integration.BLADE:blade_root/'engine-oil-dipstick-blade-inserted.step',
                     integration.HANDLE:blade_root/'engine-oil-dipstick-handle-inserted.step'})
    checks=[];hashes={};shapes={}
    for ident in sorted(integration.CHANGED_IDS):
        sp=ROOT/defs[ident]['step'].lstrip('/') if args.installed else stage/'step'/(ident+'.step')
        gp=ROOT/defs[ident]['glb'].lstrip('/') if args.installed else stage/'models'/(ident+'.glb')
        for p in [sp,gp]:
            key=str(p.relative_to(ROOT if args.installed else stage))
            declared=record['canonical_artifact_sha256'] if args.installed else record['staged_artifact_sha256']
            assert sha(p)==declared[key],f'Export artifact changed: {p}'
        for p in [sp,gp,expected[ident]]:hashes[str(p.relative_to(ROOT))]=sha(p)
        actual=b.import_step(sp);shapes[ident]=actual
        world=poses['pushrod-cover-bolt-1']*actual if ident==integration.RETAINER else actual
        reference=b.import_step(expected[ident]);delta=difference(world,reference)
        assert actual.is_valid and len(actual.solids())==1 and delta<.02,(ident,delta)
        shifted=difference(b.Pos(1,0,0)*world,reference);assert shifted>1,(ident,'translation control missed')
        mesh=trimesh.load(gp,force='mesh');bb=actual.bounding_box()
        if np.max(np.abs(mesh.extents*1000-np.array([bb.size.X,bb.size.Z,bb.size.Y])))>=.2:bb=support_bounds(actual)
        target=np.array([bb.size.X,bb.size.Z,bb.size.Y]);error=float(np.max(np.abs(mesh.extents*1000-target)))
        assert error<.2,(ident,error)
        assert max(abs(defs[ident]['model_bounds_mm'][i]-list(bb.size)[i]) for i in range(3))<.01
        checks.append({'id':ident,'symmetric_difference_mm3':delta,'shift_negative_control_mm3':shifted,'mesh_bounds_error_mm':error})
    assert occs['pushrod-cover-bolt-1']['definition']==integration.RETAINER
    for n in range(2,7):assert occs[f'pushrod-cover-bolt-{n}']['definition']=='pushrod-cover-bolt'
    for ident in integration.TUBE_IDS|{integration.BLADE,integration.HANDLE}:
        found=[o for o in m['occurrences'] if o['definition']==ident];assert len(found)==1
        o=found[0];assert o['parent']==integration.GROUP and o['position_cad_mm']==[0,0,0] and o.get('rotation_cad_deg')==[0,0,0]
    for oid in ('block','pushrod-cover-bolt-1'):
        old=next((o for o in record['before_occurrences'] if o['id']==oid),None)
        if old:
            for key in ['parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:assert old.get(key)==occs[oid].get(key)
    for key,value in integration.sources().items():assert m['sources'][key]==value
    learning=json.loads((ROOT/'inventory/engine/dipstick-learning.json').read_text())
    for key,lesson in learning.items():
        assert key in defs or key in occs
        assert set(lesson['sources'])<=set(m['sources'])
        for section in ['steps','troubleshooting']:
            for entry in lesson.get(section,[]):
                if 'part' in entry:assert entry['part'] in occs,entry
    shapes['pushrod-cover-bolt']=b.import_step(ROOT/defs['pushrod-cover-bolt']['step'].lstrip('/'))
    replayed=replay(m,shapes)
    replay_errors={ident:difference(shape,shapes[ident]) for ident,shape in replayed.items()}
    assert all(v<.02 for v in replay_errors.values()),replay_errors
    replay(m,shapes,legacy_pose=True)
    assert mp.read_bytes()==raw
    assert all(sha(ROOT/p)==h for p,h in hashes.items())
    report={'status':'PASS','scope':'Stage/installed artifact and pose binding; not browser or factory acceptance',
        'installed':args.installed,'manifest_sha256':sha(mp),'candidate_evidence':record['candidate_evidence'],
        'parts':checks,'replay_symmetric_difference_mm3':replay_errors,
        'adapter_metadata_replay_identical':True,'replay_method':'Definition callback arguments and occurrence/group inventories checked; numeric export fields reused, regenerated shapes compared independently','legacy_pilot_pose_reset':True,'learning_references_valid':True,
        'artifact_sha256':hashes,'limits':'Threads, elastic insertion, retention strength, exact owner identity and oil calibration remain unresolved.'}
    destination=ROOT/'inventory/engine/dipstick-installed-validation.json' if args.installed else stage/'validation.json'
    destination.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','installed':args.installed,'parts':checks,'replay':replay_errors},indent=2))

if __name__=='__main__':main()
