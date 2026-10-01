"""Actual GLB meshes, visually cropped to the front seat; no CAD changes."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate';PAN=ROOT/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate'
paths=[OUT/'block.glb',PAN/'pan.glb',PAN/'pan-gasket.glb']
if '--extract' in sys.argv:
 import trimesh
 data={}
 for name,p in zip(['block','pan','gasket'],paths):
  mesh=trimesh.load(p,force='mesh');data[name+'_v']=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;data[name+'_f']=np.asarray(mesh.faces)
 np.savez_compressed(OUT/'pair-render-input.npz',**data)
 (OUT/'pair-render-input-hashes.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},indent=2)+'\n');raise SystemExit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m=np.load(OUT/'pair-render-input.npz');fig=plt.figure(figsize=(15,7))
for i,az in enumerate([150,30]):
 ax=fig.add_subplot(1,2,i+1,projection='3d')
 for name,color in [('block','#9caeb4'),('pan','#b59670'),('gasket','#207f73')]:
  v,f=m[name+'_v'],m[name+'_f'];tri=v[f];center=tri.mean(axis=1);tri=tri[(center[:,0]>295)&(center[:,2]<20)&(center[:,2]>-90)]
  ax.add_collection3d(Poly3DCollection(tri,facecolors=color,edgecolor='none',shade=True))
 ax.set_xlim(295,405);ax.set_ylim(-155,220);ax.set_zlim(-90,20);ax.set_box_aspect([110,375,110]);ax.view_init(24,az);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
fig.suptitle('Actual matched GLB meshes — front seat detail (visually cropped)\nBlock gray, pan bronze, gasket green; estimated10mm backing / R10 flat pads, uninstalled')
fig.tight_layout();fig.savefig(OUT/'pair-glb-review.png',dpi=150)
