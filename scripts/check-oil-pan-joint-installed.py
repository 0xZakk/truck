"""Compare published joint STEP geometry to a QC-approved frozen baseline candidate.

Use --baseline-root pointing to the unchanged pre-integration checkout/snapshot.
This complements, not replaces, full-engine static/navigation/motion QC.
"""
from pathlib import Path
import argparse,hashlib,json,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--baseline-root',type=Path,required=True);args=parser.parse_args();BASE=args.baseline_root.resolve()
from cad_metrics import solid_volume,step_comparison_shape
import oil_pan_joint_candidate as p
from assembly_math import transforms
report=json.loads((BASE/'inventory/engine/oil-pan-joint-candidate-validation.json').read_text())
assert report['inputs_unchanged'] and not report['collisions'],'Baseline candidate has no accepted QC pass'
assert hashlib.sha256((BASE/'inventory/engine/full-assembly.json').read_bytes()).hexdigest()==report['manifest_sha256'],'Baseline manifest changed'
for path,digest in report['input_hashes'].items():assert hashlib.sha256((BASE/path).read_bytes()).hexdigest()==digest,path
for path in ['cad/engine/oil_pan_joint_candidate.py','cad/engine/oil_pan_fasteners.py']:
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==report['input_hashes'][path],path
base=json.loads((BASE/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in base['definitions']}
def old(key):
    path=defs[key]['step'].lstrip('/')
    assert hashlib.sha256((BASE/path).read_bytes()).hexdigest()==report['step_hashes'][path],path
    return b.import_step(BASE/path)
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);ds={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};poses=transforms(m)
assert not {'pan-side-gasket-1','pan-side-gasket-2'}&occ.keys()
expected={'block':p.block_interface(old('block')),'oil-pan':p.pan_interface(old('oil-pan')),'oil-pan-molded-gasket':p.gasket_shape(),'oil-pan-mounting-screw':p.screw_shape(),'oil-pan-mounting-washer':p.washer_shape()}
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
comparisons={};installed={};frozen={}
for key,s in expected.items():
    path=ROOT/ds[key]['step'].lstrip('/');frozen[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();a=b.import_step(path);installed[key]=a
    assert a.is_valid and len(a.solids())==1,key
    normalized=step_comparison_shape(s);difference=vol(a-normalized)+vol(normalized-a)
    assert difference<.02,(key,difference)
    comparisons[key]=difference;print('Installed STEP matches',key,difference,flush=True)
for n,(x,y,z) in enumerate(p.STATIONS,1):
    for role in ('screw','washer'):
        key=f'oil-pan-mounting-{role}-{n}'
        assert occ[key]['definition']==f'oil-pan-mounting-{role}',key
        expected_pose=b.Pos(x,y,z)
        # Definitions already passed geometric comparison; compare the full rigid
        # transform independently using an affine basis instead of repeat booleans.
        for point in ((0,0,0),(1,0,0),(0,1,0),(0,0,1)):
            actual_point=b.Vertex(*point).moved(poses[key]).center()
            expected_point=b.Vertex(*point).moved(expected_pose).center()
            assert (actual_point-expected_point).length<1e-9,(key,point)
        lateral=((25 if x>0 else -25) if n>20 else 0,(25 if y>0 else -25) if n<=20 else 0,-360 if role=='screw' else -340)
        assert tuple(occ[key]['explode_cad_mm'])==lateral,key
assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in frozen.items()) and raw==(ROOT/'inventory/engine/full-assembly.json').read_bytes()
result={'manifest_sha256':hashlib.sha256(raw).hexdigest(),'baseline_manifest_sha256':report['manifest_sha256'],'symmetric_difference_mm3':comparisons,'occurrence_poses_checked':50,'step_hashes':frozen,'scope':'Installed shape/pose comparison only; full-engine static, sealing and motion audits remain separate.'}
(ROOT/'inventory/engine/oil-pan-joint-installed-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS installed oil-pan joint candidate comparison')
