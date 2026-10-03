"""Repeatable views of actual exported GLBs; no source pixels redistributed."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];sys.path.extend(str(p) for p in (R/'.venv-cad/lib').glob('python*/site-packages'))
import trimesh
O=R/'cad/engine/generated/ho2s-specimen-20261003';report=R/'reference/engine/ho2s-specimen-20261003-validation.json';d=json.loads(report.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meshes={}
for name,row in d['regions'].items():
 p=R/row['glb'];assert sha(p)==d['asset_hashes'][row['glb']]
 g=trimesh.load(p,force='mesh');v=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
 meshes[name]=trimesh.Trimesh(v,g.faces,process=False)
def view(ax,names,normal,title,side=False):
 n=np.array(normal,dtype=float);n/=np.linalg.norm(n)
 right=np.array([0.,0,1]) if side else np.cross([0,0,1.],n);right/=np.linalg.norm(right);up=np.cross(n,right)
 polys=[];colors=[];depths=[]
 lightdir=np.array([.4,-.65,.65]);lightdir/=np.linalg.norm(lightdir)
 for name in names:
  m=meshes[name];xy=np.stack([m.vertices@right,m.vertices@up],axis=-1);polys.append(xy[m.faces]);depths.append((m.vertices@n)[m.faces])
  shade=.40+.60*np.clip(m.face_normals@(n*.7+lightdir*.3),0,1)
  colors.append(np.asarray(d['regions'][name]['color'][:3])[None,:]*shade[:,None])
 polys=np.concatenate(polys);colors=np.concatenate(colors);depths=np.concatenate(depths)
 lo=polys.min(axis=(0,1));hi=polys.max(axis=(0,1));pad=(hi-lo).max()*.035;lo-=pad;hi+=pad
 scale=1100/(hi-lo).max();width,height=np.ceil((hi-lo)*scale).astype(int)
 pix=(polys-lo)*scale;rgb=np.ones((height,width,3));depthbuffer=np.full((height,width),-np.inf)
 # True per-pixel depth resolves internal/back surfaces and long triangles.
 for tri,zz,color in zip(pix,depths,colors):
  xmin,ymin=np.maximum(np.floor(tri.min(0)).astype(int),0);xmax,ymax=np.minimum(np.ceil(tri.max(0)).astype(int),[width-1,height-1])
  if xmax<xmin or ymax<ymin:continue
  x0,y0=tri[0];x1,y1=tri[1];x2,y2=tri[2];den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
  if abs(den)<1e-10:continue
  xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
  aa=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/den;bb=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/den;cc=1-aa-bb
  depth=aa*zz[0]+bb*zz[1]+cc*zz[2];prior=depthbuffer[ymin:ymax+1,xmin:xmax+1]
  mask=(aa>=-1e-8)&(bb>=-1e-8)&(cc>=-1e-8)&(depth>prior)
  prior[mask]=depth[mask];rgb[ymin:ymax+1,xmin:xmax+1][mask]=color
 ax.imshow(rgb,origin='lower',extent=[lo[0],hi[0],lo[1],hi[1]],interpolation='bilinear');ax.set_aspect('equal');ax.set_axis_off();ax.set_title(title,fontsize=11)

output=[]
for frame in ['sensor','connector']:
 names=[k for k,v in d['regions'].items() if v['frame']==frame]
 fig=plt.figure(figsize=(14,9));gs=fig.add_gridspec(2,3,height_ratios=[1,1.7]);ax=fig.add_subplot(gs[0,:]);view(ax,names,(0,1,0),'Side: actual exported geometry; dimensions in the contract are estimates except 22 mm hex',True)
 for i,(normal,title) in enumerate([((.6,1,.9),'Front oblique / latch'),((.6,1,-.9),'Rear oblique / wire exits'),((0,-.001,1),'Axial mouth / protective tip')]):view(fig.add_subplot(gs[1,i]),names,normal,title)
 fig.suptitle('Bosch 15718 / 0258005718 — '+frame+' exterior study\nSeparate material regions; no host pose, full cable route or target internals',fontsize=15)
 fig.text(.05,.035,'Source comparison: manufacturer front / right / rear photographs, hashes in prior evidence ledger.\nOpen slots, stepped wire exit and four contacts are depicted; hidden dimensions and connector mating geometry remain educational estimates.',fontsize=10)
 fig.subplots_adjust(top=.84,bottom=.13,hspace=.16,wspace=.16)
 p=O/(frame+'-review.png');fig.savefig(p,dpi=150);plt.close(fig);output.append(p)
# Close view intentionally exposes actual thread valleys and cap passages.
fig,ax=plt.subplots(figsize=(12,5));view(ax,['mounting-shell','seat-ring','slotted-protective-cap'],(.4,-1,.3),'Actual GLB: helical ridge and open long slots (all thread details inferred)')
fig.tight_layout();p=O/'thread-cap-review.png';fig.savefig(p,dpi=150);plt.close(fig);output.append(p)
(O/'render.json').write_text(json.dumps({'inputs':{str(report.relative_to(R)):sha(report),str(Path(__file__).relative_to(R)):sha(Path(__file__)),**{v['glb']:d['asset_hashes'][v['glb']] for v in d['regions'].values()}},'outputs':{str(p.relative_to(R)):sha(p) for p in output},'environment':{'python':sys.version,'numpy':np.__version__,'matplotlib':matplotlib.__version__},'method':'Per-pixel depth-buffered orthographic triangles from actual GLBs converted to CAD mm; source originals excluded'},indent=2)+'\n')
print('\n'.join(str(p) for p in output))
