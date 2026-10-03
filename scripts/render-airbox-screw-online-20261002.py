"""Orthographic views of actual exported screw; no source originals included."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1]
sys.path.extend(str(p) for p in (R/'.venv-cad/lib').glob('python*/site-packages'))
import trimesh
O=R/'cad/engine/generated/airbox-screw-online-20261002'
p=O/'air-cleaner-body-bracket-screw.glb';g=trimesh.load(p,force='mesh');v=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
m=trimesh.Trimesh(v,g.faces,process=False)
fig,axes=plt.subplots(1,3,figsize=(14,7))
for ax,n,title in zip(axes,[(0,-1,0),(.4,-.85,-.3),(0,0,-1)],['Side: bearing plane to tip 19 mm','Oblique: actual helical ridge','Head: 8 mm hex / 11.5 mm flange']):
 n=np.array(n,dtype=float);n/=np.linalg.norm(n)
 right=np.array([1.,0,0])-n*n[0];right/=np.linalg.norm(right);up=np.cross(n,right)
 xy=np.stack([v@right,v@up],axis=-1);depth=(v@n)[m.faces].mean(1);order=np.argsort(depth)
 light=np.clip(m.face_normals@np.array([.3,-.5,.8]),0,1)
 colors=np.array([.47,.50,.53])[None,:]*(.38+.62*light[:,None])
 ax.add_collection(PolyCollection(xy[m.faces][order],facecolors=colors[order],edgecolors='none',rasterized=True))
 ax.autoscale_view();ax.set_aspect('equal');ax.set_axis_off();ax.set_title(title,fontsize=10)
fig.suptitle('Auveco 13019 / N610959-S2 replacement-envelope candidate\nActual GLB; estimated head height, root/profile, taper and handedness',fontsize=14)
fig.text(.06,.03,'Compare catalog printed page 102 / PDF page 2: external hex, integral washer head, coarse thread and pointed tip.\nNo host pose, pilot bore, sheet stack, manufacturing fit or installed acceptance. Source originals excluded.',fontsize=11)
fig.subplots_adjust(top=.82,bottom=.16,wspace=.18)
out=O/'source-view-review.png';fig.savefig(out,dpi=150);plt.close(fig)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(O/'render.json').write_text(json.dumps({'inputs':{str(p.relative_to(R)):sha(p),str(Path(__file__).relative_to(R)):sha(Path(__file__))},'output_sha256':sha(out),'method':'Actual exported GLB restored to CAD mm; deterministic orthographic triangle depth render; no source image included'},indent=2)+'\n')
print(out)
