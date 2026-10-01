"""Actual added-stock witness section atX360; supplementsX365.5 removal view."""
from pathlib import Path
import json,sys,numpy as np,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-seven-block-guard-study';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--extract' in sys.argv:
 import build123d as b
 paths=[ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step',OUT/'active-pan-interface-20-added.step',OUT/'water-pump-front-interface-added.step'];r={}
 for p in paths:
  sec=b.section(b.import_step(p),b.Plane.YZ.offset(360));r[p.stem]=[[list(e.position_at(i/60))for i in range(61)]for e in sec.edges()]
 (OUT/'added-x360-sections.json').write_text(json.dumps(r));(OUT/'added-x360-inputs.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p)for p in paths}));raise SystemExit
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=json.loads((OUT/'added-x360-sections.json').read_text());fig,axes=plt.subplots(1,2,figsize=(13,7))
for ax,name in zip(axes,['active-pan-interface-20-added','water-pump-front-interface-added']):
 for key,col,lw in [('block','#888888',.8),(name,'#198654',2)]:
  for e in r[key]:
   p=np.array(e);ax.plot(p[:,1],p[:,2],color=col,lw=lw)
 ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('Y mm');ax.set_ylabel('Z mm')
axes[0].set_xlim(-145,-105);axes[0].set_ylim(-30,5);axes[0].set_title('Added material insidepan20R12guard atX360')
axes[1].set_xlim(-45,15);axes[1].set_ylim(80,125);axes[1].set_title('Added material insidepumpR85guard atX360')
fig.suptitle('Actual added-stock sections — green inside broad failed guards; gray current block boundary');fig.tight_layout();p=OUT/'added-stock-locations.png';fig.savefig(p,dpi=180);r={'render':str(p.relative_to(ROOT)),'sha256':sha(p),'input_sha256':{**json.loads((OUT/'added-x360-inputs.json').read_text()),**{str(x.relative_to(ROOT)):sha(x)for x in[OUT/'added-x360-sections.json',Path(__file__)]}}};(ROOT/'inventory/engine/timing-seven-block-added-location-visual.json').write_text(json.dumps(r,indent=2)+'\n')
