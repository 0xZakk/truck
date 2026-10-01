#!/usr/bin/env python3
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-upper-contact';a=np.load(O/'contact-preview.npz')
fig=plt.figure(figsize=(16,10));ax=fig.add_subplot(221)
for n,col in [('block-v3','#719e88'),('cover-2692','#809bd1'),('terminal-sealant','#d4a644'),('unsupported','#bd665b')]:
 if n+'_vertices' in a:ax.add_collection(PolyCollection(a[n+'_vertices'][a[n+'_faces']][:,:,:2],facecolors=col,edgecolors='none',label=n))
ax.set(xlim=(-390,410),ylim=(-155,220),xlabel='X mm',ylabel='Y mm',title='Actual upper mating owners — red is unsupported face area');ax.set_aspect('equal');ax.legend(fontsize=8)
for i,(x,limits,title) in enumerate([(0,((-145,-118),(-36,-25)),'Retained left rail: actual X0 section'),(-376,((-65,65),(-58,-20)),'Retained rear: actual X−376 section'),(373.4,((-145,-100),(-30,-19)),'Front terminal pocket: actual X373.4 section')],2):
 ax=fig.add_subplot(2,2,i)
 for n,col in [('block','#719e88'),('cover','#809bd1'),('main-gasket','#a371b0'),('sealant','#d4a644'),('gasket','#333333')]:
  for k,line in enumerate(json.loads((O/f'{n}-section-{x}.json').read_text())):
   v=np.array(line);ax.plot(v[:,1],v[:,2],color=col,lw=1.5,label=n if k==0 else None)
 ax.set(xlim=limits[0],ylim=limits[1],xlabel='Y mm',ylabel='Z mm',title=title);ax.set_aspect('equal');ax.grid(alpha=.15);ax.legend(fontsize=7)
fig.suptitle('Upper pan-gasket interfaces — frozen candidate solids, physical owner study',fontsize=16)
fig.tight_layout(rect=(0,0,1,.96));fig.savefig(O/'upper-contact-review.png',dpi=170)
files=[Path(__file__),O/'upper-contact-review.png',O/'contact-preview.npz',R/'inventory/engine/timing-pan-upper-contact-review.json',R/'inventory/engine/timing-pan-upper-contact-diagnostic.json']
(R/'inventory/engine/timing-pan-upper-contact-render-review.json').write_text(json.dumps({'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}},indent=2)+'\n')
