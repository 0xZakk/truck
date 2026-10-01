#!/usr/bin/env python3
from pathlib import Path
import sys,subprocess,json,numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate'
if '--extract' in sys.argv:
 import build123d as b
 parts={n:b.import_step(OUT/(n+'.step')) for n in ['support-0','support-1','pump','bolt-0','bolt-1','pan']};rows={};meshes={}
 for name,q in parts.items():
  rows[name]=[[list(e.position_at(i/80))[:2] for i in range(81)] for e in b.section(q,section_by=b.Plane.XY.offset(-103.21674347274052)).edges()]
  if name!='pan':
   v,f=q.tessellate(.12,.15);meshes[name+'v']=np.array([tuple(x) for x in v]);meshes[name+'f']=np.array(f)
 import trimesh
 glb=trimesh.load(OUT/'block.glb',force='mesh');meshes['block_glbv']=np.asarray(glb.vertices)[:,[0,2,1]]*[1,-1,1]*1000;meshes['block_glbf']=np.asarray(glb.faces)
 (OUT/'sections.json').write_text(json.dumps(rows));np.savez(OUT/'render-meshes.npz',**meshes);sys.exit(0)
subprocess.run([str(ROOT/'.venv-cad/bin/python'),str(Path(__file__)),'--extract'],check=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,7));ax=fig.add_subplot(121,projection='3d');data=np.load(OUT/'render-meshes.npz')
for name,color in [('pump','#9ca5ad'),('support-0','#db9b43'),('support-1','#db9b43'),('bolt-0','#546272'),('bolt-1','#546272')]:
 v=data[name+'v'];f=data[name+'f'];ax.add_collection3d(Poly3DCollection(v[f],facecolors=color,edgecolor='none',alpha=1,shade=True))
allv=np.concatenate([data[k] for k in data.files if k.endswith('v') and k!='block_glbv']);lo=allv.min(0)-5;hi=allv.max(0)+5;ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_zlim(lo[2],hi[2]);ax.set_box_aspect(hi-lo);ax.view_init(24,-40);ax.set_title('Actual STEP mesh: pump, feet, columns and bolts');ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
ax=fig.add_subplot(122);rows=json.loads((OUT/'sections.json').read_text())
for name in ['pan','support-0','support-1']:
 for i,curve in enumerate(rows[name]):
  p=np.array(curve);ax.plot(p[:,0],p[:,1],color='#303030' if name=='pan' else '#b47322',label=name if i==0 else None)
r=json.loads((ROOT/'inventory/engine/timing-pump-foot-pan-witnesses.json').read_text())
for i,w in enumerate(r['witnesses']):ax.plot(*w['cube_center_mm'][:2],'x',color='red',label='old collision witnesses' if i==0 else None)
ax.set_xlim(175,275);ax.set_ylim(88,113);ax.set_aspect('equal');ax.grid(alpha=.25);ax.legend();ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_title('Actual CAD section Z−103.216743 mm\nUnchanged pan; old collision witnesses excluded')
fig.suptitle('Isolated estimated narrower pump feet — 128-segment estimate; no installation acceptance');fig.tight_layout();fig.savefig(OUT/'pump-foot-render.png',dpi=160)

v=data['block_glbv'];f=data['block_glbf'];fig2=plt.figure(figsize=(11,8));ax2=fig2.add_subplot(111,projection='3d');ax2.add_collection3d(Poly3DCollection(v[f],facecolors='#9ea7ad',edgecolor='none',shade=True));lo=v.min(0);hi=v.max(0);ax2.set_xlim(lo[0],hi[0]);ax2.set_ylim(lo[1],hi[1]);ax2.set_zlim(lo[2],hi[2]);ax2.set_box_aspect(hi-lo);ax2.view_init(22,50);ax2.set_title('Actual exported block GLB — isolated faceted foot candidate');ax2.set_xlabel('X mm');ax2.set_ylabel('Y mm');ax2.set_zlabel('Z mm');fig2.tight_layout();fig2.savefig(OUT/'block-glb-review.png',dpi=150)
# Preserve the initial flat overview alongside the shaded review view.
for coll in list(ax2.collections):coll.remove()
ax2.add_collection3d(Poly3DCollection(v[f],facecolors='#9ea7ad',edgecolor='none'));ax2.view_init(22,-50);fig2.savefig(OUT/'block-glb-render.png',dpi=150)
import hashlib
report=ROOT/'inventory/engine/timing-pump-foot-faceted-validation.json';r=json.loads(report.read_text())
for p in [OUT/'pump-foot-render.png',OUT/'block-glb-render.png',OUT/'block-glb-review.png',OUT/'sections.json']:r['artifacts'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
r['input_sha256'][str(Path(__file__).resolve().relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
report.write_text(json.dumps(r,indent=2)+'\n')
