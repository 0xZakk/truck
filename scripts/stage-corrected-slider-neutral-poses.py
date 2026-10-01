#!/usr/bin/env python3
"""Preserve event metadata; serialize physical rest phase and neutral frame contract."""
from pathlib import Path
import sys,json,hashlib,copy,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from engine_clockwise_pose_candidate import corrected_slider_frames
from assembly_math import transforms
manifest=R/'inventory/engine/full-assembly.json';m=json.loads(manifest.read_text());evidencepath=R/'inventory/engine/crank-clockwise-candidate-validation.json';e=json.loads(evidencepath.read_text());cp=R/'cad/engine/generated/crank-clockwise-candidate/crankshaft.step';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(cp)==e['candidate_step_sha256']
measured=[math.degrees(math.atan2(-p['yz'][0],p['yz'][1]))for p in e['actual_axes']];radius=m['mechanism']['stroke_mm']/2;length=m['mechanism']['rod_length_mm'];oldposes=transforms(m);changes=[];world=[];journal_errors=[];faults=[]
def matrix(p):
 t=p.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
for a in m['assemblies']:
 if not a['id'].startswith(('rod-group-','piston-group-')):continue
 i=int(a['id'].rsplit('-',1)[1]);event=a['motion']['phase_deg'];kind=a['motion']['type'];frame=corrected_slider_frames(0,event,radius,length,a['position_cad_mm'][0],measured_cad_rest_phase_degrees=measured[i-1])[kind]
 after=copy.deepcopy(a);after['motion']['event_phase_deg']=event;after['motion']['physical_rest_phase_deg']=-event
 changes.append({'id':a['id'],'before':a,'after':after,'neutral_world_matrix':matrix(frame).tolist(),'runtime_requirement':'Root adapter must consume physical_rest_phase_deg once; existing phase_deg remains event metadata.'})
 # Independent trig at physical -event. Does not read frame-construction intermediates.
 t=math.radians(-event);y=-radius*math.sin(t);z=radius*math.cos(t);height=z+math.sqrt(length**2-y*y)
 if kind=='rod':
  target=np.array([a['position_cad_mm'][0],y,z]);error=float(np.max(abs(matrix(frame)[:,3]-target)));journal_errors.append(error);assert error<1e-10
  actual=np.array(e['actual_axes'][i-1]['yz']);assert np.max(abs(actual-[y,z]))<.01
 else:assert abs(matrix(frame)[2,3]-height)<1e-10
 for o in m['occurrences']:
  if o['parent']==a['id']:
   p=frame*b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0]));world.append({'id':o['id'],'parent':o['parent'],'world_matrix':matrix(p).tolist(),'preserved_occurrence':o});faults.append(float(np.max(abs(matrix(p)-matrix(oldposes[o['id']])))))
assert len(changes)==12 and max(faults)>80
patch={'schema':'truck-guarded-integration-proposal-v1','scope':'Physical slider neutral phase contract; requires corrected runtime, preserves event phases','manifest_sha256':sha(manifest),'definitions':[],'occurrences':[],'assemblies':changes,'neutral_occurrence_frames':world,'requirements':['Apply with corrected crank/core asset patch and root runtime adapter.','Do not negate event phase inputs or use unchanged legacy phase handler.','Do not apply neutral world matrices as additional transforms on top of dynamic motion.']}
p=R/'inventory/engine/timing-corrected-slider-neutral-patch.json';p.write_text(json.dumps(patch,indent=2)+'\n')
inputs=[Path(__file__),manifest,evidencepath,cp,R/'cad/engine/engine_clockwise_pose_candidate.py',R/'cad/engine/assembly_math.py'];r={'scope':'Neutral physical phase and descendant world frame serialization, not new geometry/contact acceptance','groups':len(changes),'occurrences':len(world),'maximum_journal_center_error_mm':max(journal_errors),'legacy_rest_frame_fault_max':max(faults),'input_sha256':{str(p.relative_to(R)):sha(p)for p in inputs},'patch_sha256':sha(p)};(R/'inventory/engine/timing-corrected-slider-neutral-review.json').write_text(json.dumps(r,indent=2)+'\n');print(r['groups'],r['occurrences'],max(faults))
