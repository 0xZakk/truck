"""Check published side-cover and cam-retention interfaces, including gear motion."""
from pathlib import Path
import json,sys,itertools,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms

path=ROOT/'inventory/engine/full-assembly.json';raw=path.read_bytes();m=json.loads(raw)
defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
pose=transforms(m);cache={}
def placed(id,loc=pose):
    key=occ[id]['definition']
    if key not in cache:cache[key]=b.import_step(ROOT/defs[key]['step'].lstrip('/'))
    return cache[key].moved(loc[id])

collisions=[];checks=0
def check(a,sa,c,sc,angle=0):
    global checks
    checks+=1
    ba,bc=sa.bounding_box(),sc.bounding_box()
    if any(getattr(ba.max,k)<=getattr(bc.min,k) or getattr(bc.max,k)<=getattr(ba.min,k) for k in ['X','Y','Z']):return
    v=sa.intersect(sc);volume=sum(t.volume for t in v.solids()) if v else 0
    if volume>.01:collisions.append({'a':a,'b':c,'crank_angle_deg':angle,'volume_mm3':volume})

side=[id for id,o in occ.items() if o['parent']=='pushrod-cover-assembly']
fixed=[id for id,o in occ.items() if o['parent']=='cam-retention-assembly']
cam=fixed+['cam-gear-spacer','cam-timing-key']
assert len(side)==14 and len(fixed)==5 and len(cam)==7
for branch in [side,cam]:
    for a,c in itertools.combinations(branch,2):check(a,placed(a),c,placed(c))
    for a in branch:check(a,placed(a),'block',placed('block'))
for a in side:
    for c in ['cylinder-head','distributor-housing','oil-filter-case','oil-pressure-body']:
        check(a,placed(a),c,placed(c))
for a in cam:
    for c in ['camshaft','cam-timing-gear','timing-cover']:
        check(a,placed(a),c,placed(c))
rockers=[id for id,o in occ.items() if o['definition']=='rocker-arm']
assert len(rockers)==12
for id in rockers:check(id,placed(id),'valve-cover',placed('valve-cover'))
rear_plug=placed('rear-cam-plug')
for id in occ:
    if id!='rear-cam-plug':check('rear-cam-plug',rear_plug,id,placed(id))
angles=list(range(0,720,90))
for angle in angles:
    loc=transforms(m,angle)
    check('camshaft',placed('camshaft',loc),'rear-cam-plug',rear_plug,angle)
    for id in fixed:check('cam-timing-gear',placed('cam-timing-gear',loc),id,placed(id,loc),angle)
    for id in ['cam-timing-gear','crank-timing-gear']:
        check(id,placed(id,loc),'timing-cover',placed('timing-cover',loc),angle)
    print('Cam retention checked at crank angle',angle,flush=True)
assert path.read_bytes()==raw,'Manifest changed during verification'
report={'manifest_sha256':hashlib.sha256(raw).hexdigest(),'side_cover_occurrences':len(side),
        'cam_retention_occurrences':len(cam),'crank_angles_deg':angles,'interface_checks':checks,
        'collisions':collisions,'verified_production_fit':False,
        'limits':'Published STEP geometry, selected static interfaces and eight gear-to-retainer samples. No continuous motion, seal compression, thread engagement adequacy or production fit certification.'}
(ROOT/'inventory/engine/retention-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));assert not collisions,collisions
