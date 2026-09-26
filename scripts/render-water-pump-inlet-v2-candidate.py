"""Render actual assembled/cutaway CAD meshes; no image generation."""
import json,numpy as np,matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,7));fig.patch.set_facecolor('#eef2f6')
for index,(path,title,azim) in enumerate([('/private/tmp/water-pump-inlet-v2-actual.npz','Pump with lateral inlet neck',-35),('/private/tmp/water-pump-inlet-v2-cutaway.npz','Section through inlet passage',-50)],1):
 data=np.load(path);meta=json.loads(str(data['metadata']));ax=fig.add_subplot(1,2,index,projection='3d');verts=[]
 for i,key in enumerate(meta['parts']):
  v=data[f'vertices_{i}'];f=data[f'faces_{i}'];verts.append(v)
  normals=np.cross(v[f][:,1]-v[f][:,0],v[f][:,2]-v[f][:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-12)
  light=np.array([.2,-.7,.68]);light/=np.linalg.norm(light);intensity=.35+.65*np.abs(normals@light)
  rgb=np.array(__import__('matplotlib').colors.to_rgb(meta['colors'][i]));colors=intensity[:,None]*rgb[None,:]
  ax.add_collection3d(Poly3DCollection(v[f],facecolors=colors,linewidths=0,alpha=1))
 allv=np.concatenate(verts);lo=allv.min(0);hi=allv.max(0);mid=(hi+lo)/2;half=max(hi-lo)*.53
 ax.set_xlim(mid[0]-half,mid[0]+half);ax.set_ylim(mid[1]-half,mid[1]+half);ax.set_zlim(mid[2]-half,mid[2]+half);ax.set_box_aspect((1,1,1));ax.view_init(elev=22,azim=azim);ax.set_axis_off();ax.set_title(title)
fig.suptitle('Uninstalled pump inlet candidate · actual CAD\nSource-informed topology; all dimensions and local passage routing provisional',fontsize=14)
fig.tight_layout();fig.savefig('/private/tmp/water-pump-inlet-v2-review.png',dpi=160)
print('/private/tmp/water-pump-inlet-v2-review.png')
