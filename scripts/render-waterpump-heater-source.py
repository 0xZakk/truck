from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/waterpump-heater-source-candidate'
if '--extract'in sys.argv:
 import trimesh
 data={}
 paths={k:O/(k+'.glb')for k in ['housing','tube']};paths['cover']=R/'cad/engine/generated/timing-pump-rear-flange-candidate/cover.glb'
 for k,p in paths.items():
  m=trimesh.load(p,force='mesh');data[k+'_v']=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;data[k+'_f']=m.faces
 np.savez_compressed(O/'review-data.npz',**data);sys.exit(0)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
D=np.load(O/'review-data.npz');fig=plt.figure(figsize=(16,8));ax=fig.add_subplot(121,projection='3d');side=fig.add_subplot(122)
for n,color in [('cover','#b36c4a'),('housing','#4b88b6'),('tube','#c0b775')]:
 t=D[n+'_v'][D[n+'_f']];normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-12);light=.3+.7*np.abs(normal@np.array([.8,-.3,.52]));colors=np.array(to_rgb(color))*light[:,None];ax.add_collection3d(Poly3DCollection(t,facecolors=colors,edgecolor='none'))
 if n!='cover':side.add_collection(PolyCollection(t[:,:,[1,2]],facecolors=colors,edgecolor='none',alpha=.75))
j=json.loads((R/'inventory/engine/waterpump-heater-source-registration.json').read_text())
for name,col in [('front','green'),('rear','purple')]:
 p=np.array(j['source_fits'][name]['model_yz_NOT_MEASURED'])+[-32,170];side.plot(p[:,0],p[:,1],'o--',color=col,label=name+' photo projected landmarks')
side.plot(-132,270,'rx',markersize=10,label='old unsourced boundary');side.set(xlim=(-210,70),ylim=(30,455),xlabel='World Y mm (estimated scale)',ylabel='World Z mm');side.set_aspect('equal');side.legend(fontsize=8);side.set_title('Actual mesh projection and uncalibrated source landmarks');side.grid(alpha=.3)
ax.set(xlim=(220,520),ylim=(-205,280),zlim=(-65,440));ax.set_box_aspect((300,485,505));ax.view_init(elev=15,azim=18);ax.set_title('Actual saved coordinated solids');ax.set_xlabel('X');ax.set_ylabel('Y');ax.set_zlabel('Z');fig.suptitle('Heater root/tube study — projected coordinates and revised free boundary are estimates');fig.tight_layout();p=O/'review.png';fig.savefig(p,dpi=150)
inputs=[Path(__file__),O/'review-data.npz',R/'inventory/engine/waterpump-heater-source-registration.json',*O.glob('*.glb')];(R/'inventory/engine/waterpump-heater-source-visual.json').write_text(json.dumps({'image':str(p.relative_to(R)),'image_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inputs':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in inputs}},indent=2)+'\n')
