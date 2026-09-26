from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[3];D=R/'inventory/engine/pilot/throttle-bracket';a=np.load(D/'preview.npz');names=json.loads(str(a['metadata']))
fig=plt.figure(figsize=(14,6))
for col,(el,az) in enumerate([(25,-45),(20,130)],1):
 ax=fig.add_subplot(1,2,col,projection='3d')
 for i,name in enumerate(names):
  if name not in ['bracket','throttle-housing','candidate-shifted-nut-464.0','candidate-shifted-nut-516.0','stud-464.0','stud-516.0']:continue
  tri=a[f'v{i}'][a[f'f{i}']];ax.add_collection3d(Poly3DCollection(tri,facecolor='#cd9b38' if name=='bracket' else '#8b9ba3',edgecolor='#333333',alpha=1 if name=='bracket' else .18,linewidth=.12))
 ax.set(xlim=(360,475),ylim=(-45,130),zlim=(450,530),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((115,175,80));ax.view_init(el,az)
fig.suptitle('Photo-informed bracket candidate (gold), accepted throttle context (gray)');fig.tight_layout();fig.savefig(D/'candidate-context.png',dpi=160)
fig=plt.figure(figsize=(10,7));ax=fig.add_subplot(111,projection='3d');tri=a['v0'][a['f0']];ax.add_collection3d(Poly3DCollection(tri,facecolor='#cd9b38',edgecolor='#333333',linewidth=.2));ax.set(xlim=(370,470),ylim=(64,130),zlim=(450,530),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((100,66,80));ax.view_init(24,130);fig.savefig(D/'candidate-alone.png',dpi=150)
