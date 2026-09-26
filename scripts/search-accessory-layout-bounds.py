"""Conservative mesh-bound station screening only; not a CAD fit certificate.
Writes small temporary search caches consumed by search-accessory-layout-evidence.py.
"""
import sys,json,math
from pathlib import Path
import numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
import accessory_belt as belt
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_bytes());poses=transforms(m);defs={d['id']:d for d in m['definitions']};parents={a['id']:a['parent'] for a in m['assemblies']}
groups={'alternator-assembly':'ALT','power-steering-pump-assembly':'PS','ac-compressor':'AC','thermactor-pump-assembly':'AP','tensioner-pulley-assembly':'TENS','tensioner-support-assembly':'TENS'}
def group(o):
 p=o['parent']
 while p:
  if p in groups:return groups[p]
  p=parents.get(p)
 return None
cache={};boxes=[];ids=[];owners=[]
for o in m['occurrences']:
 if o['parent']=='accessory-support-brackets':continue
 d=o['definition']
 if d not in cache:
  mesh=trimesh.load(ROOT/defs[d]['glb'].lstrip('/'),force='mesh');cache[d]=np.asarray(mesh.vertices)[:,[0,2,1]]*[1000,-1000,1000]
 t=poses[o['id']].wrapped.Transformation();mat=np.array([[t.Value(i,j) for j in range(1,5)] for i in range(1,4)])
 v=cache[d]@mat[:,:3].T+mat[:,3];boxes.append([v.min(0),v.max(0)]);ids.append(o['id']);owners.append(group(o))
boxes=np.array(boxes);owners=np.array(owners);fixed=boxes[owners==None]
valid={}
for g in ['ALT','PS','AC','AP','TENS']:
 moving=boxes[owners==g];allowed=[]
 # individual mesh-derived bounds, overconservative; not a clearance certification
 for dy in range(-120,121,10):
  for dz in range(-120,121,10):
   moved=moving+np.array([0,dy,dz]);over=np.minimum(moved[:,None,1],fixed[None,:,1])-np.maximum(moved[:,None,0],fixed[None,:,0]);bad=np.all(over>.01,axis=2)
   if not bad.any():allowed.append([dy,dz])
 valid[g]=allowed;print(g,len(allowed),allowed[:10],flush=True)
np.savez('/private/tmp/truck-layout-bounds.npz',boxes=boxes,owners=owners,ids=ids)
Path('/private/tmp/truck-layout-valid.json').write_text(json.dumps(valid))
