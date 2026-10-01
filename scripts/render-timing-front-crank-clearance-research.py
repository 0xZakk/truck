from pathlib import Path
import sys,json,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-front-crank-clearance-research'
if '--extract' in sys.argv:
 import build123d as b
 sys.path.insert(0,str(ROOT/'cad/engine'))
 import timing_cover_front_joint_candidate as c
 parts={'block':b.import_step(ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step'),'gear':b.import_step(ROOT/'cad/engine/generated/timing-thrust-land-candidate/crank-timing-gear.step'),'envelope':b.import_step(OUT/'analytic-envelope.step'),'proposed removal':b.import_step(OUT/'proposed-removal.step'),'future center boss guard':c.disk(10,390,0,c.top(0),c.top(0)+16)}
 rows={k:[[list(e.position_at(i/120))[1:] for i in range(121)] for e in b.section(q,section_by=b.Plane.YZ.offset(380.5)).edges()] for k,q in parts.items()}
 (OUT/'section.json').write_text(json.dumps(rows));sys.exit()
subprocess.run([str(ROOT/'.venv-cad/bin/python'),str(Path(__file__)),'--extract'],check=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
fig,ax=plt.subplots(figsize=(11,7))
for (name,curves),color in zip(json.loads((OUT/'section.json').read_text()).items(),['#666666','#b87a25','#397aaa','#cf403b','#884ca1']):
 for i,curve in enumerate(curves):
  p=np.array(curve);ax.plot(p[:,0],p[:,1],color=color,linewidth=1.7,label=name if i==0 else None)
ax.set_xlim(-70,70);ax.set_ylim(-70,10);ax.set_aspect('equal');ax.grid(alpha=.25);ax.legend(loc='upper right');ax.set_xlabel('Y mm');ax.set_ylabel('Z mm');ax.set_title('Research only — actual CAD section X380.5 mm\nEstimated envelope crosses old front support and future boss guard; no block cut')
fig.tight_layout();fig.savefig(OUT/'clearance-section.png',dpi=160)
