#!/usr/bin/env python3
"""Stage one exterior casting and audit current neighbors; no canonical writes."""
from pathlib import Path
import hashlib,json,copy,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import intake_exterior_integration as adapter
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/intake-exterior-integration-stage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def volume(s):return sum(z.volume for z in s.solids()) if s else 0.
def bake(shape,name):
    folder=OUT/'baked';folder.mkdir(exist_ok=True);path=folder/(name+'.step')
    b.export_step(shape,path);result=b.import_step(path)
    assert result.is_valid and len(result.solids())==len(shape.solids()) and abs(volume(result)-volume(shape))<.1
    return result

def main():
    import full_engine as engine
    proof_path=ROOT/'inventory/engine/intake-exterior-candidate-validation.json';proof=json.loads(proof_path.read_text());assert proof['status'].startswith('PASS') and proof['input_guard_pass']
    # Historical719 neighbor artifacts are frozen fixtures. Current neighbors
    # receive a new independent audit below; source/font/fixture hashes stay bound.
    for p,h in proof['input_sha256'].items():
        path=Path(p) if Path(p).is_absolute() else ROOT/p
        assert sha(path)==h,'Candidate dependency changed: '+p
    path=ROOT/'inventory/engine/full-assembly.json';raw=path.read_bytes();m=json.loads(raw);before=copy.deepcopy(m)
    OUT.mkdir(exist_ok=True);engine.STEP=OUT/'step';engine.OUT=OUT/'models';engine.STEP.mkdir(exist_ok=True);engine.OUT.mkdir(exist_ok=True)
    definitions={d['id']:d for d in m['definitions']};poses=transforms(m)
    assets={ROOT/d[k].lstrip('/') for d in definitions.values() for k in ('step','glb')}
    initial={str(p):sha(p) for p in assets}
    engine.defs[:]=m['definitions'];engine.occurrences[:]=m['occurrences'];engine.assemblies[:]=m['assemblies'];engine.shapes.clear()
    change=adapter.install(engine.define,engine.defs,engine.occurrences,engine.assemblies,engine.shapes,m['mechanism'],engine.OUT)
    m.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies);m['sources'].update(adapter.sources())
    for kind in ('definitions','occurrences'):
        assert {r['id']:r for r in before[kind] if r['id']!=adapter.ID}=={r['id']:r for r in m[kind] if r['id']!=adapter.ID}
    assert before['assemblies']==m['assemblies']
    for a,z in zip(before['occurrences'],m['occurrences']):
        for key in ('id','definition','parent','position_cad_mm','rotation_cad_deg','motion','valvetrain'):assert a.get(key)==z.get(key),(a['id'],key)
    actual=poses[adapter.ID]*b.import_step(engine.STEP/(adapter.ID+'.step'))
    expected=b.import_step(ROOT/'cad/engine/generated/intake-exterior-study/upper-intake-exterior.step')
    assert volume(actual-expected)+volume(expected-actual)<.1
    original=poses[adapter.ID]*b.import_step(ROOT/definitions[adapter.ID]['step'].lstrip('/'))
    box=actual.bounding_box();alo=np.array(tuple(box.min));ahi=np.array(tuple(box.max));bounds={};pairs=[];tracked=set();excluded=0
    for o in m['occurrences']:
        if o['id']==adapter.ID:continue
        d=definitions[o['definition']];gp=ROOT/d['glb'].lstrip('/');tracked.add(gp)
        if d['id'] not in bounds:
            a=np.asarray(trimesh.load(gp,force='mesh').vertices);v=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000;bounds[d['id']]=(v.min(0)-.2,v.max(0)+.2)
        lo,hi=bounds[d['id']];corners=np.array([tuple(b.Vertex(x,y,z).moved(poses[o['id']]).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]);lo,hi=corners.min(0),corners.max(0)
        if np.any(ahi<lo) or np.any(hi<alo):excluded+=1;continue
        sp=ROOT/d['step'].lstrip('/');tracked.add(sp);neighbor=bake(poses[o['id']]*b.import_step(sp),'rest-'+o['id'])
        hit=volume(actual&neighbor);prior=volume(original&neighbor) if hit>.1 else 0.
        pairs.append({'neighbor':o['id'],'overlap_mm3':hit,'baseline_overlap_mm3':prior,'new_or_worsened':hit>prior+.1})
    assert not any(r['new_or_worsened'] for r in pairs),[r for r in pairs if r['new_or_worsened']]
    # Current rigid throttle descendants, including newly installed plate screws.
    assemblies={a['id']:a for a in m['assemblies']}
    def moving(o):
        parent=o.get('parent')
        while parent in assemblies:
            a=assemblies[parent]
            if (a.get('motion') or {}).get('type')=='throttle':return True
            parent=a.get('parent')
        return False
    actors=[o for o in m['occurrences'] if moving(o)];motion=[]
    for angle in range(0,91,2):
        pp=transforms(dict(m,occurrences=actors),throttle_degrees=angle)
        for o in actors:
            d=definitions[o['definition']];lo,hi=bounds[d['id']];corners=np.array([tuple(b.Vertex(x,y,z).moved(pp[o['id']]).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]);lo,hi=corners.min(0),corners.max(0)
            hit=0.
            if not(np.any(ahi<lo) or np.any(hi<alo)):
                sp=ROOT/d['step'].lstrip('/');tracked.add(sp);hit=volume(actual&bake(pp[o['id']]*b.import_step(sp),f"motion-{o['id']}-{angle}"))
            assert hit<.1,(angle,o['id'],hit)
            motion.append({'angle_deg':angle,'actor':o['id'],'overlap_mm3':hit})
    for p in tracked:assert sha(p)==initial[str(p)],'Neighbor changed: '+str(p)
    assert path.read_bytes()==raw,'Canonical manifest changed during stage'
    target=OUT/'full-assembly.json';target.write_text(json.dumps(m,indent=2)+'\n')
    report={'status':'PASS staged exterior and current-neighbor audit; not installed','before_manifest_sha256':hashlib.sha256(raw).hexdigest(),'staged_manifest_sha256':sha(target),'candidate_report_sha256':sha(proof_path),'definitions':len(m['definitions']),'occurrences':len(m['occurrences']),**change,'canonical_modified':False,'world_candidate_difference_mm3':volume(actual-expected)+volume(expected-actual),'static':{'exact_pairs':len(pairs),'aabb_excluded':excluded,'pairs':pairs},'current_throttle_motion':{'phases':46,'actors':len(actors),'pairs':len(motion),'failures':[]},'current_neighbor_sha256':{str(p.relative_to(ROOT)):sha(p) for p in tracked},'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'cad/engine/intake_exterior_integration.py',ROOT/'cad/engine/intake_exterior_candidate.py',ROOT/'reference/engine/intake-exterior-review.json']},'staged_artifact_sha256':{str(p.relative_to(OUT)):sha(p) for folder in ('step','models') for p in (OUT/folder).iterdir()}}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'inventory/engine/intake-exterior-stage-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('status','definitions','occurrences','current_throttle_motion')},indent=2))
if __name__=='__main__':main()
