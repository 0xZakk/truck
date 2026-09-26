"""Check two integral flange candidates against a frozen saved engine."""
from pathlib import Path
import argparse,hashlib,itertools,json,sys,tempfile
import build123d as cad
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import exhaust_outlet_flanges_desktop as flange
from assembly_math import transforms
from cad_metrics import solid_volume
parser=argparse.ArgumentParser();parser.add_argument('--assembly-root',type=Path,default=ROOT)
parser.add_argument('--installed',action='store_true')
args=parser.parse_args();model_root=args.assembly_root
path=model_root/'inventory/engine/full-assembly.json';raw=path.read_bytes();manifest=json.loads(raw)
hashes={Path(flange.__file__):hashlib.sha256(Path(flange.__file__).read_bytes()).hexdigest()}
definitions={}
for definition in manifest['definitions']:
    step=model_root/definition['step'].lstrip('/');hashes[step]=hashlib.sha256(step.read_bytes()).hexdigest()
    definitions[definition['id']]=cad.import_step(step)
poses=transforms(manifest)
shapes={p['id']:poses[p['id']]*definitions[p['definition']] for p in manifest['occurrences']}
def volume(shape):return sum(solid_volume(s,'adaptive') for s in shape.solids()) if shape else 0
def overlap(a,b):return volume(a.intersect(b))
candidate={};roundtrips=[];directory=ROOT/'cad/engine/candidates/exhaust-outlet-flanges-desktop';directory.mkdir(parents=True,exist_ok=True)
for identifier,adapter in flange.ADAPTERS.items():
    shape=adapter(definitions[identifier]);assert shape.is_valid and len(shape.solids())==1,identifier
    step=directory/(identifier+'.step');cad.export_step(shape,step);restored=cad.import_step(step)
    delta=volume(restored)-volume(shape);assert restored.is_valid and len(restored.solids())==1 and abs(delta)<.01,(identifier,delta)
    installed_delta=None
    if args.installed:
        saved=definitions[identifier]
        installed_delta=volume(shape-saved)+volume(saved-shape)
        assert installed_delta<.01,(identifier,installed_delta)
        restored=saved
    candidate[identifier]=poses[identifier]*restored;roundtrips.append({'part':identifier,'delta_mm3':delta,'installed_symmetric_difference_mm3':installed_delta})
shapes.update(candidate);boxes={identifier:s.bounding_box() for identifier,s in shapes.items()}
checks=0;failures=[]
for a,b in itertools.combinations(shapes,2):
    if a not in candidate and b not in candidate:continue
    if not all(min(getattr(boxes[a].max,k),getattr(boxes[b].max,k))-max(getattr(boxes[a].min,k),getattr(boxes[b].min,k))>1e-6 for k in 'XYZ'):continue
    common=overlap(shapes[a],shapes[b]);checks+=1
    if common>.01:failures.append({'a':a,'b':b,'overlap_mm3':common})
probes=[]
for identifier,x in flange.CENTERS.items():
    for dx,dy in flange.HOLES:
        frame=cad.Pos(x+dx,-180+dy,0)
        bore=frame*flange.cylinder(5.45,139,151)
        ring=frame*(flange.cylinder(8,140.1,149.9)-flange.cylinder(6,139,151))
        obstruction=overlap(candidate[identifier],bore)
        missing=abs(volume(ring)-overlap(candidate[identifier],ring))
        probes.append({'part':identifier,'hole':[dx,dy],'obstruction_mm3':obstruction,'missing_bearing_band_mm3':missing})
        if obstruction>.001 or missing>.001:failures.append(probes[-1])
    bore=cad.Pos(x,-180,0)*flange.cylinder(19.95,132.1,212.9)
    obstruction=overlap(candidate[identifier],bore)
    probes.append({'part':identifier,'outlet_obstruction_mm3':obstruction})
    if obstruction>.01:failures.append(probes[-1])
assert path.read_bytes()==raw
assert all(hashlib.sha256(p.read_bytes()).hexdigest()==h for p,h in hashes.items())
report={'passed':not failures,'installed':args.installed,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'step_roundtrips':roundtrips,'neighbor_checks':checks,'probes':probes,'failures':failures,'input_sha256':{str(p):h for p,h in hashes.items()},'limits':flange.GAPS}
(model_root/'inventory/engine'/('exhaust-outlet-flanges-desktop-installed-validation.json' if args.installed else 'exhaust-outlet-flanges-desktop-validation.json')).write_text(json.dumps(report,indent=2)+'\n')
arrays={}
for i,(identifier,shape) in enumerate(candidate.items()):
    vertices,faces=shape.tessellate(.08,.15);arrays[f'vertices_{i}']=np.array([tuple(v) for v in vertices]);arrays[f'faces_{i}']=np.array(faces);arrays[f'explode_{i}']=np.zeros(3)
arrays['metadata']=np.array(json.dumps({'assembly':'Integral outlet flange candidates — assumed dimensions','parts':2,'colors':['#87766b','#87766b'],'manifest_sha256':report['manifest_sha256']}))
np.savez_compressed('/private/tmp/exhaust-outlet-flanges-desktop.npz',**arrays)
print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'},indent=2),flush=True)
assert not failures
