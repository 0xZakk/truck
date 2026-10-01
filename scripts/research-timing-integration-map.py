"""Read-only dependency map for a coordinated timing installation."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import numpy as np
from assembly_math import transforms
import timing_valvetrain_inclined_candidate as valve
import timing_coupled_core_candidate as core
import timing_cover_attachment_v2 as joint
mp=ROOT/'inventory/engine/full-assembly.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original_hash=sha(mp);m=json.loads(mp.read_text());occ={o['id']:o for o in m['occurrences']};assemblies={a['id']:a for a in m['assemblies']}
old=transforms(m,0);new=valve.poses(m,0,0)
def matrix(loc):
 t=loc.wrapped.Transformation()
 return np.array([[t.Value(i,j) for j in range(1,5)]for i in range(1,4)])
changed=[]
for oid in occ:
 a,z=matrix(old[oid]),matrix(new[oid]);error=float(np.max(abs(a-z)))
 if error>1e-8:changed.append({'id':oid,'definition':occ[oid]['definition'],'role':occ[oid].get('valvetrain',{}).get('role','stationary linkage attachment'),'max_matrix_difference':error})
def descendants(group):
 out=[]
 for oid,o in occ.items():
  parent=o.get('parent');seen=set()
  while parent:
   assert parent not in seen;seen.add(parent)
   if parent==group:out.append(oid);break
   parent=assemblies.get(parent,{}).get('parent')
 return out
roots=['distributor-assembly','oil-pump-assembly','oil-drive-assembly']
groups={g:descendants(g)for g in roots}
for ids in groups.values():assert len(ids)==len(set(ids))
core_ids=sorted(core.MOVING|set(core.STATIONARY)|{'crank-timing-gear'})
assert set(core_ids)<=set(occ)
stacks=[f'oil-pan-mounting-{kind}-{n}'for n in joint.RELOCATIONS for kind in ['screw','washer']];assert set(stacks)<=set(occ)
watch=[mp,Path(__file__),Path(valve.__file__),Path(core.__file__),Path(joint.__file__),ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/timing_valvetrain_adapter_candidate.py',ROOT/'cad/engine/timing_valvetrain_inclined_hypothesis.py']
r={'status':'DEPENDENCY MAP ONLY; no staged or installed geometry','input_sha256':{str(p.relative_to(ROOT)):sha(p)for p in watch},'pose_comparison':{'crank_degrees':0,'axial_mm':0,'changed_occurrences':len(changed),'rows':changed},'coupled_core_world_candidate_ids':core_ids,'rigid_drive_hypothesis':{'translation_mm':[0,*valve.numeric.DELTA],'groups':groups,'requires':'Validate connected interfaces and external neighbor motion before applying'},'external_drive_dependencies':{'oil-pickup-assembly':descendants('oil-pickup-assembly'),'review':['Pump outlet passage and block joint','Distributor clamp/seat, harness and ignition wire reach','Pickup screen clearance to revised pan and retained drain region']},'relocated_pan_stacks':stacks,'geometry_replacement_candidates':['block','cylinder-head','head-gasket','rocker-arm','oil-pan','timing-cover','oil-pan-gasket','oil-pan-mounting-screw'],'unresolved_new_parts':['Main cover gasket and actual attachment hardware','Front terminal sealant representation','Source-sized front seal case/lip/spring and matching hub seat'],'coordinate_caution':'Core exports and block are world-space; head and rocker exports local. Never apply existing frames twice.','limits':['Rest-pose discovery only','No full BOM guarantee','Front block/pan and seal contracts unresolved','Browser NOT RUN']}
assert sha(mp)==original_hash
(ROOT/'inventory/engine/timing-integration-map.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'changed_valvetrain_occurrences':len(changed),'core':len(core_ids),'drive_groups':{k:len(v)for k,v in groups.items()},'relocated_pan_occurrences':len(stacks)},indent=2))
