#!/usr/bin/env python3
"""Native STEP section and independently bounded meshes, no reference artwork."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
from OCP.BRepTools import BRepTools
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
OUT=ROOT/'cad/engine/generated/front-seal-2692-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['cover','damper-hub','seal-case-installed','seal-elastomer','seal-garter-spring']
colors=['#719caf','#b5b5bd','#d5a850','#423d45','#e88455']
r={'status':'RUNNING','inputs':{},'meshes':{}}
shapes={}
for name in names:
 p=OUT/(name+'.step');r['inputs'][str(p.relative_to(ROOT))]=sha(p);s=b.import_step(p);shapes[name]=s
 BRepTools.Clean_s(s.wrapped);v,f=s.tessellate(.01,.5) if name=='seal-garter-spring' else s.tessellate(.035,.10);a=np.array([[x.X,x.Y,x.Z] for x in v]);mesh=trimesh.Trimesh(vertices=a[:,[0,2,1]]*np.array([1,1,-1])/1000,faces=f,process=False);mesh.merge_vertices();mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();p=OUT/(name+'.glb');trimesh.Scene(mesh).export(p);loaded=trimesh.load(p,force='mesh');bb=s.bounding_box();expected=np.array([[bb.min.X,bb.min.Z,-bb.max.Y],[bb.max.X,bb.max.Z,-bb.min.Y]])/1000;err=float(np.max(np.abs(loaded.bounds-expected)))*1000
 r['meshes'][name]={'sha256':sha(p),'watertight':bool(loaded.is_watertight),'bounds_error_mm':err,'triangles':len(loaded.faces)}
 assert loaded.is_watertight and err<.2,(name,r['meshes'][name]);print('mesh',name,flush=True)
fig,axs=plt.subplots(1,2,figsize=(13,6));slab=b.Pos(424,0,0)*b.Box(80,.10,110)
for name,color in zip(names,colors):
 section=shapes[name].intersect(slab)
 if not section:continue
 v,f=section.tessellate(.025,.08);a=np.array([[p.X,p.Z] for p in v])
 for ax in axs:ax.add_collection(PolyCollection(a[np.array(f)],facecolor=color,edgecolor='none',label=name))
for ax,limits in zip(axs,[(400,443,18,46),(424.8,430,23.3,29)]):
 ax.set_xlim(limits[:2]);ax.set_ylim(limits[2:]);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('World X / mm');ax.set_ylabel('World Z / mm')
axs[0].set_title('Actual exported cover, hub and seal section');axs[0].legend(fontsize=8);axs[1].set_title('Estimated lip, carrier and garter groove')
fig.suptitle('2692 envelope study — rear X420 is estimated\nFree case OD65.151; nominal installed OD65.0494; no factory contour claim')
fig.tight_layout();p=OUT/'seal-cover-hub-section.png';fig.savefig(p,dpi=180);r['render']={'path':str(p.relative_to(ROOT)),'sha256':sha(p)};r['inputs'][str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__));r['status']='PASS native mesh and rendered exported section; visual review pending'
(ROOT/'inventory/engine/front-seal-2692-render-validation.json').write_text(json.dumps(r,indent=2)+'\n')
