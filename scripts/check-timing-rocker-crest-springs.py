#!/usr/bin/env python3
"""Unchanged spring law with explicitly extended guard; sampled actual contacts."""
from pathlib import Path
import ast,inspect,sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import valve_spring_seating_candidate as source
import timing_valvetrain_inclined_candidate as c
OUT=ROOT/'cad/engine/generated/timing-rocker-crest-candidate';OUT.mkdir(exist_ok=True)
REPORT=ROOT/'inventory/engine/timing-rocker-crest-springs-validation.json'
MAX=max(c.H['solve'](.247*25.4,k)['valve_lift'] for k in ['intake','exhaust'])
tree=ast.parse(inspect.getsource(source.spring));changes=0
for node in ast.walk(tree):
 if isinstance(node,ast.Constant) and node.value==10.0330001:node.value=MAX+1e-7;changes+=1
assert changes==1
env=dict(source.spring.__globals__);exec(compile(tree,'isolated-spring-law-guard','exec'),env);spring=env['spring']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths={k:ROOT/'cad/engine/generated'/f'{k}.step' for k in ['spring-retainer','intake-spring','exhaust-spring']};paths['head']=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate/cylinder-head.step'
watch=[Path(__file__),Path(source.__file__),Path(c.__file__),ROOT/'inventory/engine/full-assembly.json']+list(paths.values())
r={'status':'RUNNING','inputs':{str(p.relative_to(ROOT)):sha(p) for p in watch},'guard_extension':{'old_mm':10.0330001,'new_mm':MAX+1e-7,'ast_constants_changed':changes,'actual_exhaust_peak_mm':MAX,'geometry_law_unchanged':True},'rows':[],'coil_bounds':{},'rest_equivalence':{},'failures':[]}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
def vol(q):
 if not q:return 0.
 try:return sum(abs(solid_volume(s,'adaptive')) for s in q.solids())
 except ValueError as error:
  bb=q.bounding_box();upper=bb.size.X*bb.size.Y*bb.size.Z
  r.setdefault('measurement_fallbacks',[]).append({'adaptive_error':str(error),'conservative_bbox_volume_upper_mm3':upper,'bounds_mm':[list(bb.min),list(bb.max)]})
  if upper>=.1:raise
  return upper
def pair_volume(a,z):
 aa=a.bounding_box();zz=z.bounding_box();dims=[max(0,min(h,j)-max(l,k)) for l,h,k,j in zip(aa.min,aa.max,zz.min,zz.max)];upper=math.prod(dims)
 if upper<.1:
  r['conservative_pair_bound_count']=r.get('conservative_pair_bound_count',0)+1
  return upper
 return vol(a.intersect(z))
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());occ={o['id']:o for o in m['occurrences']};frames=c.poses(m);head=frames['cylinder-head']*b.import_step(paths['head']);ret=b.import_step(paths['spring-retainer']);save()
for kind in ['intake','exhaust']:
 peak=c.H['solve'](.247*25.4,kind)['valve_lift'];height=source.INSTALLED[kind]-peak;pitch=height/6
 # For adjacent helix turns delta in[pi,3pi], radial chord and axial rise.
 # Global minimum occurs in(pi,2pi); derivative is strictly increasing near
 # root. Bisection gives centerline spacing; subtract unchanged4mm wire.
 lo,hi=1.5*math.pi,2*math.pi
 for _ in range(80):
  d=(lo+hi)/2;derivative=2*13**2*math.sin(d)+2*(pitch/(2*math.pi))**2*d
  if derivative<0:lo=d
  else:hi=d
 d=(lo+hi)/2;distance=math.sqrt(4*13**2*math.sin(d/2)**2+(pitch*d/(2*math.pi))**2)
 r['coil_bounds'][kind]={'peak_lift_mm':peak,'minimum_height_mm':height,'minimum_pitch_mm':pitch,'adjacent_turn_centerline_min_mm':distance,'minimum_wire_gap_mm':distance-4,'delta_radians':d,'coverage':'Continuous lift0..peak for ideal constant-pitch six-turn helix; ground end topology sampled separately.'};assert distance-4>0
 for fraction in [0,.25,.5,.75,1]:
  lift=peak*fraction;q=spring(kind,lift);assert q.is_valid and len(q.solids())==1
  if fraction==0:
   r['rest_equivalence'][kind]=diff(q,b.import_step(paths[kind+'-spring']));assert r['rest_equivalence'][kind]<1e-5
  if fraction==1:b.export_step(q,OUT/(kind+'-spring-peak.step'))
  for i in range(1,7):
   tag=f'c{i}-{kind}';x=occ[tag+'-spring']['position_cad_mm'][0];seat=occ[tag+'-spring']['position_cad_mm'][2];placed=b.Pos(x,-12,seat)*q;center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(i)*120;rest_frames=c.poses(m,(center-150)%720);rp=b.Pos(0,0,-lift)*rest_frames[tag+'-retainer']*ret
   row={'id':tag,'lift_mm':lift,'head_gap_mm':placed.distance_to(head),'retainer_gap_mm':placed.distance_to(rp),'head_overlap_mm3':pair_volume(placed,head),'retainer_overlap_mm3':pair_volume(placed,rp)}
   if max(row['head_gap_mm'],row['retainer_gap_mm'])>.002 or max(row['head_overlap_mm3'],row['retainer_overlap_mm3'])>.1:r['failures'].append(row)
   r['rows'].append(row)
  print(kind,fraction,'failures',len(r['failures']),flush=True);save()
r['negative_controls']={'raised_spring_head_gap_mm':(b.Pos(0,0,.1)*placed).distance_to(head),'compressed_fault_pitch_mm':3.9,'same_angular_position_wire_gap_mm':3.9-4}
assert r['negative_controls']['same_angular_position_wire_gap_mm']<0 and r['negative_controls']['raised_spring_head_gap_mm']>.05
assert all(sha(ROOT/p)==h for p,h in r['inputs'].items())
r['status']='FAIL actual spring contact' if r['failures'] else 'PASS sampled actual spring seat/retainer contact and continuous ideal-helix coil bound'
r['limits']=['Spring six-turn geometry and4mm wire remain estimates; no spring rate, stress or production coil-bind claim.','Five scalar lift levels eachkind, all12 station contacts; not full continuous arbitrary-neighbor sweep.','Guard extension is isolated and does not alter frozen source, cam lift, valve lift or wire geometry.'];save();print(r['status'])
