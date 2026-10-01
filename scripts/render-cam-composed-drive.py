#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/cam-composed-drive-candidate';old=R/'cad/engine/generated/cam-clockwise-candidate/camshaft-local.glb';new=O/'camshaft-local.glb'
subprocess.run([str(R/'.venv-cad/bin/python'),'-c',"import trimesh,numpy as np,sys;a={};\nfor name,path in [('old',sys.argv[1]),('new',sys.argv[2])]:\n m=trimesh.load(path,force='mesh');a[name+'_v']=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;a[name+'_f']=m.faces\nnp.savez_compressed(sys.argv[3],**a)",str(old),str(new),str(O/'render-input.npz')],check=True)
a=np.load(O/'render-input.npz');fig=plt.figure(figsize=(15,9));gs=fig.add_gridspec(2,2,height_ratios=[1,1.3]);axes=[fig.add_subplot(gs[0,:],projection='3d'),fig.add_subplot(gs[1,0],projection='3d'),fig.add_subplot(gs[1,1],projection='3d')]
for ax,name,zoom,title in zip(axes,['new','old','new'],[False,True,True],['Composed full cam — actual exported mesh','Retained failure: old tooth lead','Composed corrected tooth lead']):
 v=a[name+'_v'];f=a[name+'_f'];t=v[f]
 if zoom:t=t[(t[:,:,0].max(1)>205)&(t[:,:,0].min(1)<250)]
 n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-20);light=np.array([.3,-.4,.85]);light/=np.linalg.norm(light);shade=.35+.65*np.clip(n@light,0,1);color=np.tile([.38,.61,.68],(len(t),1));centers=t.mean(1);mask=(centers[:,0]>221.584)&(centers[:,0]<233.584);color[mask]=[.79,.58,.26];ax.add_collection3d(Poly3DCollection(t,facecolors=shade[:,None]*color,edgecolor='none'))
 ax.set_title(title);ax.set_xlabel('Local X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
 if zoom:ax.set(xlim=(205,250),ylim=(-24,24),zlim=(-24,24));ax.set_box_aspect((45,48,48));ax.view_init(25,-52)
 else:ax.set(xlim=(-405,415),ylim=(-35,35),zlim=(-35,35));ax.set_box_aspect((10,1,1));ax.view_init(20,-68)
fig.suptitle('Frozen corrected lobes + corrected crossed-drive teeth\nOnly X221.584–233.584 outside R15 changed; gear dimensions remain estimates',fontsize=14)
fig.subplots_adjust(top=.88,bottom=.06,hspace=.1,wspace=.08);fig.savefig(O/'cam-composed-drive-review.png',dpi=170)
paths=[Path(__file__),old,new,O/'render-input.npz',O/'cam-composed-drive-review.png'];(R/'inventory/engine/cam-composed-drive-render-review.json').write_text(json.dumps({'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}},indent=2)+'\n')
