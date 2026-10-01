#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-oil-boundary'
loops=json.loads((O/'classified-rim-loops.json').read_text());mapping=json.loads((O/'dry-hole-classification.json').read_text())
fig=plt.figure(figsize=(14,9));ax=fig.add_subplot(211);az=fig.add_subplot(212)
for q in loops:
 p=np.array(q['samples']);central=q['length']>1000 and max(p[:,0])<380
 col='#147a52' if central else '#999999'
 if q['length']<100:col='#bb7a32'
 for a,inds in [(ax,(0,1)),(az,(0,2))]:a.plot(p[:,inds[0]],p[:,inds[1]],'.',markersize=1,color=col)
for q in mapping:
 x,y,z=q['expected_upper_center_mm'];ax.text(x,y,str(q['station']),fontsize=7,color='#704522')
ax.set(title='Actual gasket upper rim: green central mouth, gray perimeter, numbered 25 dry holes',xlabel='X mm',ylabel='Y mm');ax.set_aspect('equal');ax.grid(alpha=.15)
az.set(title='Actual nonplanar rim elevation — no flattened or automatically filled openings',xlabel='X mm',ylabel='Z mm');az.grid(alpha=.15)
fig.tight_layout();fig.savefig(O/'rim-review.png',dpi=160)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import LineCollection
p=np.load(O/'roof-preview.npz');fig=plt.figure(figsize=(15,9));ax=fig.add_subplot(121,projection='3d')
t=p['vertices'][p['faces']];ax.add_collection3d(Poly3DCollection(t,facecolor='#709cac',edgecolor='none',alpha=.8));ax.set(xlim=(-390,400),ylim=(-160,215),zlim=(-80,10),xlabel='X',ylabel='Y',zlabel='Z');ax.set_box_aspect((790,375,90));ax.view_init(32,-60);ax.set_title('Actual temporary roof; ruled rim-to-raised center\nTest fixture only, not a vehicle part')
if (O/'station20-head-wet-path.json').exists():
 path=json.loads((O/'station20-head-wet-path.json').read_text());points=np.array([path['start_mm'],path['end_mm']]);ax.plot(points[:,0],points[:,1],points[:,2],color='#bb2233',linewidth=2,label='station20→neck R0.25 path centerline');ax.legend(fontsize=7)
az=fig.add_subplot(122)
def section(vertices,faces,y,color,label):
 t=vertices[faces];segments=[]
 for tri in t[(t[:,:,1].min(1)<=y)&(t[:,:,1].max(1)>=y)]:
  hits=[]
  for p,q in zip(tri,np.roll(tri,-1,axis=0)):
   if(p[1]<y<=q[1])or(q[1]<y<=p[1]):hits.append((p+(q-p)*(y-p[1])/(q[1]-p[1]))[[0,2]])
  if len(hits)==2:segments.append(hits)
 az.add_collection(LineCollection(segments,colors=color,linewidths=1,label=label))
section(p['vertices'],p['faces'],0,'#336688','temporary roof')
q=np.load(R/'cad/engine/generated/timing-pan-access-candidate/pan-preview.npz');section(q['vertices'],q['faces'],0,'#1a7a52','actual pan')
if (O/'candidate-cavity-preview.npz').exists():
 q=np.load(O/'candidate-cavity-preview.npz');section(q['vertices'],q['faces'],0,'#bb8844','bounded cavity')
az.set(xlim=(-400,420),ylim=(-280,20),xlabel='X mm',ylabel='Z mm',title='Actual center section; cavity shown only if isolated');az.set_aspect('equal');az.legend();az.grid(alpha=.15);fig.tight_layout();fig.savefig(O/'roof-section-review.png',dpi=160)
