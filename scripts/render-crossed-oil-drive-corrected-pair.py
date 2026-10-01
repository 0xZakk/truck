#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/crossed-oil-drive-corrected-pair'
subprocess.run([str(R/'.venv-cad/bin/python'),'-c',"import trimesh,numpy as np,sys;from pathlib import Path;o=Path(sys.argv[1]);a={};\nfor n in ['cam-drive-gear-local','distributor-drive-gear-local']:\n m=trimesh.load(o/(n+'.glb'),force='mesh');a[n+'_v']=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;a[n+'_f']=m.faces\nnp.savez_compressed(o/'render-input.npz',**a)",str(O)],check=True)
a=np.load(O/'render-input.npz');fig=plt.figure(figsize=(14,8));axis=np.array([95.1098209901611,76.08785679212888]);gear=np.array([227.584,128.9387553384538,63.7751316324048])
def rx(deg):
 t=np.radians(deg);return np.array([[1,0,0],[0,np.cos(t),-np.sin(t)],[0,np.sin(t),np.cos(t)]])
def rz(deg):
 t=np.radians(deg);return np.array([[np.cos(t),-np.sin(t),0],[np.sin(t),np.cos(t),0],[0,0,1]])
for i,angle in enumerate([0,5.625],1):
 ax=fig.add_subplot(1,2,i,projection='3d')
 for n,col,rot,origin in [('cam-drive-gear-local',np.array([.38,.65,.51]),rx(angle),np.r_[227.584,axis]),('distributor-drive-gear-local',np.array([.43,.58,.78]),rx(-20)@rz(-angle),gear)]:
  v=a[n+'_v']@rot.T+origin;t=v[a[n+'_f']];norm=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-20);light=np.array([.3,-.5,.8]);light/=np.linalg.norm(light);shade=.45+.55*np.clip(norm@light,0,1);colors=np.column_stack([shade[:,None]*col,np.ones(len(t))]);ax.add_collection3d(Poly3DCollection(t,facecolors=colors,edgecolor='none'))
 ax.set(xlim=(204,251),ylim=(74,150),zlim=(38,103),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((47,76,65));ax.view_init(29,-48);ax.set_title(f'Actual exported pair: cam +{angle}° / distributor −{angle}°')
fig.suptitle('Estimated corrected crossed drive — generated tooth lead reversed, fixed axes and connections',fontsize=14)
fig.text(.5,.08,'16 teeth each, R18 mm pitch and 12 mm face remain modeling estimates.\nActual exported meshes shown; sampled separation and phase-clearance evidence do not establish production contact pressure.',ha='center',fontsize=11)
fig.subplots_adjust(left=0,right=1,top=.9,bottom=.14,wspace=0);fig.savefig(O/'corrected-pair-review.png',dpi=170)
files=[Path(__file__),O/'render-input.npz',O/'corrected-pair-review.png',O/'cam-drive-gear-local.glb',O/'distributor-drive-gear-local.glb'];(R/'inventory/engine/crossed-oil-drive-corrected-pair-render.json').write_text(json.dumps({'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}},indent=2)+'\n')
