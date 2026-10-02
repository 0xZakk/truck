"""Render actual exported local sensor; no original photo pixels included."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
R=Path(__file__).resolve().parents[1];sys.path.extend(str(p) for p in (R/'.venv-cad/lib').glob('python*/site-packages'))
import trimesh
O=R/'cad/engine/generated/act-online-20261002-specimen';inputs={}
fig,axes=plt.subplots(1,3,figsize=(13,7))
for ax,n,title in zip(axes,[np.array([0.,-1,0]),np.array([.5,-.85,.25]),np.array([0.,0,1.])],['Side • compare5041_2','Oblique • compare5041','Connector • compare5041_CON']):
 n/=np.linalg.norm(n);right=np.array([1.,0,0])-n*n[0];right/=np.linalg.norm(right);up=np.cross(n,right)
 tri=[];colors=[];depth=[]
 for p in sorted(O.glob('act-online-*.glb')):
  inputs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest();m=trimesh.load(p,force='mesh');v=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;m=trimesh.Trimesh(v,m.faces,process=False)
  col='#c3a14f' if 'metal' in p.name else '#e8e9d8'
  if 'contact' in p.name:col='#b9bec2'
  if 'liner' in p.name:col='#343d41'
  if 'encapsulation' in p.name:col='#0584b5'
  light=np.clip(np.abs(m.face_normals@np.array([.3,-.5,.8])),0,1);colors.extend(np.array(to_rgb(col))[None,:]*(.4+.6*light[:,None]));tri.extend(np.stack([v@right,v@up],-1)[m.faces]);depth.extend((v@n)[m.faces].mean(1))
 # Orthographic per-pixel Z buffer; prevents hidden triangles bleeding through curved surfaces.
 points=np.array(tri);cc=np.array(colors);dd=[]
 for p in sorted(O.glob('act-online-*.glb')):
  mm=trimesh.load(p,force='mesh');vv=mm.vertices[:,[0,2,1]]*[1,-1,1]*1000;dd.extend((vv@n)[mm.faces])
 dd=np.array(dd);lo=points.reshape(-1,2).min(0);hi=points.reshape(-1,2).max(0);scale=900/max(hi-lo);W,H=np.ceil((hi-lo)*scale+20).astype(int);pix=np.ones((H,W,3));zbuf=np.full((H,W),-np.inf);pp=(points-lo)*scale+10
 for t,zs,col in zip(pp,dd,cc):
  xmin,ymin=np.maximum(np.floor(t.min(0)).astype(int),0);xmax,ymax=np.minimum(np.ceil(t.max(0)).astype(int),[W-1,H-1])
  x,y=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
  den=(t[1,1]-t[2,1])*(t[0,0]-t[2,0])+(t[2,0]-t[1,0])*(t[0,1]-t[2,1])
  if abs(den)<1e-10:continue
  aa=((t[1,1]-t[2,1])*(x-t[2,0])+(t[2,0]-t[1,0])*(y-t[2,1]))/den;bb=((t[2,1]-t[0,1])*(x-t[2,0])+(t[0,0]-t[2,0])*(y-t[2,1]))/den;zz=aa*zs[0]+bb*zs[1]+(1-aa-bb)*zs[2]
  zb=zbuf[ymin:ymax+1,xmin:xmax+1];mask=(aa>=-1e-8)&(bb>=-1e-8)&(aa+bb<=1+1e-8)&(zz>zb);zb[mask]=zz[mask];pix[ymin:ymax+1,xmin:xmax+1][mask]=col
 ax.imshow(pix,origin='lower');ax.set_axis_off();ax.set_title(title)
fig.suptitle('ACT/IAT local replacement specimen • actual exported GLB\nMTE5041 visual comparison;25mm hex/18TPI supported, other geometry inferred',fontsize=13)
fig.text(.06,.04,'Open guard and blue encapsulation; two recessed contacts and keyed insulator.\nHidden leads/potting/chip absent: incomplete electrical circuit. No host pose, thread gauge or sealing acceptance.',fontsize=10)
fig.subplots_adjust(top=.8,bottom=.18,wspace=.15);p=O/'act-online-20261002-review.png';fig.savefig(p,dpi=160,bbox_inches='tight');plt.close(fig)
(O/'act-online-20261002-render.json').write_text(json.dumps({'inputs':inputs,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'output':str(p.relative_to(R)),'output_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_comparison':'Manufacturer5041_2,5041,5041_CON; originals external; estimated contour/key/guard/encapsulation shape, not pixel-matched production reconstruction'},indent=2)+'\n')
