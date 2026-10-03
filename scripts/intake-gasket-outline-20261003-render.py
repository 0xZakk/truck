"""Render saved exported mesh; no source pixels are redistributed."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
ROOT=Path(__file__).resolve().parents[1];N='intake-gasket-outline-20261003'
d=np.load(ROOT/'cad/engine/generated'/N/'review-data.npz');v=d['vertices'];f=d['faces'];tri=v[f]
fig,ax=plt.subplots(figsize=(16,4));ax.add_collection(PolyCollection(tri[:,:,:2],facecolors='#a9b4b9',edgecolors='none'))
ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('Engine X (mm)');ax.set_ylabel('Engine Y (mm)')
ax.set_title('Actual exported gasket mesh — full replacement-photo outline\nSix ports and nine attachment holes; scale/thickness estimated; not installed')
fig.tight_layout();fig.savefig(ROOT/'reference/engine'/f'{N}-mesh-review.png',dpi=150)
