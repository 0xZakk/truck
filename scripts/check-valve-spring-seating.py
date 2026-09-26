"""Exact local spring/guide candidate checks against saved first-stage neighbors."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_spring_seating_candidate import OUT,FIRST,BASE,INSTALLED,STEM_DIAMETER,GUIDE_DIAMETER,RETAINER_BOTTOM,HEAD_Z,spring
from valve_layout_candidate import VALVE_Y,intersect_volume,box_overlap,solve,PIVOT_Y,PIVOT_Z
layout=json.loads((FIRST/'occurrence-layout.json').read_text());parts={};defs={};hashes={}
for o in layout['occurrences']:
 name=o['definition'];p=OUT/(name+'.step')
 if not p.exists():p=FIRST/(name+'.step')
 if not p.exists():p=BASE/(name+'.step')
 if name not in defs:defs[name]=b.import_step(p);hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 parts[o['id']]=b.Pos(*o['position'])*b.Rot(*o['orientation'])*defs[name]
failures=[];contacts=[];checks=0;min_coil_gap=999;ground_faces=[]
for lift in [0,2.5,5,7.5,10.033]:
 pose=dict(parts)
 for kind,x in zip(['intake','exhaust'],layout['stations']):
  tag='c1-'+kind;seat=RETAINER_BOTTOM-INSTALLED[kind]
  pose[tag+'-spring']=b.Pos(x,VALVE_Y,seat)*spring(kind,lift)
  pose[tag+'-seal']=b.Pos(x,VALVE_Y,seat+4.5)*defs['valve-seal']
  for suffix in ['valve','retainer','keeper-1','keeper-2']:pose[tag+'-'+suffix]=b.Pos(0,0,-lift)*parts[tag+'-'+suffix]
  # Invert the calibrated linkage to keep the neighboring rocker at this lift.
  lo,hi=0,.247*25.4
  for _ in range(50):
   mid=(lo+hi)/2
   if solve(mid)['valve_lift']<lift:lo=mid
   else:hi=mid
  s=solve((lo+hi)/2)
  pose[tag+'-rocker']=b.Pos(x,PIVOT_Y,PIVOT_Z)*b.Rot(s['angle']*180/3.141592653589793,0,0)*defs['rocker-arm']
  min_coil_gap=min(min_coil_gap,(INSTALLED[kind]-lift)/6-4)
  for a,c in [(tag+'-spring','cylinder-head'),(tag+'-spring',tag+'-retainer'),(tag+'-seal','cylinder-head')]:
   gap=pose[a].distance_to(pose[c]);contacts.append({'lift':lift,'a':a,'b':c,'gap_mm':gap})
   if gap>.002:failures.append({'contact_gap':gap,'a':a,'b':c,'lift':lift})
  # OCC extrema overestimates some trimmed helix faces. Check exact outside
  # material and positive planar end areas instead of trusting that bound.
  for z,direction in [(seat,-1),(RETAINER_BOTTOM-lift,1)]:
   outside=b.Pos(x,VALVE_Y,z+direction*25)*b.Box(40,40,50)
   volume=intersect_volume(pose[tag+'-spring'],outside)
   area=sum(f.area for f in pose[tag+'-spring'].faces() if f.geom_type==b.GeomType.PLANE and abs(f.center().Z-z)<1e-5)
   ground_faces.append({'kind':kind,'lift':lift,'z':z,'area_mm2':area,'outside_volume_mm3':volume})
   if volume>.1 or area<1:failures.append({'spring_end':kind,'lift':lift,'outside':volume,'area':area})
  # Positive radial clearance and source ranges, not a touching shaft/bore claim.
  gap=pose[tag+'-valve'].distance_to(pose['cylinder-head'])
  # At closed lift valve face seats; at open lift stem clearance may control.
  if lift and gap<.01:failures.append({'stem_clearance':gap,'kind':kind,'lift':lift})
  changed=[tag+'-'+s for s in ['spring','seal','valve']]+['cylinder-head']
  for a in changed:
   for c in pose:
    if c=='c1-piston-1' or a==c or (a=='cylinder-head' and not c.startswith(tag)):continue
    if not box_overlap(pose[a],pose[c]):continue
    v=intersect_volume(pose[a],pose[c]);checks+=1
    if v>.1:failures.append({'a':a,'b':c,'overlap_mm3':v,'lift':lift})
 if lift in [0,10.033]:b.export_step(b.Compound(children=list(pose.values())),OUT/('closed-assembly.step' if lift==0 else 'peak-assembly.step'))
 print('Lift',lift,'checks',checks,'failures',len(failures),flush=True)
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
result={'status':'PASS' if not failures else 'FAIL','lifts_mm':[0,2.5,5,7.5,10.033],'source_step_hashes':hashes,'exact_intersections':checks,'contacts':contacts,'ground_faces':ground_faces,'min_pitch_minus_wire_mm':min_coil_gap,'diametral_stem_clearance_mm':GUIDE_DIAMETER-STEM_DIAMETER,'failures':failures,'scope':'Two stations spring,seal,valve,head vs saved first-stage neighbors; spring end contact and source-based height/guide dimensions. Piston excluded because independent lift samples are not crank phases; phase-specific piston checks remain first-stage/root integration responsibility. Five lift samples; no calibrated force or production spring end geometry.'}
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(bool(failures))
