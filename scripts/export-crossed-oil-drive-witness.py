#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
from timing_coupled_core_candidate import AXIS
import oil_drive_layout as d
from timing_cover_attachment_v2 import norm
O=R/'cad/engine/generated/crossed-oil-drive-direction';m=json.loads((R/'inventory/engine/full-assembly.json').read_text());pose=transforms(m);shift=b.Pos(0,AXIS[0]-90,AXIS[1]-72);angle=5.625
cp=R/'cad/engine/generated/timing-thrust-land-candidate/camshaft.step';gp=R/'cad/engine/generated/distributor-drive-gear.step'
cam=b.Pos(0,*AXIS)*b.Rot(angle,0,0)*b.Pos(0,-AXIS[0],-AXIS[1])*b.import_step(cp)
gear=shift*d.GEAR_FRAME*b.Rot(0,0,-angle)*d.GEAR_FRAME.inverse()*pose['distributor-drive-gear']*b.import_step(gp)
overlap=norm(cam.intersect(gear));cam_window=norm(cam.intersect(b.Pos(d.DRIVE_X,*AXIS)*b.Box(12.02,55,55)))
parts={'cam-drive-window':cam_window,'distributor-gear':gear,'overlap':overlap};arrays={}
for n,s in parts.items():
 b.export_step(s,O/(n+'-witness.step'));v,f=s.tessellate(.04,.12);arrays[n+'_v']=np.array([tuple(q)for q in v]);arrays[n+'_f']=np.array(f)
np.savez_compressed(O/'witness-mesh.npz',**arrays)
files=[Path(__file__),cp,gp,R/'inventory/engine/full-assembly.json',R/'cad/engine/oil_drive_layout.py',*O.glob('*-witness.step'),O/'witness-mesh.npz']
(O/'witness-bindings.json').write_text(json.dumps({'pose':'cam+5.625deg,distributor−5.625deg','cam_window_scope':'Visualization clip only; overlap computed against complete actual camshaft','sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}},indent=2)+'\n')
