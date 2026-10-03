"""Render actual saved STEP tessellation and exported GLB, no invented geometry."""
from pathlib import Path
import json,platform
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
DATA=ROOT/'cad/engine/generated/text-to-cad-20261003/baseline/render-data.npz'
data=np.load(DATA)
fig=plt.figure(figsize=(14,10),facecolor='#f4f5f7')
for index,(key,section) in enumerate([('cad',False),('mesh',False),('cad',True),('mesh',True)]):
    ax=fig.add_subplot(2,2,index+1,projection='3d')
    verts=data[f'{key}_vertices'];faces=data[f'{key}_faces'];tris=verts[faces]
    if section:
        clipped=[]
        for triangle in tris:
            poly=[]
            for a,b in zip(triangle,np.roll(triangle,-1,axis=0)):
                ia,ib=a[1]<=0,b[1]<=0
                if ia:poly.append(a)
                if ia!=ib:poly.append(a+(b-a)*(-a[1]/(b[1]-a[1])))
            for k in range(1,len(poly)-1):clipped.append([poly[0],poly[k],poly[k+1]])
        tris=np.array(clipped)
    n=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12)
    light=np.array([-.3,-.4,.86]);light/=np.linalg.norm(light)
    shade=.5+.4*np.abs(n@light)
    colors=np.stack([shade*.77,shade*.82,shade*.88],axis=1)
    ax.add_collection3d(Poly3DCollection(tris,facecolors=colors,edgecolors='none'))
    ax.set(xlim=(-28,28),ylim=(-28,28),zlim=(0,11),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
    ax.set_box_aspect((56,56,16));ax.view_init(elev=33 if not section else 14,azim=-62 if not section else 85)
    ax.set_title(('Saved STEP tessellation' if key=='cad' else 'Saved GLB, converted to CAD mm')+(' — half-surface cutaway' if section else ' — opening view'))
fig.suptitle('MPS-59-A isolated replacement envelope\nEstimated 1 mm wall/floor; R1.5 outer / R0.5 inner. No source photograph; no installed fit claim.',fontsize=14)
fig.tight_layout(rect=[0,0,1,.94]);fig.savefig(HERE/'actual-renders.png',dpi=160);plt.close(fig)
(HERE/'render-environment.json').write_text(json.dumps({'python':platform.python_version(),'matplotlib':matplotlib.__version__,'numpy':np.__version__,'note':'Section clips mesh triangles at Y=0; open cut surfaces are visualization only, not changed artifacts.'},indent=2)+'\n')
print('Saved',HERE/'actual-renders.png')
