"""Fail-closed independent layout experiment; never writes installed geometry."""
import hashlib,json,sys,tempfile
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_layout_candidate as candidate
import accessory_belt as base
from assembly_math import transforms

raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();manifest=json.loads(raw)
poses=transforms(manifest);defs={d['id']:d for d in manifest['definitions']}
source_paths=[Path(candidate.__file__),Path(base.__file__),ROOT/'cad/engine/accessory_belt_profile.py']
frozen={str(p.relative_to(ROOT)):p.read_bytes() for p in source_paths}
parents={a['id']:a['parent'] for a in manifest['assemblies']}

def assembly(occurrence):
    p=occurrence['parent']
    while p:
        if candidate.displacement(p,1):return p
        p=parents.get(p)
    return None

report=candidate.diagnosis();shift=report['candidate_shift_mm']
assert report['full_circle_3600_sample_minimum_mm']>=report['tensioner_removed_relaxed_route_length_mm']-1e-6
assert report['relaxed_route_residual_mm']>270
assert abs(base.solve(candidate.stations(shift),False)['length']-2491)<1e-6
# Negative control: retaining the original stations cannot pass nominal length.
assert abs(base.solve(candidate.stations(0),False)['length']-2491)>290
cache={};fixed={};moved={};support_ids=set()
for o in manifest['occurrences']:
    d=o['definition']
    if d not in cache:cache[d]=cad.import_step(ROOT/defs[d]['step'].lstrip('/'))
    shape=cache[d].moved(poses[o['id']]);group=assembly(o)
    if group:moved[o['id']]=cad.Pos(*candidate.displacement(group,shift))*shape
    else:fixed[o['id']]=shape
    if o['parent']=='accessory-support-brackets':support_ids.add(o['id'])
print('Loaded',len(moved),'moving bodies and',len(fixed),'fixed bodies',flush=True)
# These are exact imported-body checks: current groove mismatch is left visible.
# No normalization or assembly writes can accidentally improve the experiment.
moved['candidate-belt']=candidate.belt_shape(shift)
step_checks=[]
with tempfile.TemporaryDirectory(prefix='truck-layout-') as tmp:
    shape=moved['candidate-belt'];assert shape.is_valid and len(shape.solids())==1
    p=Path(tmp)/'belt.step';cad.export_step(shape,p);restored=cad.import_step(p)
    assert restored.is_valid and len(restored.solids())==1
    assert abs(restored.volume-shape.volume)<max(.01,shape.volume*1e-6)
    step_checks.append('candidate-belt')
checks=0;hits=[];boxes={k:v.bounding_box() for k,v in {**fixed,**moved}.items()}

def check(a,b,sa,sb):
    global checks
    ba,bb=boxes[a],boxes[b]
    if any(min(getattr(ba.max,v),getattr(bb.max,v))-max(getattr(ba.min,v),getattr(bb.min,v))<=.01 for v in 'XYZ'):return
    checks+=1;inter=sa.intersect(sb);volume=sum(s.volume for s in inter.solids()) if inter else 0
    if volume>.01:
        hit={'a':a,'b':b,'volume_mm3':volume,'known_support_redesign':a in support_ids or b in support_ids}
        hits.append(hit);print('Overlap',hit,flush=True)

for a,sa in moved.items():
    for b,sb in fixed.items():check(a,b,sa,sb)
# Bodies within a rigidly translated assembly were already checked installed;
# compare different relocated groups and the new belt, not just neighbors.
occ={o['id']:o for o in manifest['occurrences']}
keys=list(moved)
for i,a in enumerate(keys):
    for b in keys[i+1:]:
        if a in occ and b in occ and assembly(occ[a])==assembly(occ[b]):continue
        check(a,b,moved[a],moved[b])
assert (ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw,'Manifest changed during experiment'
for path,contents in frozen.items():assert (ROOT/path).read_bytes()==contents
report.update({
    'manifest_sha256':hashlib.sha256(raw).hexdigest(),
    'source_sha256':{p:hashlib.sha256(v).hexdigest() for p,v in frozen.items()},
    'candidate_status':'rejected' if hits else 'unverified-support-redesign-required',
    'verified_production_fit':False,'ready_to_install':False,
    'candidate_outside_radius_length_mm':base.solve(candidate.stations(shift),False)['length'],
    'candidate_cord_path_length_mm':base.solve(candidate.stations(shift))['length'],
    'moved_components':len(moved)-1,'exact_intersection_checks':checks,
    'step_round_trip_checks':step_checks,'overlaps':hits,
    'support_redesign_required_even_without_overlap':sorted(support_ids),
    'geometry_limits':'Original grooves are unnormalized: belt-to-pulley hits are retained, not waived. Zero overlaps alone would not establish installed fit.',
})
out=ROOT/'inventory/engine/accessory-layout-diagnosis.json';out.write_text(json.dumps(report,indent=2)+'\n')
print('Report',out,report['candidate_status'],'checks',checks,'overlaps',len(hits),flush=True)
