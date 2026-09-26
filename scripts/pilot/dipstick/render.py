from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[3];d=np.load(ROOT/'cad/engine/pilot/dipstick/visual-meshes.npz')
fig=plt.figure(figsize=(16,10))
for k,(title,bounds) in enumerate([('Withdrawn indicator · approximate specimen form',(-30,30,-700,85)),('Open-loop handle and retention waves',(-30,30,-65,85)),('Widened blade and engineering stamp',(-10,10,-695,-580))]):
 ax=fig.add_subplot(2,3,k+1)
 for i,col in [(0,'#929ba4'),(1,'#ddb627')]:
  v=d['v'+str(i)];f=d['f'+str(i)];tri=v[f]
  from matplotlib.collections import PolyCollection

  normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-12)
  visible=normals[:,1]<-.01
  from matplotlib.colors import to_rgb
  shades=(.3+.7*np.abs(normals@np.array([.4,-.8,.4])))[:,None]*np.array(to_rgb(col))
  ax.add_collection(PolyCollection(tri[visible][:,:,[0,2]],facecolors=np.clip(shades[visible],0,1),edgecolors='none'))
 ax.set_xlim(bounds[:2]);ax.set_ylim(bounds[2:]);ax.set_aspect('equal');ax.set_title(title,fontsize=10);ax.set_xlabel('X mm');ax.set_ylabel('Z mm');ax.set_xticks([0] if k==0 else [-10,0,10])
ax=fig.add_subplot(2,1,2,projection='3d')
for j in range(6):
 v=d['n'+str(j)];f=d['nf'+str(j)];ax.add_collection3d(Poly3DCollection(v[f],facecolors='#a0a8ac',alpha=.08,edgecolors='none'))
for i,col in [(0,'#b01f55'),(1,'#ddb627')]:
 v=d['iv'+str(i)];f=d['if'+str(i)];ax.add_collection3d(Poly3DCollection(v[f],facecolors=col,edgecolors='none'))
ax.set_xlim(-440,440);ax.set_ylim(-200,350);ax.set_zlim(-300,550);ax.set_box_aspect((880,550,850));ax.view_init(15,35)
ax.set_title('UNACCEPTED pose: reference engine transparent; block passage and oil calibration unresolved',fontsize=11)
ax.set_xlabel('front +X mm');ax.set_ylabel('Y mm');ax.set_zlabel('up Z mm')
fig.suptitle('Engine oil dipstick · E9TE-6750-DA specimen comparison\n27.25 in blade is approximate; all other dimensions are estimates. No ADD/FULL marks invented.',fontsize=13)
fig.tight_layout(rect=(0,0,1,.93));fig.savefig(ROOT/'reference/engine/pilot/dipstick/cad-review.png',dpi=150)
