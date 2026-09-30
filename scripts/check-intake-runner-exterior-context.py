#!/usr/bin/env python3
"""Read-only current-context audit of isolated runner skins; no promotion."""
from pathlib import Path
import hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
from assembly_math import transforms
from cad_metrics import solid_volume
import throttle_cable_candidate as cable
import throttle_return_spring_candidate as spring
import intake_runner_exterior_candidate as candidate
OUT=ROOT/'cad/engine/generated/intake-runner-exterior-study';WORK=OUT/'context';WORK.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):
 solids=list(s.solids()) if s else []
 assert all(q.is_valid for q in solids),'Invalid Boolean solid'
 return sum(abs(solid_volume(q,'adaptive')) for q in solids)
def bbox(s):
 z=s.bounding_box();return np.array(tuple(z.min)),np.array(tuple(z.max))
def distance(a,z):return float(np.linalg.norm(np.maximum(np.maximum(a[0]-z[1],z[0]-a[1]),0)))
def bake(s,name):
 p=WORK/(name+'.step');b.export_step(s,p);v=b.import_step(p)
 assert v.is_valid and len(v.solids())==len(s.solids()) and abs(vol(v)-vol(s))<.1,name
 return v
def main():
 mp=ROOT/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);defs={d['id']:d for d in m['definitions']};poses=transforms(m)
 assert len(defs)==733 and len(m['occurrences'])==1341,'Re-review changed context'
 baseline_report_path=ROOT/'inventory/engine/atlas-static-validation.json';baseline_report=json.loads(baseline_report_path.read_text());assert baseline_report['manifest_sha256']==hashlib.sha256(raw).hexdigest() and not baseline_report['collisions']
 sources={Path(__file__),mp,baseline_report_path,OUT/'runner-exterior.step',OUT/'baseline.step',ROOT/'inventory/engine/intake-runner-exterior-candidate-validation.json',ROOT/'reference/engine/intake-runner-exterior-review.json'}
 sources|={Path(mod.__file__).resolve() for mod in list(sys.modules.values()) if getattr(mod,'__file__',None) and Path(mod.__file__).resolve().is_relative_to(ROOT/'cad/engine')}
 sources|={ROOT/d[k].lstrip('/') for d in defs.values() for k in ('step','glb')}
 before={str(p.relative_to(ROOT)):sha(p) for p in sources}
 shape=b.import_step(OUT/'runner-exterior.step');old=b.import_step(OUT/'baseline.step');box=bbox(shape);audit_shape=shape
 current=bake(poses['efi-upper-intake']*b.import_step(ROOT/defs['efi-upper-intake']['step'].lstrip('/')),'current-intake')
 baseline_diff=vol(old-current)+vol(current-old);assert baseline_diff<.1
 assert sha(OUT/'runner-exterior.step')==json.loads((ROOT/'inventory/engine/intake-runner-exterior-candidate-validation.json').read_text())['step_sha256']
 added=b.Compound(children=list((shape-old).solids()));assert added.is_valid
 removed_volume=vol(old-shape);assert removed_volume<.1
 added_box=bbox(added);added_bounds=[added_box[0].tolist(),added_box[1].tolist()]
 cache={};bounds={};rows=[]
 def actor(o,pose):
  did=o['definition']
  if did not in cache:cache[did]=b.import_step(ROOT/defs[did]['step'].lstrip('/'))
  return pose*cache[did]
 def mesh_box(o,pose):
  did=o['definition']
  if did not in bounds:
   mesh=trimesh.load(ROOT/defs[did]['glb'].lstrip('/'),force='mesh');v=np.asarray(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;bounds[did]=(v.min(0)-.2,v.max(0)+.2)
  lo,hi=bounds[did];corners=np.array([tuple(b.Vertex(x,y,z).moved(pose).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]);return corners.min(0),corners.max(0)
 def check(s,name,family,angle,otherbox=None):
  gap=distance(box,otherbox if otherbox is not None else bbox(s));r=dict(actor=name,family=family,angle_deg=angle,aabb_distance_lower_mm=gap,exact=False)
  if gap<=0:
   print('Checking',family,name,angle,flush=True)
   try:s=bake(s,family+'-'+name+'-'+str(angle))
   except ValueError as error:
    if 'Volume integration did not converge' not in str(error):raise
    separation=distance(added_box,bbox(s));assert separation>1e-5 and removed_volume<.1 and family=='static'
    r.update(exact=False,baseline_static_inherited=True,added_material_aabb_distance_lower_mm=separation,normalization_mass_integration=str(error),new_overlap_mm3=0.);rows.append(r);print('Inherited unchanged static separation',name,separation,flush=True);return
   hit=vol(audit_shape&s);prior=vol(old&s) if family=='static' else 0.;r.update(exact=True,overlap_mm3=hit,baseline_overlap_mm3=prior,new_overlap_mm3=max(0,hit-prior));print('Exact',family,name,angle,hit,prior,flush=True)
  rows.append(r)
 for o in m['occurrences']:
  if o['id']=='efi-upper-intake':continue
  bb=mesh_box(o,poses[o['id']]);gap=distance(box,bb)
  if gap>0:rows.append(dict(actor=o['id'],family='static',angle_deg=0,aabb_distance_lower_mm=gap,exact=False))
  else:check(actor(o,poses[o['id']]),o['id'],'static',0,bb)
 print('Static complete',len(rows),flush=True)
 box=added_box;audit_shape=added
 assemblies={a['id']:a for a in m['assemblies']}
 def throttle(o):
  parent=o.get('parent')
  while parent in assemblies:
   a=assemblies[parent]
   if (a.get('motion') or {}).get('type')=='throttle':return True
   parent=a.get('parent')
  return False
 rockers=[o for o in m['occurrences'] if o.get('valvetrain',{}).get('role')=='rocker'];rigid=[o for o in m['occurrences'] if throttle(o) and not o['id'].startswith('throttle-cable-') and o['id']!='throttle-return-spring-illustrative']
 angles=set(range(0,721,5))
 for phase in range(0,720,120):
  for peak in (246,468):
   for delta in (-135,0,135):angles.add((phase+peak+delta)%720)
 throttle_angles=sorted(set(range(0,91,2))|{45})
 for family,actors,phases in [('rocker',rockers,sorted(angles)),('throttle-rigid',rigid,throttle_angles)]:
  for angle in phases:
   pp=transforms(dict(m,occurrences=actors),angle if family=='rocker' else 0,throttle_degrees=angle if family!='rocker' else 0)
   for o in actors:
    bb=mesh_box(o,pp[o['id']]);gap=distance(box,bb)
    if gap>0:rows.append(dict(actor=o['id'],family=family,angle_deg=angle,aabb_distance_lower_mm=gap,exact=False))
    else:check(actor(o,pp[o['id']]),o['id'],family,angle,bb)
  print(family,'complete',flush=True)
 for angle in throttle_angles:
  pp=transforms(m,throttle_degrees=angle);moving,metrics=cable.moving(angle)
  for name,s in moving.items():
   assert s.is_valid and len(s.solids())==1,name
   check(pp['throttle-housing']*s,name,'cable-exact-shape',angle)
  s=spring.spring(angle).moved(pp['throttle-return-spring-illustrative']);assert s.is_valid
  check(s,'throttle-return-spring-illustrative','spring-exact-shape',angle)
  print('Dynamic geometry',angle,flush=True)
 # A deliberately filled bore and exterior intrusion must trip the same exact predicates.
 path=candidate.paths()[0];plug=b.Plane(origin=path@.55,z_dir=path%.55)*b.Cylinder(15,8)
 controls={'runner_plug_overlap_mm3':vol(b.Compound(children=list((shape+plug).solids()))&plug),'casting_intrusion_overlap_mm3':vol(shape&(b.Pos(*(tuple(path@.55)))*b.Box(60,60,60)))}
 assert min(controls.values())>1
 after={str(p.relative_to(ROOT)):sha(p) for p in sources};assert before==after,'Context changed during audit'
 failures=[r for r in rows if r.get('new_overlap_mm3',0)>.1]
 report=dict(status='FAIL new interference' if failures else 'PASS bounded current733 context',manifest_sha256=hashlib.sha256(raw).hexdigest(),definitions=len(defs),occurrences=len(m['occurrences']),baseline_symmetric_difference_mm3=baseline_diff,added_material_bounds_mm=added_bounds,removed_material_mm3=removed_volume,baseline_static_report_sha256=sha(baseline_report_path),input_sha256_before=before,input_sha256_after=after,input_guard_pass=True,negative_controls=controls,rows=rows,failures=failures,summary={f:dict(pairs=len([r for r in rows if r['family']==f]),exact_pairs=len([r for r in rows if r['family']==f and r['exact']])) for f in sorted({r['family'] for r in rows})},limits=['Dynamic gates compare only exact added material; unchanged installed baseline motion is inherited. Sampled exact dynamic cable/shaft spring geometry at47poses, rigid throttle at47poses and12rockers at181phases; not continuous motion proof.','One nonconvergent unchanged static neighbor may inherit the hash-bound current733 baseline static report only with disjoint exact added-material bounds and zero removed volume. Only new or worsened overlap relative to installed intake is rejected; existing contacts separately reported.','Inferred exterior proportions; source comparison and integration review still required.'])
 (ROOT/'inventory/engine/intake-runner-exterior-context-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['summary'],flush=True);assert not failures
if __name__=='__main__':main()
