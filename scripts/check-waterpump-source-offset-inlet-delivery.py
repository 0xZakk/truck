"""Freeze separate statuses without erasing sensitivity or inherited failures."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reports=[R/'inventory/engine'/('waterpump-source-offset-'+s+'.json')for s in ['inlet-export','inlet-interfaces','inlet-neighbors','inlet-visual','residual']]
e,i,n,v,res=[json.loads(p.read_text())for p in reports]
for report in [e,i,n,v,res]:
 for p,h in report.get('inputs',{}).items():assert sha(R/p)==h,(p,h)
nom=i['variants']['nominal'];nomrows=[x for x in n['exact_pairs']if x['variant']=='nominal']
gates={'valid_exports':all(x['valid']and x['watertight']and x['solids']==1 for x in e['parts'].values()),'source_replay':max(e['replay'].values())<1e-5,'nominal_all_actual_q0_neighbors':not any(x['overlap_mm3']>.1 for x in nomrows)and not any(x['variant']=='nominal'for x in n['errors']),'all_offsets_fluid_wall_rear':all(max(x[k]for k in ['fluid_probe_obstruction_mm3','neck_bore_obstruction_mm3','nominal3_8mm_wall_missing_mm3','rear_belowX389_added_mm3','rear_belowX389_removed_mm3'])<1e-5 and x['blocked_probe_negative_control_mm3']>1 for x in i['variants'].values()),'nominal_inlet_owned_pump_tools':all(x['housing_overlap_mm3']<.1 for x in nom['pump_tools']if x['station']!=3),'all_access':False,'full_source_offset_sensitivity':False}
files=reports+[Path(__file__),R/'inventory/engine/waterpump-neck-registration-research.json',R/'docs/components/waterpump-source-offset-inlet-candidate.md']
r={'status':'FAIL bounded candidate; nominal inlet feasibility only','gates':gates,'parts':e['parts'],'nominal_exact_pairs':len(nomrows),'occurrences_checked':n['occurrences_checked'],'failures':['Heater pump3 tool504.5872707mm3 inherited','Rear main3 tool61.1070628mm3 inherited','High offset pump1 tool680.4620480mm3','Low offset actual carrier conflict confirmed by0.216mm3 interior cube; adaptive total volume NOT VERIFIED'],'visual_review':'Actual saved mesh image inspected; geometry, four mounts and unchanged cover visible.','limits':['Photo normalized coordinates remain estimates; perspective/application and old dimensional uncertainty remain.','Staticq0 only; no continuous motion or installation/browser verification.','R2 passage and wall gauge do not establish full volute/hydraulic capacity.','Radiator hose not modeled; nominal free end changed.','Inherited rear gasket strip topology failure retained in its frozen report.'],'files':{str(p.relative_to(R)):sha(p)for p in files}}
(R/'inventory/engine/waterpump-source-offset-inlet-delivery.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],gates)
