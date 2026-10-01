"""Verify serialized sealing proposal and render exported GLBs without CAD."""
from pathlib import Path
import json,hashlib,copy,sys
import numpy as np
R=Path(__file__).resolve().parents[1];P=R/'inventory/engine/timing-front-sealing-patch.json';j=json.loads(P.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((R/'inventory/engine/full-assembly.json').read_text())
def verify(p):
 assert p['manifest_sha256']==sha(R/'inventory/engine/full-assembly.json')
 assert p['front_patch_sha256']==sha(R/'inventory/engine/timing-front-coordinated-patch.json')
 for category in ['definitions','occurrences']:
  ids={q['id']for q in m[category]}
  for q in p[category]:assert q['before']is None and q['id']not in ids;ids.add(q['id'])
 for q in p['definitions']:
  for a in q['copy_assets'].values():assert sha(R/a['from'])==a['sha256']
 for k in ['learning','sources']:assert sha(R/p[k]['path'])==p[k]['sha256']
verify(j);controls={}
for name in ['stale-manifest','duplicate-occurrence','altered-asset']:
 bad=copy.deepcopy(j)
 if name=='stale-manifest':bad['manifest_sha256']='0'*64
 elif name=='duplicate-occurrence':bad['occurrences'].append(copy.deepcopy(bad['occurrences'][0]))
 else:bad['definitions'][0]['copy_assets']['glb']['sha256']='0'*64
 try:verify(bad);controls[name]=False
 except AssertionError:controls[name]=True
assert all(controls.values())
O=R/'cad/engine/generated/timing-front-sealing-stage'
if '--extract' in sys.argv:
 import trimesh
 data={}
 for n,q in enumerate(j['definitions']):
  mesh=trimesh.load(R/q['copy_assets']['glb']['from'],force='mesh');data[f'v{n}']=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000+np.array([403,0,0]);data[f'f{n}']=mesh.faces
 np.savez_compressed(O/'exported-mesh-review.npz',**data);sys.exit(0)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
fig=plt.figure(figsize=(13,6));colors=['#759785','#d7a345','#d7a345'];data=np.load(O/'exported-mesh-review.npz');meshes=[(data[f'v{n}'],data[f'f{n}'],color) for n,color in enumerate(colors)]
for i in [1,2]:
 ax=fig.add_subplot(1,2,i)
 for v,f,c in meshes:
  pc=PolyCollection(v[f][:,:,[1,2]],facecolor=c,edgecolor='none');ax.add_collection(pc)
 if i==1:ax.set(xlim=(-155,275),ylim=(-35,220));ax.set_title('Actual exported gasket and separate terminal deposits')
 else:ax.set(xlim=(-143,-102),ylim=(-25,-21));ax.set_title('Terminal 1: lower joint detail')
 ax.set_aspect('equal');ax.set_xlabel('Y mm');ax.set_ylabel('Z mm');ax.grid(alpha=.15)
fig.tight_layout();image=O/'review.png';fig.savefig(image,dpi=180);plt.close(fig)
r={'status':'PASS serialized guards and exported mesh review generated','negative_controls':controls,'patch_sha256':sha(P),'image':str(image.relative_to(R)),'image_sha256':sha(image),'checker_sha256':sha(Path(__file__))};(R/'inventory/engine/timing-front-sealing-serialization-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
