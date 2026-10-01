"""Verify a noninstalled accessory-pose proposal; never write a live manifest."""
from pathlib import Path
import copy,hashlib,json,sys
import numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'cad/engine'))
from assembly_clockwise_candidate import transforms
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=R/'inventory/engine/corrected-engine-stage-v3.json'
ep=R/'inventory/engine/accessory-constrained-layout-envelopes.json'
sp=R/'inventory/engine/accessory-constrained-layout-step-check.json'
m=json.loads(mp.read_text()); e=json.loads(ep.read_text()); s=json.loads(sp.read_text())
assert sha(mp)==e['stage_sha256']=='f512d6024ed4d3d0d86c45c39492b4ab525e039a9c50fb71b67940633b8a2055'
assert s['input_sha256'][str(ep.relative_to(R))]==sha(ep)
owner={}
for group,ids in e['moving_occurrence_ownership'].items():
 for oid in ids:
  assert oid not in owner,oid
  owner[oid]=group
roots={'alternator-assembly':'ALT','thermactor-pump-assembly':'AP','power-steering-pump-assembly':'PS','ac-compressor':'AC','tensioner-pulley-assembly':'TENS','tensioner-support-assembly':'TENS'}
delta={g:np.array([0,*s['posedelta_yz_mm'][g]],float) for g in e['moving_occurrence_ownership']}
a={x['id']:x for x in m['assemblies']}; o={x['id']:x for x in m['occurrences']}
assert set(owner)<=set(o)
def inherited(parent):
 result=np.zeros(3); seen=set()
 while parent:
  assert parent not in seen;seen.add(parent)
  if parent in roots:result+=delta[roots[parent]]
  parent=a[parent].get('parent')
 return result
trial=copy.deepcopy(m); edits=[]
for row in trial['assemblies']:
 if row['id'] in roots:
  before=list(row['position_cad_mm']); row['position_cad_mm']=(np.array(before)+delta[roots[row['id']]]).tolist()
  edits.append({'table':'assemblies','id':row['id'],'before':before,'after':row['position_cad_mm']})
for row in trial['occurrences']:
 desired=delta[owner[row['id']]] if row['id'] in owner else np.zeros(3)
 residual=desired-inherited(row['parent'])
 if np.max(abs(residual))>1e-12:
  # All residual corrections have fixed, unrotated parent chains. Other cases need inverse rotation.
  parent=row['parent']
  while parent:
   assert a[parent].get('rotation_cad_deg',[0,0,0])==[0,0,0]
   assert not a[parent].get('motion')
   parent=a[parent].get('parent')
  before=list(row['position_cad_mm']);row['position_cad_mm']=(np.array(before)+residual).tolist()
  edits.append({'table':'occurrences','id':row['id'],'before':before,'after':row['position_cad_mm']})
def matrix(p):
 t=p.wrapped.Transformation()
 return np.array([[t.Value(i,j) for j in range(1,5)] for i in range(1,4)])
def compare(candidate,params):
 before=transforms(m,**params);after=transforms(candidate,**params);errors={}
 for oid in o:
  expected=matrix(before[oid]);expected[:,3]+=delta[owner[oid]] if oid in owner else 0
  error=float(abs(matrix(after[oid])-expected).max())
  if error>1e-8:errors[oid]=error
 return errors
states=[{'degrees':q,'axial_mm':x,'throttle_degrees':t,'compressor_degrees':c,'compressor_engaged':eng} for q,x,t,c,eng in [(0,0,0,0,True),(55,0,30,73,True),(120,-.1,90,180,True),(240,0,0,359,False),(360,-.1,45,90,False),(719,0,90,270,True)]]
for state in states:assert not compare(trial,state),state
bad=copy.deepcopy(trial)
for row in bad['occurrences']:
 if row['id']=='thermactor-engine-bolt-1':row['position_cad_mm']=o[row['id']]['position_cad_mm']
fixed_failure=compare(bad,states[0]);assert 'thermactor-engine-bolt-1' in fixed_failure
bad=copy.deepcopy(trial)
for row in bad['occurrences']:
 if row['id'] in owner and owner[row['id']]=='AC':row['position_cad_mm']=(np.array(row['position_cad_mm'])+delta['AC']).tolist()
double_failure=compare(bad,states[1]);assert double_failure
inputs=[mp,ep,sp,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py']
result={'status':'PASS pose-only candidate serialization; no geometry installation','input_sha256':{str(p.relative_to(R)):sha(p) for p in inputs},'moving_group_counts':{g:len(v) for g,v in e['moving_occurrence_ownership'].items()},'edits':edits,'states':states,'occurrence_frame_comparisons':len(o)*len(states),'tolerance':1e-8,'fixed_bolt_negative_control':fixed_failure,'double_compressor_translation_negative_control':double_failure,'limits':['No solid collision/source/retention/belt/hoses/browser acceptance','Replacement carriers required; original carrier shapes would be incompatible with this pose-only proposal','Only six declared motion states; no full continuous-motion proof']}
(R/'inventory/engine/accessory-pose-serialization.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',result['occurrence_frame_comparisons'],'frame comparisons;',len(edits),'guarded edits; two fault controls')
