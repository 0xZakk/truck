"""Render actual assembled/cutaway CAD meshes; no image generation."""
from pathlib import Path
import json,numpy as np,matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'cad/engine/candidates/mechanical-seal'
OUT=ROOT/'reference/engine/qc/water-pump-mechanical-seal.png'
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,7));fig.patch.set_facecolor('#eef2f6')
for index,(path,title,azim) in enumerate([(DATA/'water-pump-mechanical-seal-actual.npz','Exploded construction study (35%)',-65),(DATA/'water-pump-mechanical-seal-cutaway.npz','Section through seal axis',145)],1):
 data=np.load(path);meta=json.loads(str(data['metadata']));ax=fig.add_subplot(1,2,index,projection='3d');verts=[]; all_faces=[]; all_colors=[]
 for i,key in enumerate(meta['parts']):
  v=data[f'vertices_{i}'].copy();f=data[f'faces_{i}']
  if index==1:v[:,0]+=.35*{'water-pump-seal-carrier':285,'water-pump-seal-stationary-face':230,'water-pump-seal-rotating-face':200,'water-pump-seal-shaft-collar':180,'water-pump-seal-bellows':250,'water-pump-seal-spring':270}[key]
  verts.append(v)
  normals=np.cross(v[f][:,1]-v[f][:,0],v[f][:,2]-v[f][:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-12)
  light=np.array([.2,-.7,.68]);light/=np.linalg.norm(light);intensity=.35+.65*np.abs(normals@light)
  rgb=np.array(__import__('matplotlib').colors.to_rgb(meta['colors'][i]));colors=intensity[:,None]*rgb[None,:]
  all_faces.extend(v[f]); all_colors.extend(colors)
 ax.add_collection3d(Poly3DCollection(all_faces,facecolors=all_colors,linewidths=0,alpha=1))
 allv=np.concatenate(verts);lo=allv.min(0);hi=allv.max(0);mid=(hi+lo)/2;half=max(hi-lo)*.53
 ax.set_xlim(mid[0]-half,mid[0]+half);ax.set_ylim(mid[1]-half,mid[1]+half);ax.set_zlim(mid[2]-half,mid[2]+half);ax.set_box_aspect((1,1,1));ax.view_init(elev=22,azim=azim);ax.set_axis_off();ax.set_title(title)
fig.suptitle('Illustrative mechanical seal study · actual CAD\nGeneric manufacturer architecture; Gates 44009 internals unverified',fontsize=14)
fig.tight_layout(rect=(0,0,1,.89));fig.savefig(OUT,dpi=160)
print(OUT)
