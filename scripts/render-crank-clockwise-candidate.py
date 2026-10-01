"""Inspect actual exported old/new crank meshes; no source originals."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/crank-clockwise-candidate'
paths=[R/'models/engine/crankshaft.glb',O/'crankshaft.glb']
if '--extract' in sys.argv:
 import trimesh
 arrays={}
 for i,p in enumerate(paths):
  m=trimesh.load(p,force='mesh');arrays[f'vertices{i}']=np.asarray(m.vertices)[:,[0,2,1]]*[1,-1,1]*1000;arrays[f'faces{i}']=m.faces
 np.savez(O/'render-meshes.npz',**arrays)
 raise SystemExit(0)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/crank-clockwise-candidate'
paths=[R/'models/engine/crankshaft.glb',O/'crankshaft.glb']
fig=plt.figure(figsize=(15,7));titles=['Original physical rest phases','Corrected physical rest phases']
for i,(p,title) in enumerate(zip(paths,titles),1):
 data=np.load(O/'render-meshes.npz');v=data[f'vertices{i-1}'];faces=data[f'faces{i-1}']
 tri=v[faces];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12)
 light=np.array([.3,-.5,.8]);light/=np.linalg.norm(light);shade=.3+.7*np.maximum(0,normal@light);colors=shade[:,None]*np.array([.62,.73,.79])[None,:]
 view=np.array([.25,-.85,.5]);view/=np.linalg.norm(view)
 right=np.cross(np.array([0,0,1]),view);right/=np.linalg.norm(right);up=np.cross(view,right)
 xy=np.column_stack((v@right,v@up));order=np.argsort((tri.mean(axis=1))@view)
 ax=fig.add_subplot(2,1,i);ax.add_collection(PolyCollection(xy[faces][order],facecolors=colors[order],edgecolors='none'))
 lo,hi=xy.min(0),xy.max(0);pad=(hi-lo)*.06
 ax.set_xlim(lo[0]-pad[0],hi[0]+pad[0]);ax.set_ylim(lo[1]-pad[1],hi[1]+pad[1]);ax.set_aspect('equal');ax.axis('off');ax.set_title(title)
fig.suptitle('Actual crankshaft mesh comparison — throw rephasing only\nMain journals and end interfaces preserved; production contours remain provisional')
fig.subplots_adjust(top=.86,bottom=.05,hspace=.25);image=O/'crank-phase-comparison.png';fig.savefig(image,dpi=150)
files=[Path(__file__),*paths,O/'render-meshes.npz',image,R/'inventory/engine/crank-clockwise-candidate-validation.json']
report={'status':'Rendered actual exported meshes; root visual review pending','sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(R/'inventory/engine/crank-clockwise-render-review.json').write_text(json.dumps(report,indent=2)+'\n')
