#!/usr/bin/env python3
from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-cover-attachment-v2';a=np.load(O/'preview.npz');names=json.loads((O/'names.json').read_text())
def color(n):
 if 'screw' in n:return '#bd833f'
 if 'washer' in n:return '#74593c'
 return {'cover':'#8d9fa8','main-gasket':'#b5954a','future-block-land':'#517b72','pan-gasket':'#416eaa','pan':'#b9bdc0','front-terminal-sealant':'#c45c40','front-seal':'#333333','damper-hub':'#9960a6'}[n]
fig=plt.figure(figsize=(17,8));ax=fig.add_subplot(131,projection='3d')
for i,n in enumerate(names):
 if n in ('front-seal','damper-hub'):continue
 t=a['v'+str(i)][a['f'+str(i)]];t=t[(t[:,:,0].mean(1)>330)&(t[:,:,2].mean(1)<0)]
 if n in ('cover','main-gasket'):continue
 ax.add_collection3d(Poly3DCollection(t,facecolors=color(n),edgecolors='none'))
ax.set(xlim=(330,405),ylim=(-155,218),zlim=(-85,0),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title='Actual five pan screw/washer stacks\nCover hidden; no main-cover screws invented');ax.set_xticks([335,373,399]);ax.set_zticks([-80,-40,0]);ax.set_box_aspect((75,373,85));ax.view_init(20,-30)
for plot,axis,val,limits,wanted,title in [(2,1,-132,(354,377,-41,-6),['future-block-land','pan-gasket','pan','oil-pan-mounting-screw-20','oil-pan-mounting-washer-20'],'Actual thread section through Y = −132\nIdeal female form; no preload/tolerance claim'),(3,1,0,(381,399,-75,-42),['cover','pan-gasket','pan','oil-pan-mounting-screw-23','oil-pan-mounting-washer-23'],'Actual center front socket, Y = 0\nSame male; estimated conjugate casting thread')]:
 ax=fig.add_subplot(1,3,plot)
 for i,n in enumerate(names):
  if n not in wanted:continue
  t=a['v'+str(i)][a['f'+str(i)]];t=t[(t[:,:,axis].min(1)<=val)&(t[:,:,axis].max(1)>=val)];segs=[]
  for tri in t:
   hits=[]
   for p,q in zip(tri,np.roll(tri,-1,axis=0)):
    if (p[axis]<val<=q[axis])or(q[axis]<val<=p[axis]):hits.append((p+(q-p)*(val-p[axis])/(q[axis]-p[axis]))[[0,2]])
   if len(hits)==2:segs.append(hits)
  ax.add_collection(LineCollection(segs,colors=color(n),linewidths=1.5,label=n))
 ax.set(xlim=limits[:2],ylim=limits[2:],xlabel='X mm',ylabel='Z mm',title=title);ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=7,loc='upper center',bbox_to_anchor=(.5,-.13))
fig.suptitle('Attachment v2 — five estimated female sockets; canonical geometry remains unchanged');fig.tight_layout(rect=(0,.12,1,.95));fig.savefig(O/'attachment-review.png',dpi=160)
