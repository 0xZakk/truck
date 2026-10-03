"""Compact restart audit. Hash validation is not geometry or installed acceptance."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];P='pump-cover-candidate-20261003';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reports={};inputs={}
for s in ['build','check','neighbors','tools','rotor-containment','non-spring-mesh','spring-mesh','source-compare','deck-registration']:
 p=R/f'reference/engine/{P}-{s}.json';j=json.loads(p.read_text());bad=[];count=0
 for path,h in j.get('inputs',{}).items():
  q=R/path;count+=1
  if not q.exists() or sha(q)!=h:bad.append(path)
 if s=='build':
  for group in ['parts','regions','block_features']:
   for n,v in j[group].items():
    q=R/v['path'];count+=1
    if not q.exists() or sha(q)!=v['sha256']:bad.append(v['path'])
 reports[s]={'path':str(p.relative_to(R)),'sha256':sha(p),'checked_input_or_export_hashes':count,'mismatches':bad};inputs[s]=j
mesh=inputs['non-spring-mesh']['parts'];check=inputs['check']['checks']
r={'status':'CANDIDATE FAIL; source datum and local flow work remain','baseline':'5584306a595f87b60b29eca9ea82b527ade5ae98','reports':reports,'hashes_current':all(not v['mismatches'] for v in reports.values()),'part_count':len(inputs['build']['parts']),'neighbors':{'pairs':inputs['neighbors']['pairs_total'],'conflicts':len(inputs['neighbors']['conflicts']),'errors':len(inputs['neighbors']['errors'])},'tools':{'checks':len(inputs['tools']['checks']),'conflicts':len(inputs['tools']['conflicts'])},'mesh':{'non_spring_count':len(mesh),'watertight_count':sum(v['watertight'] for v in mesh.values()),'consistent_winding_count':sum(v['winding'] for v in mesh.values()),'max_cad_bounds_error_mm':max(v['cad_bounds_error_mm'] for v in mesh.values())},'inlet_flow_obstruction_mm3':check['inlet_path']['obstruction_mm3'],'rotor_actual_outside_swept_volume_mm3':inputs['rotor-containment']['actual_impeller_outside_exact_swept_envelope_mm3'],'source_shape_verdict':inputs['source-compare']['verdict'],'dimensions_verdict':'FAIL installed registration: fourth axis Z260.259 > Ford nominal block deck254; primary source supports preserving deck','unrun':['Fresh installed browser integration','Continuous coupled engine/pump motion','Revised downstream belt/hose and accessory carrier integration'],'frozen_spring':'Unchanged; separate analytic illustration mesh only. No new physical spring claim.','script_sha256':sha(Path(__file__))}
(R/f'reference/engine/{P}-resume-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='reports'},indent=2))
