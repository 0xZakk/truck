#!/usr/bin/env python3
"""Conservative actual-CAD slab certificate replacing an impossible closest-point result."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
from assembly_clockwise_candidate import transforms
O=R/'cad/engine/generated/accessory-psac-carrier';sp=O/'trial1-carrier.step';mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());o=next(o for o in m['occurrences']if o['id']=='water-pump-housing');d=next(d for d in m['definitions']if d['id']==o['definition']);p=R/d['step'].lstrip('/');s=b.import_step(sp);a=transforms(m,0,0)[o['id']]*b.import_step(p);bb=a.bounding_box();pb=np.array([tuple(bb.min),tuple(bb.max)]);rows=[];total=0
for name,center in [('low-Y',-440),('high-Y',620)]:
 # Adjacent boxes tile Y−1000..1240 at exact Y120; whole carrier lies inside.
 extent=1120 if name=='low-Y'else 1000
 box=b.Pos(500,center,0)*b.Box(2000,extent,2000);q=s.intersect(box);v=solid_volume(q);total+=v;bnd=np.array([tuple(q.bounding_box().min),tuple(q.bounding_box().max)]);axis_gaps=np.maximum(np.maximum(pb[0]-bnd[1],bnd[0]-pb[1]),0);gap=float(np.linalg.norm(axis_gaps));assert q.is_valid and gap>=1
 w=O/f'trial1-pump-certificate-{name}.step';b.export_step(q,w);rows.append({'part':name,'volume_mm3':v,'bounds':bnd.tolist(),'axis_gaps_mm':axis_gaps.tolist(),'minimum_distance_lower_bound_mm':gap})
err=abs(total-solid_volume(s));assert err<.1
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'status':'PASS conservative exact-CAD partition separation; raw OCC zero retained as invalid result','partition':'Y120, with both exact subvolumes valid and total volume conserved','pump_bounds':pb.tolist(),'rows':rows,'partition_volume_error_mm3':err,'minimum_distance_lower_bound_mm':min(x['minimum_distance_lower_bound_mm']for x in rows),'inputs':{str(x.relative_to(R)):sha(x)for x in [sp,mp,p,Path(__file__)]}}
(R/'inventory/engine/accessory-psac-carrier-pump-separation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
