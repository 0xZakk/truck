#!/usr/bin/env python3
"""Render authored actual-CAD collision meshes; no source originals."""
from pathlib import Path
import json,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/intake-joint-validation-20261003';report=json.loads((OUT/'fuel-return-conflict.json').read_text());bounds=np.array(report['intersection_bounds_mm']);mid=bounds.mean(0)
fig=plt.figure(figsize=(14,6))
for index,zoom in enumerate([False,True],1):
 ax=fig.add_subplot(1,2,index,projection='3d')
 for name,color,alpha in [('candidate-upper',[.55,.65,.70],.25),('fuel-return-tube',[.80,.40,.10],1),('intersection',[.85,.05,.03],1)]:
  if zoom and name=='fuel-return-tube':continue
  data=np.load(OUT/(name+'.npz'));vv=data['vertices'];faces=data['faces'];tri=vv[faces]
  if zoom:tri=tri[(tri.max(1)[:,0]>mid[0]-45)&(tri.min(1)[:,0]<mid[0]+45)&(tri.max(1)[:,1]>mid[1]-40)&(tri.min(1)[:,1]<mid[1]+40)&(tri.max(1)[:,2]>mid[2]-30)&(tri.min(1)[:,2]<mid[2]+35)]
  poly=Poly3DCollection(tri,facecolor=color,edgecolor='none',alpha=alpha,rasterized=True);ax.add_collection3d(poly)
 if zoom:
  ax.plot([-345,-285],[-190,-190],[370,370],color='#ca6519',linestyle='--',linewidth=1,label='Tube axis; tube hidden to expose intersection')
  ax.legend(fontsize=7,loc='lower left')
  lo=mid-np.array([45,40,30]);hi=mid+np.array([45,40,35])
 else:lo=np.array([-365,-280,340]);hi=np.array([340,105,540])
 ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),zlim=(lo[2],hi[2]),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title='Conflict detail' if zoom else 'Upper casting and installed return tube');ax.set_box_aspect(hi-lo);ax.view_init(elev=32,azim=-65)
fig.suptitle('Actual CAD intersection295.587mm³ shown red — candidate remains unaccepted',fontsize=13);fig.tight_layout();fig.savefig(OUT/'fuel-return-conflict.png',dpi=160)
