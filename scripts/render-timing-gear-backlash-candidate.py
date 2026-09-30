#!/usr/bin/env python3
"""Actual exported meshes and retained replacement source; no geometry edits."""
from pathlib import Path
import json,hashlib,math
import numpy as np
import trimesh
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-gear-backlash-candidate'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
data={};axis=np.array([0,95.1098209901611,76.08785679212888])
for key in ['crank','cam']:
 m=trimesh.load(OUT/(key+'.glb'),force='mesh');v=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
 if key=='cam':v+=axis
 data[key]=v[m.faces]
fig=plt.figure(figsize=(16,12));source=ROOT/'reference/engine/timing-gear-evidence/elgin-c2766s-front.jpg'
ax=fig.add_subplot(2,2,1);ax.imshow(plt.imread(source));ax.axis('off');ax.set_title('Elgin C-2766S replacement comparison; independent photograph pose')
for panel,angle,title in [(2,(15,5),'Actual candidate front / oblique'),(3,(10,175),'Actual candidate back / thrust land'),(4,(0,0),'Actual contact-region mesh detail; no clearance exaggeration')]:
 ax=fig.add_subplot(2,2,panel,projection='3d')
 for key,color in [('crank','#8b929a'),('cam','#b09263')]:
  tri=data[key];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);el,az=np.radians(angle);eye=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)]);tri=tri[normal@eye>1e-10]
  colors=np.tile(np.array(to_rgb(color)),(len(tri),1));colors[tri[:,:,0].mean(1)<6.85]*=.60
  ax.add_collection3d(Poly3DCollection(tri,facecolors=colors,edgecolor='none',shade=True,antialiased=False))
 ax.set(xlim=(-14,14),ylim=(-50,184),zlim=(-50,164));ax.set_box_aspect((28,234,214));ax.view_init(*angle);ax.set_title(title);ax.set_axis_off()
 if panel==4:ax.set(xlim=(-8,8),ylim=(23,45),zlim=(15,37));ax.set_box_aspect((16,22,22))
fig.suptitle('58/29 midpoint backlash candidate — 0.0381 mm thinning per gear\nEstimated profiles, axes and helix; unchanged hubs/keys/marks/thrust land; not installed or factory-calibrated')
fig.tight_layout();fig.savefig(OUT/'source-comparison.png',dpi=140)
record=dict(script_sha256=sha(__file__),source_sha256=sha(source),mesh_sha256={k:sha(OUT/(k+'.glb')) for k in data},render_sha256=sha(OUT/'source-comparison.png'),scope='Actual unscaled mesh geometry at neutral phase; photograph independent pose; local composite excluded from Git/releases')
(OUT/'render-record.json').write_text(json.dumps(record,indent=2)+'\n')
