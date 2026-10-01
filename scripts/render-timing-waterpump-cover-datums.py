from pathlib import Path
import numpy as np,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-waterpump-cover-datum-audit';d=np.load(O/'sections.npz');fig,axes=plt.subplots(2,2,figsize=(13,10));colors={'cover':'#bf3f30','old-cover':'#888888','water-pump-housing':'#1876a3','water-pump-gasket':'#36a45a'}
for ax,x in zip(axes.flat,[374,376,390,414]):
 for n,c in colors.items():
  key=f'{n}_{x}'
  if key not in d:continue
  for i,edge in enumerate(d[key]):ax.plot(edge[:,1],edge[:,2],color=c,lw=1.4,label=n if i==0 else None,linestyle='--'if n=='old-cover'else'-')
 ax.set(xlim=(-125,145),ylim=(65,260),xlabel='Y mm',ylabel='Z mm',title=f'Actual YZ section at X={x} mm');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.suptitle('Unchanged pump versus independently registered cover — diagnostic sections');fig.tight_layout();p=O/'sections-review.png';fig.savefig(p,dpi=160);j={'image':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((O/'sections.npz').read_bytes()).hexdigest()};(R/'inventory/engine/timing-waterpump-cover-render.json').write_text(json.dumps(j,indent=2)+'\n')
