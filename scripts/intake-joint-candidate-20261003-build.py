#!/usr/bin/env python3
from pathlib import Path
import sys,importlib.util,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
p=ROOT/'cad/engine/intake-joint-candidate-20261003.py';spec=importlib.util.spec_from_file_location('joint_candidate',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=ROOT/'cad/engine/generated/intake-joint-candidate-20261003';out.mkdir(exist_ok=True)
print('Building coordinated parts',flush=True);start=time.time();parts,lower,upper=m.parts();print('Built',time.time()-start,flush=True)
report={'readiness':'candidate; not installed','parameters_sha256':hashlib.sha256(m.PARAM.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'parts':{},'stud_hypotheses':[]}
for key,shape in parts.items():
 print('Export',key,flush=True);path=out/(key+'.step');b.export_step(shape,path);reload=b.import_step(path);box=shape.bounding_box();box2=reload.bounding_box()
 report['parts'][key]={'valid':shape.is_valid,'roundtrip_valid':reload.is_valid,'roundtrip_solids':len(reload.solids()),'roundtrip_volume_delta_mm3':abs(reload.volume-shape.volume),'solids':len(shape.solids()),'volume_mm3':shape.volume,'step_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'roundtrip_bounds_max_mm':max(abs(a-c) for a,c in zip((*box.min,*box.max),(*box2.min,*box2.max))),'bounds_mm':[list(box.min),list(box.max)]}
for i,h in enumerate(m.P['stud_hole_hypothesis'],1):report['stud_hypotheses'].append({'id':f'efi-upper-stud-{i}','definition':'efi-upper-stud','position_cad_mm':[*m.H[h],371.5],'rotation_cad_deg':[0,0,0],'hole':h,'accepted':False,'role_resolved':i not in (3,5)})
(out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
