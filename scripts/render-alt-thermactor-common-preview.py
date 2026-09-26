from pathlib import Path
import numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];d=np.load('/private/tmp/truck-alt-ap-common.npz');v=d['vertices'];f=d['faces'];tri=v[f]
n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12)
intensity=.38+.62*np.abs(n@np.array([.65,-.4,.65]));colors=intensity[:,None]*np.array([.68,.74,.78])
fig=plt.figure(figsize=(13,7))
for i,(az,title) in enumerate([(-40,'Oblique: one continuous casting'),(0,'Front: open accessory cradles')],1):
 ax=fig.add_subplot(1,2,i,projection='3d');ax.add_collection3d(Poly3DCollection(tri,facecolors=colors,linewidths=0))
 mid=(v.max(0)+v.min(0))/2;half=max(v.max(0)-v.min(0))*.55
 ax.set_xlim(mid[0]-half,mid[0]+half);ax.set_ylim(mid[1]-half,mid[1]+half);ax.set_zlim(mid[2]-half,mid[2]+half);ax.set_box_aspect((1,1,1));ax.view_init(elev=12 if i==1 else 0,azim=az);ax.set_axis_off();ax.set_title(title)
fig.suptitle('Alternator / Thermactor common-carrier candidate\nSource-supported one-piece topology; hole mapping and all dimensions remain provisional')
fig.tight_layout(rect=(0,0,1,.86));fig.savefig(ROOT/'reference/engine/alt-thermactor-common-carrier-preview.png',dpi=160)
