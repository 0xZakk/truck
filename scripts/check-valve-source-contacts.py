"""All12 phase-correct cam/pad witnesses and ground spring seating contacts."""
from pathlib import Path
import sys,json,hashlib,math,importlib.util
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_source_integration import candidate_transforms,occurrence_shape,state
from valve_layout_integration import FIRING_ORDER
import valve_source_layout as v
OUT=ROOT/'cad/engine/candidates/valve-source-all12';BASE=OUT/'baseline'
m=json.loads((OUT/'manifest.json').read_text());occ={o['id']:o for o in m['occurrences']}
spec=importlib.util.spec_from_file_location('frozen_source_assembly_math',BASE/'assembly_math.py');authority=importlib.util.module_from_spec(spec);spec.loader.exec_module(authority)
names=['camshaft','cylinder-head']
for c in range(1,7):
 for k in ['intake','exhaust']:
  names += [f'c{c}-{k}-{s}' for s in ['rocker','valve','spring','retainer','seal','fulcrum','pushrod','lifter-pushrod-cup','lifter-body']]
dmap={d['id']:d for d in m['definitions']};defs={};hashes={}
for oid in names:
 did=occ[oid]['definition']
 if did in defs:continue
 path=ROOT/dmap[did]['step'].lstrip('/');defs[did]=b.import_step(path);hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
angles=[0,111,150,180,210,246,282,333,342,360,372,420,468,516,540,564,603,720]
contacts=[];failures=[];negative_controls=0
for angle in angles:
 poses=candidate_transforms(m,angle,base_transforms=authority.transforms)
 placed={oid:occurrence_shape(occ[oid],defs[occ[oid]['definition']],angle).moved(poses[oid]) for oid in names}
 for c in range(1,7):
  for kind in ['intake','exhaust']:
   tag=f'c{c}-{kind}';s=state(angle,c,kind);x=occ[tag+'-valve']['position_cad_mm'][0]
   for one,two in [(tag+'-spring','cylinder-head'),(tag+'-spring',tag+'-retainer'),(tag+'-seal','cylinder-head'),(tag+'-rocker',tag+'-fulcrum'),(tag+'-rocker',tag+'-pushrod'),(tag+'-pushrod',tag+'-lifter-pushrod-cup')]:
    gap=placed[one].distance_to(placed[two]);entry={'crank_deg':angle,'a':one,'b':two,'gap_mm':gap};contacts.append(entry)
    if gap>.002:failures.append(entry)
   pad=b.Vertex(x,s['pad_y'],261+v.LENGTHS[kind]-s['valve_lift'])
   center=(468 if kind=='intake' else 246)+FIRING_ORDER.index(c)*120
   offset=(angle-center+360)%720-360;u=offset/135;q=96/135;k=-math.log(.05/.247)*(1-q*q)/(q*q)
   slope=0 if abs(u)>=1 else s['lifter_lift']*(-2*k*u/(1-u*u)**2)/math.radians(67.5)
   cam=b.Vertex(x,90-slope,90+s['lifter_lift'])
   for point,one,two in [(pad,tag+'-rocker',tag+'-valve'),(cam,'camshaft',tag+'-lifter-body')]:
    gap=max(point.distance_to(placed[one]),point.distance_to(placed[two]));entry={'crank_deg':angle,'a':one,'b':two,'gap_mm':gap,'method':'common tangent witness'};contacts.append(entry)
    if gap>.002:failures.append(entry)
    for sign in [-1,1]:
     displaced=b.Pos(0,0,sign*.1)*point;distance=max(displaced.distance_to(placed[one]),displaced.distance_to(placed[two]));negative_controls+=1
     if distance<.05:failures.append({'crank_deg':angle,'a':one,'b':two,'negative_control_gap_mm':distance})
 print('Contacts',angle,len(contacts),'failures',len(failures),flush=True)
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
report={'status':'PASS' if not failures else 'FAIL','candidate_manifest_sha256':hashlib.sha256((OUT/'manifest.json').read_bytes()).hexdigest(),'source_step_hashes':hashes,'crank_angles_deg':angles,'contacts':contacts,'negative_controls':negative_controls,'failures':failures,'scope':'All12 sampled source-v2 positive contacts and negative witness controls; not a collision audit.'}
(OUT/'contact-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(contacts),negative_controls,len(failures));sys.exit(bool(failures))
