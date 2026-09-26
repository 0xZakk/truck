"""Fail-closed independent layout experiment; never writes installed geometry."""
import hashlib,json,sys,tempfile
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_layout_evidence as candidate
import accessory_belt_profile as profile
import accessory_belt as base
from assembly_math import transforms

raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();manifest=json.loads(raw)
poses=transforms(manifest);defs={d['id']:d for d in manifest['definitions']}
source_paths=[Path(candidate.__file__),Path(base.__file__),ROOT/'cad/engine/accessory_belt_profile.py',Path(__file__)]
frozen={str(p.relative_to(ROOT)):p.read_bytes() for p in source_paths}
parents={a['id']:a['parent'] for a in manifest['assemblies']}

def assembly(occurrence):
    p=occurrence['parent']
    while p:
        if p in candidate.GROUPS:return candidate.GROUPS[p]
        p=parents.get(p)
    return None

shift=candidate.matched_ac_up();shifts=candidate.shifts(shift)
solution=base.solve(candidate.stations(shift),False)
assert solution['length']<base.solve(cord_path=False)['length']-100
centers={n['id']:n['center'] for n in candidate.stations(shift)}
assert centers['PS'][1]>centers['TENS'][1]>centers['ALT'][1]>centers['WP'][1]>centers['AC'][1]
assert centers['TENS'][0]>centers['WP'][0]
assert abs(sum(-a['side']*a['wrap_degrees'] for a in solution['arcs'])+360)<1e-6
report={'displacements_yz_mm':shifts,'candidate_routing':solution,'limits':candidate.LIMITS,
        'search_method':'10 mm grid, ±120 mm station range; moving mesh bounds checked against fixed engine excluding support brackets, then valid winding/pulley separation/moving-body constraints. Qualitative source ordering imposed; A/C held below water-pump center. Nominal-length fit deliberately unresolved; all dimensions unverified.'}
cache={};fixed={};moved={};support_ids=set()
for o in manifest['occurrences']:
    d=o['definition']
    if d not in cache:cache[d]=cad.import_step(ROOT/defs[d]['step'].lstrip('/'))
    shape=profile.normalize_definition(d,cache[d]).moved(poses[o['id']]);group=assembly(o)
    if group:moved[o['id']]=cad.Pos(0,*shifts[group])*shape
    else:fixed[o['id']]=shape
    if o['parent']=='accessory-support-brackets':support_ids.add(o['id'])
print('Loaded',len(moved),'moving bodies and',len(fixed),'fixed bodies',flush=True)
# These are exact imported-body checks: current groove mismatch is left visible.
# No normalization or assembly writes can accidentally improve the experiment.
moved['candidate-belt']=candidate.belt_shape()
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
        if a in occ and b in occ and assembly(occ[a])==assembly(occ[b]) and 'pulley' not in a and 'pulley' not in b:continue
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
    'geometry_limits':'Five pulley grooves use the existing PK normalization adapter locally. Existing supports stay in place and collisions are recorded; zero overlaps alone would not establish installed fit.',
})
out=ROOT/'inventory/engine/accessory-layout-evidence-validation.json';out.write_text(json.dumps(report,indent=2)+'\n')
print('Report',out,report['candidate_status'],'checks',checks,'overlaps',len(hits),flush=True)
