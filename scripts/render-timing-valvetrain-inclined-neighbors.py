#!/usr/bin/env python3
"""Actual exported rocker/cover sections illustrating a measured failed interface."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import timing_valvetrain_inclined_candidate as c
OUT=ROOT/'cad/engine/generated/timing-valvetrain-inclined-neighbors';OUT.mkdir(parents=True,exist_ok=True)
rockp=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate/rocker-arm.step';coverp=ROOT/'cad/engine/generated/valve-cover.step';m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
rock=b.import_step(rockp);cover=b.import_step(coverp);fig,axs=plt.subplots(1,2,figsize=(12,6))
def draw(ax,q,color,label):
 if not q:return
 v,f=q.tessellate(.07,.13);a=np.array([[p.Y,p.Z] for p in v]);ax.add_collection(PolyCollection(a[np.array(f)],facecolor=color,edgecolor='none',alpha=.85,label=label))
for theta,ax,title in [(318,axs[0],'Intake rest — clear'),(468,axs[1],'Intake peak — roof collision')]:
 frames=c.poses(m,theta);r=frames['c1-intake-rocker']*rock;v=frames['valve-cover']*cover
 section=b.Pos(259.48,90,400)*b.Box(.5,80,60)
 draw(ax,v.intersect(section),'#7293a2','Actual cover section');draw(ax,r.intersect(section),'#dfa43d','Actual rocker section');draw(ax,r.intersect(v).intersect(section) if r.intersect(v) else None,'#c64740','Exact overlap section')
 ax.set_xlim(64,112);ax.set_ylim(385,416);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('WorldY / mm');ax.set_ylabel('WorldZ / mm');ax.set_title(title);ax.legend(loc='lower left',fontsize=8)
fig.suptitle('Uninstalled inclined candidate — failed valve-cover clearance\nActual STEP geometry; source dimensions remain estimated');fig.tight_layout();p=OUT/'rocker-cover-conflict.png';fig.savefig(p,dpi=170)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'status':'RENDERED physical conflict; not a source comparison','inputs':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(c.__file__),rockp,coverp,ROOT/'inventory/engine/full-assembly.json']},'render':str(p.relative_to(ROOT)),'render_sha256':sha(p)}
(ROOT/'inventory/engine/timing-valvetrain-inclined-neighbors-render-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
