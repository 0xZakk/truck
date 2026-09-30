#!/usr/bin/env python3
from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];r=json.loads((ROOT/'inventory/engine/timing-block-side-cover-conflict.json').read_text());fig,axes=plt.subplots(3,2,figsize=(15,10));colors={'baseline':'#222222','candidate':'#dc4326','gasket':'#218b3c','cover':'#2367cb'}
for row,section in enumerate(r['sections']):
 for col,ax in enumerate(axes[row]):
  for name,curves in section['contours_xy'].items():
   for i,curve in enumerate(curves):
    p=np.array(curve);ax.plot(p[:,0],p[:,1],color=colors[name],linewidth=1.2 if name!='baseline' else 2,linestyle='--' if name=='candidate' else '-',label=name if i==0 else None)
  ax.set_xlim((-340,340) if col==0 else (240,335));ax.set_ylim((75,130) if col==0 else (98,126));ax.set_title(f'Actual section Z={section["z_mm"]} mm'+(' — front zoom' if col else ''));ax.grid(alpha=.25);ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.legend(fontsize=8,loc='lower left')
fig.suptitle('Fixed side-cover conflict — actual CAD sections; original protected failure retained',fontsize=14);fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(ROOT/'cad/engine/generated/timing-block-axis-feature-candidate/side-cover-sections.png',dpi=160)
