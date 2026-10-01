"""Render actual staged local GLBs through serialized occurrence transforms."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
O=R/'cad/engine/generated/timing-front-coordinated-stage';pp=R/'inventory/engine/timing-front-coordinated-patch.json';m=json.loads((R/'inventory/engine/full-assembly.json').read_text());patch=json.loads(pp.read_text());report=json.loads((R/'inventory/engine/timing-front-coordinated-stage-validation.json').read_text())
if '--extract' in sys.argv:
 import trimesh
 from assembly_math import transforms
 for group in ['definitions','occurrences']:
  index={q['id']:i for i,q in enumerate(m[group])}
  for change in patch[group]:
   if change['before']is None:m[group].append(change['after'])
   else:m[group][index[change['id']]]=change['after']
 poses=transforms(m);parts={p['id']:p for p in report['parts']};meshes={}
 for name in ['block','timing-cover','oil-pan','oil-pan-molded-gasket']+[f'timing-cover-mounting-screw-{i}'for i in range(1,8)]:
  ident='timing-cover-mounting-screw'if name.startswith('timing-cover-mounting-screw-')else name;mesh=trimesh.load(R/parts[ident]['glb'],force='mesh');v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;t=poses[name].wrapped.Transformation();rot=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);trans=np.array([t.Value(i,4)for i in range(1,4)]);meshes[name]=(v@rot.T+trans,mesh.faces)
 np.savez_compressed(O/'serialized-world-meshes.npz',**{n+'__'+k:a for n,(v,f)in meshes.items()for k,a in [('v',v),('f',f)]})
 raise SystemExit
a=np.load(O/'serialized-world-meshes.npz');meshes={k[:-3]:(a[k],a[k[:-3]+'__f'])for k in a.files if k.endswith('__v')}
parts={p['id']:p for p in report['parts']}
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
camera=np.array([1,-1,.4]);camera/=np.linalg.norm(camera);right=np.cross([0,0,1],camera);right/=np.linalg.norm(right);up=np.cross(camera,right);basis=np.array([right,up,camera]).T
colors={'block':'#477176','timing-cover':'#9eaeb4','oil-pan':'#42686c','oil-pan-molded-gasket':'#dda34c'}
def draw(ax,names):
 triangles=[];colorset=[]
 for n in names:
  v,f=meshes[n];t=v[f];normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);keep=normal@camera>0;t=t[keep];normal=normal[keep];triangles.append(t@basis);colorset.append((.3+.7*np.clip(normal@camera,0,1))[:,None]*to_rgb(colors.get(n,'#c39a57')))
 t=np.concatenate(triangles);col=np.concatenate(colorset);order=np.argsort(t[:,:,2].mean(1));ax.add_collection(PolyCollection(t[order,:,:2],facecolors=col[order],edgecolors='none'));p=t[:,:,:2].reshape(-1,2);lo=p.min(0);hi=p.max(0);pad=max(hi-lo)*.04;ax.set_xlim(lo[0]-pad,hi[0]+pad);ax.set_ylim(lo[1]-pad,hi[1]+pad);ax.set_aspect('equal');ax.axis('off')
fig,axes=plt.subplots(1,2,figsize=(16,8));draw(axes[0],list(meshes));draw(axes[1],['timing-cover']+[f'timing-cover-mounting-screw-{i}'for i in range(1,8)]);axes[0].set_title('Actual staged block, cover, pan, gasket and seven screws\nReconstructed serialized world transforms; no display offsets');axes[1].set_title('Cover and seven recessed comparison fasteners\nOther parts hidden only for this view');fig.suptitle('Coordinated front integration candidate — estimates retained; required seal/gasket dependencies separate');fig.tight_layout(rect=[0,0,1,.94]);p=O/'stage-review.png';fig.savefig(p,dpi=160);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'render':str(p.relative_to(R)),'sha256':sha(p),'inputs_sha256':{str(x.relative_to(R)):sha(x)for x in [pp,Path(__file__),*[R/p['glb']for p in parts.values()]]}};(R/'inventory/engine/timing-front-coordinated-stage-visual.json').write_text(json.dumps(r,indent=2)+'\n')
