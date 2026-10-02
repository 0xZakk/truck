"""Depth-buffered actual GLB views; no source-image redistribution."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from engine_qc_raster import rasterize
R=Path(__file__).resolve().parents[1]
sys.path.extend(str(p) for p in (R/'.venv-cad/lib').glob('python*/site-packages'))
import trimesh
O=R/'cad/engine/generated/airbox-refined-20261002';OLD=R/'cad/engine/generated/online-airbox-duct-specimen'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={};fig,axes=plt.subplots(3,1,figsize=(15,11));views=[]
for ax,folder,n,title in zip(axes,[OLD,O,O],[np.array([0.,0.,1.]),np.array([0.,0.,1.]),np.array([-.25,-.45,.857])],['Frozen baseline · actual mesh','Refined local candidate · same plan camera','Refined candidate · oblique view of cuffs, channel and bridge']):
 n/=np.linalg.norm(n);right=np.array([1.,0,0])-n*n[0];right/=np.linalg.norm(right);up=np.cross(n,right)
 tris=[];cols=[]
 for p in sorted(folder.glob('online-*.glb')):
  inputs[str(p.relative_to(R))]=sha(p);m=trimesh.load(p,force='mesh');v=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
  tri=v[m.faces];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1,keepdims=True),1e-15)
  light=.4+.6*np.abs(norm@np.array([.2,-.3,.93]));base=np.array([.24,.28,.29]) if 'clamp-' not in p.name else np.array([.45,.52,.55])
  tris.append(tri@np.array([right,-up,n]).T);cols.append(base[None,:]*light[:,None])
 tri=np.concatenate(tris);colors=np.concatenate(cols);del tris,cols
 # Same metric scale and center for before/after; oblique uses same scale.
 tri[:,:,:2]=(tri[:,:,:2]-np.array([279.5,0]))*2.4+np.array([750,250])
 pixels=rasterize(tri,colors,1500,500);ax.imshow(pixels);ax.set_axis_off();ax.set_title(title)
 views.append({'folder':str(folder.relative_to(R)),'camera':n.tolist(),'pixels_per_mm':2.4})
fig.suptitle('Paired intake duct contour refinement — actual exported geometry\nSource specimen photos4/6/12 support topology; all numeric contours remain estimates',fontsize=14)
fig.text(.05,.02,'Rounded crests, bulged cuffs, gradual shoulders and shaped web/channel replace the earlier geometric simplifications.\nCircular insertion profiles remain unverified; no installed reach, material compliance or engine fit is claimed.',fontsize=10)
fig.subplots_adjust(top=.89,bottom=.08,hspace=.23)
p=O/'airbox-refined-20261002-source-view.png';fig.savefig(p,dpi=140,bbox_inches='tight');plt.close(fig)
inputs.update({str(q.relative_to(R)):sha(q) for q in [Path(__file__),R/'scripts/engine_qc_raster.py']})
(O/'airbox-refined-20261002-render.json').write_text(json.dumps({'inputs':inputs,'output_sha256':sha(p),'views':views,'method':'Depth-buffered actual GLB triangles at fixed metric scale; no omitted faces or source pixels'},indent=2)+'\n');print(p)
