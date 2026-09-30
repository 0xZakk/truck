#!/usr/bin/env python3
"""Render isolated outlet neck preview using actual meshes and source pixels."""
from pathlib import Path
import json,hashlib,sys,math,itertools,inspect,struct
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/rear-exhaust-neck-candidate'
REPORT=ROOT/'inventory/engine/exhaust-rear-collector-validation.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def render():
 import numpy as np
 import trimesh
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 light=np.array([.2,.7,.65]);light/=np.linalg.norm(light)
 def colors(tri):
  normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-20)
  shade=.30+.70*np.maximum(0,normal@light)
  return np.clip(shade[:,None]*np.array([.67,.57,.48]),0,1)
 paths=[OUT/'baseline.glb',OUT/'candidate.glb']
 fig=plt.figure(figsize=(15,11));angles=[(0,90),(-90,90),(35,-60)]
 sources=['front','back','three-quarter']
 for row,(elev,azim) in enumerate(angles):
  ax=fig.add_subplot(3,3,row*3+1);ax.imshow(plt.imread(ROOT/f'reference/engine/dorman-674186-{sources[row]}.jpg'));ax.axis('off');ax.set_title('Dorman674-186 · independent photograph pose')
  for col,p in enumerate(paths,2):
   mesh=trimesh.load(p,force='mesh');v=mesh.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000
   ax=fig.add_subplot(3,3,row*3+col,projection='3d');pc=Poly3DCollection(v[mesh.faces],facecolors=colors(v[mesh.faces]),edgecolors='none');ax.add_collection3d(pc)
   low,high=v.min(0),v.max(0);ax.set_xlim(-315,10);ax.set_ylim(-220,-125);ax.set_zlim(135,330);ax.set_box_aspect([325,95,195]);ax.view_init(elev=elev,azim=azim);ax.set_axis_off();ax.set_title(('Installed baseline' if col==2 else 'Estimated neck blend'))
 fig.suptitle('Outlet exterior study · side / bottom / oblique rows; identical mesh cameras and scale; photographs independently posed',fontsize=15)
 fig.tight_layout();fig.savefig(OUT/'source-comparison.png',dpi=135);plt.close(fig)
 # Actual half-mesh section uses triangles whose centroids lie behind Y=-180.
 fig=plt.figure(figsize=(14,5))
 for col,p in enumerate(paths,1):
  mesh=trimesh.load(p,force='mesh');v=mesh.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000;tri=v[mesh.faces];tri=tri[tri[:,:,1].mean(1)<-180]
  ax=fig.add_subplot(1,2,col,projection='3d');ax.add_collection3d(Poly3DCollection(tri,facecolors=colors(tri),edgecolors='none'));ax.set_xlim(-315,10);ax.set_ylim(-220,-125);ax.set_zlim(135,330);ax.set_box_aspect([325,95,195]);ax.view_init(elev=8,azim=90);ax.set_axis_off();ax.set_title('Baseline' if col==1 else 'Candidate · actual exported mesh half-view')
 fig.tight_layout();fig.savefig(OUT/'section-review.png',dpi=150);plt.close(fig)
 (OUT/'render-record.json').write_text(json.dumps(dict(script_sha256=sha(__file__),mesh_sha256={p.name:sha(p) for p in paths},images={p.name:sha(p) for p in [OUT/'source-comparison.png',OUT/'section-review.png']},scope='Actual exported mesh render; half-view is triangle-clipped, not an exact CAD section'),indent=2)+'\n')
 print('Rendered actual meshes and source comparison')


if __name__=="__main__":render()
