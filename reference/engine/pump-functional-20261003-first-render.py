from pathlib import Path
import numpy as np,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];p=R/'reference/engine/pump-functional-20261003-render-data.npz';d=np.load(p);names=[k[:-10]for k in d if k.endswith('__vertices')]
fig=plt.figure(figsize=(16,9))
panels=[('Rear attachment / +X view',0,180),('Side / chamber and short tower',0,90),('Front-quarter actual mesh',25,-35),('Actual v4 affected neighbors',22,145)]
colors={'water-pump-housing':'#9bbdc0','heater-pump-return-elbow':'#c3a261','water-pump-impeller':'#899398','water-pump-gasket':'#927247','water-pump-drive-hub':'#bf834b','water-pump-pulley':'#344966'}
neighbor=['timing-cover','timing-cover-mounting-screw-3','thermactor-engine-bolt-1','alternator-thermactor-common-carrier']
for k,(title,elev,azim)in enumerate(panels):
 ax=fig.add_subplot(2,2,k+1,projection='3d')
 for n in names:
  if k<3 and(n in neighbor or n in ['water-pump-pulley','water-pump-shaft']):continue
  vs=d[n+'__vertices'];fs=d[n+'__faces'];tris=vs[fs]
  ax.add_collection3d(Poly3DCollection(tris,facecolor=colors.get(n,'#9c7ca1'if n not in neighbor else'#c66b5b'),edgecolor='none',alpha=.75 if n in neighbor else 1))
 ax.set(xlim=(345,495),ylim=(-190,65),zlim=(65,425),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
 ax.set_box_aspect((150,255,360));ax.view_init(elev,azim);ax.set_proj_type('ortho');ax.set_title(title)
fig.suptitle('Functional-region pump candidate — 98.43mm mounting-to-hub face\nEstimated casting/ports; actual five neighbor conflicts retained; spring omitted from these external views')
fig.tight_layout();out=R/'reference/engine/pump-functional-20261003-review.png';fig.savefig(out,dpi=135)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(R/'reference/engine/pump-functional-20261003-render.json').write_text(json.dumps({'image':str(out.relative_to(R)),'sha256':sha(out),'data_sha256':sha(p),'script_sha256':sha(Path(__file__)),'source_pixels_excluded':True,'scope':'actual exported candidate surfaces; actual v4 neighbor STEP tessellation; orthographic comparison views not camera registration'},indent=2)+'\n')
