"""Review actual GLB surfaces/sections; prepare under CAD Python, render under plot Python."""
from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];P='pump-cover-candidate-20261003';rp=R/f'reference/engine/{P}-inlet-analytic-mesh.json';j=json.loads(rp.read_text());gp=R/j['path'];oldp=R/'cad/engine/generated/pump-cover-candidate-20261003/water-pump-housing.glb';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(gp)==j['sha256'];dp=R/f'reference/engine/{P}-inlet-analytic-render-data.npz'
if '--prepare' in sys.argv:
 import trimesh
 def load(p):
  m=trimesh.load(p,force='mesh');m.vertices=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;return m
 m=load(gp);old=load(oldp);data={'vertices':m.vertices,'faces':m.faces,'bounds':m.bounds}
 for name,mesh in [('old',old),('new',m)]:
  data[name]=trimesh.intersections.mesh_plane(mesh,plane_origin=(398,0,0),plane_normal=(1,0,0))
 np.savez_compressed(dp,**data);sys.exit()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
d=np.load(dp)
fig=plt.figure(figsize=(13,6));ax=fig.add_subplot(121,projection='3d');tri=d['vertices'][d['faces']];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-12);shade=.5+.5*np.abs(norm@np.array([.4,-.5,.75]));ax.add_collection3d(Poly3DCollection(tri,facecolors=np.array([.50,.66,.70])[None,:]*shade[:,None],edgecolor='none'));lo,hi=d['bounds'];ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),zlim=(lo[2],hi[2]));ax.set_box_aspect(hi-lo);ax.view_init(15,145);ax.set_axis_off();ax.set_title('Actual diagnostic GLB: attachment-side view')
ax=fig.add_subplot(122)
for name,color,label in [('old','#b55145','Frozen housing'),('new','#227c91','Own-axis channel successor')]:
 first=True
 for curve in d[name]:
  ax.plot(curve[:,1],curve[:,2],color=color,lw=1.5,label=label if first else None);first=False
ax.set(xlim=(-70,-30),ylim=(140,180),xlabel='World Y / mm',ylabel='World Z / mm',title='Actual mesh section X398 / inlet throat');ax.set_aspect('equal');ax.legend(fontsize=9)
fig.suptitle('Local inlet successor: flow probes clear; full gasket and bolt regions retained\nSame failed option B pose; no installed or factory-fidelity acceptance',fontsize=13);fig.tight_layout();out=R/f'reference/engine/{P}-inlet-analytic-review.png';fig.savefig(out,dpi=140)
(R/f'reference/engine/{P}-inlet-analytic-render.json').write_text(json.dumps({'image':str(out.relative_to(R)),'sha256':sha(out),'scope':'Actual exported GLB surfaces and mesh sections, no source pixels','inputs':{str(p.relative_to(R)):sha(p) for p in [rp,gp,oldp,dp,Path(__file__)]}},indent=2)+'\n')
