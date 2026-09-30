#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-thrust-land-candidate';d=np.load(OUT/'render-input.npz')
ids=[k[:-9] for k in d.files if k.endswith('_vertices') and not k.startswith('section_')]
fig=plt.figure(figsize=(18,7));colors={'camshaft':'#6d98ac','cam-timing-gear':'#b6955c','cam-thrust-plate':'#708085','cam-gear-spacer':'#acbac1'}
for i,(el,az) in enumerate([(15,10),(15,175),(0,90)],1):
 if i==3:
  ax=fig.add_subplot(1,3,i)
  for name,color in colors.items():
   key='section_'+name;tri=d[key+'_vertices'][d[key+'_faces']]
   tri=tri[np.max(abs(tri[:,:,1]-95.1098209901611),axis=1)<1e-5]
   ax.add_collection(PolyCollection(tri[:,:,[0,2]],facecolors=color,edgecolors='none',label=name))
  ax.set(xlim=(370,389),ylim=(90,105),xlabel='Axial X mm',ylabel='Z mm');ax.set_aspect('equal');ax.grid(alpha=.2)
  ax.set_title('Actual CAD section at Y=95.109821, travel 0\nBlue shaft / gray plate / gold gear land')
  ax.annotate('0.1 mm face gap',xy=(378.21,100.5),xytext=(381,103.5),arrowprops={'arrowstyle':'->'},fontsize=9)
  continue
 ax=fig.add_subplot(1,3,i,projection='3d')
 for name in ids:
  if i==2 and name!='cam-timing-gear':continue
  if i==3 and name not in colors:continue
  key=('section_' if i==3 else '')+name
  tri=d[key+'_vertices'][d[key+'_faces']]
  if i==1:tri=tri[tri[:,:,0].min(1)>350]
  if not len(tri):continue
  normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);e,a=np.radians([el,az]);eye=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
  tri=tri[normals@eye>1e-10]
  if not len(tri):continue
  ax.add_collection3d(Poly3DCollection(tri,facecolors=colors.get(name,'#abb3b8'),edgecolor='none',shade=True,antialiased=False))
 if i<3:
  ax.set(xlim=(350,405),ylim=(-48,182) if i==1 else (8,182),zlim=(-48,165) if i==1 else (-10,165));ax.set_box_aspect((55,230 if i==1 else 174,213 if i==1 else 175))
  ax.set_title('Coordinated front core' if i==1 else 'Actual revised gear back; estimated annular land')
 else:
  ax.set(xlim=(370,389),ylim=(94.9,95.2),zlim=(90,105));ax.set_box_aspect((19,.3,15));ax.set_title('Actual axial section at travel 0\nBlue shaft / gray plate / gold gear land')
 ax.set(xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.view_init(el,az)
fig.suptitle('Estimated BACK thrust-land revision · uninstalled candidate\nR20.65–26 mm; provisional axial travel −0.1..0 mm · factory backside unknown; original failed core preserved')
fig.tight_layout();fig.savefig(OUT/'thrust-land-render.png',dpi=160)
