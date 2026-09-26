"""Sampled rotating-neighbor and exploded-joint clearance; not continuous sweep proof."""
from pathlib import Path
import hashlib,json,sys,itertools,math
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import oil_pan_joint_candidate as p
from assembly_math import transforms
from explode_stages_candidate import explode_offset,pan_hardware_stages
paths=[Path(__file__),ROOT/'cad/engine/explode_stages_candidate.py',ROOT/'viewer/engine-explode-stages-candidate.js',Path(p.__file__),ROOT/'cad/engine/oil_pan_fasteners.py',ROOT/'cad/engine/assembly_math.py',ROOT/'inventory/engine/full-assembly.json']
hashes={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths}
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};cache={};step_hashes={}
def load(key):
    if key not in cache:
        path=ROOT/defs[key]['step'].lstrip('/');step_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();cache[key]=b.import_step(path)
    return cache[key]
def vol(s):return sum(q.volume for q in s.solids()) if s else 0
def broad(a,c):
    return all(min(getattr(a.max,k),getattr(c.max,k))-max(getattr(a.min,k),getattr(c.min,k))>.001 for k in 'XYZ')
pan=b.Pos(0,-12,-96)*p.pan_interface(load('oil-pan'));pb=pan.bounding_box(optimal=False)
active={a['id'] for a in m['assemblies'] if a.get('motion')}
while True:
    expanded=active|{a['id'] for a in m['assemblies'] if a['parent'] in active}
    if expanded==active:break
    active=expanded
moving=[o for o in m['occurrences'] if o['parent'] in active]
checks=0;failures=[];distance_fallbacks=[]; envelope_fallbacks=[]; envelope_clearances=[]
for angle in range(0,721,30):
    poses=transforms(m,angle)
    for o in moving:
        s=poses[o['id']]*load(o['definition'])
        if broad(pb,s.bounding_box(optimal=False)):
            checks+=1;v=vol(pan&s)
            if v>.1:failures.append({'kind':'rotating','degrees':angle,'part':o['id'],'mm3':v})
    print('Motion phase',angle,'checks',checks,flush=True)
screw,washer=p.screw_shape(),p.washer_shape();gasket=p.gasket_shape()
stock=p.cylinder(p.DIAMETER/2,0,p.LENGTH)+(b.Pos(0,0,-5.3)*b.extrude(b.RegularPolygon(12.7/math.sqrt(3),6),amount=5.3))
exploded_checks=0
fractions=(0,.1,.25,.34,.35,.36,.5,.59,.6,.61,.75,1)
for alpha in fractions:
    envelopes={}
    positioned={'pan':b.Pos(0,0,-320*alpha)*pan,'gasket':b.Pos(0,0,-210*alpha)*gasket}
    for n,(x,y,z) in enumerate(p.STATIONS,1):
        dx=(25 if x>0 else -25) if n>20 else 0;dy=(25 if y>0 else -25) if n<=20 else 0
        for role,s,dz in [('screw',screw,-360),('washer',washer,-340)]:
            offset=explode_offset({'explode_stages':pan_hardware_stages((dx,dy,dz))},alpha)
            positioned[f'{role}-{n}']=b.Pos(x+offset[0],y+offset[1],z+offset[2])*s
    for n,(x,y,z) in enumerate(p.STATIONS,1):
        dx=(25 if x>0 else -25) if n>20 else 0;dy=(25 if y>0 else -25) if n<=20 else 0
        # screw_shape only SUBTRACTS the thread cutter from this stock.
        # Therefore this enclosure is a rigorous superset, not a collision exception.
        offset=explode_offset({'explode_stages':pan_hardware_stages((dx,dy,-360))},alpha)
        envelopes[f'screw-{n}']=b.Pos(x+offset[0],y+offset[1],z+offset[2])*stock
    bounds={key:s.bounding_box(optimal=False) for key,s in positioned.items()}
    for (a,s),(c,t) in itertools.combinations(positioned.items(),2):
        if broad(bounds[a],bounds[c]):
            exploded_checks+=1
            if a in envelopes or c in envelopes:
                envelope_volume=vol(envelopes.get(a,s)&envelopes.get(c,t))
                if envelope_volume<1e-8:
                    envelope_clearances.append({'fraction':alpha,'a':a,'b':c,'stock_superset_intersection_mm3':envelope_volume})
                    continue
            try:v=vol(s&t)
            except ValueError as error:
                distance=s.distance_to(t)
                print('Intersection fallback',alpha,a,c,'distance',distance,flush=True)
                if distance<=1e-6:
                    if a not in envelopes and c not in envelopes:raise
                    envelope_volume=vol(envelopes.get(a,s)&envelopes.get(c,t))
                    if envelope_volume>1e-6:raise
                    envelope_fallbacks.append({'fraction':alpha,'a':a,'b':c,'superset_intersection_mm3':envelope_volume,'error':str(error)})
                distance_fallbacks.append({'fraction':alpha,'a':a,'b':c,'exact_distance_mm':distance,'error':str(error)})
                v=0
            if v>.1:failures.append({'kind':'exploded','fraction':alpha,'a':a,'b':c,'mm3':v})
    print('Exploded fraction',alpha,'checks',exploded_checks,flush=True)
unchanged=all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in dict(hashes,**step_hashes).items())
result={'input_hashes':hashes,'step_hashes':step_hashes,'inputs_unchanged':unchanged,'sampled_crank_degrees':list(range(0,721,30)),'rotating_neighbor_checks':checks,'exploded_fractions':list(fractions),'exploded_pair_checks':exploded_checks,'wrapper_null_intersections':distance_fallbacks,'stock_enclosure_verified_empty_intersections':envelope_fallbacks,'conservative_stock_clearances':envelope_clearances,'failures':failures,'scope':'25 sampled crank phases and12staged exploded poses; no continuous swept-volume or production-fit proof. Starter engagement and independent compressor controls are outside this pan-specific audit.'}
(ROOT/'inventory/engine/oil-pan-joint-staged-motion-validation.json').write_text(json.dumps(result,indent=2)+'\n')
assert unchanged and not failures,result
print('PASS pan sampled motion/explosion')
