"""Negative controls show the seal void test detects missing secondary/face seals."""
from pathlib import Path
import sys,hashlib,json
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_mechanical_seal_candidate as s
from water_pump_joint_candidate import cx
BASE=Path('/private/tmp/truck-seal-inlet-baseline-2032a3da')
paths=[Path(__file__),Path(s.__file__),ROOT/'cad/engine/water_pump_joint_candidate.py',BASE/'water-pump-housing.step',BASE/'water-pump-shaft.step',BASE/'full-assembly.json'];hashes={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths}
housing=b.import_step(BASE/'water-pump-housing.step');shaft=b.import_step(BASE/'water-pump-shaft.step');parts=s.components();wet=b.Pos(10.5,20,0)*b.Sphere(.1);dry=b.Pos(21.5,8.5,0)*b.Sphere(.1)
def vol(q):return sum(v.volume for v in q.solids()) if q else 0
def compound(q):return b.Compound(children=list(q)) if isinstance(q,b.ShapeList) else q
def connected(parts):
 void=cx(30,10,22)-housing-shaft
 for part in parts.values():void=compound(void)-part
 solids=compound(void).solids();w=[i for i,v in enumerate(solids) if vol(v&wet)>.004];d=[i for i,v in enumerate(solids) if vol(v&dry)>.004];assert len(w)==len(d)==1,(w,d)
 return w==d
results={'intact_connected':connected(parts),'missing_bellows_connected':connected({k:v for k,v in parts.items() if k!='water-pump-seal-bellows'}),'face_gap_connected':connected({k:(b.Pos(-.1,0,0)*v if k=='water-pump-seal-rotating-face' else v) for k,v in parts.items()})}
assert results=={'intact_connected':False,'missing_bellows_connected':True,'face_gap_connected':True},results
assert all(hashlib.sha256(Path(q).read_bytes()).hexdigest()==h for q,h in hashes.items());(ROOT/'inventory/engine/water-pump-seal-leak-controls-validation.json').write_text(json.dumps({'status':'PASS','input_hashes':hashes,'results':results,'scope':'Ideal zero-gap geometric fluid connectivity only, not hydraulic performance.'},indent=2)+'\n');print(results)
