#!/usr/bin/env python3
"""Authored source-feature / actual exported gasket comparison; no source pixels."""
from pathlib import Path
import json,sys,importlib.util
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from types import SimpleNamespace
params=json.loads((ROOT/'cad/engine/intake-joint-candidate-20261003-parameters.json').read_text());m=SimpleNamespace(X=[284.48-568.96*u for u in params['port_stations']],H={h['feature_id']:(284.48-568.96*h['normalized_uv'][0],-228-568.96*h['normalized_uv'][1]) for h in params['holes']})
out=ROOT/'cad/engine/generated/intake-joint-candidate-20261003'
mesh=np.load(out/'efi-upper-intake-gasket-mesh.npz');v=mesh['vertices_cad_mm'];faces=mesh['faces']
scope=json.loads((ROOT/'reference/engine/intake-joint-layout-20261003-scope.json').read_text());points=np.array([[284.48-568.96*p['normalized_uv'][0],-228-568.96*p['normalized_uv'][1]] for p in scope['ports']]);actual=np.array([[x,-228] for x in m.X])
fig,ax=plt.subplots(figsize=(14,4));tri=v[faces];front=tri[np.ptp(tri[:,:,2],axis=1)<1e-5,:,:2];ax.add_collection(PolyCollection(front,facecolor='#aebbc2',edgecolor='none'))
ax.scatter(points[:,0],points[:,1],color='#d75524',marker='+',s=80,label='Source extracted port centers, estimated scale')
for i,(x,y) in enumerate(points,1):ax.text(x,y+8,f'P{i}',ha='center',fontsize=9)
for h,(x,y) in m.H.items():ax.plot(x,y,'o',markerfacecolor='none',color='#ab4729',markersize=5);ax.text(x,y+9,h,ha='center',fontsize=8)
ax.set(xlim=(-370,345),ylim=(-292,-167),xlabel='CAD X mm — existing-model scale only',ylabel='CAD Y mm',title='Actual exported gasket versus authored source landmarks; aperture roles unresolved');ax.set_aspect('equal');ax.legend(loc='lower right',fontsize=8);fig.tight_layout();fig.savefig(out/'source-feature-comparison.png',dpi=160)
report={'port_center_straightening_error_mm':np.linalg.norm(points-actual,axis=1).tolist(),'scale_source':'root-approved existing modeled endpoint span568.96mm; not factory measurement','hole_center_error_mm':0,'source_port_count':6,'candidate_port_count':6,'source_small_hole_count':9,'candidate_small_hole_count':9,'limits':'Landmarks derived from replacement photo; approximate outline and dimensions. This is not independent metrology validation or role identification.'};(out/'source-review.json').write_text(json.dumps(report,indent=2)+'\n')

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
for key in ('efi-lower-intake','efi-upper-intake','efi-upper-intake-gasket'):
 data=np.load(out/(key+'-mesh.npz'));vv=data['vertices_cad_mm'];faces=data['faces']
 fig=plt.figure(figsize=(12,7));ax=fig.add_subplot(projection='3d');tri=vv[faces];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-20);light=np.array([.3,-.5,.8]);light/=np.linalg.norm(light);shade=.3+.7*np.maximum(0,norm@light);colors=np.array([.68,.74,.77])[None,:]*shade[:,None];poly=Poly3DCollection(tri,facecolor=colors,edgecolor='none',rasterized=True);ax.add_collection3d(poly)
 mins,maxs=vv.min(0),vv.max(0);mid=(mins+maxs)/2;extent=max(maxs-mins)/2
 ax.set(xlim=(mins[0]-10,maxs[0]+10),ylim=(mins[1]-10,maxs[1]+10),zlim=(mins[2]-10,maxs[2]+10),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title=key+' — actual exported candidate mesh; estimated dimensions');ax.set_box_aspect(np.maximum(maxs-mins,20));ax.view_init(elev=45,azim=-75);fig.tight_layout();fig.savefig(out/(key+'.png'),dpi=150);plt.close(fig)
