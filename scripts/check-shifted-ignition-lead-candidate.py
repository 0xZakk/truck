#!/usr/bin/env python3
import sys,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import shifted_ignition_lead_candidate as c
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/shifted-ignition-lead-candidate';OUT.mkdir(exist_ok=True)
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());poses=transforms(m);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};inputs={}
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def bind(p):inputs[p]=sha(p);return ROOT/p
def vol(s):return sum(x.volume for x in s.solids()) if s else 0.
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
def old(i):return poses[i]*b.import_step(bind(defs[occ[i]['definition']]['step'].lstrip('/')))
for p in ['scripts/check-shifted-ignition-lead-candidate.py','cad/engine/shifted_ignition_lead_candidate.py','cad/engine/ignition_leads.py','cad/engine/oil_drive_layout.py','cad/engine/timing_block_axis_feature_candidate.py','inventory/engine/full-assembly.json']:bind(p)
cap= b.Pos(*c.DELTA)*old('distributor-cap');report={'status':'RUNNING','inputs':inputs,'families':[],'artifacts':{}}
if '--resume' in sys.argv:
 previous=json.loads((ROOT/'inventory/engine/shifted-ignition-lead-build-validation.json').read_text());report['families']=previous['families'];report['artifacts']=previous['artifacts'];report['resumed_from_checker_sha256']=previous['inputs']['scripts/check-shifted-ignition-lead-candidate.py'];inputs.update({p:h for p,h in previous['inputs'].items() if p not in inputs})
def save():report['inputs']=inputs;(ROOT/'inventory/engine/shifted-ignition-lead-build-validation.json').write_text(json.dumps(report,indent=2)+'\n')
for cylinder in [1,2,3,4,5,6,None]:
 prefix=f'ignition-lead-{cylinder}' if cylinder else 'ignition-coil-lead'
 if any(r['prefix']==prefix for r in report['families']):continue
 print('family',prefix,flush=True)
 parts,data=c.build(cylinder);sourcepath=c.src.plug_path(cylinder) if cylinder else c.src.coil_path();sf=c.src.cap_frame(c.src.TOWER_BY_CYLINDER[cylinder]) if cylinder else c.src.coil_frame();oj,oc=c.src.cable(sourcepath,sf)
 termid=f'distributor-terminal-{c.src.TOWER_BY_CYLINDER[cylinder]}' if cylinder else 'distributor-coil-terminal';terminal=b.Pos(*c.DELTA)*old(termid)
 row={'prefix':prefix,'controls_old':data['old_controls'],'controls_new':data['new_controls'],'parts':{},'pairs':[],'fixed_endpoint_mm':list(c.src.point(data['fixed_frame'],46 if cylinder else 62))}
 for suffix,replay in [('jacket',oj),('carbon-core',oc)]:
  baseline=old(prefix+'-'+suffix)
  # Full coplanar subtraction is retained rejected in separate diagnostic.
  # Independent actual shell vertices/edge interiors check both directions.
  radii=[3.5,1.05] if suffix=='jacket' else [1.]
  errors=[];bs=baseline.shells()[0];rs=replay.shells()[0]
  for a,z in [(baseline,rs),(replay,bs)]:
   for edge in a.edges():
    for t in [0.,.25,.5,.75,1.]:errors.append(z.distance_to(b.Vertex(edge.position_at(t))))
  for t in [i/32 for i in range(33)]:
   center=sourcepath.position_at(t);normal=sourcepath.tangent_at(t).normalized();u=normal.cross(b.Vector(0,1,0)).normalized();v=normal.cross(u)
   for radius in radii:
    for j in range(8):errors.append(bs.distance_to(b.Vertex(center+radius*(u*math.cos(j*math.tau/8)+v*math.sin(j*math.tau/8)))))
  volume_error=abs(vol(baseline)-vol(replay));be=max(abs(x-y) for x,y in zip(list(baseline.bounding_box().min)+list(baseline.bounding_box().max),list(replay.bounding_box().min)+list(replay.bounding_box().max)))
  center=sourcepath.position_at(.5);normal=sourcepath.tangent_at(.5).normalized();u=normal.cross(b.Vector(0,1,0)).normalized();fault=bs.distance_to(b.Vertex(center+(radii[0]+.2)*u))
  assert volume_error<1e-5 and be<1e-5 and max(errors)<.001 and fault>.1,(prefix,suffix,volume_error,be,max(errors),fault)
  row['parts'][suffix]={'replay_volume_error_mm3':volume_error,'replay_bounds_error_mm':be,'bidirectional_edge_and_circle_samples':len(errors),'max_surface_error_mm':max(errors),'radial_fault_0_2mm_distance_mm':fault,'coplanar_symmetric_difference':'UNTRUSTED retained separate failure'};print('replay surfaces',suffix,max(errors),flush=True)
 # Exact fixed curve and both source radii provide an independent retained surface witness.
 fixed=data['fixed_path'];normal=fixed.tangent_at(0);plane=b.Plane(origin=fixed@0,z_dir=normal)
 probe=b.sweep(plane*(b.Circle(3.4)-b.Circle(1.15)),path=fixed,is_frenet=cylinder is not None)
 missing=vol(probe.cut(parts[prefix+'-jacket']));row['fixed_jacket_interior_subtraction_mm3_untrusted']=missing;print('fixed subtraction diagnostic',missing,flush=True)
 fixederrors=[];inside=[];baselinej=old(prefix+'-jacket');newj=parts[prefix+'-jacket']
 for t in [i/32 for i in range(33)]:
  center=fixed.position_at(t);normal=fixed.tangent_at(t).normalized();u=normal.cross(b.Vector(0,1,0)).normalized();v=normal.cross(u)
  for j in range(8):
   radial=u*math.cos(j*math.tau/8)+v*math.sin(j*math.tau/8)
   for radius in [1.05,3.5]:
    point=b.Vertex(center+radius*radial);fixederrors.extend([baselinej.shells()[0].distance_to(point),newj.shells()[0].distance_to(point)])
   if 0<t<1:inside.append(newj.is_inside(center+2*radial,tolerance=1e-7))
 assert max(fixederrors)<.001 and all(inside),(prefix,max(fixederrors),sum(inside),len(inside))
 row['fixed_path_surface_max_error_mm']=max(fixederrors);row['fixed_path_surface_samples']=len(fixederrors);row['fixed_wall_interior_samples']=len(inside)
 for ident,q in parts.items():
  assert q.is_valid and len(q.solids())==1
  p=OUT/(ident+'.step');b.export_step(q,p);rt=b.import_step(p);assert rt.is_valid and len(rt.solids())==1
  row['parts'].setdefault(ident.removeprefix(prefix+'-'),{})['step_volume_error_mm3']=abs(vol(q)-vol(rt))
  report['artifacts'][str(p.relative_to(ROOT))]=sha(str(p.relative_to(ROOT)))
  for name,s in [('cap',cap),('terminal',terminal)]:
   overlap=vol(rt.intersect(s));row['pairs'].append({'part':ident,'neighbor':name,'overlap_mm3':overlap});assert overlap<.1,(ident,name,overlap)
  if ident.endswith(('cap-boot','cap-contact')):assert diff(q,b.Pos(*c.DELTA)*old(ident))<1e-5
 # Terminal and core share actual boundary with the electrical connector.
 contact=parts[prefix+'-cap-contact'];core=parts[prefix+'-carbon-core'];areas={}
 for name,s in [('terminal',terminal),('core',core)]:
  common=contact.shells()[0].intersect(s.shells()[0]);areas[name]=common.area if common else 0.;assert areas[name]>.1,(name,areas)
 row['actual_contact_area_mm2']=areas
 row['stale_cap_boot_overlap_mm3']=vol(cap.intersect(old(prefix+'-cap-boot')));assert row['stale_cap_boot_overlap_mm3']>.1
 report['families'].append(row);save();print('local PASS',prefix,areas,flush=True)
report['status']='PASS seven local re-registered cap joints; mesh/neighborhood and visuals pending';save()
