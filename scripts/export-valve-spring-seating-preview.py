"""Export close-up actual CAD spring-seat study for the existing raster renderer."""
from pathlib import Path
import json,sys,numpy as np
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_spring_seating_candidate import OUT,FIRST,BASE,INSTALLED,RETAINER_BOTTOM,spring
from valve_layout_candidate import VALVE_Y
layout=json.loads((FIRST/'occurrence-layout.json').read_text());arrays={};metadata=[]
for panel,kind in enumerate(['intake','exhaust']):
 x=layout['stations'][panel];seat=RETAINER_BOTTOM-INSTALLED[kind];tag='c1-'+kind
 parts={}
 for o in layout['occurrences']:
  if not(o['id'] in [tag+'-'+v for v in ['valve','seal','retainer','keeper-1','keeper-2']] or o['id']=='cylinder-head'):continue
  name=o['definition'];path=OUT/(name+'.step')
  if not path.exists():path=BASE/(name+'.step')
  pos=o['position'] if not o['id'].endswith('-seal') else [x,VALVE_Y,seat+4.5]
  parts[o['id']]=b.Pos(*pos)*b.Rot(*o['orientation'])*b.import_step(path)
 parts['spring']=b.Pos(x,VALVE_Y,seat)*spring(kind)
 parts['cylinder-head']&=b.Pos(x-6,-12,305)*b.Box(4,60,100)
 for oid,s in parts.items():
  v,f=s.tessellate(.12);i=len(metadata)
  arrays[f'v{i}']=np.asarray([tuple(p) for p in v]);arrays[f'f{i}']=np.asarray(f)
  color=[.72,.59,.28] if oid=='spring' else [.54,.64,.61] if oid=='cylinder-head' else [.65,.71,.75]
  metadata.append({'id':oid,'panel':panel,'color':color})
arrays['metadata']=np.array(json.dumps(metadata));np.savez_compressed('/private/tmp/valve-spring-seating-preview.npz',**arrays)
