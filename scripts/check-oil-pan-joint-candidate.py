"""Frozen isolated oil-pan matched-joint checker; no production-fit claim."""
from pathlib import Path
import hashlib,json,sys,tempfile,itertools
from contextlib import nullcontext
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
paths=[Path(__file__),ROOT/'cad/engine/oil_pan_joint_candidate.py',ROOT/'cad/engine/oil_pan_fasteners.py',ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'reference/engine/felpro-os34601r-topology-reviewed.json']
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
import oil_pan_joint_candidate as p
from assembly_math import transforms
from cad_metrics import solid_volume
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);loc=transforms(m)
defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};cache={};step_hashes={};bbox_cache={}
def original(key):
    ident=occ[key]['definition']
    if ident not in cache:
        path=ROOT/defs[ident]['step'].lstrip('/');step_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();cache[ident]=b.import_step(path)
    return loc[key]*cache[ident]
def volume(s):return sum(q.volume for q in s.solids()) if s else 0
def bbox(s):
    if id(s) not in bbox_cache:bbox_cache[id(s)]=(s,s.bounding_box(optimal=False))
    return bbox_cache[id(s)][1]
def broad(a,c):
    ab,cb=bbox(a),bbox(c)
    return all(min(getattr(ab.max,k),getattr(cb.max,k))-max(getattr(ab.min,k),getattr(cb.min,k))>.001 for k in 'XYZ')
print('Building gasket and hardware',flush=True)
gasket=p.gasket_shape();screw=p.screw_shape();washer=p.washer_shape()
print('Building pan interface',flush=True)
oldpan=original('oil-pan');pan=b.Pos(0,-12,-96)*p.pan_interface(b.Pos(0,12,96)*oldpan)
print('Building block interface',flush=True)
oldblock=original('block');block=p.block_interface(oldblock)
changed={'block':block,'oil-pan':pan,'oil-pan-molded-gasket':gasket}
parts={}
for n,(x,y,z) in enumerate(p.STATIONS,1):
    for role,s in [('screw',screw),('washer',washer)]:parts[f'oil-pan-mounting-{role}-{n}']=b.Pos(x,y,z)*s
print('Candidate construction complete',flush=True)
directory='/private/tmp/truck-pan-joint-candidate-step'
Path(directory).mkdir(exist_ok=True)
with nullcontext(directory) as directory:
    for key,s in dict(screw=screw,washer=washer,**changed).items():
        assert s.is_valid and len(s.solids())==1,(key,s.is_valid,len(s.solids()))
        path=Path(directory)/(key+'.step');b.export_step(s,path);r=b.import_step(path)
        delta=solid_volume(r,'adaptive')-solid_volume(s,'adaptive')
        print('STEP',key,'adaptive volume delta',delta,flush=True)
        assert r.is_valid and len(r.solids())==1 and abs(delta)<.02,(key,r.is_valid,len(r.solids()),delta)
print('Five STEP roundtrips PASS',flush=True)
assert screw.distance_to(washer)<1e-6
contacts=[]
for n,(x,y,z) in enumerate(p.STATIONS,1):
    patch=b.Pos(x,y)*p.cylinder(7.4,z+1.6,z+1.7)-b.Pos(x,y)*p.cylinder(4.4,z+1.5,z+1.8)
    area=volume(patch&pan)/.1;assert area>60,(n,area)
    probe=b.Pos(x,y)*p.cylinder(4.05,z+7.7,z+p.LENGTH+.5)
    assert volume(probe&block)<.001,n
    floor=b.Pos(x,y)*p.cylinder(3.9,z+p.LENGTH+1.1,z+p.LENGTH+1.2)
    assert abs(volume(floor&block)-floor.volume)<.001,n
    contacts.append({'station':n,'pan_bearing_area_mm2':area})
print('25 flange/bore/floor controls PASS',flush=True)
# Test altered parts and hardware against each other, then all unchanged neighbors.
subjects=dict(changed,**parts);checks=0;collisions=[]
for (a,s),(c,t) in itertools.combinations(subjects.items(),2):
    if broad(s,t):
        checks+=1;v=volume(s&t)
        if v>.1:collisions.append({'a':a,'b':c,'mm3':v})
print('Changed-part pair checks finished',collisions,flush=True)
for index,key in enumerate(occ):
    if key in ('block','oil-pan','pan-side-gasket-1','pan-side-gasket-2'):continue
    if index%50==0:print(f'Neighbors {index}/{len(occ)}; exact checks {checks}',flush=True)
    neighbor=original(key)
    for ident,s in subjects.items():
        if broad(s,neighbor):
            checks+=1;v=volume(s&neighbor)
            if v>.1:collisions.append({'a':ident,'b':key,'mm3':v})
unchanged=(ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw and all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in dict(hashes,**step_hashes).items())
report={'manifest_sha256':hashlib.sha256(raw).hexdigest(),'input_hashes':hashes,'step_hashes':step_hashes,'inputs_unchanged':unchanged,'source_count':25,'topology':'10+10 side holes;3+2 end holes','step_roundtrips':5,'step_volume_method':'cad_metrics.solid_volume adaptive, tolerance0.02mm3','seating_controls':contacts,'neighbor_intersections':checks,'collisions':collisions,'production_fit_verified':False,'limits':p.GAPS}
(ROOT/'inventory/engine/oil-pan-joint-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert unchanged,'Inputs changed during audit'
assert not collisions,collisions
print('PASS matched oil-pan joint candidate',flush=True)
