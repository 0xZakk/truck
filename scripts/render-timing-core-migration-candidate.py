#!/usr/bin/env python3
"""Actual exported-mesh views; no synthetic model imagery."""
from pathlib import Path
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-core-migration-candidate'
d=np.load(OUT/'render-input.npz');ids=[k[:-9] for k in d.files if k.endswith('_vertices')]
fig=plt.figure(figsize=(18,7))
for i,(el,az) in enumerate([(20,-65),(20,10),(10,175)],1):
 ax=fig.add_subplot(1,3,i,projection='3d')
 for name in ids:
  if i==3 and name in ['camshaft','cam-timing-gear','crank-timing-gear']:continue
  tri=d[name+'_vertices'][d[name+'_faces']]
  if i>1:tri=tri[tri[:,:,0].min(1)>350]
  if not len(tri):continue
  normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);e,a=np.radians([el,az]);eye=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
  tri=tri[normals@eye>1e-10]
  if not len(tri):continue
  color='#b09263' if 'gear' in name and 'spacer' not in name else '#789caa' if name=='camshaft' else '#c4c9ce' if 'bearing' in name else '#a38a69' if 'plug' in name else '#748395'
  ax.add_collection3d(Poly3DCollection(tri,facecolors=color,edgecolor='none',shade=True,antialiased=False))
 if i==1:ax.set(xlim=(-390,408),ylim=(-50,182),zlim=(-48,165));ax.set_box_aspect((798,232,213));ax.set_title('Complete translated core; fixed crank gear')
 else:ax.set(xlim=(355,405),ylim=(-48,182),zlim=(-48,165));ax.set_box_aspect((50,230,213));ax.set_title('Front gear/key side' if i==2 else 'Retention detail; gears/shaft hidden')
 ax.set(xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.view_init(el,az)
fig.suptitle('Isolated timing-core migration · 121.8 mm same-ray hypothesis\nExisting axial stations and local shapes; refined 58/29 gears · no block/cover adaptation or installed acceptance')
fig.tight_layout();fig.savefig(OUT/'timing-core-render.png',dpi=160)
