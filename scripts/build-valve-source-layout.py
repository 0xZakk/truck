"""Build first two stations from immutable first-stage candidate, no live writes.

All-cylinder build will adopt root's separately accepted source baseline.
"""
from pathlib import Path
import json,sys,hashlib,math
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import valve_source_layout as v
from valve_layout_candidate import OUT as FIRST,BASE
layout=json.loads((FIRST/'occurrence-layout.json').read_text());defs={};hashes={}
for o in layout['occurrences']:
 name=o['definition'];p=FIRST/(name+'.step')
 if not p.exists():p=BASE/(name+'.step')
 if name not in defs:defs[name]=b.import_step(p);hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
changed={'valve-cover':v.cover(),'rocker-arm':v.rocker(),'pushrod':v.pushrod(),'lifter-body':v.lifter_body(defs['lifter-body']),'lifter-pushrod-cup':v.lifter_cup(),'valve-seal':v.seal(),
'cylinder-head':v.head_adapter(defs['cylinder-head'],layout['stations'])}
for kind in v.LENGTHS:
 changed[kind+'-valve']=v.valve(defs[kind+'-valve'],kind);changed[kind+'-spring']=v.spring(kind)
for name,s in changed.items():
 assert s.is_valid and len(s.solids())==1,(name,type(s))
 b.export_step(s,v.OUT/(name+'.step'))
placed={};out_layout=[]
for original in layout['occurrences']:
 o=dict(original);name=o['definition'];oid=o['id'];pos=list(o['position']);rot=list(o['orientation'])
 for kind,x in zip(['intake','exhaust'],layout['stations']):
  tag='c1-'+kind
  if not oid.startswith(tag+'-'):continue
  s=v.solve(0,kind);delta=v.LENGTHS[kind]-109
  if oid.endswith('-valve'):pass
  elif oid.endswith('-spring') and '-lifter-' not in oid:
   pos=[x,v.VALVE_Y,363+delta-v.INSTALLED[kind]];name=kind+'-spring'
  elif oid.endswith('-seal'):pos=[x,v.VALVE_Y,363+delta-v.INSTALLED[kind]+4.5]
  elif any(oid.endswith('-'+a) for a in ['retainer','keeper-1','keeper-2']) and '-lifter-' not in oid:pos[2]+=delta
  elif oid.endswith('-rocker'):pos=[x,v.PIVOT_Y,s['pivot_z']];rot=[math.degrees(s['angle']),0,0]
  elif oid.endswith('-fulcrum') or oid.endswith('-rocker-bolt'):pos=[x,v.PIVOT_Y,s['pivot_z']]
  elif oid.endswith('-guide'):pos=[x,v.PIVOT_Y,s['pivot_z']-18]
  elif oid.endswith('-pushrod'):
   top,bottom=s['top'],s['bottom'];pos=[x,(top[0]+bottom[0])/2,(top[1]+bottom[1])/2];rot=[-math.degrees(math.atan2(top[0]-bottom[0],top[1]-bottom[1])),0,0]
  elif '-lifter-' in oid:pos[2]-=1.2
 shape=changed.get(name,defs.get(name));placed[oid]=b.Pos(*pos)*b.Rot(*rot)*shape
 out_layout.append({**o,'definition':name,'position':pos,'orientation':rot})
b.export_step(b.Compound(children=list(placed.values())),v.OUT/'two-station-assembly.step')
(v.OUT/'occurrence-layout.json').write_text(json.dumps({'stations':layout['stations'],'occurrences':out_layout},indent=2)+'\n')
r=v.metadata();r['input_hashes']=hashes;r['scope']='First two coordinated stations; rest and motion audits separate. No live or all12 acceptance.'
r['shape_hashes']={n:hashlib.sha256((v.OUT/(n+'.step')).read_bytes()).hexdigest() for n in changed}
(v.OUT/'provenance.json').write_text(json.dumps(r,indent=2)+'\n');print('Built',len(changed),'definitions',len(placed),'placed components')
