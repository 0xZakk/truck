from pathlib import Path
import numpy as np,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pump-rear-contract-preflight';d=np.load(O/'sections.npz');fig,axes=plt.subplots(1,3,figsize=(15,6));colors={'cover-trial':'#bf3f30','cover-old':'#bbaaaa','pump-trial':'#1876a3','pump-old':'#aaaaaa','gasket-trial':'#36a45a'}
for ax,x in zip(axes.flat,[374,376,380]):
 for n,c in colors.items():
  key=f'{n}_{x}'
  if key not in d:continue
  for i,edge in enumerate(d[key]):ax.plot(edge[:,1],edge[:,2],color=c,lw=1.4,label=n if i==0 else None,linestyle='--'if n.endswith('old')else'-')
 ax.set(xlim=(-35,45),ylim=(85,155),xlabel='Y mm',ylabel='Z mm',title=f'Actual YZ section at X={x} mm');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.suptitle('Rear-only analytical hypothesis — axes fixed, no replacement assets');fig.tight_layout();p=O/'sections-review.png';fig.savefig(p,dpi=160);j={'image':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((O/'sections.npz').read_bytes()).hexdigest()};(R/'inventory/engine/timing-pump-rear-contract-render.json').write_text(json.dumps(j,indent=2)+'\n')
