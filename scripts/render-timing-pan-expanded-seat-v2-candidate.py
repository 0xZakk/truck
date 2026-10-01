#!/usr/bin/env python3
"""Actual exported sections; proposals and nominal tool bounds labeled separately."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate';F=R/'cad/engine/generated/timing-cover-attachment-v2'
a=np.load(F/'preview.npz');names=json.loads((F/'names.json').read_text());g=np.load(O/'gasket-preview.npz');p=np.load(O/'pan-preview.npz');old=np.load(R/'cad/engine/generated/timing-pan-access-candidate/pan-preview.npz')
def mesh(name):
 if name=='pan-gasket':return g['vertices'],g['faces']
 if name=='new pan':return p['vertices'],p['faces']
 if name=='previous pan':return old['vertices'],old['faces']
 i=names.index(name);return a['v'+str(i)],a['f'+str(i)]
def section(ax,name,axis,coord,color,lw=1.2):
 v,f=mesh(name);t=v[f];inds=[j for j in range(3)if j!=axis];segs=[]
 for tri in t[(t[:,:,axis].min(1)<=coord)&(t[:,:,axis].max(1)>=coord)]:
  hits=[]
  for x,y in zip(tri,np.roll(tri,-1,axis=0)):
   if(x[axis]<coord<=y[axis])or(y[axis]<coord<=x[axis]):hits.append((x+(y-x)*(coord-x[axis])/(y[axis]-x[axis]))[inds])
  if len(hits)==2:segs.append(hits)
 ax.add_collection(LineCollection(segs,colors=color,linewidths=lw,label=name))
fig=plt.figure(figsize=(16,12));ax=fig.add_subplot(221)
section(ax,'previous pan',2,-70,'#bbbbbb');section(ax,'new pan',2,-70,'#167a55',1.8)
for n,x,y in [(20,365.5,-132),(10,365.5,196),(21,390,-110),(22,390,180),(23,390,0)]:
 ax.add_patch(plt.Circle((x,y),8.763,fill=False,color='#ad772c'));ax.text(x+10,y,str(n),fontsize=8)
ax.text(339,15,'Wet side',color='#227599');ax.text(390,65,'Dry',color='#ad772c');ax.set(xlim=(325,412),ylim=(-150,218),xlabel='X mm',ylabel='Y mm',title='A. Actual Z−70 section and nominal socket outlines');ax.set_aspect('equal');ax.legend(fontsize=7)
ax=fig.add_subplot(222)
for n,col in [('previous pan','#bbbbbb'),('new pan','#167a55'),('pan-gasket','#336699'),('oil-pan-mounting-screw-20','#a8793c'),('oil-pan-mounting-washer-20','#704a29')]:section(ax,n,0,365.5,col)
ax.fill_between([-132-8.763,-132+8.763],-100,-32.1,color='#d7b164',alpha=.15,label='nominal SHD03013 envelope')
ax.text(-141,-92,'Dry tool side',fontsize=9);ax.text(-117,-75,'Wet side',fontsize=9,color='#227599',rotation=90)
ax.set(xlim=(-146,-108),ylim=(-100,-22),xlabel='Y mm',ylabel='Z mm',title='B. Station20 actual section: R10 flat seat and dry-side wall');ax.set_aspect('equal');ax.legend(fontsize=7)
ax=fig.add_subplot(223)
section(ax,'new pan',1,0,'#167a55',1.6);section(ax,'pan-gasket',1,0,'#336699')
ax.plot([370,350,350,330],[-70,-70,-82,-90],color='#bb6633',marker='o',markersize=3,label='R1 mm tested wet-path centerline')
ax.set(xlim=(320,400),ylim=(-105,-54),xlabel='X mm',ylabel='Z mm',title='C. Actual shoulder section; bent wet passage retained');ax.set_aspect('equal');ax.legend(fontsize=7)
ax=fig.add_subplot(224,projection='3d');v,f=mesh('new pan');t=v[f];ax.add_collection3d(Poly3DCollection(t,facecolor='#75a08e',edgecolor='none',alpha=.95));ax.set(xlim=(-400,410),ylim=(-160,215),zlim=(-280,-20),xlabel='X',ylabel='Y',zlabel='Z');ax.set_box_aspect((810,375,260));ax.view_init(32,-42);ax.set_title('D. Actual exported pan; estimated sharp wall returns')
for q in fig.axes:
 if q.name!='3d':q.grid(alpha=.15)
fig.suptitle('Uninstalled expanded-seat v2 candidate — local checks only, full oil containment unverified',fontsize=15);fig.tight_layout(rect=(0,0,1,.96));fig.savefig(O/'review.png',dpi=160)
