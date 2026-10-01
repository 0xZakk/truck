#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());o=next(o for o in m['occurrences']if o['id']=='water-pump-housing');d=next(d for d in m['definitions']if d['id']==o['definition']);p=R/d['step'].lstrip('/');s=b.import_step(R/'cad/engine/generated/accessory-psac-carrier/trial1-carrier.step');a=transforms(m,0,0)[o['id']]*b.import_step(p);q=BRepExtrema_DistShapeShape(s.wrapped,a.wrapped);q.Perform();rows=[]
for i in range(1,q.NbSolution()+1):
 x=q.PointOnShape1(i);z=q.PointOnShape2(i);rows.append({'carrier':[x.X(),x.Y(),x.Z()],'pump':[z.X(),z.Y(),z.Z()]})
r={'inputs':{str(k.relative_to(R)):hashlib.sha256(k.read_bytes()).hexdigest()for k in [mp,p,Path(__file__),R/'cad/engine/generated/accessory-psac-carrier/trial1-carrier.step']},'distance_mm':q.Value(),'done':q.IsDone(),'points':rows,'pump_bounds':[tuple(a.bounding_box().min),tuple(a.bounding_box().max)]};(R/'inventory/engine/accessory-psac-carrier-distance-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
