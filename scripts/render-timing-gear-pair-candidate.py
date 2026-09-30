#!/usr/bin/env python3
from pathlib import Path
import sys
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/('cad/engine/generated/timing-gear-pair-refined' if '--refined' in sys.argv else 'cad/engine/generated/timing-gear-pair-candidate');data=np.load(OUT/'render-input.npz')
fig=plt.figure(figsize=(19,7))
for panel,angle in enumerate([(25,10),(5,0),(0,0)],1):
 ax=fig.add_subplot(1,3,panel,projection='3d')
 for key,color in [('crank','#8b929a'),('cam','#b09263')]:
  tri=data[key+'_vertices'][data[key+'_faces']];normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);el,az=np.radians(angle);eye=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)]);tri=tri[normals@eye>1e-10]
  colors=np.tile(np.array(to_rgb(color)),(len(tri),1));colors[tri[:,:,0].mean(1)<6.85]*=.55
  ax.add_collection3d(Poly3DCollection(tri,facecolors=colors,edgecolor='none',shade=True,antialiased=False))
 ax.set(xlim=(-14,14),ylim=(-50,184),zlim=(-50,164),xlabel='Axial X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((28,234,214));ax.view_init(*angle)
 if panel==3:ax.set(xlim=(-8,8),ylim=(23,44),zlim=(15,37));ax.set_box_aspect((16,21,22));ax.set_title('Estimated timing marks at reference mesh')
fig.suptitle('Independent 58/29 helical pair · uninstalled hypothesis\nComparison envelopes; estimated 2.8 mm transverse module, 25° helix, 121.8 mm center; depth shading clarifies recesses; production profile and axes unknown')
fig.tight_layout();fig.savefig(OUT/'pair-render.png',dpi=150)
