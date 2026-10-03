from pathlib import Path
import sys,json,hashlib,time
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_cover_candidate_20261003 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();c.O.mkdir(exist_ok=True)
r={'status':'RUNNING','parts':{},'regions':{},'block_features':{},'inputs':{}};rp=R/'reference/engine/pump-cover-candidate-20261003-build.json'
def save():rp.write_text(json.dumps(r,indent=2)+'\n')
def write(n,s,key):
 p=c.O/((''if key=='parts'else key+'-')+n+'.step');b.export_step(s,p);q=b.import_step(p);r[key][n]={'path':str(p.relative_to(R)),'sha256':sha(p),'valid':q.is_valid,'solids':len(q.solids()),'bounds':[list(q.bounding_box().min),list(q.bounding_box().max)]};save();print(key,n,len(q.solids()),q.is_valid,flush=True)
if '--housing-only' in sys.argv:
 r=json.loads(rp.read_text());g=c.gasket_oldframe();regions=c.regions_oldframe(g);write('water-pump-housing',c.T*c.housing(g,regions),'parts');r['inputs'][str(Path(c.__file__).relative_to(R))]=sha(Path(c.__file__));r['inputs'][str(Path(__file__).relative_to(R))]=sha(Path(__file__));r['revision']='sequential own-cavity construction; trial1 preserved';r['status']='EXPORTED revision2; dependent housingchecks stale until rerun';save();print('HOUSING DONE',flush=True);sys.exit()
print('PUMP BUILD START',flush=True);save();parts,regions=c.pump_parts()
for n,s in parts.items():write(n,s,'parts')
for n,s in regions.items():write(n,s,'regions')
print('BLOCK BUILD START',flush=True);block,features=c.block_parts();write('block',block,'parts')
for n,s in features.items():write(n,s,'block_features')
for p in [Path(__file__),Path(c.__file__),R/'docs/components/pump-cover-candidate-20261003-contract.md',c.MP,R/'reference/engine/pump-cover-joint-20261003-delivery.json',R/'reference/engine/pump-cover-joint-20261003-datums.json',R/'reference/engine/pump-functional-20261003-build.json']:r['inputs'][str(p.relative_to(R))]=sha(p)
r['status']='EXPORTED; named checks pending';save();print('DONE',flush=True)
