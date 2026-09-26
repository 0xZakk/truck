#!/usr/bin/env python3
"""Stage only: coordinated intake/cap definitions and frames; never writes canonical assets."""
from pathlib import Path
import copy,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import intake_cap_coordination as integration

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    import full_engine as engine
    import build123d as b
    import numpy as np
    import trimesh
    from assembly_math import transforms
    from upper_intake_clearance_candidate import bake,volume
    candidate=ROOT/'cad/engine/generated/upper-intake-clearance-study/validation.json'
    checked=json.loads(candidate.read_text())
    assert checked['input_guard_pass'] and all(checked['gate_summary'].values()),'Candidate gates incomplete'
    for p,h in checked['input_hashes'].items():assert sha(ROOT/p)==h,f'Stale candidate input: {p}'
    path=ROOT/'inventory/engine/full-assembly.json';raw=path.read_bytes();manifest=json.loads(raw);before=copy.deepcopy(manifest)
    out=ROOT/'cad/engine/generated/intake-cap-integration-stage';out.mkdir(exist_ok=True)
    engine.STEP=out/'step';engine.OUT=out/'models';engine.STEP.mkdir(exist_ok=True);engine.OUT.mkdir(exist_ok=True)
    engine.defs[:]=manifest['definitions'];engine.occurrences[:]=manifest['occurrences'];engine.assemblies[:]=manifest['assemblies'];engine.shapes.clear()
    changed=integration.install(engine.define,engine.add,engine.group,engine.defs,engine.occurrences,engine.assemblies,engine.shapes,manifest['mechanism'])
    for d in engine.defs:
        if d['id'] in integration.CHANGED_IDS:
            size=engine.shapes[d['id']].bounding_box().size;d['model_bounds_mm']=[size.X,size.Y,size.Z]
    manifest.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies)
    manifest['sources'].update(integration.sources());manifest['coverage'].update(modeled_definitions=len(engine.defs),modeled_occurrences=len(engine.occurrences))
    for kind,allowed in [('definitions',integration.CHANGED_IDS),('occurrences',set(changed['changed_occurrences'])),('assemblies',set(changed['changed_assemblies']))]:
        assert {r['id']:r for r in before[kind] if r['id'] not in allowed}=={r['id']:r for r in manifest[kind] if r['id'] not in allowed},'Unrelated '+kind
        ids=[r['id'] for r in manifest[kind]];assert len(ids)==len(set(ids))
    oldposes=transforms(before);newposes=transforms(manifest)
    oldocc={o['id']:o for o in before['occurrences']};parents={a['id']:a.get('parent') for a in before['assemblies']}
    def under(o,root):
        parent=o.get('parent')
        while parent:
            if parent==root:return True
            parent=parents.get(parent)
        return False
    frame_checks=[]
    for ident,o in oldocc.items():
        delta=(-167,0,0) if under(o,'throttle-assembly') else (167,0,25) if under(o,'egr-valve-assembly') or under(o,'egr-position-sensor') or ident in ('egr-intake-gasket','egr-mount-bolt-1','egr-mount-bolt-2') else (60,0,0) if ident=='oil-filler-cap' else (0,0,0)
        expected=b.Pos(*delta)*oldposes[ident]
        error=max((b.Vertex(*p).moved(expected).center()-b.Vertex(*p).moved(newposes[ident]).center()).length for p in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)])
        assert error<1e-6,(ident,error)
        if any(delta):frame_checks.append({'id':ident,'delta_mm':delta,'frame_error_mm':error})
    aliases={'efi-upper-intake':'upper-intake','valve-cover':'cover-with-neck','oil-filler-cap':'cap','oil-filler-cap-seal':'seal'}
    geometry=[]
    for ident in integration.CHANGED_IDS:
        expected=b.import_step(ROOT/'cad/engine/generated/upper-intake-clearance-study/baked'/(aliases.get(ident,'route-'+ident)+'.step'))
        local=b.import_step(engine.STEP/(ident+'.step'));actual=bake(newposes[ident]*local,'stage-world-'+ident)
        diff=volume(actual-expected)+volume(expected-actual)
        assert diff<.1,(ident,diff)
        mesh=trimesh.load(engine.OUT/(ident+'.glb'),force='mesh');raw_watertight=mesh.is_watertight;raw_vertices=len(mesh.vertices)
        # Shared exporter preserves coincident per-face vertices for shading.
        # Weld positional duplicates at10nm for topological closure inspection;
        # no asset geometry is rewritten or missing face filled.
        mesh.merge_vertices(digits_vertex=8);a=np.asarray(mesh.vertices);v=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000
        box=local.bounding_box();error=float(np.max(np.abs(np.array([v.min(0),v.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
        assert error<.2 and mesh.is_watertight,(ident,error,mesh.is_watertight)
        geometry.append({'id':ident,'world_symmetric_difference_mm3':diff,'mesh_bounds_error_mm':error,'watertight_after_coincident_vertex_weld':mesh.is_watertight,'raw_watertight':raw_watertight,'raw_vertices':raw_vertices,'welded_vertices':len(mesh.vertices),'weld_grid_mm':.00001})
    target=out/'full-assembly.json';target.write_text(json.dumps(manifest,indent=2)+'\n')
    report={'status':'PASS staged geometry and frame equivalence; not installed','candidate_report_sha256':sha(candidate),'before_manifest_sha256':hashlib.sha256(raw).hexdigest(),'staged_manifest_sha256':sha(target),'canonical_modified':False,**changed,'frame_checks':frame_checks,'geometry_checks':geometry,'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'cad/engine/intake_cap_coordination.py',ROOT/'reference/engine/intake-cap-frame-contract.json',ROOT/'reference/engine/upper-intake-topology-review.json',ROOT/'inventory/engine/intake-cap-replay-validation.json',ROOT/'scripts/install-intake-cap-coordination.py',ROOT/'scripts/check-intake-cap-coordination-installed.py',ROOT/'inventory/engine/intake-cap-promotion-transaction-validation.json']},'staged_artifact_sha256':{str(p.relative_to(out)):sha(p) for sub in ['step','models'] for p in (out/sub).iterdir()}}
    assert path.read_bytes()==raw,'Canonical manifest changed during staging'
    for p,h in checked['input_hashes'].items():assert sha(ROOT/p)==h,f'Input changed during staging: {p}'
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'definitions':len(engine.defs),'occurrences':len(engine.occurrences),'out':str(out)},indent=2))
if __name__=='__main__':main()
