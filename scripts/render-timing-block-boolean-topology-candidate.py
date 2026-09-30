#!/usr/bin/env python3
"""Actual exported triangle comparison; no inferred photographic geometry."""
from pathlib import Path
import numpy as np,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'cad/engine/generated/timing-block-boolean-topology-candidate'
if '--extract' in sys.argv:
 import trimesh
 mesh=trimesh.load(out/'block.glb',force='mesh');np.savez(out/'render-mesh.npz',vertices=np.asarray(mesh.vertices),faces=np.asarray(mesh.faces));sys.exit(0)
subprocess.run([str(ROOT/'.venv-cad/bin/python'),str(Path(__file__)),'--extract'],check=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'cad/engine/generated/timing-block-boolean-topology-candidate'
mesh=np.load(out/'render-mesh.npz');v=mesh['vertices'][:,[0,2,1]]*[1,-1,1]*1000
fig=plt.figure(figsize=(15,8));fig.suptitle('Isolated shifted block — actual exported mesh, estimated cam datum',fontsize=15)
for i,(elev,azim) in enumerate([(18,38),(15,142)],1):
 ax=fig.add_subplot(1,2,i,projection='3d');tri=v[mesh['faces']];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-12);shade=.4+.6*np.maximum(0,norm@np.array([.3,.5,.812]));col=np.column_stack([.55*shade,.67*shade,.75*shade,np.ones(len(shade))]);ax.add_collection3d(Poly3DCollection(tri,facecolors=col,linewidths=0,rasterized=True));ax.set_xlim(-390,390);ax.set_ylim(-190,210);ax.set_zlim(-125,285);ax.set_box_aspect((780,400,410));ax.view_init(elev,azim);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_zlabel('Z mm')
fig.text(.5,.02,'No canonical installation. Protected-region and core-fit reports govern acceptance.',ha='center');fig.savefig(out/'block-render.png',dpi=140);plt.close(fig)
