#!/usr/bin/env python3
"""Bounded real-CAD neighbor triage, with explicitly conservative spring envelopes."""
from pathlib import Path
import sys,json,hashlib,math,argparse,itertools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_valvetrain_inclined_candidate as c
from valve_spring_seating_candidate import INSTALLED
parser=argparse.ArgumentParser();parser.add_argument('--triage',action='store_true');args=parser.parse_args()
OUT=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate';REPORT=ROOT/'inventory/engine/timing-valvetrain-inclined-neighbors-validation.json'
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
fixed=['cylinder-head','block','head-gasket','valve-cover','valve-cover-gasket'];suffixes=['rocker','pushrod','lifter-body','valve','spring','retainer','keeper-1','keeper-2','seal','guide','fulcrum','rocker-bolt','lifter-pushrod-cup'];targets=['rocker','pushrod','lifter-body','valve']
ids=fixed+[f'c{i}-{kind}-{suffix}' for i,kind,x in c.stations(m) for suffix in suffixes]
keys=set(occ[o]['definition'] for o in ids);paths={k:OUT/(k+'.step') if k in ['rocker-arm','cylinder-head','block','head-gasket'] else ROOT/defs[k]['step'].lstrip('/') for k in keys}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
watch=[Path(__file__),Path(c.__file__),ROOT/'inventory/engine/full-assembly.json',ROOT/'cad/engine/valve_spring_seating_candidate.py']+list(paths.values())
r={'status':'RUNNING','mode':'triage' if args.triage else 'sampled120','inputs':{str(p.relative_to(ROOT)):sha(p) for p in watch},'comparisons':0,'bounds_separated':0,'exact_tests':[],'conflicts':[],'spring_envelope_refinements':[],'cross_branch_x_bounds':[],'limits':['Finite event phases and axial endpoints only; no continuous general collision claim.','Dynamic springs use declared annular clearance envelope; overlap is inconclusive.','Valve guide/seat and intended mating contacts are still checked for positive volume; no unreported pair whitelist.']}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
sh={k:b.import_step(p) for k,p in paths.items()};save()
def bound(q):
 z=q.bounding_box();return ([z.min.X,z.min.Y,z.min.Z],[z.max.X,z.max.Y,z.max.Z])
def overlap(a,z):return all(min(a[1][i],z[1][i])-max(a[0][i],z[0][i])>1e-7 for i in range(3))
def witness(a,z):
 common=a.intersect(z)
 if common:
  for solid in common.solids():
   p=solid.center()
   if a.is_inside(p) and z.is_inside(p):return list(p)
 aa,zz=bound(a),bound(z);lo=[max(aa[0][i],zz[0][i]) for i in range(3)];hi=[min(aa[1][i],zz[1][i]) for i in range(3)]
 for p in itertools.product(*[[l+(h-l)*t for t in [.15,.35,.5,.65,.85]] for l,h in zip(lo,hi)]):
  if a.is_inside(p) and z.is_inside(p):return list(p)
 return None
# X extents are invariant under all contract motions; this bound covers all phases.
base=c.poses(m)
for (i,kind,x),(j,other,y) in itertools.combinations(c.stations(m),2):
 names1=[f'c{i}-{kind}-{s}' for s in suffixes];names2=[f'c{j}-{other}-{s}' for s in suffixes]
 bb1=[bound(base[n]*sh[occ[n]['definition']]) for n in names1];bb2=[bound(base[n]*sh[occ[n]['definition']]) for n in names2]
 a=[min(z[0][0] for z in bb1),max(z[1][0] for z in bb1)];z=[min(v[0][0] for v in bb2),max(v[1][0] for v in bb2)]
 gap=max(z[0]-a[1],a[0]-z[1]);r['cross_branch_x_bounds'].append({'branches':[f'c{i}-{kind}',f'c{j}-{other}'],'gap_mm':gap})
 assert gap>0
shift=a[0]-z[0];fault=[v+shift for v in z];faultgap=max(fault[0]-a[1],a[0]-fault[1])
r['cross_branch_fault_control']={'original_intervals':[a,z],'fault_translation_x_mm':shift,'fault_interval':fault,'fault_gap_mm':faultgap};assert faultgap<0
for i,kind,x in (c.stations(m)[:2] if args.triage else c.stations(m)):
 tag=f'c{i}-{kind}';center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(i)*120
 for off in ([-150,0] if args.triage else [-150,-96,0,96,150]):
  for axial in ([0.] if args.triage else [0.,-.1]):
   theta=(center+off)%720;frames=c.poses(m,theta,axial);s=c.contract.state(theta,i,kind,axial)
   names=fixed+[tag+'-'+suffix for suffix in suffixes];placed={n:frames[n]*sh[occ[n]['definition']] for n in names}
   dynamic=s['valve_lift']>1e-9
   if dynamic:
    h=INSTALLED[kind]-s['valve_lift'];seat=occ[tag+'-spring']['position_cad_mm'][2]
    placed[tag+'-spring']=b.Pos(x,-12,seat+h/2)*(b.Cylinder(15,h)-b.Cylinder(11,h+2))
   bounds={n:bound(q) for n,q in placed.items()};done=set()
   for suffix in targets:
    a=tag+'-'+suffix
    for z in names:
     if a==z or frozenset([a,z]) in done:continue
     done.add(frozenset([a,z]));r['comparisons']+=1
     if not overlap(bounds[a],bounds[z]):r['bounds_separated']+=1;continue
     common=placed[a].intersect(placed[z]);v=vol(common);row={'target':a,'neighbor':z,'theta':theta,'axial':axial,'overlap_mm3':v,'spring_envelope':dynamic and z.endswith('-spring')}
     r['exact_tests'].append(row)
     if v>.1:
      if row['spring_envelope']:r['spring_envelope_refinements'].append(row)
      else:
       row['strict_interior_witness']=witness(placed[a],placed[z]);r['conflicts'].append(row)
     save()
   print(tag,off,axial,'conflicts',len(r['conflicts']),'spring refinements',len(r['spring_envelope_refinements']),flush=True)
# Deliberately raise a verified clear rest rocker10 mm into the cover roof.
rest=c.poses(m,318);cover=rest['valve-cover']*sh['valve-cover'];rocker=rest['c1-intake-rocker']*sh['rocker-arm']
fault=b.Pos(0,0,10)*rocker
r['cover_fault_control']={'rest_overlap_mm3':vol(rocker.intersect(cover)),'translation_z_mm':10,'fault_overlap_mm3':vol(fault.intersect(cover)),'strict_interior_witness':witness(fault,cover)}
assert r['cover_fault_control']['rest_overlap_mm3']<.1 and r['cover_fault_control']['fault_overlap_mm3']>.1 and r['cover_fault_control']['strict_interior_witness']
assert all(sha(ROOT/p)==h for p,h in r['inputs'].items())
r['status']='FAIL physical conflicts found' if r['conflicts'] else ('INCONCLUSIVE spring envelope refinement required' if r['spring_envelope_refinements'] else 'PASS bounded neighbor scope')
save();print(r['status'])
