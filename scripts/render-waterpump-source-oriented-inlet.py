from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/waterpump-source-oriented-inlet-candidate'
if '--extract'in sys.argv:
 import trimesh
 data={}
 paths={k:O/(k+'-housing.glb')for k in ['nominal','low-angle','high-angle']};paths['cover']=R/'cad/engine/generated/timing-pump-rear-flange-candidate/cover.glb'
 for k,p in paths.items():
  m=trimesh.load(p,force='mesh');data[k+'_v']=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;data[k+'_f']=m.faces
 np.savez_compressed(O/'review-data.npz',**data);sys.exit(0)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb
D=np.load(O/'review-data.npz');fig=plt.figure(figsize=(17,6))
for i,k in enumerate(['nominal','low-angle','high-angle'],1):
 ax=fig.add_subplot(1,3,i,projection='3d')
 for n,color in [('cover','#b36c4a'),(k,'#4b88b6')]:
  t=D[n+'_v'][D[n+'_f']];normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-12);light=.3+.7*np.abs(normal@np.array([.8,-.3,.52]));ax.add_collection3d(Poly3DCollection(t,facecolors=np.array(to_rgb(color))*light[:,None],edgecolor='none'))
 ax.set(xlim=(360,515),ylim=(-175,275),zlim=(-70,260));ax.set_box_aspect((155,450,330));ax.view_init(elev=8,azim=6);ax.set_title(k+' — actual saved meshes');ax.set_xlabel('X');ax.set_ylabel('Y');ax.set_zlabel('Z')
fig.suptitle('Orientation-only trial: physical nominal fit passes; tool and endpoint failures retained');fig.tight_layout();p=O/'review.png';fig.savefig(p,dpi=150);(R/'inventory/engine/waterpump-source-oriented-inlet-visual.json').write_text(json.dumps({'image':str(p.relative_to(R)),'image_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inputs':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in [Path(__file__),O/'review-data.npz',*O.glob('*.glb')]}},indent=2)+'\n')
