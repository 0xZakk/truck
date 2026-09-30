#!/usr/bin/env python3
"""Rotation-invariant stationary-core certificates for the actual keyed group."""
from pathlib import Path
import sys,json,hashlib,itertools,math,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
from OCP.BRepTools import BRepTools
import timing_coupled_core_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-coupled-core-candidate';OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def comp(q):return b.Compound(children=list(q.solids()))
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
def dump(p,r):Path(p).write_text(json.dumps(r,indent=2)+'\n')
landpath=ROOT/'inventory/engine/timing-thrust-land-candidate-validation.json';land=read(landpath)
backpath=ROOT/'inventory/engine/timing-gear-backlash-candidate-validation.json';back=read(backpath)
assert back['status'].startswith('PASS isolated candidate after explicit additive metadata rebind')
assert all(row['core_difference_mm3']<1e-5 for row in back['build']['protected_core'].values())
manifest=read(ROOT/'inventory/engine/full-assembly.json');occ={o['id']:o for o in manifest['occurrences']}
for key in c.MOVING:assert occ[key]['parent']=='cam-motion'
for key in c.STATIONARY:
 assert occ[key]['parent']!='cam-motion'
 if 'thrust-' in key:assert occ[key]['parent']=='cam-retention-assembly'
assert not [o for o in manifest['occurrences'] if o['parent']=='cam-motion' and 'bolt' in o['id']]
names=sorted(c.MOVING|set(c.STATIONARY)|{'crank-timing-gear'});membership={k:occ[k] for k in names}
watch=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/cad_metrics.py',ROOT/'cad/engine/cam_retention.py',landpath,backpath]
source=read(ROOT/'reference/engine/timing-gear-backlash-review.json')['sources'][0];assert sha(ROOT/source['path'])==source['sha256'];watch.append(ROOT/source['path'])
for key in names:
 for ext in ['step','glb']:
  p=ROOT/f'cad/engine/generated/timing-thrust-land-candidate/{key}.{ext}';assert sha(p)==land['exports'][key][ext+'_sha256'];watch.append(p)
for key in ['crank','cam']:
 for ext in ['step','glb']:
  p=ROOT/f'cad/engine/generated/timing-gear-backlash-candidate/{key}.{ext}';assert sha(p)==back['build']['exports'][key][ext+'_sha256'];watch.append(p)
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch};parts=c.parts()
# Six shared-rigid-body pairs inherit exact local geometry from the accepted
# core; all non-gear group members lie entirely inside the preserved gear core.
rigid=[]
for key in c.MOVING-{'cam-timing-gear'}:
 q=parts[key];assert vol(q.cut(c.cylinder(77.2,-500,500)))<1e-5
for a,z in itertools.combinations(sorted(c.MOVING),2):
 row=next(x for x in land['all_affected_pairs'] if {x['a'],x['b']}=={a,z});assert row['relative_pose_constant'] and max(row['overlap_mm3'])<1e-5
 rigid.append(dict(a=a,b=z,proof='Same rigid cam_frame applied to both; local geometry equals frozen core inside R77.2; inherited zero-overlap and gaps/contact invariant',inherited_report_sha256=sha(landpath)))
# Numerical transform check catches a mistaken rotation about the origin or
# leaving one keyed member stationary, without expensive repeated booleans.
framechecks=[]
for theta,delta in [(0,-.1),(180,-.1),(360,0),(720,-.1)]:
 f=c.cam_frame(theta,delta);inv=f.inverse();pose=c.posed(parts,theta,delta)
 for key in c.MOVING:
  point=b.Vertex(*tuple(parts[key].center()));p=inv*(f*point);assert (p.center()-point.center()).length<1e-8
  assert (pose[key].center()-(f*point).center()).length<1e-7
 for key in c.STATIONARY:assert pose[key] is parts[key]
 stationary_key_error=(parts['cam-timing-key'].center()-(f*b.Vertex(*tuple(parts['cam-timing-key'].center()))).center()).length
 if delta==-0.1:assert stationary_key_error>.09
 framechecks.append(dict(crank_degrees=theta,axial_mm=delta,rigid_inverse_error_below_mm=1e-8,stationary_objects_identical=True,actual_posed_center_error_below_mm=1e-7,left_stationary_key_fault_mm=stationary_key_error))
print('Membership and rigid interfaces PASS',flush=True)

def radial_box_radius(q):
 bb=q.bounding_box();return max(math.hypot(y-c.AXIS[0],z-c.AXIS[1]) for y in [bb.min.Y,bb.max.Y] for z in [bb.min.Z,bb.max.Z])

def slab(q,lo,hi):return comp(q.intersect(b.Pos((lo+hi)/2,*c.AXIS)*b.Box(hi-lo,500,500)))

certs=[]
for moving,fixed in itertools.product(sorted(c.MOVING),c.STATIONARY):
 q=parts[moving];z=parts[fixed];qb=q.bounding_box();zb=z.bounding_box()
 if qb.max.X<zb.min.X-1e-8 or qb.min.X-.1>zb.max.X+1e-8:
  cert=dict(proof='Entire translated X interval separated; rotation preserves X',axial_intervals_mm=[[qb.min.X-.1,qb.max.X],[zb.min.X,zb.max.X]])
 elif moving=='cam-timing-gear' and fixed=='cam-thrust-plate':
  assert abs(qb.min.X-.1-zb.max.X)<1e-6
  cert=dict(proof='Gear remains at or ahead of stationary plate front plane for entire axial interval; rotation preserves plane',stop_x_mm=zb.max.X)
 elif moving=='camshaft' and fixed=='cam-thrust-plate':
  section=slab(q,zb.min.X,zb.max.X+.100001)
  nose=c.cylinder(15.875,zb.min.X-1,zb.max.X+2)
  assert vol(section.cut(nose))<1e-5 and vol(nose.intersect(z))<1e-5
  cert=dict(proof='Every shaft source point that can enter plate slab is in coaxial R15.875 nose; rear shoulder stays X<=373 under negative travel',radial_support_mm=15.875)
 elif moving=='cam-timing-gear':
  # Axisymmetric superset of every possible rotating gear pose: inner land,
  # outer tooth ring and forward web. All bounds expand for full axial travel.
  lo=c.GEAR_X-7.1;hi=c.GEAR_X+7
  support=c.cylinder(26,lo,hi)+(c.cylinder(83.947001,lo,hi)-c.cylinder(46.999999,lo-1,hi+1))+c.cylinder(83.947001,c.GEAR_X+.9,hi)
  missing=vol(q.cut(support));hit=vol(support.intersect(z));assert missing<1e-5 and hit<1e-5,(moving,fixed,missing,hit)
  cert=dict(proof='Actual gear contained in axisymmetric land/ring/front-web superset expanded for all axial travel; superset clears stationary part',support_missing_mm3=missing,support_overlap_mm3=hit,land_radius_mm=26,relief_radius_mm=47,forward_web_min_x_mm=c.GEAR_X+.9)
 else:
  section=slab(q,zb.min.X,zb.max.X+.100001)
  if not section.solids():cert=dict(proof='No source material can enter stationary X slab anywhere in allowed travel')
  else:
   radius=25.62225 if moving=='camshaft' else 19.05 if moving=='cam-gear-spacer' else radial_box_radius(section)+1e-6
   support=c.cylinder(radius,zb.min.X-.2,zb.max.X+.2)
   missing=vol(section.cut(c.cylinder(radius,zb.min.X-.2,zb.max.X+.3)));hit=vol(support.intersect(z));assert missing<1e-5 and hit<1e-5,(moving,fixed,radius,missing,hit)
   cert=dict(proof='All eligible source material contained in coaxial cylinder; rotation and axial travel remain inside stationary-slab support; support clears fixed part',radius_mm=radius,source_outside_support_mm3=missing,support_overlap_mm3=hit)
 cert.update(moving=moving,stationary=fixed,rotation_coverage='all cam angles',axial_interval_mm=[-.1,0.]);certs.append(cert);print('Certificate',moving,fixed,flush=True);dump(OUT/'certificate-progress.json',certs)
# Cam group vs rotating crank gear, excluding tooth mesh already bound above:
# unchanged inner members have rotation-invariant radial separation.
crankclear=[]
for key in sorted(c.MOVING-{'cam-timing-gear'}):
 radius=radial_box_radius(parts[key]);margin=121.8-radius-43.18
 assert margin>0,(key,radius,margin)
 crankclear.append(dict(moving=key,radial_box_bound_mm=radius,radial_separation_lower_bound_mm=margin,scope='all independent cam/crank angles and allowed axial travel'))

# Actual endpoint contact and overtravel checks at two different cam phases.
def face_area(q,z):
 area=0.
 for f in q.faces():
  fb=f.bounding_box()
  if fb.size.X>1e-5:continue
  for g in z.faces():
   gb=g.bounding_box()
   if gb.size.X<1e-5 and abs(fb.min.X-gb.min.X)<1e-6 and f.normal_at().X*g.normal_at().X<-.99:
    common=f.intersect(g)
    if common:area+=sum(a.area for a in common.faces())
 return area
stops=[];faults=[]
for theta in [0.,180.]:
 for delta,key in [(-.1,'cam-timing-gear'),(0.,'camshaft')]:
  q=c.cam_frame(theta,delta)*parts[key]
  if key=='cam-timing-gear':q=comp(q.intersect(c.cylinder(27,c.GEAR_X-8,c.GEAR_X+8)))
  else:q=slab(q,372.9,379)
  z=parts['cam-thrust-plate'];area=face_area(q,z);overlap=vol(q.intersect(z));assert area>1 and overlap<1e-5
  stops.append(dict(crank_degrees=theta,axial_mm=delta,moving=key,contact_area_mm2=area,overlap_mm3=overlap))
 for delta,key in [(-.11,'cam-timing-gear'),(.11,'camshaft')]:
  q=c.cam_frame(theta,delta)*parts[key]
  q=comp(q.intersect(c.cylinder(27,372,395))) if key=='cam-timing-gear' else slab(q,372,380)
  hit=vol(q.intersect(parts['cam-thrust-plate']));assert hit>.1
  faults.append(dict(crank_degrees=theta,axial_mm=delta,moving=key,overlap_mm3=hit))
 print('Endpoint contacts and overtravel',theta,'PASS',flush=True)
# Full annular support makes both stop contacts invariant under all rotations,
# rather than inheriting that conclusion from two sampled face intersections.
def ring(r1,r2,a,z):return c.cylinder(r2,a,z)-c.cylinder(r1,a-1,z+1)
annular_stops=[]
for name,r1,r2,moving,wafer,plate in [('gear_land',20.65,26.,'cam-timing-gear',(c.GEAR_X-7,c.GEAR_X-6.99),(378.149375,378.159375)),('shaft_shoulder',20.6375,25.62225,'camshaft',(372.99,373.),(373.,373.01))]:
 a=ring(r1,r2,*wafer);z=ring(r1,r2,*plate);missing_moving=vol(a.cut(parts[moving]));missing_fixed=vol(z.cut(parts['cam-thrust-plate']));assert missing_moving<1e-5 and missing_fixed<1e-5
 annular_stops.append(dict(stop=name,radii_mm=[r1,r2],moving_support_missing_mm3=missing_moving,plate_support_missing_mm3=missing_fixed,contact_area_mm2=math.pi*(r2*r2-r1*r1),proof='Full coaxial annular material on opposing faces; contact invariant under every cam rotation'))
# Plate-shift fault must break established travel/contact relation.
shifted=b.Pos(.05,0,0)*parts['cam-thrust-plate'];fault_gear=c.cam_frame(0,-.1)*parts['cam-timing-gear'];fault_gear=comp(fault_gear.intersect(c.cylinder(27,372,395)));plate_fault=vol(fault_gear.intersect(shifted));assert plate_fault>.1
exports={}
for key,q in parts.items():
 if key not in ['cam-timing-gear','crank-timing-gear']:
  for ext in ['step','glb']:shutil.copy2(ROOT/f'cad/engine/generated/timing-thrust-land-candidate/{key}.{ext}',OUT/(key+'.'+ext))
  exports[key]={**land['exports'][key], 'inherited_identical_bytes':True};continue
 sp=OUT/(key+'.step');b.export_step(q,sp);rt=b.import_step(sp);assert rt.is_valid and len(rt.solids())==1;errvol=abs(vol(q)-vol(rt));assert errvol<.001
 BRepTools.Clean_s(q.wrapped);v,f=q.tessellate(.05,.1);mesh=trimesh.Trimesh(np.array([tuple(x) for x in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(key+'.glb');mesh.export(gp)
 actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8);assert actual.is_watertight and actual.nondegenerate_faces().all() and actual.unique_faces().all()
 vv=actual.vertices[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert err<.15
 exports[key]=dict(step_sha256=sha(sp),glb_sha256=sha(gp),valid=True,solids=1,watertight=True,triangles=len(actual.faces),bounds_error_mm=err,roundtrip_volume_error_mm3=errvol)
assert all(sha(ROOT/p)==h for p,h in inputs.items())
now={o['id']:o for o in read(ROOT/'inventory/engine/full-assembly.json')['occurrences']};assert membership=={k:now[k] for k in names}
r=dict(status='PASS isolated coupled modeled core; block/cover/linkage integration NOT RUN',input_sha256=inputs,membership=membership,rotating_cam_group=sorted(c.MOVING),stationary_group=list(c.STATIONARY),retaining_bolt='No separate gear-retaining bolt established in manifest/source; no bolt invented',keyed_rigid_interfaces=rigid,transform_controls=framechecks,stationary_certificates=certs,other_cam_members_vs_crank=crankclear,tooth_mesh_inheritance=dict(report_sha256=sha(backpath),scope='Exact same local new gears and compensated poses: 25 rotations, 2 endpoints, construction-level axial interpolation; NOT continuous rotation'),stop_contacts=stops,all_angle_annular_stops=annular_stops,overtravel_faults=faults,shifted_plate_fault_mm3=plate_fault,exports=exports,limits=['All-angle certificates cover stationary timing core only, not block/cover or crankshaft/cam-lobe interaction','Keyed assembly motion must remain rigid; retention fit/preload not established','Valvetrain linkage and distributor/pump drive phase coupling are unresolved integration dependencies','Missing/unestablished retention components are not invented; production identity and dimensions remain estimates'])
dump(ROOT/'inventory/engine/timing-coupled-core-candidate-validation.json',r);print(r['status'],flush=True)
