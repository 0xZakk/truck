from pathlib import Path
import numpy as np,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/online-heater-route-candidate';D=np.load(O/'review-data.npz')
fig=plt.figure(figsize=(15,7));ax=fig.add_subplot(121,projection='3d');side=fig.add_subplot(122)
for n,col in [('housing','#5885a1'),('old','#b95644'),('new','#ceb651')]:
 t=D[n+'_v'][D[n+'_f']];normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-12);colors=np.array(to_rgb(col))*(.3+.7*np.abs(normal@np.array([.8,-.3,.52])))[:,None]
 ax.add_collection3d(Poly3DCollection(t,facecolors=colors,edgecolor='none',alpha=.85))
 side.add_collection(PolyCollection(t[:,:,[0,2]],facecolors=colors,edgecolor='none',alpha=.75))
ax.set(xlim=(215,520),ylim=(-210,70),zlim=(85,435));ax.set_box_aspect((305,280,350));ax.view_init(elev=20,azim=25);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm');ax.set_title('Actual saved STEP-derived meshes')
side.set(xlim=(215,525),ylim=(85,435),xlabel='World X mm',ylabel='World Z mm');side.set_aspect('equal');side.grid(alpha=.3);side.axvline(375,color='k',ls='--',lw=1);side.set_title('Gold: axial hypothesis / red: frozen failed tube')
fig.suptitle('New GMB side-view axial hypothesis — retained radial route is unregistered\nAll tube dimensions inferred; no full 3D source match or installation acceptance',fontsize=13);fig.tight_layout();p=O/'review.png';fig.savefig(p,dpi=150)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(R/'inventory/engine/online-heater-route-visual.json').write_text(json.dumps({'image':str(p.relative_to(R)),'image_sha256':sha(p),'inputs':{str(q.relative_to(R)):sha(q)for q in [Path(__file__),O/'review-data.npz',R/'inventory/engine/online-heater-route-export.json']}},indent=2)+'\n')
