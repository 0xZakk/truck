"""Render exported assets; no source pixels or conceptual replacement drawing."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1]
sys.path.extend(str(p) for p in (R/'.venv-cad/lib').glob('python*/site-packages'))
import trimesh
O=R/'cad/engine/generated/online-airbox-duct-specimen'
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
fig,axes=plt.subplots(2,1,figsize=(15,9));inputs={}
for ax,(n,title) in zip(axes,[(np.array([0.,0.,1.]),'Plan view: large cuffs at left, narrow cuffs at right'),(np.array([-.25,-.45,.857]),'Oblique view: open cuffs, external web and retainer')]):
 n=n/np.linalg.norm(n);right=np.array([1.,0,0])-n*n[0];right/=np.linalg.norm(right);up=np.cross(n,right)
 triangles=[];colors=[];depth=[]
 for p in sorted(O.glob('online-*.glb')):
  inputs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
  m=trimesh.load(p,force='mesh');v=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
  color='#3c4447' if 'duct-' in p.name else '#7b878d'
  if 'joining' in p.name:color='#465458'
  if 'retainer' in p.name:color='#50656b'
  mesh=trimesh.Trimesh(v,m.faces,process=False)
  light=np.clip(np.abs(mesh.face_normals@np.array([.2,-.3,.9])),0,1)
  colors.extend(np.array(to_rgb(color))[None,:]*(.45+.55*light[:,None]))
  triangles.extend(np.stack([v@right,v@up],axis=-1)[m.faces]);depth.extend((v@n)[m.faces].mean(1))
 order=np.argsort(depth);triangles=np.array(triangles)[order];colors=np.array(colors)[order]
 ax.add_collection(PolyCollection(triangles,facecolors=colors,edgecolors='none',rasterized=True))
 ax.autoscale_view();ax.set_aspect('equal');ax.set_axis_off();ax.set_title(title)
fig.subplots_adjust(top=.83,bottom=.12,hspace=.35)
fig.suptitle('Local paired-duct specimen — actual exported mesh\nTopology informed by E7TE-9R504-AF photos; numeric sections, wall and free-state shape estimated',fontsize=14)
fig.text(.06,.035,'Compare with eBay 196038453283 photos 4 / 6 / 12: unequal branches, local bellows, long smooth ends, web, four clamps.\n559 / 533 mm are selected projected spans within broad tape estimates; no installed reach, engine fit or original wall specification.',fontsize=10)
p=O/'source-view-review.png';fig.savefig(p,dpi=150,bbox_inches='tight');plt.close(fig)
(O/'render.json').write_text(json.dumps({'inputs':inputs,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'Actual exported runtime GLB meshes restored to CAD mm; orthographic views; source originals not included'},indent=2)+'\n')
print(p)
