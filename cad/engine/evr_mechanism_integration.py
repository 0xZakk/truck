"""Scoped EVR adapter: same original occurrence frame, illustrative internals."""
from pathlib import Path
import hashlib
import build123d as b
from OCP.BRepTools import BRepTools
import evr,evr_mechanism_candidate as candidate
import iac_attachment_integration as frames
from cad_metrics import support_bounds
ROOT=Path(__file__).resolve().parents[2]
REPLACED={'evr-body','evr-cap','evr-terminal-supply','evr-terminal-control'}
NEW_IDS={'evr-vent-filter-illustrative','evr-core-illustrative','evr-bobbin-illustrative','evr-winding-illustrative','evr-magnetic-shell-illustrative','evr-disc-illustrative','evr-disc-spring-illustrative'}
CHANGED_IDS=GEOMETRY_IDS=REPLACED|NEW_IDS
NEW_OCCURRENCES=NEW_IDS
SOURCE_IDS=['evr-detail-mechanism-comparison']
GAPS=['Exact1994 supports filtered vent and electromagnetic disc/orifice operation. Complete hidden arrangement is an explicitly illustrative positive-gain comparison, not a factory internal replica.',
'All new dimensions, fifteen winding turns, wire size, spring rate/preload, filter permeability pattern and cap bead/groove are uncalibrated estimates. Actual installed identity remains unknown.',
'Five discrete disc/spring poses illustrate vent opening only; no PCM duty-cycle, pressure, resistance, force, flow or elastic simulation. Mounting bracket, fasteners and vehicle hose routing remain unfinished.']
LABELS={'evr-body':'EVR chamber and ports','evr-cap':'EVR vent cap and illustrative capture','evr-terminal-supply':'EVR supply terminal','evr-terminal-control':'EVR control terminal','evr-vent-filter-illustrative':'EVR filter · illustrative','evr-core-illustrative':'EVR hollow core · illustrative','evr-bobbin-illustrative':'EVR winding insulator · illustrative','evr-winding-illustrative':'EVR continuous winding · illustrative','evr-magnetic-shell-illustrative':'EVR magnetic shell · illustrative','evr-disc-illustrative':'EVR vent disc · illustrative','evr-disc-spring-illustrative':'EVR disc spring · illustrative'}
COLORS={'evr-vent-filter-illustrative':'#d6b857','evr-core-illustrative':'#627c94','evr-bobbin-illustrative':'#ceb989','evr-winding-illustrative':'#b77643','evr-magnetic-shell-illustrative':'#8c969d','evr-disc-illustrative':'#b6bcc2','evr-disc-spring-illustrative':'#9c9ca1'}
def sources():
 p=ROOT/'reference/engine/evr-detail-mechanism-review.json'
 return {SOURCE_IDS[0]:dict(title='EVR exact1994 topology and comparative illustrative mechanism',path='/'+str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),url='https://github.com/0xZakk/truck/issues/58')}
def install(define,add,group,definitions,occurrences,assemblies,shapes):
 old={d['id']:d for d in definitions};rows={i:[o for o in occurrences if o['definition']==i] for i in REPLACED}
 if any(len(v)!=1 for v in rows.values()):raise ValueError('Expected exactly one occurrence for each original EVR part')
 anchor=rows['evr-body'][0];af=frames.occurrence_frame(anchor,assemblies)
 for i,v in rows.items():
  if v[0]['parent']!=anchor['parent'] or frames.frame_error(af,frames.occurrence_frame(v[0],assemblies))>1e-6:raise ValueError('Changed EVR relative frame: '+i)
 parts=candidate.build(.8)
 definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS];occurrences[:]=[o for o in occurrences if o['id'] not in NEW_IDS]
 for ident in sorted(CHANGED_IDS):
  prior=old.get(ident,{});shape=parts[ident];BRepTools.Clean_s(shape.wrapped);shape.tessellate(.02 if ident=='evr-body' else .025,.06 if ident=='evr-body' else .1)
  fn=prior.get('function','') if ident in {'evr-terminal-supply','evr-terminal-control'} else 'Illustrative positive-gain EVR component; see source-bound mechanism lesson. Geometry and calibration are not production measurements.'
  gaps=[g for g in prior.get('unresolved',[]) if g!=evr.GAPS[1]]
  define(ident,shape,LABELS[ident],fn,prior.get('system','induction'),prior.get('color',COLORS.get(ident,'#9c9ca1')),list(dict.fromkeys(prior.get('sources',evr.SOURCES)+SOURCE_IDS)),list(dict.fromkeys(gaps+GAPS)),prior.get('dimension_claims',[]),prepared=True)
  row=next(d for d in definitions if d['id']==ident);box=support_bounds(shape);row['model_bounds_mm']=list(box.size)
  for o in occurrences:
   if o['definition']==ident:o.update(name=LABELS[ident],function=fn)
 for n,ident in enumerate(sorted(NEW_IDS)):
  add(ident,ident,anchor['parent'],pos=anchor['position_cad_mm'],rotation=anchor.get('rotation_cad_deg',[0,0,0]),explode=(-70,0,80+15*n))
 return dict(changed_definitions=sorted(CHANGED_IDS),geometry_definitions=sorted(CHANGED_IDS),changed_occurrences=sorted(CHANGED_IDS),new_definitions=sorted(NEW_IDS),new_occurrences=sorted(NEW_IDS))

def mesh_bounds(path):
 """Read exporter GLB accessor bounds; reject hidden node transforms."""
 import json,struct,numpy as np
 with open(path,'rb') as f:
  header=f.read(20);magic,version,total,length,kind=struct.unpack('<5I',header)
  if magic!=0x46546c67 or version!=2 or kind!=0x4e4f534a:raise ValueError('Expected GLB2 JSON chunk')
  j=json.loads(f.read(length))
 if any(any(k in n for k in ['translation','rotation','scale','matrix']) for n in j.get('nodes',[])):
  import trimesh
  v=np.asarray(trimesh.load(path,force='mesh').vertices)
  v=v[:,[0,2,1]]*np.array([1,-1,1])*1000
  return np.array([v.min(0),v.max(0)])
 rows=[j['accessors'][p['attributes']['POSITION']] for m in j['meshes'] for p in m['primitives']]
 v=np.array([r[k] for r in rows for k in ['min','max']]);v=v[:,[0,2,1]]*np.array([1,-1,1])*1000
 return np.array([v.min(0),v.max(0)])
def neighbor_ids(m):
 import numpy as np,itertools
 from assembly_math import transforms
 D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m);inv=poses['evr-body'].inverse();cache={};result=[]
 region=np.array([[-20,-35,-9],[34,35,60]])
 for key,o in O.items():
  if key in CHANGED_IDS:continue
  ident=o['definition']
  if ident not in cache:cache[ident]=mesh_bounds(ROOT/D[ident]['glb'].lstrip('/'))
  low,high=cache[ident];loc=inv*poses[key];v=np.array([tuple(b.Vertex(*p).moved(loc).center()) for p in itertools.product(*zip(low,high))])
  if np.all(v.min(0)<=region[1]+.5) and np.all(region[0]<=v.max(0)+.5):result.append(key)
 return sorted(result)
