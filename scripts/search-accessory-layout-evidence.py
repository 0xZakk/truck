"""Search schematic-consistent bounded accessory stations after bounds screening.
This is a local discrete search, not a proof of a global optimum.
"""
import sys,json,math,random
from pathlib import Path
import numpy as np
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cad/engine'));import accessory_belt as b
valid=json.load(open('/private/tmp/truck-layout-valid.json'));ids=list(valid);base={n['id']:n for n in b.PULLEYS};random.seed(49)
raw=np.load('/private/tmp/truck-layout-bounds.npz',allow_pickle=True);boxes=raw['boxes'];owners=raw['owners'];bs={k:boxes[owners==k] for k in ids}
@lru_cache(None)
def clash(k,km,l,lm):
 a=bs[k]+[0,*km];c=bs[l]+[0,*lm]
 if np.any(np.minimum(a[:,1].max(0),c[:,1].max(0))-np.maximum(a[:,0].min(0),c[:,0].min(0))<=.01):return False
 return np.all(np.minimum(a[:,None,1],c[None,:,1])-np.maximum(a[:,None,0],c[None,:,0])>.01,axis=2).any()
def evaluate(values):
 nodes=[dict(n) for n in b.PULLEYS]
 for n in nodes:
  if n['id'] in values:n['center']=tuple(a+c for a,c in zip(n['center'],values[n['id']]))
 centers={n['id']:n['center'] for n in nodes}
 if not (centers['TENS'][0]>centers['WP'][0] and centers['PS'][1]>centers['TENS'][1]>centers['ALT'][1]>centers['WP'][1]>=centers['AC'][1] and centers['ALT'][1]>centers['AP'][1]>centers['CS'][1]):return 1e6
 try:s=b.solve(nodes,False)
 except AssertionError:return 1e6
 if abs(sum(-a['side']*a['wrap_degrees'] for a in s['arcs'])+360)>1e-5:return 1e6
 for i in range(len(nodes)):
  for j in range(i):
   if math.dist(nodes[i]['center'],nodes[j]['center'])<nodes[i]['radius']+nodes[j]['radius']+1:return 1e6
 for i,k in enumerate(ids):
  for l in ids[:i]:
   if clash(k,tuple(values[k]),l,tuple(values[l])):return 1e6
 return s['length']
best=(1e6,None)
for iteration in range(3):
 values={'ALT':[0,-30],'PS':[0,30],'AC':[30,60],'AP':[-50,60],'TENS':[100,-20]} if iteration==0 else {k:random.choice(v) for k,v in valid.items()}
 for sweep in range(5):
  for k in random.sample(ids,len(ids)):
   options=[]
   for move in valid[k]:
    v={**values,k:move};score=evaluate(v);options.append((score,move))
   _,values[k]=min(options)
 score=evaluate(values)
 if score<best[0]:best=(score,values.copy());print(best,flush=True)
Path('/private/tmp/truck-layout-evidence-optimum.json').write_text(json.dumps({'length':best[0],'displacements':best[1]},indent=2))
