#!/usr/bin/env python3
"""Render saved CAD comparison; no geometry rebuild or source photographs."""
from pathlib import Path
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
root=Path(__file__).resolve().parents[1];out=root/'cad/engine/generated/timing-cover-pan-joint-proposal'
a=np.load(out/'terminal-preview.npz');fig,ax=plt.subplots(figsize=(11,8))
for i,color in [(0,'#ba8d46'),(1,'#397eb2')]:
 t=a[f'v{i}'][a[f'f{i}']][:,:,[1,2]];ax.add_collection(PolyCollection(t,facecolors=color,edgecolors='none',alpha=.9))
ax.plot([],[],color='#ba8d46',lw=6,label='Current main cover gasket estimate')
ax.plot([],[],color='#397eb2',lw=6,label='Unchanged current pan gasket front segment')
ax.annotate('Long terminal gap ≥ 13.625 mm',xy=(-116,-24),xytext=(-125,45),arrowprops={'arrowstyle':'->'})
ax.annotate('Short terminal region gap ≥ 37.228 mm',xy=(150,-20),xytext=(80,75),arrowprops={'arrowstyle':'->'})
ax.scatter([0],[0],marker='+',s=80,color='black',label='Fixed crank axis')
ax.set(xlim=(-150,250),ylim=(-85,215),xlabel='Y (model mm)',ylabel='Z (model mm)',title='Rejected joint registration: main-gasket terminals do not meet the pan gasket\nNo new bridge or sealant geometry is proposed');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(loc='upper left');fig.tight_layout();fig.savefig(out/'terminal-review.png',dpi=160)
