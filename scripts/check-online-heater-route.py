"""Actual STEP q0 candidate interfaces and whole-stage neighbors; no mutation."""
from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
import online_heater_route_candidate as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return b.Compound(s)if isinstance(s,b.ShapeList)else s
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in norm(s).solids())if s else 0.
def bb(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
mp=R/'inventory/engine/corrected-engine-stage-v4.json';m=json.loads(mp.read_text());t=transforms(m,0,0);defs={q['id']:q for q in m['definitions']}
inputs={str(p.relative_to(R)):sha(p)for p in [mp,Path(__file__),Path(c.__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py',R/'cad/engine/cad_metrics.py',R/'inventory/engine/online-heater-route-export.json']}
hp=c.old.O/'housing.step';h=b.import_step(hp);inputs[str(hp.relative_to(R))]=sha(hp)
shapes={v:b.import_step(c.O/(v+'-tube.step'))for v in c.END_X}
for v in shapes:
 p=c.O/(v+'-tube.step');inputs[str(p.relative_to(R))]=sha(p)
# Deliberately coordinated neighboring pump interfaces, all world-mm exports.
overrides={'water-pump-housing':hp,'timing-cover':c.old.rear.O/'cover.step','timing-cover-main-gasket':c.old.rear.O/'main-gasket.step','water-pump-gasket':c.old.rear.O/'pump-gasket.step'}
r={'status':'RUNNING','scope':'three inferred tube endpoints vs actual v4 q0, with explicitly listed conditional coordinated pump/rear-interface substitutions','inputs':inputs,'overrides':{k:str(p.relative_to(R))for k,p in overrides.items()},'interfaces':{},'pairs':[],'errors':[],'conflicts':[],'bounds_excluded':[],'threshold_mm3':.1,'broadphase_padding_mm':2.,'housing_unchanged':True}
out=R/'inventory/engine/online-heater-route-check.json'
def save():out.write_text(json.dumps(r,indent=2)+'\n')
for v,s in shapes.items():
 try:
  socket=c.old.segment(8,c.START,c.ROOT);sf=b.Compound([f for f in socket.faces()if f.geom_type==b.GeomType.CYLINDER]);contacts={}
  for n,part in [('housing',h),('tube',s)]:
   op=BRepAlgoAPI_Cut(sf.wrapped,b.Compound(list(part.faces())).wrapped);op.Build();assert op.IsDone();contacts[n]={'expected_area_mm2':sf.area,'missing_area_mm2':b.Compound(op.Shape()).area}
  probe=c.sweep(.7,v)+c.old.segment(.7,c.ROOT-46*c.DIR,c.START+c.DIR);wall=c.sweep(7.9,v)-c.sweep(6.6,v);plug=b.Pos(*(c.ROOT+10*c.DIR))*b.Sphere(2)
  r['interfaces'][v]={'housing_tube_overlap_mm3':vol(h.intersect(s)),'lumen_obstruction_mm3':vol(probe.intersect(b.Compound([h,s]))),'plug_fault_overlap_mm3':vol(probe.intersect(plug)),'wall_gauge_missing_mm3':vol(norm(wall).cut(s)),'socket_contacts':contacts}
 except Exception as e:r['errors'].append({'variant':v,'interface_error':repr(e)})
save();loaded={};vb={v:bb(s)for v,s in shapes.items()}
for index,o in enumerate(m['occurrences'],1):
 n=o['id']
 if n=='heater-pump-return-elbow':continue
 try:
  if n in overrides:
   p=overrides[n];s=b.import_step(p)
  else:
   p=R/defs[o['definition']]['step'].lstrip('/')
   if p not in loaded:loaded[p]=b.import_step(p)
   s=t[n]*occurrence_shape(o,loaded[p],0,0)
  inputs[str(p.relative_to(R))]=sha(p);box=bb(s);tested=False
  for v,tube in shapes.items():
   if np.any(np.minimum(box[1],vb[v][1])-np.maximum(box[0],vb[v][0]) < -2):continue
   tested=True;row={'variant':v,'neighbor':n}
   try:
    hit=norm(tube.intersect(s));volume=vol(hit);row['overlap_mm3']=volume
    if volume>.1:
     wp=c.O/(v+'__'+n+'.step');b.export_step(hit,wp);row.update(witness=str(wp.relative_to(R)),witness_sha256=sha(wp),bounds_mm=bb(hit).tolist());r['conflicts'].append(row);print('OVERLAP',v,n,volume,flush=True)
   except Exception as e:row['error']=repr(e);r['errors'].append(row)
   r['pairs'].append(row)
  if not tested:r['bounds_excluded'].append(n)
 except Exception as e:r['errors'].append({'neighbor':n,'error':repr(e)})
 if index%100==0:print('CHECKED',index,'pairs',len(r['pairs']),flush=True);save()
r['input_changes']=[p for p,h in inputs.items()if sha(R/p)!=h]
r['status']='FAIL'if r['conflicts']else'INCONCLUSIVE'if r['errors']or r['input_changes']else'PASS static conditional neighbors only'
save();print(r['status'],'pairs',len(r['pairs']),'conflicts',len(r['conflicts']),'errors',len(r['errors']),flush=True)
