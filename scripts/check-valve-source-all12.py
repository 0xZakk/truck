"""Delta collision/contact audit of frozen source-sized all12 candidate."""
from pathlib import Path
import sys,json,hashlib,math,argparse,importlib.util
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_source_integration import candidate_transforms,occurrence_shape,state
from valve_layout_candidate import intersect_volume,box_overlap
import valve_source_layout as v
OUT=ROOT/'cad/engine/candidates/valve-source-all12';BASE=OUT/'baseline'
p=argparse.ArgumentParser();p.add_argument('--angles',default='0');p.add_argument('--report');a=p.parse_args();angles=[float(s) for s in a.angles.split(',')]
m=json.loads((OUT/'manifest.json').read_text());baseline=json.loads((BASE/'manifest.json').read_text());provenance=json.loads((OUT/'provenance.json').read_text())
spec=importlib.util.spec_from_file_location('frozen_source_assembly_math',BASE/'assembly_math.py');authority=importlib.util.module_from_spec(spec);spec.loader.exec_module(authority)
occ={o['id']:o for o in m['occurrences']};old_occ={o['id']:o for o in baseline['occurrences']};defs={};hashes={}
for d in m['definitions']:
 path=ROOT/d['step'].lstrip('/');defs[d['id']]=b.import_step(path);hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
print('Loaded',len(defs),'frozen definitions',flush=True)
changed={o['id'] for o in m['occurrences'] if o['definition'] in provenance['shape_hashes'] or o['position_cad_mm']!=old_occ[o['id']]['position_cad_mm'] or o.get('rotation_cad_deg')!=old_occ[o['id']].get('rotation_cad_deg')}
checks=0;contacts=[];failures=[]
for angle in angles:
 poses=candidate_transforms(m,angle,base_transforms=authority.transforms)
 placed={oid:occurrence_shape(o,defs[o['definition']],angle).moved(poses[oid]) for oid,o in occ.items()}
 boxes={oid:shape.bounding_box() for oid,shape in placed.items()}
 def bounds_overlap(a,b):
  aa,bb=boxes[a],boxes[b]
  return all(min(getattr(aa.max,k),getattr(bb.max,k))-max(getattr(aa.min,k),getattr(bb.min,k))>.001 for k in ['X','Y','Z'])
 keys=list(placed)
 for i,aid in enumerate(keys):
  if i%200==0:print('Collision progress',angle,i,'of',len(keys),'exact',checks,'failures',len(failures),flush=True)
  for bid in keys[i+1:]:
   if aid not in changed and bid not in changed:continue
   if not bounds_overlap(aid,bid):continue
   vol=intersect_volume(placed[aid],placed[bid]);checks+=1
   if vol>.1:
    f={'crank_deg':angle,'a':aid,'b':bid,'overlap_mm3':vol};failures.append(f);print(f,flush=True)
 for cylinder in range(1,7):
  for kind in ['intake','exhaust']:
   tag=f'c{cylinder}-{kind}';s=state(angle,cylinder,kind);x=occ[tag+'-valve']['position_cad_mm'][0]
   for one,two in [(tag+'-spring','cylinder-head'),(tag+'-spring',tag+'-retainer'),(tag+'-seal','cylinder-head'),(tag+'-rocker',tag+'-fulcrum'),(tag+'-rocker',tag+'-pushrod'),(tag+'-pushrod',tag+'-lifter-pushrod-cup')]:
    gap=placed[one].distance_to(placed[two]);contacts.append({'crank_deg':angle,'a':one,'b':two,'gap_mm':gap})
    if gap>.002:failures.append(contacts[-1])
   witness=b.Vertex(x,s['pad_y'],261+v.LENGTHS[kind]-s['valve_lift'])
   gap=max(witness.distance_to(placed[tag+'-rocker']),witness.distance_to(placed[tag+'-valve']))
   contacts.append({'crank_deg':angle,'a':tag+'-rocker','b':tag+'-valve','gap_mm':gap,'method':'common tangent witness'})
   if gap>.002:failures.append(contacts[-1])
 print('Angle',angle,'changed',len(changed),'exact',checks,'contacts',len(contacts),'failures',len(failures),flush=True)
 if angle==0:b.export_step(b.Compound(children=list(placed.values())),OUT/'all12-at-crank0.step')
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items()),'Geometry changed during audit'
report={'status':'PASS' if not failures else 'FAIL','baseline_manifest_sha256':provenance['baseline_manifest_sha256'],'candidate_manifest_sha256':hashlib.sha256((OUT/'manifest.json').read_bytes()).hexdigest(),'source_step_hashes':hashes,'changed_occurrences':sorted(changed),'crank_angles_deg':angles,'exact_intersections':checks,'contacts':contacts,'failures':failures,'overlap_failure_threshold_mm3':.1,'contact_failure_threshold_mm':.002,'scope':'All changed source-sized occurrences against every frozen engine occurrence. Unchanged/unchanged pairs inherit baseline and are not rechecked. Sampled motion, not continuous proof.'}
(OUT/(a.report or ('static-validation.json' if angles==[0] else 'motion-validation.json'))).write_text(json.dumps(report,indent=2)+'\n');print(report['status'],checks,len(contacts),len(failures),flush=True);sys.exit(bool(failures))
