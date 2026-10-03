from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_functional_20261003 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c.O.mkdir(exist_ok=True)
r={'status':'RUNNING','height_mm':c.HEIGHT,'parts':{},'regions':{},'inputs':{}}
p=c.R/'reference/engine/pump-functional-20261003-build.json'
def save():p.write_text(json.dumps(r,indent=2)+'\n')
if '--housing-only' in sys.argv:r=json.loads(p.read_text())
save();print('BUILD START',flush=True)
parts,inputs,regions=c.parts()
for n,s in parts.items():
 if '--housing-only' in sys.argv and n!='water-pump-housing':continue
 f=c.O/(n+'.step');b.export_step(s,f);s=b.import_step(f);r['parts'][n]={'path':str(f.relative_to(R)),'sha256':sha(f),'valid':s.is_valid,'solids':len(s.solids()),'bounds':[list(s.bounding_box().min),list(s.bounding_box().max)]};save();print(n,len(s.solids()),s.is_valid,flush=True)
for n,s in regions.items():
 f=c.O/('region-'+n+'.step');b.export_step(s,f);r['regions'][n]={'path':str(f.relative_to(R)),'sha256':sha(f)}
for f in [Path(__file__),Path(c.__file__),Path(c.core.__file__),Path(c.old_ports.__file__),c.core.MP,c.core.REAR,R/'docs/components/pump-functional-20261003-contract.md',*inputs.values()]:r['inputs'][str(f.relative_to(R))]=sha(f)
r['status']='EXPORTED; validation pending';save();print('DONE',flush=True)
