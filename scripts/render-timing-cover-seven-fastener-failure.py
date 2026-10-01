"""Actual STEP surfaces and Boolean witness; display crop only, no CAD edits."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate'
NAMES=['cover','main-cover-screw-1','head-cover-1']
if '--extract' in sys.argv:
 import build123d as b
 for name in NAMES:
  s=b.import_step(OUT/(name+'.step'));v,f=s.tessellate(.08,.15)
  np.savez_compressed(OUT/(name+'-review.npz'),v=np.array([tuple(p)for p in v]),f=np.array(f))
 raise SystemExit
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
camera=np.array([1,-.65,.5]);camera/=np.linalg.norm(camera);right=np.cross([0,0,1],camera);right/=np.linalg.norm(right);up=np.cross(camera,right);basis=np.array([right,up,camera]).T
meshes={n:np.load(OUT/(n+'-review.npz'))for n in NAMES}
def draw(ax,names,crop=False):
 ts=[];cs=[]
 for n in names:
  m=meshes[n];t=m['v'][m['f']]
  if crop:
   ctr=t.mean(1);t=t[(ctr[:,1]>-140)&(ctr[:,1]<-90)&(ctr[:,2]>-35)&(ctr[:,2]<15)]
  normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);vis=normal@camera>0;t=t[vis];normal=normal[vis]
  color={'cover':'#a5b5bc','main-cover-screw-1':'#d8a94a','head-cover-1':'#d63834'}[n];cs.append((.3+.7*np.clip(normal@camera,0,1))[:,None]*to_rgb(color));ts.append(t@basis)
 t=np.concatenate(ts);colors=np.concatenate(cs);order=np.argsort(t[:,:,2].mean(1));ax.add_collection(PolyCollection(t[order,:,:2],facecolors=colors[order],edgecolors='none'));p=t[:,:,:2].reshape(-1,2);lo=p.min(0);hi=p.max(0);pad=max(hi-lo)*.05;ax.set_xlim(lo[0]-pad,hi[0]+pad);ax.set_ylim(lo[1]-pad,hi[1]+pad);ax.set_aspect('equal');ax.axis('off')
fig,ax=plt.subplots(1,3,figsize=(16,7));draw(ax[0],['cover','main-cover-screw-1']);draw(ax[1],['head-cover-1']);draw(ax[2],['main-cover-screw-1','head-cover-1']);ax[0].set_title('Actual candidate cover and station 1 screw');ax[1].set_title('Isolated collision witness at preserved socket 21');ax[2].set_title('Red: actual head–cover intersection witness')
fig.suptitle('FAILED comparison trial: 68.134962 mm³ head collision\n1986 comparison bolt; estimated head and recess geometry; no 1994 fidelity claim');fig.tight_layout();path=OUT/'failure-review.png';fig.savefig(path,dpi=160)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r={'inputs':{str((OUT/(n+'.step')).relative_to(ROOT)):sha(OUT/(n+'.step'))for n in NAMES},'script_sha256':sha(Path(__file__)),'render':str(path.relative_to(ROOT)),'render_sha256':sha(path),'scope':'Actual STEP tessellation, shaded by normals. Display crop is not a CAD section. No mesh export qualification.'};(ROOT/'inventory/engine/timing-cover-seven-fastener-visual-review.json').write_text(json.dumps(r,indent=2)+'\n')
