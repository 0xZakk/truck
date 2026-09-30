#!/usr/bin/env python3
"""Sections through preserved actual tessellation; no CAD rebuild or checks rerun."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/air-cleaner-candidate'
source=OUT/'preview.npz';data=np.load(source)
colors=['#455b6b','#26313b','#b98c33','#c25f29']
labels=['Lower tray','Cover','Paper / perimeter carrier','Seal']
def segments(tris,axis,value):
 result=[]
 keep=[i for i in range(3) if i!=axis]
 for tri in tris:
  points=[]
  for a,b in zip(tri,np.roll(tri,-1,axis=0)):
   da,db=a[axis]-value,b[axis]-value
   if abs(da)<1e-8: points.append(a)
   if da*db<0: points.append(a+(b-a)*da/(da-db))
  unique=[]
  for p in points:
   if not any(np.linalg.norm(p-q)<1e-7 for q in unique):unique.append(p)
  if len(unique)==2:result.append(np.array(unique)[:,keep])
 return result
fig,axes=plt.subplots(3,1,figsize=(14,11),gridspec_kw={'height_ratios':[2,1.1,1.2]})
views=[(1,0,(-205,180),(-105,65),'Longitudinal section at Y = 0: actual exported tessellation','X (mm)'),(1,0,(-30,30),(-45,-3),'Pleat detail: estimated 0.65 mm Z offset and 35 mm fold depth','X (mm)'),(0,0,(58,88),(-13,8),'Transverse seat detail at X = 0: estimated stack, no compression simulation','Y (mm)')]
for ax,(axis,value,xlim,ylim,title,xlabel) in zip(axes,views):
 for i in range(4):
  triangles=data[f'v{i}'][data[f'f{i}']]
  ax.add_collection(LineCollection(segments(triangles,axis,value),colors=colors[i],linewidths=1.3,label=labels[i]))
 ax.set(xlim=xlim,ylim=ylim,title=title,xlabel=xlabel,ylabel='Z (mm)');ax.set_aspect('equal');ax.grid(alpha=.2)
axes[0].legend(loc='upper left',fontsize=8,ncol=4)
axes[2].annotate('Cover flange: Z 0 to +3',xy=(72,1.5),xytext=(79,5),arrowprops={'arrowstyle':'->'},fontsize=9)
axes[2].annotate('Seal: Z −4 to 0',xy=(72,-2),xytext=(78,-1),arrowprops={'arrowstyle':'->'},fontsize=9)
axes[2].annotate('Tray seat: Z −7 to −4',xy=(72,-5.5),xytext=(77,-10),arrowprops={'arrowstyle':'->'},fontsize=9)
axes[2].annotate('Paper carrier meets seal\nat Z −4, Y 63 to 65',xy=(64,-4),xytext=(58,-11),arrowprops={'arrowstyle':'->'},fontsize=8)
fig.suptitle('Air-cleaner candidate — section outlines of saved CAD mesh\nAll section dimensions estimated; porous paper flow and installed retention remain unverified',fontsize=13)
fig.tight_layout(rect=(0,0,1,.95));target=OUT/'candidate-section-review.png';fig.savefig(target,dpi=170)
report={'status':'RENDER ONLY; previous CAD checks unchanged','input_sha256':{str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest(),str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'output':str(target.relative_to(ROOT)),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'method':'Triangle/plane intersections of preserved preview.npz mesh; no invented section drawing; no geometry edits or validation rerun'}
(OUT/'section-render.json').write_text(json.dumps(report,indent=2)+'\n')
print(target)
