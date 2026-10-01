#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-perimeter-contact';a=np.load(O/'contact-mesh.npz');v=a['vertices'];f=a['faces'];p=np.load(O/'contact-route.npz')['points']
fig=plt.figure(figsize=(16,10));ax=fig.add_subplot(221)
ax.add_collection(PolyCollection(v[f][:,:,:2],facecolors='#a8cbbb',edgecolors='none'));ax.plot(p[:,0],p[:,1],color='#b97719',lw=1);ax.set(xlim=(-390,420),ylim=(-155,225),xlabel='X mm',ylabel='Y mm',title='Actual shared mating surface and closed contact route');ax.set_aspect('equal');ax.grid(alpha=.15)
ax=fig.add_subplot(222,projection='3d');ax.add_collection3d(Poly3DCollection(v[f],facecolor='#a8cbbb',edgecolor='none'));ax.plot(p[:,0],p[:,1],p[:,2],color='#b97719',lw=1.2);ax.set(xlim=(-390,420),ylim=(-155,225),zlim=(-70,-20),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((810,380,170));ax.view_init(28,-50);ax.set_title('Actual contact surface in 3D — Z scale expanded for review')
for n,variant in enumerate(['fault-left','fault-front'],3):
 ax=fig.add_subplot(2,2,n);a=np.load(O/variant/'contact-mesh.npz');t=a['vertices'][a['faces']];ax.add_collection(PolyCollection(t[:,:,:2],facecolors='#a8cbbb',edgecolors='none'))
 if variant=='fault-left':ax.set(xlim=(-20,20),ylim=(-150,-120));title='Control: 4 mm transverse loss across left rail'
 else:ax.set(xlim=(350,410),ylim=(-20,20));title='Control: 4 mm transverse loss across complete front band'
 ax.set_aspect('equal');ax.set_title(title);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.grid(alpha=.15)
fig.suptitle('Unchanged pan/gasket: bounded full-perimeter contact study',fontsize=16)
fig.text(.5,.025,'Route width ≥2.066 mm after sampling/tessellation allowance. Both full-width faults destroy the enclosing band.\nOriginal rear full-face failure retained. No gasket compression, block-side sealing or fluid-containment claim.',ha='center',fontsize=11)
fig.tight_layout(rect=(0,.075,1,.96));fig.savefig(O/'contact-review.png',dpi=170)
files=[Path(__file__),O/'contact-review.png',O/'contact-mesh.npz',O/'contact-route.npz',R/'inventory/engine/timing-pan-perimeter-contact-review.json']
(R/'inventory/engine/timing-pan-perimeter-contact-render-review.json').write_text(json.dumps({'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}},indent=2)+'\n')
