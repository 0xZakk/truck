"""Render the actual exported combined candidate; no source images."""
from pathlib import Path
import sys
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'cad/engine/generated/timing-front-block-expanded-seat-v2-candidate'
if '--extract' in sys.argv:
    import trimesh
    mesh = trimesh.load(OUT / 'block.glb', force='mesh')
    np.savez_compressed(OUT / 'render-mesh.npz', v=np.asarray(mesh.vertices)[:, [0, 2, 1]] * [1, -1, 1] * 1000, f=mesh.faces)
    raise SystemExit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m = np.load(OUT / 'render-mesh.npz'); v, f = m['v'], m['f']
fig = plt.figure(figsize=(14, 7))
for i, azimuth in enumerate([50, -50]):
    ax = fig.add_subplot(1, 2, i + 1, projection='3d')
    ax.add_collection3d(Poly3DCollection(v[f], facecolors='#9caeb4', edgecolor='none', shade=True))
    lo, hi = v.min(0), v.max(0)
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect(hi-lo); ax.view_init(30, azimuth)
    ax.set_xlabel('X mm'); ax.set_ylabel('Y mm'); ax.set_zlabel('Z mm')
fig.suptitle('Actual expanded-seat v2 block GLB — estimated geometry, uninstalled\nShared X300..365 transition with estimated10mm upper seat support; acceptance gates remain open')
fig.tight_layout(); fig.savefig(OUT / 'block-glb-review.png', dpi=140)
