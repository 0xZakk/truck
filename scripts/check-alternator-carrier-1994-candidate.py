#!/usr/bin/env python3
"""Read-only full installed-neighbor audit of an independent ALT candidate."""
import argparse, hashlib, json, sys, tempfile
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import alternator_carrier_1994_candidate as candidate
from assembly_math import transforms

parser=argparse.ArgumentParser();parser.add_argument('--assembly-root',type=Path,required=True)
parser.add_argument('--installed',action='store_true',help='Audit saved candidate placement instead of constructing relocation')
args=parser.parse_args();assembly=args.assembly_root
manifest_path=assembly/'inventory/engine/full-assembly.json'
raw=manifest_path.read_bytes();manifest=json.loads(raw)
poses=transforms(manifest);defs={x['id']:x for x in manifest['definitions']}
fixed={};moved={};cache={};hashes={};overlaps=[];checks=0;installed_checks=[]
replacements=candidate.replacements()
for o in manifest['occurrences']:
    identifier=o['id'];definition=o['definition']
    if definition not in cache:
        path=assembly/defs[definition]['step'].lstrip('/')
        hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        cache[definition]=cad.import_step(path)
    shape=cache[definition].moved(poses[identifier])
    if identifier in replacements:
        if args.installed:
            expected=replacements[identifier]
            def difference(a,b):
                diff=a-b
                return sum(x.volume for x in diff.solids()) if diff else 0
            delta=difference(shape,expected)+difference(expected,shape)
            assert delta<.01,(identifier,'saved shape differs',delta)
            moved[identifier]=shape;installed_checks.append(identifier)
        else:moved[identifier]=replacements[identifier]
    elif o['parent']=='alternator-assembly':
        if args.installed:
            expected=cad.Pos(*candidate.POSITION)*cad.Rot(0,90,0)
            actual=poses[identifier]
            error=max(abs(actual.wrapped.Transformation().Value(i,j)-expected.wrapped.Transformation().Value(i,j)) for i in range(1,4) for j in range(1,5))
            assert error<1e-6,(identifier,'saved transform differs',error)
            moved[identifier]=shape;installed_checks.append(identifier)
        else:moved[identifier]=cad.Pos(*candidate.DISPLACEMENT)*shape
    else:fixed[identifier]=shape
print('Loaded',len(moved),'candidate parts and',len(fixed),'neighbors',flush=True)
roundtrips=[]
with tempfile.TemporaryDirectory(prefix='truck-alt94-') as tmp:
    for identifier,shape in moved.items():
        assert shape.is_valid and len(shape.solids())==1,identifier
        path=Path(tmp)/(identifier+'.step');cad.export_step(shape,path);restored=cad.import_step(path)
        assert restored.is_valid and len(restored.solids())==1
        assert abs(restored.volume-shape.volume)<max(.01,shape.volume*1e-6)
        roundtrips.append(identifier)
boxes={k:v.bounding_box() for k,v in {**fixed,**moved}.items()}
def check(a,b,sa,sb):
    global checks
    ba,bb=boxes[a],boxes[b]
    if any(min(getattr(ba.max,v),getattr(bb.max,v))-max(getattr(ba.min,v),getattr(bb.min,v))<=.01 for v in 'XYZ'):return
    checks+=1;inter=sa.intersect(sb);volume=sum(s.volume for s in inter.solids()) if inter else 0
    if volume>.01:
        overlaps.append({'a':a,'b':b,'volume_mm3':volume});print('OVERLAP',overlaps[-1],flush=True)
for a,sa in moved.items():
    for b,sb in fixed.items():check(a,b,sa,sb)
keys=list(moved)
for i,a in enumerate(keys):
    for b in keys[i+1:]:check(a,b,moved[a],moved[b])
joints=[]
for target in ('block','cylinder-head','alt-engine-bracket-bolt-1','alt-engine-bracket-bolt-2'):
    if target not in fixed:continue
    distance=moved['alternator-support-bracket'].distance_to(fixed[target]);joints.append({'part':target,'distance_mm':distance})
assert manifest_path.read_bytes()==raw
for path,digest in hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest
report={'status':'rejected' if overlaps else ('installed-static-pass' if args.installed else 'static-candidate-ready-for-visual-qc'),'production_fit':False,
 'assembly_root':str(assembly),'manifest_sha256':hashlib.sha256(raw).hexdigest(),
 'candidate_sha256':hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
 'position':candidate.POSITION,'displacement':candidate.DISPLACEMENT,'limits':candidate.GAPS,
 'changed_parts':sorted(moved),'step_roundtrips':roundtrips,'exact_intersection_checks':checks,
 'overlaps':overlaps,'joint_distances':joints,'input_step_sha256':hashes,'installed_geometry_pose_checks':installed_checks}
out=(assembly if args.installed else ROOT)/('inventory/engine/alternator-carrier-1994-installed-validation.json' if args.installed else 'inventory/engine/alternator-carrier-1994-candidate-validation.json')
out.write_text(json.dumps(report,indent=2)+'\n');print('RESULT',report['status'],checks,len(overlaps),joints,flush=True)
