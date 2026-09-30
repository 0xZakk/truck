#!/usr/bin/env python3
from pathlib import Path
import numpy as np,trimesh,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-thrust-land-candidate';data={}
for p in OUT.glob('*.glb'):
 m=trimesh.load(p,force='mesh');data[p.stem+'_vertices']=np.asarray(m.vertices)[:,[0,2,1]]*[1,-1,1]*1000;data[p.stem+'_faces']=np.asarray(m.faces)
# Actual CAD cut through the axial/radial section, not a hand-drawn profile.
y=95.1098209901611;z=76.08785679212888
cutter=b.Pos(380,y-50,z)*b.Box(40,100,70)
for name in ['camshaft','cam-timing-gear','cam-thrust-plate','cam-gear-spacer']:
 q=b.import_step(OUT/(name+'.step')).intersect(cutter);v,f=q.tessellate(.03,.1)
 data['section_'+name+'_vertices']=np.array([tuple(x) for x in v]);data['section_'+name+'_faces']=np.array(f)
np.savez_compressed(OUT/'render-input.npz',**data)
