#!/usr/bin/env python3
from pathlib import Path
import numpy as np,matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-cover-front-joint-candidate';a=np.load(O/'preview.npz');colors=['#8b9ba2','#b58b45','#5b817c','#b46145','#416e9f','#b0b1af'];fig=plt.figure(figsize=(16,9))
for view in range(2):
 ax=fig.add_subplot(1,2,view+1,projection='3d')
 for i in range(6):
  prefix='c' if view else '';v=a[f'{prefix}v{i}'];f=a[f'{prefix}f{i}'];t=v[f].copy()
  if not view:
   t=t[t[:,:,0].mean(1)>330];t[:,:,0]+=[25,8,-10,8,0,0][i];t[:,:,2]+=[0,0,0,0,-8,-20][i]
  n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12);shade=.4+.6*abs(n@np.array([.5,-.4,.7]));ax.add_collection3d(Poly3DCollection(t,facecolors=shade[:,None]*np.array(to_rgb(colors[i])),edgecolors='none'))
 ax.set(xlim=(315,450),ylim=(-165,260),zlim=(-100,220),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_xticks([335,373,414]);ax.set_box_aspect((135,425,320));ax.view_init(20,145 if view else -35);ax.set_title('Actual section at Y = 100 mm' if view else 'Exploded front crop: cover / main gasket / future land / pan gasket / pan')
fig.suptitle('Isolated coordinated front joint — dimensions and registration are estimated\nTwo terminal sealant patches are intentional; no canonical installation',fontsize=14);fig.tight_layout();fig.savefig(O/'candidate-review.png',dpi=160)
# Actual exported triangle intersections, not a conceptual seal diagram.
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
fig,axs=plt.subplots(1,3,figsize=(17,6))
for ax,(x,limits,title) in zip(axs,[(373.4,(-153,-118,-33,-18),'Left terminal'),(373.4,(185,218,-33,-18),'Right terminal'),(365.5,(-146,-118,-34,-14),'Revised side clamp seat')]):
 for i in range(6):
  t=a[f'v{i}'][a[f'f{i}']];t=t[(t[:,:,0].min(1)<=x)&(t[:,:,0].max(1)>=x)];segs=[]
  for tri in t:
   hits=[]
   for p,q in zip(tri,np.roll(tri,-1,axis=0)):
    if (p[0]<x<=q[0]) or (q[0]<x<=p[0]):hits.append((p+(q-p)*(x-p[0])/(q[0]-p[0]))[1:])
   if len(hits)==2:segs.append(hits)
  ax.add_collection(LineCollection(segs,colors=colors[i],linewidths=2))
 ax.set(xlim=limits[:2],ylim=limits[2:],xlabel='Y mm',ylabel='Z mm',title=f'{title}; X = {x} mm');ax.set_aspect('equal');ax.grid(alpha=.2)
fig.legend([Line2D([0],[0],color=q,lw=3) for q in colors],['Cover','Main gasket','Future block land','Two terminal sealant patches','Pan gasket','Pan'],loc='lower center',ncol=6)
fig.suptitle('Actual exported joint sections — estimated common seating plane Z = −24.5 mm');fig.tight_layout(rect=(0,.08,1,.93));fig.savefig(O/'terminal-contact-review.png',dpi=180)
# Local source comparison remains excluded from Git/release with original photo.
photo=R/'cad/engine/generated/timing-cover-joint-candidate/reference/dorman-635109-002.jpg'
if photo.exists():
 fig=plt.figure(figsize=(14,8));ax=fig.add_subplot(121);ax.imshow(plt.imread(photo)[:,::-1]);ax.axis('off');ax.set_title('Dorman 635-109 back, mirrored for CAD view convention')
 ax=fig.add_subplot(122,projection='3d');v=a['v0'];f=a['f0'];t=v[f];n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12);shade=.35+.65*abs(n@np.array([.8,.3,.4]));ax.add_collection3d(Poly3DCollection(t,facecolors=shade[:,None]*np.array(to_rgb(colors[0])),edgecolors='none'))
 ax.set(xlim=(365,420),ylim=(-160,260),zlim=(-75,235));ax.set_box_aspect((55,420,310));ax.view_init(10,165);ax.set_proj_type('ortho');ax.set_axis_off();ax.set_title('Actual candidate rear shell; estimated registration')
 fig.suptitle('Seven bosses, open rear cavity and lower bridge compared\nFront pan width, bolt stations, casting details and scale remain estimates');fig.tight_layout();fig.savefig(O/'source-comparison.png',dpi=160)
