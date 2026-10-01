#!/usr/bin/env python3
"""Actual exported meshes, orthographic projection and cap-terminal section."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import numpy as np,trimesh,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection,LineCollection
import shifted_ignition_lead_candidate as c
OUT=ROOT/'cad/engine/generated/shifted-ignition-lead-candidate'
fig,axs=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[2,1]});colors=plt.cm.tab10.colors;inputs={}
for i,prefix in enumerate([f'ignition-lead-{n}' for n in range(1,7)]+['ignition-coil-lead']):
 for suffix in ['jacket','cap-boot']:
  p=OUT/(prefix+'-'+suffix+'.glb');inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();m=trimesh.load(p,force='mesh');v=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
  # Render all exported triangles, projected X/Y.
  axs[0].add_collection(PolyCollection(v[m.faces][:,:,[0,1]],facecolor=colors[i],edgecolor='none',alpha=.9))
 axs[0].plot([],[],color=colors[i],label=prefix.replace('ignition-',''))
# Actual exported GLB transverse section at lead1 cap local Z108.
_,_,contract=c.path_and_contract(1);frame=contract['cap_frame'];origin=np.array(tuple(c.src.point(frame,108)));normal=np.array(tuple(c.src.direction(frame)));ux=np.array([1.,0.,0.]);uy=np.cross(normal,ux)
for suffix,col in [('cap-boot','#457b9d'),('cap-contact','#e09f3e')]:
 p=OUT/('ignition-lead-1-'+suffix+'.glb');inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();m=trimesh.load(p,force='mesh');m.vertices=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;s=trimesh.intersections.mesh_plane(m,normal,origin);xy=np.stack([(s-origin)@ux,(s-origin)@uy],axis=-1);axs[1].add_collection(LineCollection(xy,colors=col,linewidths=2,label=suffix))
for ax in axs:ax.autoscale();ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('mm');ax.legend(fontsize=8,loc="upper left")
axs[0].set_title('Actual exported routes • world X/Y\nSeven colors; fixed plug/coil endpoints retained');axs[0].set_ylabel('world Y (mm)')
axs[1].set_title('Actual mesh section • lead 1\nCap-local Z108: contact and boot rings');axs[1].set_xlim(-10,10);axs[1].set_ylim(-10,10)
fig.suptitle('Shifted ignition joints — scoped uninstalled candidate');fig.tight_layout();p=OUT/'ignition-lead-review.png';fig.savefig(p,dpi=150);inputs[str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();(ROOT/'inventory/engine/shifted-ignition-lead-render.json').write_text(json.dumps({'inputs':inputs,'image':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'Actual exported GLB projection and transverse mesh section; source dimensions remain estimated'},indent=2)+'\n')
