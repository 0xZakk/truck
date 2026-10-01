"""Actual exported part meshes plus exact STEP section at relocated socket."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate'
if '--sections' in sys.argv:
 sys.path.insert(0,str(ROOT/'cad/engine'));import build123d as b;import timing_pan21_lateral_candidate as c
 shapes={n:b.import_step(OUT/(n+'.step'))for n in ['cover','pan','pan-gasket']};shapes['screw']=b.Pos(*c.NEW)*b.import_step(c.MALE);shapes['washer']=b.Pos(*c.NEW)*b.import_step(c.WASHER)
 r={}
 for n,s in shapes.items():
  q=b.section(s,b.Plane.YZ.offset(390));r[n]=[[tuple(e.position_at(float(t)))for t in np.linspace(0,1,50)]for e in q.edges()]
 (OUT/'section-x390.json').write_text(json.dumps(r));raise SystemExit
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
camera=np.array([1,-1,.3]);camera/=np.linalg.norm(camera);right=np.cross([0,0,1],camera);right/=np.linalg.norm(right);up=np.cross(camera,right);basis=np.array([right,up,camera]).T
colors={'cover':'#91a8b4','pan':'#668879','pan-gasket':'#e7a847','screw':'#a589be','washer':'#b46c48'}
fig,(ax,sec)=plt.subplots(1,2,figsize=(15,8));ts=[];cs=[]
for name,offset in [('cover',0),('pan-gasket',-12),('pan',-35)]:
 m=np.load(OUT/(name+'-preview.npz'));v=m['vertices']+[0,0,offset];t=v[m['faces']];normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);keep=normal@camera>0;t=t[keep];normal=normal[keep];ts.append(t@basis);cs.append((.3+.7*np.clip(normal@camera,0,1))[:,None]*to_rgb(colors[name]))
t=np.concatenate(ts);col=np.concatenate(cs);order=np.argsort(t[:,:,2].mean(1));ax.add_collection(PolyCollection(t[order,:,:2],facecolors=col[order],edgecolors='none'));p=t[:,:,:2].reshape(-1,2);lo=p.min(0);hi=p.max(0);ax.set_xlim(lo[0]-20,hi[0]+20);ax.set_ylim(lo[1]-20,hi[1]+20);ax.set_aspect('equal');ax.axis('off');ax.set_title('Actual meshes; display-only vertical separation\nCover0 / gasket−12 / pan−35mm')
r=json.loads((OUT/'section-x390.json').read_text())
for n,edges in r.items():
 for i,e in enumerate(edges):
  p=np.array(e);sec.plot(p[:,1],p[:,2],color=colors[n],linewidth=1,label=n if i==0 else None)
sec.set_xlim(-125,-75);sec.set_ylim(-41,-3);sec.set_aspect('equal');sec.grid(alpha=.2);sec.set_xlabel('Y mm');sec.set_ylabel('Z mm');sec.legend();sec.set_title('Actual STEP sectionX390 through relocated blind socket\nSource female, real wall/floor and dry-side fastener')
fig.suptitle('Pan21 lateral feasibility candidate: Y−95mm — estimated datum and blind boss, not factory geometry');fig.tight_layout();p=OUT/'review.png';fig.savefig(p,dpi=160)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'render':str(p.relative_to(ROOT)),'sha256':sha(p),'inputs_sha256':{str(q.relative_to(ROOT)):sha(q)for q in [*OUT.glob('*-preview.npz'),OUT/'section-x390.json',Path(__file__)]}};(ROOT/'inventory/engine/timing-pan21-lateral-visual-review.json').write_text(json.dumps(r,indent=2)+'\n')
