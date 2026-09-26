"""Actual candidate tessellation preview with installed accessory context."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_carrier_1994 as candidate
from assembly_math import transforms
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);poses=transforms(m);defs={d['id']:d for d in m['definitions']};source=Path(candidate.__file__).read_bytes()
parts=candidate.parts();colors={k:('#7d8997' if k=='ps-ac-support-bracket' else '#baaa91') for k in parts}
context={'ps-pump-reservoir','ps-pump-pulley','ac-compressor-front-cylinder','ac-compressor-rear-cylinder','ac-compressor-clutch-pulley'}
for o in m['occurrences']:
 if o['id'] in context:
  d=defs[o['definition']];parts[o['id']]=cad.import_step(ROOT/d['step'].lstrip('/')).moved(poses[o['id']]);colors[o['id']]=d['color']
arrays={}
for i,(k,s) in enumerate(parts.items()):
 assert s.is_valid and len(s.solids())==1,k
 vertices,faces=s.tessellate(.3,.25);arrays[f'vertices_{i}']=np.asarray([tuple(v) for v in vertices]);arrays[f'faces_{i}']=np.asarray(faces)
 offset=(0,0,0)
 if k.startswith('tensioner'):offset=(150,0,0)
 elif k in context:offset=(200,60,0)
 elif k.startswith('carrier-block'):offset=(0,100,0)
 elif k=='carrier-side-head-bolt-2':offset=(0,100,0)
 elif k=='carrier-front-head-bolt-1':offset=(100,0,0)
 arrays[f'explode_{i}']=np.array(offset)
assert (ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw
assert Path(candidate.__file__).read_bytes()==source
arrays['metadata']=np.array(json.dumps({'assembly':'1994 shared accessory carrier candidate','parts':len(parts),'colors':list(colors.values()),'identifiers':list(parts),'installed':False,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':hashlib.sha256(source).hexdigest()}))
np.savez_compressed(sys.argv[1],**arrays);print(sys.argv[1],flush=True)
