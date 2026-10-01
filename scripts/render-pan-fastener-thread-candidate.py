#!/usr/bin/env python3
from pathlib import Path
import numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/pan-fastener-thread-candidate';a=np.load(O/'preview.npz');colors=['#b78543','#527d73','#84919a'];fig=plt.figure(figsize=(15,8));ax=fig.add_subplot(131,projection='3d')
for i in [0,2]:
 v=a['v'+str(i)];t=v[a['f'+str(i)]];ax.add_collection3d(Poly3DCollection(t,facecolor=colors[i],edgecolors='none'))
ax.set(xlim=(-8,8),ylim=(-8,8),zlim=(-6,23),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title='Actual reusable male and existing washer');ax.set_box_aspect((16,16,29));ax.view_init(18,-55)
for plot,shift,title in [(2,0,'Matched thread section'),(3,.3,'Wrong axial phase: +0.3 mm\nInterference is intentional fault control')]:
 ax=fig.add_subplot(1,3,plot)
 for i in [1,0]:
  t=a['v'+str(i)][a['f'+str(i)]].copy()
  if i==0:t[:,:,2]+=shift
  t=t[(t[:,:,1].min(1)<=0)&(t[:,:,1].max(1)>=0)];segs=[]
  for tri in t:
   hits=[]
   for p,q in zip(tri,np.roll(tri,-1,axis=0)):
    if (p[1]<0<=q[1])or(q[1]<0<=p[1]):hits.append((p+(q-p)*(-p[1])/(q[1]-p[1]))[[0,2]])
   if len(hits)==2:segs.append(hits)
  ax.add_collection(LineCollection(segs,colors=colors[i],linewidths=1.5,label='Male'if i==0 else 'Female coupon'))
 ax.set(xlim=(2.9,4.3),ylim=(9,14),xlabel='Radius coordinate X mm',ylabel='Z mm',title=title);ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(loc='lower right')
fig.suptitle('Isolated 5/16-18 × 0.87 in nominal study — estimated thread form and zero-clearance test coupon\nNo canonical replacement, female coupon is not an installed insert');fig.tight_layout(rect=(0,0,1,.91));fig.savefig(O/'thread-review.png',dpi=180)
