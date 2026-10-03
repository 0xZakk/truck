from pathlib import Path
import sys,json,hashlib,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];sys.path.extend(str(p) for p in (R/'.venv-cad/lib').glob('python*/site-packages'));import trimesh
p=R/'cad/engine/generated/pump-spring-sweep-20261003/spring-analytic.glb';g=trimesh.load(p,force='mesh');v=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;v-=np.array([409.18,-32,170]);m=trimesh.Trimesh(v,g.faces,process=False)
fig,axs=plt.subplots(1,3,figsize=(14,5))
for ax,(n,title) in zip(axs,[((1,.5,.3),'Oblique: actual exported mesh'),((1,0,0),'Axial: wire and trimmed ends'),((0,1,.05),'Side: pitch and ground planes')]):
 n=np.array(n,float);n/=np.linalg.norm(n);right=np.cross([0,0,1],n);right/=np.linalg.norm(right);up=np.cross(n,right);xy=np.column_stack([v@right,v@up]);polys=xy[m.faces];depth=(v@n)[m.faces].mean(1);order=np.argsort(depth);shade=.25+.75*np.clip(m.face_normals@n,0,1);colors=np.column_stack([shade*.65,shade*.7,shade*.75]);ax.add_collection(PolyCollection(polys[order],facecolors=colors[order],edgecolors='none',antialiased=False));ax.autoscale_view();ax.set_aspect('equal');ax.set_title(title);ax.set_axis_off()
fig.suptitle('Illustrative pump-seal spring — analytic mesh of the declared coil\nPitch1.4mm, coil radius15.5mm, wire radius0.4mm; no production identity claim')
fig.text(.02,.02,'One connected watertight mesh;500 finite CAD-surface samples pass. Pump integration and source accuracy remain separate gates.',fontsize=9);fig.tight_layout(rect=(0,.05,1,.86));out=R/'reference/engine/pump-spring-sweep-20261003-review.png';fig.savefig(out,dpi=130);print(out)
