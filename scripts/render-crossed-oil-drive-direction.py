#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/crossed-oil-drive-direction';a=np.load(O/'witness-mesh.npz');fig=plt.figure(figsize=(13,7))
for i,(el,az)in enumerate([(28,-50),(35,125)],1):
 ax=fig.add_subplot(1,2,i,projection='3d')
 for n,col,alpha in [('cam-drive-window','#719e88',.75),('distributor-gear','#7391c6',.65),('overlap','#d13e36',1)]:ax.add_collection3d(Poly3DCollection(a[n+'_v'][a[n+'_f']],facecolor=col,edgecolor='none',alpha=alpha))
 ax.set(xlim=(204,251),ylim=(75,150),zlim=(40,103),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((47,75,63));ax.view_init(el,az)
fig.suptitle('Actual crossed-drive defect at cam +5.625° / distributor −5.625°',fontsize=15)
fig.text(.5,.07,'Green: actual cam drive region. Blue: actual distributor gear. Red:114.105 mm³ intersection.\nBoth frozen gears retain their original signed lead; only the distributor branch datum is translated.',ha='center',fontsize=11)
fig.subplots_adjust(left=0,right=1,top=.9,bottom=.14,wspace=0);fig.savefig(O/'direction-defect-review.png',dpi=170)
files=[Path(__file__),O/'witness-mesh.npz',O/'direction-defect-review.png',O/'witness-bindings.json',R/'inventory/engine/crossed-oil-drive-direction-review.json'];(R/'inventory/engine/crossed-oil-drive-direction-render.json').write_text(json.dumps({'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}},indent=2)+'\n')
