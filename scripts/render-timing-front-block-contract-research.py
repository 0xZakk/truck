from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-front-block-contract-research'
rows=json.loads((OUT/'sections.json').read_text());colors={'block':'#4b4b4b','cover':'#bd7433','main-gasket':'#277bc0','future-block-land':'#47945c','pan-gasket':'#347ac1','water-pump-gasket':'#ac478d','cam-thrust-plate':'#814aac','analytic dry prism':'#bb4444'}
for region,(ys,zs) in {'lower-front':((-125,125),(-75,10)),'full-front':((-155,220),(-75,260))}.items():
 fig,axes=plt.subplots(2,2,figsize=(14,10))
 for ax,(x,parts) in zip(axes.flat,rows.items()):
  for name,curves in parts.items():
   for i,curve in enumerate(curves):
    p=np.array(curve);ax.plot(p[:,0],p[:,1],color=colors[name],lw=1.1,ls='--' if name=='analytic dry prism' else '-',label=name if i==0 else None)
  ax.set_xlim(*ys);ax.set_ylim(*zs);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_title('Actual CAD section X'+x+' mm');ax.set_xlabel('Y mm');ax.set_ylabel('Z mm')
 handles,labels=[],[]
 for ax in axes.flat:
  h,l=ax.get_legend_handles_labels()
  for a,c in zip(h,l):
   if c not in labels:handles.append(a);labels.append(c)
 fig.legend(handles,labels,loc='lower center',ncol=4,fontsize=9);fig.suptitle('Coordinated front-block contract research — no geometry mutation');fig.tight_layout(rect=(0,.07,1,.95));fig.savefig(OUT/(region+'-sections.png'),dpi=150)
