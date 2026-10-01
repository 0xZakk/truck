#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,numpy as np,trimesh,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection,LineCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/oil-pump-topology-candidate';fig,axs=plt.subplots(1,2,figsize=(12,5));inputs={}
for name,color,shift in [('housing','#91a4aa',0),('pickup-gasket','#c17e40',-15),('pickup-tube-flange','#677f9e',-28)]:
 p=OUT/('oil-pump-topology-'+name+'.glb');inputs[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();m=trimesh.load(p,force='mesh');m.vertices=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;v=m.vertices.copy();v[:,0]+=shift
 axs[0].add_collection(PolyCollection(v[m.faces][:,:,[0,2]],facecolor=color,edgecolor='none'));s=trimesh.intersections.mesh_plane(m,[0,1,0],[0,0,0]);s[:,:,0]+=shift;axs[1].add_collection(LineCollection(s[:,:,[0,2]],colors=color,linewidths=1.5));axs[0].plot([],[],color=color,label=name)
for ax in axs:ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('pump-local X (mm)');ax.set_ylabel('pump-local Z (mm)');ax.grid(alpha=.2)
axs[0].legend(loc='lower left');axs[0].set_title('Actual GLBs • pickup joint exploded along X');axs[1].set_title('Actual mesh section • Y=0\nUpper drive bore exists; discharge is MISSING');fig.suptitle('TOPOLOGY STUDY — flange sizes are display estimates; NOT INSTALLABLE');fig.tight_layout();p=OUT/'topology-review.png';fig.savefig(p,dpi=150);(ROOT/'inventory/engine/oil-pump-topology-render.json').write_text(json.dumps({'inputs':inputs,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'image':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n')
