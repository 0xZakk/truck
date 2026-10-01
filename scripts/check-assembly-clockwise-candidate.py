"""Independent pose-contract checks; fixture does not claim complete staged engine."""
from pathlib import Path
import sys,json,copy,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import assembly_clockwise_candidate as adapter
import engine_clockwise_pose_candidate as physical
import cam_clockwise_candidate as cam
from assembly_math import transforms as legacy
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((R/'inventory/engine/full-assembly.json').read_text());m=copy.deepcopy(base)
p=json.loads((R/'inventory/engine/clockwise-linkage-pose-patch.json').read_text());lookup={o['id']:o for o in m['occurrences']}
for row in p['occurrences']:
 assert lookup[row['id']]==row['before'];lookup[row['id']].clear();lookup[row['id']].update(row['after'])
m['motion_revision']=adapter.REVISION
for a in m['assemblies']:
 if (a.get('motion') or {}).get('type') in ['rod','piston']:a['motion']['physical_rest_phase_deg']=-a['motion'].get('phase_deg',0)
 if a['id']=='cam-motion':a['position_cad_mm']=[0,*physical.AXIS]
def mat(p):
 t=p.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
maximum=0;checks=0
for q in [0,55,120,246,468,719]:
 for x in [0,-.1]:
  got=adapter.transforms(m,q,x);expected=cam.linkage_frames(base,q,x)
  expected['crankshaft']=physical.crank_frame(q)
  expected['camshaft']=physical.cam_frame(q,x)*b.Pos(0,*physical.AXIS)
  for o in m['occurrences']:
   if o['parent'].startswith(('rod-group-','piston-group-')):
    a=next(a for a in m['assemblies']if a['id']==o['parent']);motion=a['motion'];kind=motion['type']
    f=physical.corrected_slider_frames(q,motion['phase_deg'],m['mechanism']['stroke_mm']/2,m['mechanism']['rod_length_mm'],a['position_cad_mm'][0],measured_cad_rest_phase_degrees=motion['physical_rest_phase_deg'])[kind]
    expected[o['id']]=f*b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0]))
  for key,want in expected.items():
   maximum=max(maximum,float(np.max(abs(mat(got[key])-mat(want)))));checks+=1
assert maximum<1e-8,(maximum,checks)
controls=[]
for label in ['legacy-manifest','missing-physical-phase','mixed-valve-revision','out-of-range-endplay']:
 bad=copy.deepcopy(m);x=0
 if label=='legacy-manifest':bad.pop('motion_revision')
 if label=='missing-physical-phase':next(a for a in bad['assemblies']if a['id']=='rod-group-2')['motion'].pop('physical_rest_phase_deg')
 if label=='mixed-valve-revision':next(o for o in bad['occurrences']if o.get('valvetrain'))['valvetrain']['model']='source-sized-v2'
 if label=='out-of-range-endplay':x=.1
 try:adapter.transforms(bad,55,x)
 except ValueError:controls.append(label)
 else:raise AssertionError(label)
paths=[Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py',R/'cad/engine/cam_clockwise_candidate.py',R/'cad/engine/engine_clockwise_pose_candidate.py',R/'cad/engine/crossed_oil_drive_endplay_candidate.py',R/'inventory/engine/full-assembly.json',R/'inventory/engine/clockwise-linkage-pose-patch.json']
report={'status':'PASS independent motion contracts','fixture_scope':'Neutral valve patch and declared corrected axis/physical phases; not complete core asset stage','matrix_checks':checks,'maximum_matrix_error':maximum,'rejected_controls':controls,'bindings':{str(p.relative_to(R)):sha(p)for p in paths},'limits':['Distributor/oil-pump downstream matrices require staged branch audit','No springshape deformation here','No asset/CAD interference or browser acceptance']}
(R/'inventory/engine/assembly-clockwise-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],checks,maximum)
