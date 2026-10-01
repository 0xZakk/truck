#!/usr/bin/env python3
"""Actual mesh silhouette and BRep section; no generated design imagery."""
from pathlib import Path
import sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import numpy as np,build123d as b,trimesh
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import cam_clockwise_candidate as c
OUT=ROOT/'cad/engine/generated/cam-clockwise-candidate'
mesh=trimesh.load(OUT/'camshaft-local.glb',force='mesh');v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;tri=v[mesh.faces]
fig=plt.figure(figsize=(13,7.8),facecolor='#f6f7f9');grid=fig.add_gridspec(2,2,height_ratios=[1,3],width_ratios=[1,1])
ax=fig.add_subplot(grid[0,:]);order=np.argsort(tri[:,:,1].mean(1));projected=tri[:,:,[0,2]].copy();projected[:,:,1]+=.45*tri[:,:,1]
normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.linalg.norm(normal,axis=1)[:,None]
shade=.58+.32*np.abs(normal@np.array([.2,-.5,.84]));colors=np.array([.31,.53,.59])[None,:]*shade[:,None]
ax.add_collection(PolyCollection(projected[order],facecolors=colors[order],edgecolors='none'));ax.set_xlim(v[:,0].min()-10,v[:,0].max()+10);ax.set_ylim(-35,35);ax.set_aspect('equal');ax.set_yticks([]);ax.set_xlabel('Shaft X (mm)');ax.set_title('Actual exported corrected cam mesh · original shaft, journals and keyed ends retained')
def section(shape,x):
 wire=b.section(shape,section_by=b.Plane.YZ.offset(x)).wires()[0]
 return np.array([tuple(wire.position_at(i/1024))[1:] for i in range(1025)])
def spin(p,degrees):
 a=math.radians(degrees);return p@np.array([[math.cos(a),math.sin(a)],[-math.sin(a),math.cos(a)]])
old=b.Pos(0,-c.AXIS[0],-c.AXIS[1])*b.import_step(c.BASE);new=b.import_step(OUT/'camshaft-local.step');x=259.48;q=372
p=section(old,x);n=section(new,x)
ax=fig.add_subplot(grid[1,0]);ax.plot(*spin(p,-q/2).T,color='#6f7782',label='Prior lobe / prior spin');ax.plot(*spin(n,q/2).T,color='#127a73',label='Corrected lobe / corrected spin');ax.plot(*spin(p,q/2).T,'--',color='#bd4b44',label='Old lobe / corrected spin: fault')
w=c.tangent(q,1,'intake',0,x);y,z=w[1]-c.AXIS[0],w[2]-c.AXIS[1];ax.plot([-11.124565,11.124565],[z,z],color='#1c2430',lw=3);ax.scatter(y,z,color='#127a73',zorder=5)
ax.set_aspect('equal');ax.set_xlim(-28,28);ax.set_ylim(-25,30);ax.grid(alpha=.2);ax.set_xlabel('Local Y (mm)');ax.set_ylabel('Local Z (mm)');ax.set_title('Actual section · cylinder 1 intake rising flank');ax.legend(fontsize=8,loc='lower left')
ax=fig.add_subplot(grid[1,1]);ax.axis('off');ax.text(.02,.91,'Same lift, opposite contact side',fontsize=18,weight='bold');ax.text(.02,.80,'q = 372°   ·   axial position = 0 mm',fontsize=12);ax.text(.02,.66,'The gray and green lobes reach the same\nflat follower plane. The green contact lies\non the opposite side of the lifter center.',fontsize=12,linespacing=1.5);ax.text(.02,.43,'The red dashed curve shows why changing\nspin without rephasing the actual lobe fails.',fontsize=12,linespacing=1.5);ax.text(.02,.24,'120 sampled contacts pass.\nContinuous whole-engine motion and\ncrossed-drive handedness remain open.',fontsize=12,linespacing=1.5,color='#555d68')
fig.tight_layout();fig.savefig(OUT/'cam-clockwise-review.png',dpi=160);plt.close(fig)
