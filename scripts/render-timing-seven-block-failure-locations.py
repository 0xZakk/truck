"""Overlay exact broad-guard Boolean sections; original comparison retained."""
from pathlib import Path
import json,hashlib,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-seven-block-guard-study';lines=json.loads((OUT/'sections.json').read_text());fault=json.loads((OUT/'failure-sections.json').read_text());fig,axes=plt.subplots(1,2,figsize=(13,7))
for j,(ax,prefix)in enumerate(zip(axes,['active-pan-interface-20','water-pump-front-interface'])):
 for edges in [lines['new']]:
  for e in edges:
   p=np.array(e);ax.plot(p[:,1],p[:,2],color='#888888',lw=.8)
 for label,col in [('added','#198654'),('removed','#d13e3e')]:
  for i,e in enumerate(fault[prefix+'-'+label]):
   p=np.array(e);ax.plot(p[:,1],p[:,2],color=col,lw=2,label=label if i==0 else None)
 ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('Y mm');ax.set_ylabel('Z mm');ax.legend()
axes[0].add_patch(Rectangle((-144,-24.5),24,17.4,fill=False,ls='--',edgecolor='#485cad'));axes[0].set_xlim(-146,-106);axes[0].set_ylim(-28,3);axes[0].annotate('Pan20 female unchanged',(-132,-17),xytext=(-143,-26),arrowprops={'arrowstyle':'->'},fontsize=9);axes[0].set_title('Pan20 broadR12 guard, actualX365.5 section\nAdded green / removed red / unchanged gray')
axes[1].add_patch(Circle((-32,170),85,fill=False,ls='--',edgecolor='#485cad'));axes[1].set_xlim(-50,12);axes[1].set_ylim(80,126);axes[1].annotate('Existing chamber boundary',(-32,111),xytext=(-46,121),arrowprops={'arrowstyle':'->'},fontsize=9);axes[1].set_title('Lower pumpR85 guard, actualX365.5 section\nMain3 changes remain below modeled chamber')
fig.suptitle('Broad guard FAIL preserved — exact Boolean witness boundaries, not waived by functional checks');fig.tight_layout();p=OUT/'failure-locations.png';fig.savefig(p,dpi=180);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'render':str(p.relative_to(ROOT)),'sha256':sha(p),'input_sha256':{str(p.relative_to(ROOT)):sha(p)for p in[OUT/'sections.json',OUT/'failure-sections.json',Path(__file__)]}};(ROOT/'inventory/engine/timing-seven-block-failure-location-visual.json').write_text(json.dumps(r,indent=2)+'\n')
