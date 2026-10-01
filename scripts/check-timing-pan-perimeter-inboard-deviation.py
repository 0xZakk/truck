#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from timing_cover_attachment_v2 import norm
O=ROOT/'cad/engine/generated/timing-pan-perimeter-contact';F=ROOT/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate'
p=norm(b.import_step(F/'pan.step'));g=norm(b.import_step(F/'pan-gasket.step'));a=np.load(O/'inboard-route.npz')['points'];points=np.concatenate([a,(a[:-1]+a[1:])/2]);points=np.unique(points,axis=0)
points=points[np.linspace(0,len(points)-1,min(700,len(points))).astype(int)]
results=[]
for shape in [p,g]:results.append(max(shape.distance_to(b.Vertex(*q)) for q in points))
r={'scope':'700 evenly indexed unique centerline nodes/midpoints checked against actual STEP solids; sampled deviation, not contact pressure','points_checked':len(points),'maximum_distance_to_actual_pan_mm':results[0],'maximum_distance_to_actual_gasket_mm':results[1],'tessellation_allowance_mm':.025,'status':'PASS' if max(results)<.025 else 'FAIL','input_sha256':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest()for x in [Path(__file__),O/'inboard-route.npz',F/'pan.step',F/'pan-gasket.step']}}
(O/'inboard-route-deviation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
