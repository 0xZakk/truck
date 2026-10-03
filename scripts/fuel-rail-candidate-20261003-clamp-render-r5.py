from pathlib import Path
import json,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';fig,axs=plt.subplots(1,2,figsize=(13,6));colors={'regulator-lower-housing':'#377eb8','regulator-upper-housing':'#333333','regulator-diaphragm':'#b83395'}
for ax,rev in zip(axs,['r4','r5']):
 d=json.loads((BASE/rev/'pressure-section.json').read_text())
 for ident,color in colors.items():
  for n,line in enumerate(d[ident]['polylines_r_z_mm']):
   p=np.array(line);ax.plot(p[:,0],p[:,1],color=color,lw=2,label=ident if n==0 else None)
 ax.set(xlim=(15.5,21),ylim=(387,391),xlabel='Radial offset mm',ylabel='Engine Z mm',title=rev+' actual saved STEP section');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=8,loc='lower left')
fig.suptitle('Actual estimated diaphragm clamp correction — lower O-ring boundary still open');fig.tight_layout();fig.savefig(BASE/'r5/actual-clamp-section.png',dpi=180)
