from pathlib import Path
import json,hashlib,numpy as np
from types import SimpleNamespace
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];rp=R/'reference/engine/pump-height-20261002-ports-trial3.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=json.loads((R/'reference/engine/pump-height-20261002-mesh.json').read_text());data=np.load(R/'reference/engine/pump-height-20261002-meshes.npz');meshes={n:SimpleNamespace(triangles=data[n+'__vertices'][data[n+'__faces']])for n in rows}
fig=plt.figure(figsize=(13,7));ax=fig.add_subplot(121,projection='3d');sec=fig.add_subplot(122)
colors={'water-pump-housing':'#819da2','heater-pump-return-elbow':'#b79b51','water-pump-shaft':'#c05d36','water-pump-pulley':'#333d50','water-pump-drive-hub':'#d1944d','water-pump-bearing':'#6a8e5b'}
for n,m in meshes.items():
 if n.startswith(('fan-clutch-','cooling-fan-','water-pump-pulley-bolt')):continue
 color=colors.get(n,'#986bac');tris=m.triangles
 if False:tris=tris[tris.mean(1)[:,1]>=-32]
 ax.add_collection3d(Poly3DCollection(tris,facecolor=color,edgecolor='none',alpha=1))
 segments=[]
 for tri in m.triangles:
  hits=[]
  for i,j in [(0,1),(1,2),(2,0)]:
   u,v=tri[i],tri[j]
   if (u[1]+32)*(v[1]+32)<0:hits.append(u+(-32-u[1])/(v[1]-u[1])*(v-u))
  if len(hits)==2:segments.append(np.array(hits)[:,[0,2]])
 from matplotlib.collections import LineCollection
 sec.add_collection(LineCollection(segments,colors=color,linewidths=.7))
ax.set(xlim=(350,505),ylim=(-180,85),zlim=(80,435),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((155,265,355));ax.view_init(25,140);ax.set_title('Actual whole exported meshes / ports')
sec.set(xlim=(355,505),ylim=(105,240),xlabel='X mm',ylabel='Z mm',aspect='equal',title='Actual mesh section at shaft Y−32');sec.axvline(375,color='black',ls=':');sec.axvline(473.43,color='orange',ls=':');sec.grid(alpha=.2)
fig.suptitle('98.43mm replacement-height hypothesis — no installation\nPorts and internals estimated; affected-neighbor failures retained');fig.tight_layout();out=R/'reference/engine/pump-height-20261002-review-full.png';fig.savefig(out,dpi=140)
(R/'reference/engine/pump-height-20261002-visual-full.json').write_text(json.dumps({'parts':rows,'image':str(out.relative_to(R)),'image_sha256':sha(out),'inputs':{str(p.relative_to(R)):sha(p)for p in[rp,Path(__file__)]},'section_is_mesh_plane_not_fluid_proof':True},indent=2)+'\n');print('EXPORTED',len(rows),flush=True)
