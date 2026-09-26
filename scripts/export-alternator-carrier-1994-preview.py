"""Tessellate candidate front accessory context without modifying installed files."""
import json,sys
from pathlib import Path
import numpy as np
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import alternator_carrier_1994_candidate as candidate
from assembly_math import transforms
assembly=Path(sys.argv[1]);m=json.loads((assembly/'inventory/engine/full-assembly.json').read_text())
poses=transforms(m);defs={d['id']:d for d in m['definitions']}
parts=candidate.replacements();colors={k:'#899498' for k in parts}
context={'block','cylinder-head','coolant-outlet-housing','alternator-drive-housing','alternator-rear-housing','alternator-pulley','alternator-fan','ps-ac-support-bracket','tensioner-pulley-wheel','ps-pump-pulley','ac-compressor-clutch-pulley','water-pump-pulley','crank-damper','thermactor-pump-pulley','alt-engine-bracket-bolt-1','alt-engine-bracket-bolt-2'}
for o in m['occurrences']:
 if o['id'] in context:
  d=defs[o['definition']];s=cad.import_step(assembly/d['step'].lstrip('/')).moved(poses[o['id']])
  if o['parent']=='alternator-assembly':s=cad.Pos(*candidate.DISPLACEMENT)*s
  parts[o['id']]=s;colors[o['id']]=d['color']
arrays={}
for i,(identifier,s) in enumerate(parts.items()):
 vertices,faces=s.tessellate(.5,.3)
 arrays[f'vertices_{i}']=np.asarray([tuple(v) for v in vertices]);arrays[f'faces_{i}']=np.asarray(faces)
 arrays[f'explode_{i}']=np.array((80,0,0) if identifier.startswith('alternator') else (0,0,0))
arrays['metadata']=np.array(json.dumps({'assembly':'1994 alternator carrier candidate','parts':len(parts),'colors':list(colors.values()),'identifiers':list(parts),'installed':False}))
np.savez_compressed(sys.argv[2],**arrays);print('Saved',len(parts),'parts',sys.argv[2],flush=True)
