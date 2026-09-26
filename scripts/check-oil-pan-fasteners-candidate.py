"""Independent source-counted pan hardware fit study, not production validation."""
from pathlib import Path
import hashlib,json,sys,tempfile,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
frozen_paths=[ROOT/'cad/engine/oil_pan_fasteners.py',Path(__file__),ROOT/'reference/engine/ford-oil-pan-hardware-reviewed.json',ROOT/'cad/engine/assembly_math.py']
frozen_hashes={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in frozen_paths}
import oil_pan_fasteners as p
from assembly_math import transforms
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw)
loc=transforms(m)
defs={d['id']:d for d in m['definitions']}
occ={o['id']:o for o in m['occurrences']}
cache={}
step_hashes={}
installed='--installed' in sys.argv
def original(key):
    ident=occ[key]['definition']
    if ident not in cache:
        path=ROOT/defs[ident]['step'].lstrip('/')
        step_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        cache[ident]=b.import_step(path)
    return loc[key]*cache[ident]
def volume(s):return sum(x.volume for x in s.solids()) if s else 0

def overlaps(a,c):
    ab,cb=a.bounding_box(),c.bounding_box()
    return all(min(getattr(ab.max,k),getattr(cb.max,k))-max(getattr(ab.min,k),getattr(cb.min,k))>.001 for k in 'XYZ')

screw,washer=p.screw_shape(),p.washer_shape()
oldblock=original('block')
changed={'block':oldblock if installed else p.block_interface(oldblock)}
for key in ['oil-pan','pan-side-gasket-1','pan-side-gasket-2']:
    shape=original(key)
    if not installed:
        for x,y in p.STATIONS:shape-=b.Pos(x,y)*p.cylinder(4.3,-40,-30)
    changed[key]=shape
parts={}
for n,(x,y) in enumerate(p.STATIONS,1):
    for role,shape in [('screw',screw),('washer',washer)]:
        key=f'oil-pan-mounting-{role}-{n}'
        parts[key]=original(key) if installed else b.Pos(x,y,p.UNDER_HEAD_Z)*shape
        if installed:
            expected=b.Pos(x,y,p.UNDER_HEAD_Z)*shape
            assert volume(parts[key]-expected)+volume(expected-parts[key])<.02,key
assert len(parts)==50
print('Candidate construction complete',flush=True)
with tempfile.TemporaryDirectory(prefix='pan-fastener-step-') as directory:
    for key,s in dict(screw=screw,washer=washer,**changed).items():
        assert s.is_valid and len(s.solids())==1,(key,s.is_valid,len(s.solids()))
        file=Path(directory)/(key+'.step');b.export_step(s,file);r=b.import_step(file)
        assert r.is_valid and len(r.solids())==1,key
        assert abs(r.volume-s.volume)<.02,(key,r.volume-s.volume)
print('Six single-solid STEP roundtrips PASS',flush=True)
contacts=[]
for n,(x,y) in enumerate(p.STATIONS,1):
    bolt=parts[f'oil-pan-mounting-screw-{n}'];ring=parts[f'oil-pan-mounting-washer-{n}']
    assert bolt.distance_to(ring)<1e-6
    assert ring.distance_to(changed['oil-pan'])<1e-6
    # Positive contact-area controls on flange and pad, plus bore-bottom wall.
    patch=b.Pos(x,y)*p.cylinder(7.4,-38,-37.9)-b.Pos(x,y)*p.cylinder(4.4,-38.1,-37.8)
    bearing_area=volume(patch & changed['oil-pan'])/.1
    assert bearing_area>60,(n,bearing_area)
    bore=b.Pos(x,y)*p.cylinder(4.05,-31.9,-17)
    assert volume(bore & changed['block'])<.001,n
    floor=b.Pos(x,y)*p.cylinder(3.9,-16.4,-16.3)
    assert abs(volume(floor & changed['block'])-floor.volume)<.001,n
    assert volume(bolt & changed['block'])<.001,n
    contacts.append({'station':n,'pan_bearing_area_mm2':bearing_area})
print('All25 seating pairs, open sockets and blind floor controls PASS',flush=True)
# The original block is unchanged except these dry pads/socket drillings.
subjects=dict(parts)
if not installed:
    print('Computing added block material',flush=True)
    added=changed['block']-oldblock
    if isinstance(added,b.ShapeList):added=b.Compound(children=list(added))
    subjects['block-added-material']=added
    print('Added block material computed',flush=True)
checks=0;collisions=[]
for index,key in enumerate(occ):
    if index%50==0:print(f'Neighbor sweep {index}/{len(occ)}; exact checks {checks}',flush=True)
    if key in parts:continue
    neighbor=changed.get(key)
    if neighbor is None:neighbor=original(key)
    for ident,shape in subjects.items():
        if ident=='block-added-material' and key=='block':continue
        if not overlaps(shape,neighbor):continue
        checks+=1;v=volume(shape & neighbor)
        if v>.1:collisions.append({'a':ident,'b':key,'mm3':v})
for (a,s),(c,t) in itertools.combinations(parts.items(),2):
    if overlaps(s,t):
        checks+=1;v=volume(s&t)
        if v>.1:collisions.append({'a':a,'b':c,'mm3':v})
assert all(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest for path,digest in frozen_hashes.items()),'Audit source changed'
report={'input_source_hashes':frozen_hashes,'manifest_sha256':hashlib.sha256(raw).hexdigest(),
 'module_sha256':hashlib.sha256((ROOT/'cad/engine/oil_pan_fasteners.py').read_bytes()).hexdigest(),
 'source_sha256':hashlib.sha256((ROOT/'reference/engine/ford-oil-pan-hardware-reviewed.json').read_bytes()).hexdigest(),
 'source_supported':{'screw_washer_assembly_count':25,'thread_diameter_mm':p.DIAMETER,'pitch_mm':p.PITCH,'nominal_length_mm':p.LENGTH},
 'installed':installed,'candidate_occurrences':len(parts),'step_roundtrips':6,'stations':p.STATIONS,'seating_controls':contacts,
 'neighbor_intersections':checks,'collisions':collisions,'manifest_unchanged':(ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw,
 'production_fit_verified':False,'limitations':p.GAPS}
report['step_hashes']=step_hashes
report['step_inputs_unchanged']=all(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest for path,digest in step_hashes.items())
report_name='oil-pan-fasteners-installed-validation.json' if installed else 'oil-pan-fasteners-candidate-validation.json'
(ROOT/'inventory/engine'/report_name).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
assert report['manifest_unchanged'] and report['step_inputs_unchanged'],'Assembly changed during audit'
assert not collisions,collisions
print('PASS isolated pan fastening candidate',flush=True)
