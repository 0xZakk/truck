from pathlib import Path
import sys,json,hashlib,itertools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_height_20261002_ports as c
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.core.norm(s).solids())if s else 0.
c.O.mkdir(exist_ok=True);r={'status':'RUNNING core only; ports present; validation pending','variants':{},'inputs':{str(p.relative_to(R)):sha(p)for p in[Path(__file__),Path(c.__file__),c.core.MP,c.core.REAR,R/'docs/components/pump-height-20261002-ports-contract.md']}};rp=R/'reference/engine/pump-height-20261002-ports.json'
def save():rp.write_text(json.dumps(r,indent=2)+'\n')
save()
for name,height in [('nominal',98.43),('inch-value',98.552)]:
 parts,inputs=c.parts(height);rows={};pairs=[];errors=[]
 for n,s in parts.items():
  p=c.O/(name+'-'+n+'.step');b.export_step(s,p);s=b.import_step(p);parts[n]=s;rows[n]={'path':str(p.relative_to(R)),'sha256':sha(p),'valid':s.is_valid,'solids':len(s.solids()),'bounds':[list(s.bounding_box().min),list(s.bounding_box().max)]}
 for p in inputs.values():r['inputs'][str(p.relative_to(R))]=sha(p)
 # Rebuilt housing/shaft/web vs all other pump parts; rigid translated pairs not reaccepted.
 keys=[n for n in parts if not n.startswith(('fan-clutch-','cooling-fan-'))]
 for a,z in itertools.combinations(keys,2):
  if not set([a,z])&{'water-pump-housing','water-pump-shaft','water-pump-pulley'}:continue
  try:pairs.append({'a':a,'b':z,'overlap_mm3':vol(parts[a].intersect(parts[z]))})
  except Exception as e:errors.append({'a':a,'b':z,'error':repr(e)})
 r['variants'][name]={'height_mm':height,'parts':rows,'pairs':pairs,'errors':errors,'conflicts':[x for x in pairs if x['overlap_mm3']>.1]};save();print(name,'parts',len(parts),'conflicts',r['variants'][name]['conflicts'],'errors',errors,flush=True)
r['status']='PORT EXPORT/LOCAL PAIRS COMPLETE; passages and affected neighbors pending';save()
