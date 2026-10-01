from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pump-rear-flange-candidate'
if '--extract' in sys.argv:
 import build123d as b,trimesh
 data={}
 for name in ['housing','pump-gasket','cover','main-gasket']:
  mesh=trimesh.load(O/(name+'.glb'),force='mesh');data[name+'_vertices']=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;data[name+'_faces']=mesh.faces
  shape=b.import_step(O/(name+'.step'));section=b.section(shape,b.Plane.YZ.offset(376 if name in ['housing','cover'] else 374 if name=='pump-gasket' else 373.4));edges=[np.array([tuple(e.position_at(t))for t in np.linspace(0,1,80)])for e in section.edges()]
  if edges:data[name+'_edges']=np.array(edges)
 np.savez_compressed(O/'review-data.npz',**data);sys.exit(0)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb
D=np.load(O/'review-data.npz');fig=plt.figure(figsize=(14,7));ax=fig.add_subplot(121,projection='3d');colors={'cover':'#b85a43','main-gasket':'#e6bb64','housing':'#4786ad','pump-gasket':'#68a477'}
for name,color in colors.items():
 v=D[name+'_vertices'];f=D[name+'_faces'];t=v[f];n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12);light=.35+.65*np.abs(n@np.array([.8,-.3,.52]));fc=np.array(to_rgb(color))*light[:,None];ax.add_collection3d(Poly3DCollection(t,facecolors=fc,edgecolor='none'))
ax.set(xlim=(350,485),ylim=(-155,275),zlim=(-70,260));ax.set_box_aspect((135,430,330));ax.view_init(elev=12,azim=12);ax.set_title('Actual saved meshes — inlet conflict remains');ax.set_xlabel('X');ax.set_ylabel('Y');ax.set_zlabel('Z')
bx=fig.add_subplot(122)
for name in ['housing','cover','pump-gasket','main-gasket']:
 for i,e in enumerate(D[name+'_edges']):bx.plot(e[:,1],e[:,2],color=colors[name],label=name if i==0 else None,lw=1.5)
bx.set(xlim=(-35,40),ylim=(88,142),xlabel='Y mm',ylabel='Z mm',title='Rear sections: housing/cover X376; gasket midplanes');bx.set_aspect('equal');bx.grid(alpha=.2);bx.legend();fig.tight_layout();p=O/'review.png';fig.savefig(p,dpi=160);plt.close(fig)
r={'image':str(p.relative_to(R)),'image_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inputs':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in [Path(__file__),O/'review-data.npz',*O.glob('*.step'),*O.glob('*.glb')]}};(R/'inventory/engine/timing-pump-rear-flange-visual-review.json').write_text(json.dumps(r,indent=2)+'\n')
