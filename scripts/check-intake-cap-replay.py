#!/usr/bin/env python3
"""Exercise target replay, mixed partial refresh and unknown-state rejection."""
from pathlib import Path
import copy,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import intake_cap_coordination as adapter
from assembly_math import transforms
from upper_intake_clearance_candidate import volume,bake

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(manifest,loaded):
    m=copy.deepcopy(manifest);shapes=dict(loaded);old={d['id']:d for d in m['definitions']}
    def define(ident,shape,name,function,system,color,sources,gaps,claims,prepared=False):
        assert prepared
        d=copy.deepcopy(old.get(ident,{}));d.update(id=ident,name=name,function=function,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims)
        m['definitions'].append(d);shapes[ident]=shape
    result=adapter.install(define,None,None,m['definitions'],m['occurrences'],m['assemblies'],shapes,m['mechanism'])
    return m,shapes,result

def main():
    stage=ROOT/'cad/engine/generated/intake-cap-integration-stage'
    manifest=json.loads((stage/'full-assembly.json').read_text())
    loaded={ident:b.import_step(stage/'step'/(ident+'.step')) for ident in adapter.CHANGED_IDS}
    expected_poses=transforms(manifest);expected={i:bake(expected_poses[i]*s,'replay-expected-'+i) for i,s in loaded.items()}
    rows=[]
    first,parts,state=run(manifest,loaded)
    second,parts2,state2=run(first,parts)
    assert first==second,'Repeated metadata normalization changed output'
    assert state['cover_input_state']==state2['cover_input_state']=='coordinated'
    rows.append({'case':'repeat coordinated metadata','status':'PASS','duplicate_seals':sum(o['id']==adapter.SEAL for o in second['occurrences'])-1})
    mixed=copy.deepcopy(first);mixed_parts=dict(parts)
    contract=json.loads((ROOT/'reference/engine/intake-cap-frame-contract.json').read_text())
    cap=next(o for o in mixed['occurrences'] if o['id']=='oil-filler-cap');cap['position_cad_mm']=contract['frames']['oil-filler-cap']['baseline_position_cad_mm']
    mixed_parts['valve-cover']=b.import_step(ROOT/'cad/engine/generated/intake-cap-contract/legacy-valve-cover.step')
    next(d for d in mixed['definitions'] if d['id']=='valve-cover').pop('intake_cap_coordination_contract',None)
    third,parts3,state3=run(mixed,mixed_parts);assert state3['cover_input_state']=='reviewed legacy'
    assert first==third,'Mixed partial refresh did not normalize to identical metadata'
    for label,m,ps in [('target replay',second,parts2),('legacy cover and cap partial refresh',third,parts3)]:
        poses=transforms(m);diffs=[]
        for ident in adapter.CHANGED_IDS:
            actual=bake(poses[ident]*ps[ident],'replay-'+label.split()[0]+'-'+ident)
            diff=volume(actual-expected[ident])+volume(expected[ident]-actual);assert diff<.1,(label,ident,diff)
            diffs.append({'id':ident,'world_difference_mm3':diff})
        rows.append({'case':label,'status':'PASS','geometry':diffs})
    bad=copy.deepcopy(first);next(o for o in bad['occurrences'] if o['id']=='oil-filler-cap')['position_cad_mm'][0]+=1
    try:run(bad,parts)
    except ValueError as e:rows.append({'case':'unknown cap station','status':'PASS rejected','reason':str(e)})
    else:raise AssertionError('Unknown cap station accepted')
    wrong=dict(parts);wrong['valve-cover']=wrong['valve-cover']+b.Pos(0,0,0)*b.Box(2,2,2)
    try:run(first,wrong)
    except ValueError as e:rows.append({'case':'unreviewed cover solid','status':'PASS rejected','reason':str(e)})
    else:raise AssertionError('Unreviewed cover accepted')
    report={'status':'PASS explicit state replay and negative controls','cases':rows,'canonical_modified':False,'input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'cad/engine/intake_cap_coordination.py',ROOT/'reference/engine/intake-cap-frame-contract.json',stage/'full-assembly.json']}}
    (ROOT/'inventory/engine/intake-cap-replay-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
if __name__=='__main__':main()
