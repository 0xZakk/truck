#!/usr/bin/env python3
"""Isolated revision export, protected-region identity, complete core axial pairs."""
from pathlib import Path
import sys,json,hashlib,itertools,math,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import timing_thrust_land_candidate as c
from cad_metrics import solid_volume
BASE=ROOT/'cad/engine/generated/timing-core-migration-candidate';OUT=ROOT/'cad/engine/generated/timing-thrust-land-candidate';OUT.mkdir(parents=True,exist_ok=True)
AXIS=(95.1098209901611,76.08785679212888);GEAR_X=385.259375
MOVING={'camshaft','cam-timing-gear','cam-gear-spacer','cam-timing-key'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def compound(q):return b.Compound(children=list(q.solids()))
corepath=ROOT/'inventory/engine/timing-core-migration-candidate-validation.json';core=json.loads(corepath.read_text());names=list(core['exports'])
refpath=ROOT/'inventory/engine/timing-gear-pair-refinement-validation.json';ref=json.loads(refpath.read_text())
localpath=ROOT/'cad/engine/generated/timing-gear-pair-refined/cam.step';assert sha(localpath)==ref['exports']['cam']['step_sha256']
watch=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/cad_metrics.py',corepath,refpath,localpath]+[BASE/(n+'.step') for n in names]+[BASE/(n+'.glb') for n in names]
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
for n in names:
 assert sha(BASE/(n+'.step'))==core['exports'][n]['step_sha256']
 assert sha(BASE/(n+'.glb'))==core['exports'][n]['glb_sha256']
old=b.import_step(localpath);new=c.revise(old);assert new.is_valid and len(new.solids())==1
added=new.cut(old);removed=old.cut(new)
assert not removed.solids()
protected={}
for name,radius in [('bore',16.1),('key_and_spacer',20.64)]:
 guard=c.cylinder(radius,30);delta=vol(compound(new.intersect(guard)).cut(compound(old.intersect(guard))))+vol(compound(old.intersect(guard)).cut(compound(new.intersect(guard))))
 assert delta<1e-6;protected[name+'_difference_mm3']=delta
assert not compound(added).cut(c.cylinder(26.000001,30)).solids()
assert not compound(added).cut(c.cylinder(77.65,30)).solids()
protected.update(removed_solids=0,added_outside_outer_radius_solids=0,added_outside_tooth_root_guard_solids=0,added_volume_mm3=vol(added))
parts={n:b.import_step(BASE/(n+'.step')) for n in names};parts['cam-timing-gear']=b.Pos(GEAR_X,*AXIS)*new
exports={}
for n in names:
 if n!='cam-timing-gear':
  for ext in ['step','glb']:shutil.copy2(BASE/(n+'.'+ext),OUT/(n+'.'+ext))
  exports[n]={**core['exports'][n],'inherited_unchanged':True};continue
 q=parts[n];sp=OUT/(n+'.step');b.export_step(q,sp);rt=b.import_step(sp);assert rt.is_valid and len(rt.solids())==1
 v,f=q.tessellate(.05,.1);v=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(n+'.glb');mesh.export(gp)
 actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8);assert actual.is_watertight and actual.nondegenerate_faces().all() and actual.unique_faces().all()
 vv=np.asarray(actual.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
 ve=abs(vol(q)-vol(rt));assert err<.15 and ve<.001
 exports[n]={'valid':True,'solids':1,'watertight':True,'bounds_error_mm':err,'step_volume_error_mm3':ve,'triangles':len(actual.faces),'step_sha256':sha(sp),'glb_sha256':sha(gp)}
print('Protected regions and exports PASS',flush=True)
# All50 pairs having at least one of four axially-moving members. Constant
# relative-pose pairs are tested once. Gear pair has a separate helical sweep.
pairs=[(a,d) for a,d in itertools.combinations(names,2) if a in MOVING or d in MOVING]
def bounds(q):z=q.bounding_box();return np.array(tuple(z.min)),np.array(tuple(z.max))
def disjoint(a,d):
 lo,hi=bounds(a);l,h=bounds(d);return bool(np.any(hi<l-1e-8) or np.any(h<lo-1e-8))
def scoped(a,d,q,r):
 # Omitted shaft material is >=1mm axially from the neighbor; it cannot
 # enter during0.1mm travel. Cam teeth omitted only when counterpart stays
 # inside radius49, also leaving >=1mm radial distance to omitted material.
 if a=='camshaft':
  bb=r.bounding_box();q=q.intersect(b.Pos((bb.min.X+bb.max.X)/2,0,0)*b.Box(bb.size.X+2,600,600))
 if d=='camshaft':return tuple(reversed(scoped(d,a,r,q)))
 for n in [a,d]:
  if n=='cam-timing-gear' and 'crank-timing-gear' not in [a,d]:
   other=r if n==a else q;bb=other.bounding_box();maxrad=max(math.hypot(y-AXIS[0],z-AXIS[1]) for y in [bb.min.Y,bb.max.Y] for z in [bb.min.Z,bb.max.Z])
   if maxrad<49:
    guard=b.Pos(GEAR_X,*AXIS)*c.cylinder(50,30)
    if n==a:q=q.intersect(guard)
    else:r=r.intersect(guard)
 return compound(q),compound(r)
rows=[]
for a,d in pairs:
 if {a,d}=={'cam-timing-gear','crank-timing-gear'}:
  rows.append({'a':a,'b':d,'coverage':'separate25pose helical endpoint sweep'});continue
 common=a in MOVING and d in MOVING
 poses=[0.] if common else [-.1,-.075,-.05,-.025,0.]
 overlaps=[]
 for t in poses:
  q=b.Pos(t if a in MOVING else 0,0,0)*parts[a];r=b.Pos(t if d in MOVING else 0,0,0)*parts[d]
  if disjoint(q,r):overlaps.append(0.);continue
  q,r=scoped(a,d,q,r);overlaps.append(vol(q.intersect(r)))
 assert max(overlaps)<1e-5,(a,d,overlaps)
 rows.append({'a':a,'b':d,'axial_samples_mm':poses,'overlap_mm3':overlaps,'relative_pose_constant':common})
 print('pair',a,d,'PASS',flush=True)
 (OUT/'pair-progress.json').write_text(json.dumps(rows,indent=2)+'\n')
# Exact continuous-travel conservative certificates for every non-gear pair.
# Bounding-box sweep first, then positive distance greater than travel, then
# explicit cylindrical/half-space stop geometry for touching/sliding pairs.
continuous=[]
for row in rows:
 a,d=row['a'],row['b']
 if 'relative_pose_constant' not in row:continue
 if row['relative_pose_constant']:continuous.append({'a':a,'b':d,'proof':'rigid shared translation; relative solids unchanged'});continue
 if a not in MOVING:a,d=d,a
 q=parts[a];r=parts[d];lo,hi=bounds(q);lo[0]-=.1;l,h=bounds(r)
 if np.any(hi<l-1e-8) or np.any(h<lo-1e-8):continuous.append({'a':a,'b':d,'proof':'entire travel swept AABB separated'});continue
 if a=='camshaft' and d.startswith('cam-bearing-'):
  bb=r.bounding_box();margin=.100001;section=q.intersect(b.Pos((bb.min.X+bb.max.X+margin)/2,0,0)*b.Box(bb.size.X+margin,600,600))
  cylinder=b.Pos((bb.min.X+bb.max.X)/2,*AXIS)*c.cylinder(25.62225,bb.size.X+2)
  assert vol(compound(section).cut(cylinder))<1e-5
  assert vol(cylinder.intersect(r))<1e-5
  continuous.append({'a':a,'b':d,'proof':'entire source axial interval contained in coaxial journal cylinder; cylinder clears bearing','journal_radius_mm':25.62225});continue
 if a=='camshaft' and d=='cam-thrust-plate':
  # Every source point able to enter plate slab is behindX373 or in nose.
  bb=r.bounding_box();section=q.intersect(b.Pos((bb.min.X+bb.max.X+.1)/2,0,0)*b.Box(bb.size.X+.100001,600,600))
  nose=b.Pos(380,*AXIS)*c.cylinder(15.875,40)
  back=b.Pos(323,*AXIS)*b.Box(100,120,120)
  assert vol(compound(section).cut(nose+back))<1e-5
  assert vol((nose+back).intersect(r))<1e-5
  continuous.append({'a':a,'b':d,'proof':'shaft shoulder remainsX<=373; nose cylinder clears plate for full negative travel'});continue
 if a=='cam-timing-gear' and d=='cam-thrust-plate':
  assert abs(q.bounding_box().min.X-.1-r.bounding_box().max.X)<1e-6
  continuous.append({'a':a,'b':d,'proof':'entire gear stays at/forward of plate front plane throughout travel'});continue
 qq,rr=scoped(a,d,q,r)
 if not qq.solids() or not rr.solids():
  # Neighbor lies outside bounded shaft slab; omitted material separated>1mm.
  continuous.append({'a':a,'b':d,'proof':'empty local interface slab; omitted shaft distance>=1mm'});continue
 gap=qq.distance_to(rr)
 assert gap>.100001,(a,d,gap)
 continuous.append({'a':a,'b':d,'proof':'local gap and omitted-region separation exceed total0.1mm translation','local_gap_mm':gap})
# Opposing face contact areas are measured at actual endpoints, not projected
# across a gap; fault poses move every rotating member together.
def face_area(q,r):
 area=0.
 for f in q.faces():
  bb=f.bounding_box()
  if bb.size.X>1e-5:continue
  for g in r.faces():
   gb=g.bounding_box()
   if gb.size.X<1e-5 and abs(bb.min.X-gb.min.X)<1e-6 and f.normal_at().X*g.normal_at().X<-.99:
    common=f.intersect(g)
    if common:area+=sum(x.area for x in common.faces())
 return area
stops=[]
for t,name in [(-.1,'cam-timing-gear'),(0.,'camshaft')]:
 q=b.Pos(t,0,0)*parts[name];area=face_area(q,parts['cam-thrust-plate']);assert area>1
 stops.append({'travel_mm':t,'moving_part':name,'opposing_face_contact_area_mm2':area,'overlap_mm3':vol(q.intersect(parts['cam-thrust-plate']))})
faults=[]
for t,name in [(-.11,'cam-timing-gear'),(.11,'camshaft')]:
 q=b.Pos(t,0,0)*parts[name];overlap=vol(q.intersect(parts['cam-thrust-plate']));assert overlap>.1
 faults.append({'travel_mm':t,'moving_part':name,'overlap_mm3':overlap})
assert inputs=={p:sha(ROOT/p) for p in inputs}
r={'status':'PASS isolated thrust land and complete core axial-pair checks; helical endpoint report REQUIRED; UNINSTALLED','input_sha256':inputs,'parameters':c.PARAMS,'protected_regions':protected,'exports':exports,'axial_interval_mm':[-.1,0.],'all_affected_pairs':rows,'continuous_axial_certificates_non_helical':continuous,'stop_contacts':stops,'overtravel_faults':faults,'limitations':['Estimated backside topology, no production identity','Gear-pair helical endpoint/axial certificate separate; do not infer from fixed axial pose','Full engine block/cover/valvetrain/distributor not adapted','Crank key missing; no press-fit/load/browser claim']}
(ROOT/'inventory/engine/timing-thrust-land-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
