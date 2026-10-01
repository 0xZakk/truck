from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[R/'inventory/engine'/('waterpump-heater-source-'+s+'.json')for s in ['registration','export','interfaces','neighbors','stud','visual','context']];reports=[json.loads(p.read_text())for p in paths]
for report in reports:
 for p,h in report.get('inputs',{}).items():assert sha(R/p)==h,(p,h)
s,e,i,n,stud,v,context=reports
metrics=i['metrics'];functional=all(x<1e-5 for k,x in metrics.items()if k!='blocked_probe_negative_control_mm3')and metrics['blocked_probe_negative_control_mm3']>1
contact=all(x['missing_mm2']<1e-5 and x['actual_mm2']>600 for x in i['socket_contact'].values())
gates={'exports':all(x['valid']and x['watertight']and x['solids']==1 for x in e['parts'].values()),'source_replay':max(e['source_replay'].values())<1e-5,'functional_wall_locality':functional,'tube_insertion_contact':contact,'all_four_pump_tools':all(max(x['housing_overlap_mm3'],x['tube_overlap_mm3'])<.1 for x in i['tools']if x['type']=='pump'),'housing_q0_neighbors':not any(x['variant']=='housing'for x in n['conflicts']+n['errors']),'tube_q0_neighbors':False,'main3_inherited_tool':False}
files=paths+[Path(__file__),R/'docs/components/waterpump-heater-source-candidate.md']
r={'status':'FAIL whole-engine tube route; bounded local root/contact gates pass','gates':gates,'parts':e['parts'],'neighbors_checked':n['occurrences_checked'],'exact_pairs_including_resolved_stud':len(n['exact_pairs'])+1,'conflicts':n['conflicts']+[stud],'original_error':'Neighbor report retains ShapeList container error; supplementary stud report resolves exact two-solid intersection.','source_class':'Gates44009 replacement topology; every new3D dimension inferred, not measured Ford1994 geometry.','boundary':{'old_world_mm':[438,-132,270],'new_world_mm':e['hose_boundary_world_mm'],'new_direction':e['hose_boundary_direction'],'status':'Changed only in candidate; no vehicle heater hose geometry exists.'},'visual_review':'review.png and context.png inspected against original three pump photos; separate root radialangle/stem tangent retained; whole route conflict clearly visible.','limits':['Nominal source topology study, not production tolerance or physical fit specification.','Source side axial scaling and tip position remain weak, perspective dependent.','No browser installation, full moving-engine sweep, pressure/retention/flow capacity validation.','Frozen offset sensitivity failures and rear main3/strip failures remain unchanged.'],'files':{str(p.relative_to(R)):sha(p)for p in files}}
(R/'inventory/engine/waterpump-heater-source-delivery.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],gates)
