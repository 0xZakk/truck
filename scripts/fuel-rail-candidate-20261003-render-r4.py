from pathlib import Path
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r4'
fig=plt.figure(figsize=(16,12))
for row,label in enumerate(['plus','minus']):
 for col,context in enumerate([False,True]):
  ax=fig.add_subplot(2,2,row*2+col+1,projection='3d');folder=OUT/label
  for name,color in [('fuel-supply-rail','#7895a5'),('fuel-return-tube','#cb863e'),('regulator-vacuum-hose','#444444')]:
   mesh=np.load(folder/('local-'+name+('.npz' if name.endswith('repaired') else '-mesh.npz')));v=mesh['vertices_cad_mm']
   ax.add_collection3d(Poly3DCollection(v[mesh['faces']],facecolor=color,linewidth=0,rasterized=True))
  for name in ['regulator-upper-housing','regulator-lower-housing','fuel-supply-coupling-male','fuel-return-coupling-male']:
   d=np.load(folder/(name+'-mesh.npz'));ax.add_collection3d(Poly3DCollection(d['vertices_cad_mm'][d['faces']],facecolor='#abb0b5',linewidth=0,rasterized=True))
  if context:
   for name in ['efi-upper-intake','efi-lower-intake']:
    d=np.load(ROOT/'cad/engine/generated/intake-joint-candidate-20261003'/(name+'-mesh.npz'));key='vertices_cad_mm' if 'vertices_cad_mm' in d else 'vertices';ax.add_collection3d(Poly3DCollection(d[key][d['faces']],facecolor='#a8bd99',alpha=.20,linewidth=0,rasterized=True))
  lo=np.array([-380,-260,335]);hi=np.array([330,20 if context else -100,520 if context else 465]);ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),zlim=(lo[2],hi[2]),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title=label+' transverse study — '+('frozen intake context' if context else 'actual exported fuel components'));ax.set_box_aspect(hi-lo);ax.view_init(elev=45,azim=-65)
fig.suptitle('Both approved hypotheses — dimensions estimated, neither selected or integration-ready',fontsize=15);fig.tight_layout();fig.savefig(OUT/'actual-export-context.png',dpi=145)
