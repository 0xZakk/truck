#!/usr/bin/env python3
from pathlib import Path
import sys,subprocess,json,numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-pump-foot-candidate'
if '--extract' in sys.argv:
 import build123d as b
 parts={n:b.import_step(OUT/(n+'.step')) for n in ['support-0','support-1','pump','bolt-0','bolt-1','pan']};rows={};meshes={}
 for name,q in parts.items():
  rows[name]=[[list(e.position_at(i/80))[:2] for i in range(81)] for e in b.section(q,section_by=b.Plane.XY.offset(-103.21674347274052)).edges()]
  if name!='pan':
   meshes[name+'edges']=np.array([[list(e.position_at(i/80)) for i in range(81)] for e in q.edges()])
 (OUT/'sections.json').write_text(json.dumps(rows));np.savez(OUT/'render-meshes.npz',**meshes);sys.exit(0)
subprocess.run([str(ROOT/'.venv-cad/bin/python'),str(Path(__file__)),'--extract'],check=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,7));ax=fig.add_subplot(121,projection='3d');data=np.load(OUT/'render-meshes.npz')
for name,color in [('pump','#9ca5ad'),('support-0','#db9b43'),('support-1','#db9b43'),('bolt-0','#546272'),('bolt-1','#546272')]:

 for edge in data[name+'edges']:ax.plot(edge[:,0],edge[:,1],edge[:,2],color=color,linewidth=.5)
ax.set_xlim(175,272);ax.set_ylim(45,150);ax.set_zlim(-145,0);ax.set_box_aspect((97,105,145));ax.view_init(24,-40);ax.set_title('Actual STEP edges: pump, feet, columns and bolts');ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
ax=fig.add_subplot(122);rows=json.loads((OUT/'sections.json').read_text())
for name in ['pan','support-0','support-1']:
 for i,curve in enumerate(rows[name]):
  p=np.array(curve);ax.plot(p[:,0],p[:,1],color='#303030' if name=='pan' else '#b47322',label=name if i==0 else None)
r=json.loads((ROOT/'inventory/engine/timing-pump-foot-pan-witnesses.json').read_text())
for i,w in enumerate(r['witnesses']):ax.plot(*w['cube_center_mm'][:2],'x',color='red',label='old collision witnesses' if i==0 else None)
ax.set_xlim(175,275);ax.set_ylim(88,113);ax.set_aspect('equal');ax.grid(alpha=.25);ax.legend();ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_title('Actual CAD section Z−103.216743 mm\nUnchanged pan; old collision witnesses excluded')
fig.suptitle('Isolated estimated narrower pump feet — mesh export FAIL; no installation acceptance');fig.tight_layout();fig.savefig(OUT/'pump-foot-render.png',dpi=160)
