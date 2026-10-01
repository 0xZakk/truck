"""Actual STEP section comparison and mesh qualification of frozen block."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-seven-block-guard-study';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--extract' in sys.argv:
 sys.path.insert(0,str(ROOT/'cad/engine'));import build123d as b,trimesh;import timing_cover_seven_fastener_candidate as c
 p=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step';q=b.import_step(p);old=b.import_step(c.BLOCK);lines={}
 for name,s in [('old',old),('new',q)]:
  sec=b.section(s,b.Plane.YZ.offset(365.5));lines[name]=[[tuple(e.position_at(float(t)))for t in np.linspace(0,1,60)]for e in sec.edges()]
 (OUT/'sections.json').write_text(json.dumps(lines));v,f=q.tessellate(.08,.12);mesh=trimesh.Trimesh(np.array([tuple(vv)for vv in v]),np.array(f));mesh.merge_vertices(digits_vertex=6)
 r={'input_sha256':{str(x.relative_to(ROOT)):sha(x)for x in [p,c.BLOCK,Path(__file__)]},'valid':q.is_valid,'solids':len(q.solids()),'mesh_watertight':mesh.is_watertight,'mesh_winding_consistent':mesh.is_winding_consistent,'mesh_components':len(mesh.split(only_watertight=False)),'mesh_signed_volume_mm3':float(mesh.volume),'cad_mesh_bounds_error_mm':float(np.max(np.abs(mesh.bounds-np.array([tuple(q.bounding_box().min),tuple(q.bounding_box().max)]))))};(ROOT/'inventory/engine/timing-seven-block-mesh-review.json').write_text(json.dumps(r,indent=2)+'\n');print(r);raise SystemExit
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
lines=json.loads((OUT/'sections.json').read_text());fig,axes=plt.subplots(1,2,figsize=(13,7))
for ax in axes:
 for n,edges in lines.items():
  for i,e in enumerate(edges):
   p=np.array(e);ax.plot(p[:,1],p[:,2],color='#333333'if n=='old'else'#4488bb',ls='--'if n=='old'else'-',lw=1,label=n if i==0 else None)
 ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('Y mm');ax.set_ylabel('Z mm');ax.legend()
axes[0].set_xlim(-147,-98);axes[0].set_ylim(-35,12);axes[0].set_title('Main1/pan20 neighborhood\nBroadR12stock changes; functionalR6.2 checked separately')
axes[1].set_xlim(-110,45);axes[1].set_ylim(78,255);axes[1].set_title('Main3/pump region\nBroadR85stock changes; chamber/mounts checked separately')
fig.suptitle('Actual frozen block STEP sections atX365.5 — oldV3 dashed / seven-screw trial blue');fig.tight_layout();p=OUT/'guard-review.png';fig.savefig(p,dpi=160);r={'render':str(p.relative_to(ROOT)),'sha256':sha(p),'inputs_sha256':{str(x.relative_to(ROOT)):sha(x)for x in[OUT/'sections.json',Path(__file__)]}};(ROOT/'inventory/engine/timing-seven-block-visual-review.json').write_text(json.dumps(r,indent=2)+'\n')
