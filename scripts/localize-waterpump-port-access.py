"""Classify existing access obstructions by declared analytic port stock."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
import water_pump_joint_candidate as p,water_pump_inlet_v3_candidate as inlet
from cooling_connections import cylinder
O=R/'cad/engine/generated/waterpump-port-access-research';O.mkdir(exist_ok=True)
mp=R/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());poses=transforms(m);defs={q['id']:q for q in m['definitions']};path=R/defs['water-pump-housing']['step'].lstrip('/');housing=poses['water-pump-housing']*b.import_step(path);frame=b.Pos(*p.PUMP_POSITION)
regions={'large-inlet':frame*(inlet.outer()-inlet.passage()),'heater-boss':frame*(cylinder(12,32,(-2,-45,15),(0,1,0))-cylinder(8.1,39,(-2,-44.5,15),(0,1,0)))}
def vol(s):return sum(abs(q.volume)for q in s.solids())if s else 0.
rows=[]
for n,a in enumerate(p.MOUNTING,1):
 y,z=a[0]-32,a[1]+170;tool=p.cx(10.5,389,449,y,z);hit=housing.intersect(tool);row={'station':n,'overlap_mm3':vol(hit),'source_port_regions_mm3':{k:vol(hit.intersect(s))if hit else 0. for k,s in regions.items()}}
 if hit and hit.solids():
  q=O/f'pump-tool-{n}-obstruction.step';b.export_step(hit,q);row['witness']=str(q.relative_to(R));row['witness_sha256']=hashlib.sha256(q.read_bytes()).hexdigest();row['bounds_mm']=[list(hit.bounding_box().min),list(hit.bounding_box().max)]
 rows.append(row)
inputs=[Path(__file__),mp,path,R/'cad/engine/water_pump_joint_candidate.py',R/'cad/engine/water_pump_inlet_v3_candidate.py',R/'cad/engine/cooling_connections.py'];j={'status':'Research only; no geometry edit','rows':rows,'interpretation':'Test whether guessed port orientation, rather than missing drilled access tunnels, owns current obstructions. Source photos must decide architecture.','inputs':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in inputs}};(R/'inventory/engine/waterpump-port-access-research.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
