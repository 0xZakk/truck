#!/usr/bin/env python3
"""Actual exported candidate sections alongside frozen hardware."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-access-candidate';F=R/'cad/engine/generated/timing-cover-attachment-v2'
a=np.load(F/'preview.npz');names=json.loads((F/'names.json').read_text());p=np.load(O/'pan-preview.npz')
def mesh(name):
 if name=='candidate pan':return p['vertices'],p['faces']
 i=names.index(name);return a['v'+str(i)],a['f'+str(i)]
def section(ax,name,y,col):
 v,f=mesh(name);t=v[f];segs=[]
 for tri in t[(t[:,:,1].min(1)<=y)&(t[:,:,1].max(1)>=y)]:
  hits=[]
  for q,r in zip(tri,np.roll(tri,-1,axis=0)):
   if(q[1]<y<=r[1])or(r[1]<y<=q[1]):hits.append((q+(r-q)*(y-q[1])/(r[1]-q[1]))[[0,2]])
  if len(hits)==2:segs.append(hits)
 ax.add_collection(LineCollection(segs,colors=col,linewidths=1.3,label=name))
fig=plt.figure(figsize=(15,11))
for i,(n,y,xlim,ylim) in enumerate([(23,0,(350,406),(-100,-55)),(10,196,(350,405),(-80,-20)),(22,180,(350,406),(-85,-20))]):
 ax=fig.add_subplot(2,2,i+1)
 for name,col in [('pan','#bbbbbb'),('candidate pan','#167a55'),('pan-gasket','#3366aa'),(f'oil-pan-mounting-screw-{n}','#ba8844'),(f'oil-pan-mounting-washer-{n}','#885522')]:section(ax,name,y,col)
 x=365.5 if n==10 else 390;z=-67 if n==23 else-32.1
 ax.fill_between([x-11,x+11],-100,z+1.6,color='#e9c86a',alpha=.15,label='estimated socket')
 ax.set(xlim=xlim,ylim=ylim,xlabel='X mm',ylabel='Z mm',title=f'Actual section Y{y}; station {n}');ax.set_aspect('equal');ax.legend(fontsize=6);ax.grid(alpha=.15)
ax=fig.add_subplot(224,projection='3d');v,f=mesh('candidate pan');t=v[f];t=t[t[:,:,0].min(1)>330];ax.add_collection3d(Poly3DCollection(t,facecolor='#6a9d86',edgecolor='none',alpha=.9));ax.set(xlim=(330,405),ylim=(-155,215),zlim=(-100,-20),xlabel='X',ylabel='Y',zlabel='Z');ax.view_init(24,-35);ax.set_box_aspect((75,370,80));ax.set_title('Actual exported front pan; estimated wall contours')
fig.suptitle('Uninstalled pan-access candidate — green actual CAD, gray frozen failure; tool envelope estimated');fig.tight_layout();fig.savefig(O/'review.png',dpi=160)
