"""Actual candidate preview using frozen post-valve head and thermostat definitions."""
import json,sys
from pathlib import Path
import numpy as np
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import coolant_outlet_head_candidate as candidate
baseline=ROOT/'cad/engine/candidates/outlet-head-20260925/baseline'
m=json.loads((baseline/'manifest.json').read_text());defs={d['id']:d for d in m['definitions']}
head=cad.Pos(0,0,255.5)*candidate.head_interface(cad.import_step(baseline/'cylinder-head.step'))
# Show only the front portion; this crop is preview-only and never an installed head.
parts={'head-front-context':head & cad.Pos(352,0,295)*cad.Box(44,180,90)}
colors={'head-front-context':'#a1afb6'};offsets={'head-front-context':(0,0,0)}
local=candidate.parts();mount=cad.Pos(*candidate.POSITION)
for o in m['occurrences']:
 identifier=o['id'];d=o['definition']
 if d in local:
  if d=='heater-supply-ect-elbow':s=local[d]
  elif d=='thermostat-piston':s=mount*cad.Pos(*candidate.THERMOSTAT_POSITION)*local[d]
  elif d=='coolant-outlet-bolt':
   y,z=candidate.HOLES[int(identifier.rsplit('-',1)[1])-1];s=mount*cad.Pos(0,y,z)*local[d]
  else:s=mount*local[d]
  parts[identifier]=s;colors[identifier]=defs[d]['color'];offsets[identifier]=(180 if 'bolt' in identifier else 140 if 'housing' in identifier else 85,0,0)
 elif o['parent']=='thermostat-assembly':
  parts[identifier]=mount*cad.Pos(*candidate.THERMOSTAT_POSITION)*cad.import_step(baseline/(d+'.step'))
  colors[identifier]=defs[d]['color'];offsets[identifier]=(45,0,0)
 elif o['parent']=='engine-coolant-temperature-assembly':
  parts[identifier]=cad.Pos(*candidate.ect_position(identifier))*cad.import_step(baseline/(d+'.step'))
  colors[identifier]=defs[d]['color'];offsets[identifier]=(85,0,70)
arrays={}
for i,(identifier,s) in enumerate(parts.items()):
 vertices,faces=s.tessellate(.25,.25);arrays[f'vertices_{i}']=np.asarray([tuple(v) for v in vertices]);arrays[f'faces_{i}']=np.asarray(faces);arrays[f'explode_{i}']=np.asarray(offsets[identifier])
arrays['metadata']=np.array(json.dumps({'assembly':'Local head outlet and thermostat joint candidate','parts':len(parts),'colors':list(colors.values()),'identifiers':list(parts),'installed':False}))
np.savez_compressed(sys.argv[1],**arrays);print('Saved',len(parts),sys.argv[1])
