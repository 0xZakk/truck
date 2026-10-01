"""Rebind frozen interface evidence by exact asset/frame identity; no new Booleans."""
from pathlib import Path
import copy,hashlib,json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms
import accessory_matched_carriers_trial6 as alt
import accessory_psac_carrier_trial1 as ps
sha=lambda p:hashlib.sha256((R/p).read_bytes()).hexdigest()
inputs={}
def read(p):inputs[p]=sha(p);return json.loads((R/p).read_text())
def bind(p,h):assert sha(p)==h,p;inputs[p]=h
v3=read('inventory/engine/corrected-engine-stage-v3.json');v4=read('inventory/engine/corrected-engine-stage-v4.json')
assert inputs['inventory/engine/corrected-engine-stage-v4.json']=='9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9'
c=read('inventory/engine/accessory-coordinated-stage-contract.json');comp=read('inventory/engine/accessory-stage-v4-composition.json');assert comp['stage_sha256']==inputs['inventory/engine/corrected-engine-stage-v4.json']
for p,h in c['input_sha256'].items():bind(p,h)
report_names=['accessory-matched-carriers-trial6-final-check','accessory-matched-carriers-trial6-check','accessory-matched-carriers-fasteners','accessory-psac-carrier-final-check','accessory-psac-carrier-trial1-check','accessory-psac-carrier-trial1-fasteners','accessory-psac-carrier-clamp-stacks']
reports={}
for n in report_names:
 r=read('inventory/engine/'+n+'.json');reports[n]=r
 for p,h in r['inputs'].items():bind(p,h)
for n in ['accessory-matched-carriers-delivery','accessory-psac-carrier-delivery']:
 for p,h in read('inventory/engine/'+n+'.json')['files_sha256'].items():bind(p,h)
a=reports['accessory-matched-carriers-trial6-final-check'];s=reports['accessory-psac-carrier-final-check'];cl=reports['accessory-psac-carrier-clamp-stacks']
ids=['alternator-thermactor-common-carrier','ps-ac-support-bracket'];ds3={r['id']:r for r in v3['definitions']};ds4={r['id']:r for r in v4['definitions']};os3={r['id']:r for r in v3['occurrences']};os4={r['id']:r for r in v4['occurrences']}
assert set(os3)==set(os4);assert set(ds3)==set(ds4)
owner={oid:g for g,oids in c['moving_occurrence_ownership'].items()for oid in oids}
def matrix(t):
 tr=t.wrapped.Transformation();return np.array([[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)])
def expected(state):
 t=transforms(v3,**state);return {n:b.Pos(*c['delta_world_mm'][owner[n]])*p if n in owner else p for n,p in t.items()}
max_error=0
for state in c['verification']['states']:
 ex=expected(state);actual=transforms(v4,**state)
 for n in os3:
  err=float(abs(matrix(ex[n])-matrix(actual[n])).max());max_error=max(max_error,err);assert err<1e-8,n
zero={'degrees':0,'axial_mm':0};ex=expected(zero);actual=transforms(v4,**zero);bounds={};asset_rows=[]
for row in c['carrier_replacements']:
 n=row['id'];assert np.max(abs(matrix(actual[n])-np.eye(4)[:3]))<1e-8
 for kind in ['step','glb']:
  p=ds4[n][kind].lstrip('/');bind(p,row['replacement_assets'][kind]['sha256'])
 shape=b.import_step(R/ds4[n]['step'].lstrip('/'));bb=shape.bounding_box();bounds[n]=np.array([tuple(bb.min),tuple(bb.max)])
 asset_rows.append({'id':n,'world_matrix':matrix(actual[n]).tolist(),'actual_STEP_bounds_mm':bounds[n].tolist(),'STEP_sha256':sha(ds4[n]['step'].lstrip('/')),'GLB_sha256':sha(ds4[n]['glb'].lstrip('/'))})
for n in os3:
 if n in ids:continue
 assert os3[n]['definition']==os4[n]['definition']
 assert ds3[os3[n]['definition']]==ds4[os4[n]['definition']],n
 # Motion/deformation metadata must be identical, not merely the q0 matrix.
 assert {k:v for k,v in os3[n].items()if k!='position_cad_mm'}=={k:v for k,v in os4[n].items()if k!='position_cad_mm'},n

def owner_binding(n):
 if n=='candidate':raise AssertionError('Resolve candidate identity before binding')
 d=ds4[os4[n]['definition']];p=d['step'].lstrip('/');assert p in inputs,('unbound contact owner',n,p);assert sha(p)==inputs[p]
 return {'id':n,'definition':d['id'],'STEP_sha256':inputs[p],'matrix_world':matrix(actual[n]).tolist(),'delta_group':owner.get(n),'relative_to_identity_carrier':'same as frozen study expected world pose'}
rows=[]
for r in a['named_seats']:
 n=r['name'];mate=('cylinder-head'if n=='engine-1'else'block')if n.startswith('engine-')else r['mate_owners'][0]
 rows.append({'family':'ALT/AP support','name':n,'carrier':ids[0],'mate':owner_binding(mate),'frozen_result':r,'evidence':'REUSED exact asset and expected frame identity; no fresh solid contact calculation'})
for r in s['named_seats']:rows.append({'family':'PS/AC support','name':r['name'],'carrier':ids[1],'mate':owner_binding(r['owner']),'frozen_result':r,'evidence':'REUSED exact asset and expected frame identity; no fresh solid contact calculation'})
clamps=[]
for r in cl['rows']:
 owners=[ids[1]if r[k]=='candidate'else r[k]for k in ['low_owner','high_owner']]
 clamps.append({'name':r['name'],'owners':[owner_binding(n)for n in owners],'frozen_result':r,'evidence':'REUSED q0 annulus geometry by identical two-owner frames/assets and frozen witness code'})
assert len(rows)==20 and len(clamps)==15
for r in rows:assert abs(r['frozen_result']['carrier_missing_mm3'])<1e-6 and abs(r['frozen_result']['mate_missing_mm3'])<1e-6
for r in clamps:assert abs(r['frozen_result']['low_missing_mm3'])<1e-6 and abs(r['frozen_result']['high_missing_mm3'])<1e-6
# Opposite carrier was replaced since old tool checks. Do not reuse that old pair:
# exact finite cylinder boxes conservatively certify separation without Booleans.
new_tool_pairs=[]
def tool_box(name,axis,u,z,start,r,other):
 box=np.array([[start,u-r,z-r],[start+40,u+r,z+r]])if axis=='X'else np.array([[u-r,start,z-r],[u+r,start+40,z+r]])
 ob=bounds[other];gap=float(np.max(np.maximum(ob[0]-box[1],box[0]-ob[1])));assert gap>1
 new_tool_pairs.append({'tool':name,'opposite_new_carrier':other,'conservative_tool_bounds_mm':box.tolist(),'positive_axis_separation_mm':gap,'evidence':'FRESH analytic enclosing-box separation against actual imported STEP bounds; not fresh Boolean'})
for r in a['named_seats']:
 x,y,z=r['axis_world_mm'];width=12 if r['name'].startswith('engine-')else 10;tool_box('ALT/AP '+r['name'],'X',y,z,x+width+6,11,ids[1])
pscoords={'front-head':('X',90,300),**{'side-'+str(i):('Y',x,z)for i,(x,z)in enumerate(ps.SIDE)},**{'PS-'+str(i):('X',y,z)for i,(y,z)in enumerate(ps.PS_EARS)},**{'AC-'+str(i):('X',y,z)for i,(y,z)in enumerate(ps.AC_EARS)},'tensioner':('X',*ps.PIVOT)}
for r in s['tools']:
 axis,u,z=pscoords[r['seat']];tool_box('PS/AC '+r['seat'],axis,u,z,r['headfront_mm'],r['radius_mm'],ids[0])
# Fresh frame-based bad conditions. Frozen solid sensitivity results retained separately.
control={}
for n,delta in [('thermactor-engine-bolt-1',c['delta_world_mm']['AP']),(ids[0],c['delta_world_mm']['ALT']),('ps-bracket-bolt-1',[1,0,0])]:
 wrong=matrix(actual[n]).copy();wrong[:,3]+=delta;err=float(abs(wrong-matrix(ex[n])).max());assert err>1e-8;control[n]={'introduced_translation_mm':delta,'detected_matrix_error':err}
controls={'new_frame_controls':control,'frozen_ALTAP_1mm_gap_missing_mm3':a['wrong_seat_gap_missing_mm3'],'frozen_PSAC_1mm_gap_missing_mm3':s['wrong_seat_gap_control_missing_mm3']};assert controls['frozen_ALTAP_1mm_gap_missing_mm3']>.1 and controls['frozen_PSAC_1mm_gap_missing_mm3']>.1
for p in [str(Path(__file__).relative_to(R)),'cad/engine/accessory_psac_carrier_trial1.py','cad/engine/accessory_matched_carriers_trial6.py']:inputs[p]=sha(p)
out={'status':'PASS invariant interface rebind; inherited tool FAIL and production gaps retained','stage_sha256':sha('inventory/engine/corrected-engine-stage-v4.json'),'input_sha256':dict(sorted(inputs.items())),'fresh_checks':{'all_occurrence_frames':8166,'maximum_matrix_error':max_error,'q0_unchanged_geometry_occurrences':1359,'rigidly_translated_occurrences':len(owner),'fixed_occurrences':len(os3)-len(owner),'group_counts':{g:len(v)for g,v in c['moving_occurrence_ownership'].items()},'carrier_assets_and_frames':asset_rows,'opposite_carrier_tool_bounds':new_tool_pairs},'support_seats_reused':rows,'clamp_annuli_reused':clamps,'holes_and_carrier_tools_reused':{'ALTAP':a['holes_and_carrier_tools'],'PSAC':s['holes']},'blind_floors_reused':s['blind_floors'],'tool_neighbor_results_reused':{'ALTAP':a['rebound_tool_neighbor_results'],'PSAC':s['tools']},'negative_controls':controls,'scope_limits':['No new solid contact, bore, blind-floor or tool intersections calculated; those results reused only by exact source/assets/witness and expected q0 frame identity.','All old noncarrier neighbor geometry/poses match study inputs. Opposite carrier replacements receive new conservative tool-box checks; whole changed-neighbor collision audit belongs to root.','Six frame states do not prove continuous tensioner, belt or whole-engine motion.','Seven PS/AC pulley-blocked tool approaches and lower ALT/AP bolt against three separate new pump hypotheses remain FAIL.','Threads/preload/strength, source silhouette, hoses, belt and browser not accepted.']}
(R/'inventory/engine/accessory-stage-v4-interfaces.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(rows),'support seats',len(clamps),'clamps',len(new_tool_pairs),'fresh cross-carrier tool bounds')
