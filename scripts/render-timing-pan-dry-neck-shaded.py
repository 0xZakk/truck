#!/usr/bin/env python3
"""Shaded actual exported GLB review; no geometric changes or smoothing."""
from pathlib import Path
import json,hashlib
import numpy as np
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-dry-neck-candidate';glb=O/'pan.glb'
actual=O/'shaded-glb-input.npz'
subprocess.run([str(R/'.venv-cad/bin/python'),'-c',"import trimesh,numpy as np,sys;m=trimesh.load(sys.argv[1],force='mesh');np.savez_compressed(sys.argv[2],vertices=m.vertices,faces=m.faces)",str(glb),str(actual)],check=True)
a=np.load(actual);vertices=a['vertices'][:,[0,2,1]]*[1,-1,1]*1000;triangles=vertices[a['faces']];n=np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0]);n/=np.linalg.norm(n,axis=1)[:,None];light=np.array([.45,-.65,1.]);light/=np.linalg.norm(light);intensity=.28+.72*np.clip(n@light,0,1);base=np.array([.43,.64,.56]);colors=np.column_stack([intensity[:,None]*base,np.ones(len(n))])
fig=plt.figure(figsize=(16,9),facecolor='#f4f6f6')
for i,(elev,azim,title)in enumerate([(36,-48,'Front / left side: inward wall beneath preserved flange'),(33,43,'Front / right side: wider return and shoulder')],1):
 ax=fig.add_subplot(1,2,i,projection='3d',facecolor='#f4f6f6');ax.add_collection3d(Poly3DCollection(triangles,facecolors=colors,edgecolors='none',linewidths=0,zsort='average'))
 lo,hi=vertices.min(axis=0),vertices.max(axis=0);pad=np.array([20,20,15]);ax.set(xlim=(lo[0]-pad[0],hi[0]+pad[0]),ylim=(lo[1]-pad[1],hi[1]+pad[1]),zlim=(lo[2]-pad[2],hi[2]+pad[2]),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect(hi-lo);ax.view_init(elev,azim);ax.set_title(title,fontsize=11,pad=8);ax.grid(False)
 for axis_obj in [ax.xaxis,ax.yaxis,ax.zaxis]:axis_obj.pane.fill=False
fig.suptitle('Actual exported dry-neck pan GLB — directional face shading; no mesh edits',fontsize=16,y=.93)
fig.text(.5,.08,'Estimated sharp wall returns and flange contours. Uninstalled candidate; full containment remains unverified.',ha='center',fontsize=11)
fig.subplots_adjust(left=0,right=1,bottom=.1,top=.88,wspace=0);png=O/'shaded-glb-review.png';fig.savefig(png,dpi=170,facecolor=fig.get_facecolor())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'scope':'Additional actual exported GLB views, directional per-face shading; original review.png preserved','glb_sha256':sha(glb),'renderer_sha256':sha(Path(__file__)),'png_sha256':sha(png),'glb_axis_conversion':'meters(x,z,-y)→CADmillimeters(x,y,z)','triangle_count':len(a['faces']),'geometry_changed':False,'output':str(png.relative_to(R))}
(R/'inventory/engine/timing-pan-dry-neck-render-review.json').write_text(json.dumps(record,indent=2)+'\n')
