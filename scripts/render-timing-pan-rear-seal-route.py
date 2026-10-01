#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-rear-seal-review'
fig,axes=plt.subplots(1,2,figsize=(13,7))
for ax,x,title in zip(axes,[-376,-367.5],['Supported rear sealing corridor','Inner overhang: localized full-face failure']):
 for name,col in [('pan','#167a55'),('gasket','#336699')]:
  for i,line in enumerate(json.loads((O/f'{name}-section-{x}.json').read_text())):
   a=np.array(line);ax.plot(a[:,1],a[:,2],color=col,lw=2,label=name if i==0 else None)
 if x==-376:
  theta=np.linspace(np.arcsin(34/53.1),np.pi-np.arcsin(34/53.1),160);ax.plot(53.1*np.cos(theta),-53.1*np.sin(theta),'--',color='#df8c21',lw=1.6,label='verified shared contact surface')
  for sign in [-1,1]:ax.plot([sign*40.7873755,sign*60],[-34,-34],'--',color='#df8c21')
 else:
  for sign in [-1,1]:ax.annotate('unsupported patch',xy=(sign*41.6,-33),xytext=(sign*43,-22),ha='center',fontsize=8,arrowprops={'arrowstyle':'->','color':'#ab4338'})
 ax.set(xlim=(-65,65),ylim=(-63,-16),xlabel='Y mm',ylabel='Z mm',title=f'{title}\nActual section X{x} mm');ax.set_aspect('equal');ax.grid(alpha=.15);ax.legend(fontsize=8,loc='lower center')
fig.suptitle('Rear gasket contact review — actual STEP sections, unchanged candidate',fontsize=15)
fig.text(.5,.08,'A continuous 4 mm axial contact strip survives across the rear arch and both flat lands.\nThe 25.5356 mm² inner overhang remains unsupported; whole-perimeter sealing and containment are unverified.',ha='center',fontsize=11)
fig.tight_layout(rect=(0,.15,1,.95));fig.savefig(O/'rear-contact-review.png',dpi=170)
files=[Path(__file__),O/'rear-contact-review.png',O/'contact-route.step',R/'inventory/engine/timing-pan-rear-seal-route-review.json',*O.glob('*section*.json')]
(R/'inventory/engine/timing-pan-rear-seal-render-review.json').write_text(json.dumps({'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
