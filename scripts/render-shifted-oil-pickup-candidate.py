#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import numpy as np,trimesh,build123d as b
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from assembly_math import transforms
import shifted_oil_pickup_candidate as c
OUT=ROOT/'cad/engine/generated/shifted-oil-pickup-candidate';m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());poses=transforms(m)
paths=['scripts/render-shifted-oil-pickup-candidate.py','inventory/engine/full-assembly.json','cad/engine/shifted_oil_pickup_candidate.py','cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube.glb','cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube-world.step','cad/engine/generated/oil-pump-housing.step']
fig,ax=plt.subplots(1,2,figsize=(14,6),facecolor='#f6f7f9')
items=[('new tube',OUT/'oil-pickup-tube.glb',poses['oil-pickup-tube'],[.18,.58,.60]),('pump',ROOT/'models/engine/oil-pump-housing.glb',b.Pos(*c.DELTA)*poses['oil-pump-housing'],[.55,.59,.63]),('bell',ROOT/'models/engine/oil-pickup-bell.glb',poses['oil-pickup-bell'],[.7,.55,.3])]
for name,p,loc,col in items:
 paths.append(str(p.relative_to(ROOT)));mesh=trimesh.load(p,force='mesh');v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;mat=np.array(loc.to_tuple()[0]) if False else np.array([[loc.wrapped.Transformation().Value(i,j) for j in range(1,5)] for i in range(1,4)]);v=v@mat[:,:3].T+mat[:,3];t=v[mesh.faces];proj=t[:,:,[0,2]];norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);shade=.55+.4*abs(norm@np.array([.2,-.8,.5]))/np.maximum(np.linalg.norm(norm,axis=1),1e-20);order=np.argsort(t[:,:,1].mean(1));ax[0].add_collection(PolyCollection(proj[order],facecolors=shade[order,None]*col,edgecolors='none',label=name))
ax[0].autoscale();ax[0].set_aspect('equal');ax[0].set_title('Actual exported meshes · fixed sump end');ax[0].set_xlabel('World X (mm)');ax[0].set_ylabel('World Z (mm)')
frame=b.Pos(*c.DELTA)*c.drive.PUMP_FRAME
pump=frame.inverse()*b.Pos(*c.DELTA)*poses['oil-pump-housing']*b.import_step(ROOT/'cad/engine/generated/oil-pump-housing.step');tube=frame.inverse()*b.import_step(OUT/'oil-pickup-tube-world.step')
for s,color in [(pump,'#66727b'),(tube,'#168f99')]:
 sec=b.section(s,section_by=b.Plane.YZ.offset(-32))
 for w in sec.wires():
  points=np.array([tuple(w.position_at(i/256))[1:] for i in range(257)]);ax[1].plot(points[:,0],points[:,1],c=color,lw=2)
ax[1].set_aspect('equal');ax[1].set_xlim(-9,9);ax[1].set_ylim(-4,14);ax[1].grid(alpha=.2);ax[1].set_title('Actual inserted section · pump local X−32');ax[1].set_xlabel('Pump local Y (mm)');ax[1].set_ylabel('Pump local Z (mm)')
fig.suptitle('Estimated pickup reconnection only · pump discharge/gasket and bell retention remain unresolved',fontsize=12);fig.tight_layout();p=OUT/'pickup-review.png';fig.savefig(p,dpi=160);plt.close(fig)
r={'status':'Actual mesh/section render; visual review pending','inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in set(paths)},'render':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(ROOT/'inventory/engine/shifted-oil-pickup-render-validation.json').write_text(json.dumps(r,indent=2)+'\n')
