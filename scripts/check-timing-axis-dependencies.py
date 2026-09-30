#!/usr/bin/env python3
"""Read-only datum extraction; stdout JSON. No CAD imports or installation."""
import hashlib,json,math,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
a={x['id']:x for x in m['assemblies']};o={x['id']:x for x in m['occurrences']}
files=['cad/engine/full_engine.py','cad/engine/cam_retention.py','cad/engine/expansion_plugs.py','cad/engine/rear_cam_clearance_desktop.py','cad/engine/oil_drive_layout.py','cad/engine/oil_pump_drive.py','cad/engine/valve_source_layout.py','cad/engine/valve_source_integration.py','cad/engine/valve_dimensions_candidate.py','cad/engine/valve_layout_integration.py','cad/engine/valvetrain_dispatch.py','cad/engine/assembly_math.py','viewer/engine-valve-source.js','reference/engine/timing-axis-datum-leads.json']
assert a['cam-motion']['position_cad_mm']==[0,90,72]
assert m['valvetrain_model']=='source-sized-v2'
assert len([x for x in o if x.startswith('cam-bearing-')])==4
assert len([x for x in o if x.endswith('-lifter-body')])==12
assert all(x['valvetrain']['model']=='source-sized-v2' for x in o.values() if x.get('valvetrain'))
ids=['camshaft','cam-timing-gear','crank-timing-gear','cam-thrust-plate','cam-gear-spacer','cam-timing-key','rear-cam-plug']+[f'cam-bearing-{i}' for i in range(1,5)]+[f'c1-{k}-{s}' for k in ['intake','exhaust'] for s in ['lifter-body','lifter-pushrod-cup','pushrod','rocker','fulcrum','valve']]
base=math.hypot(90,72)
hyp=[]
for center,kind in [(121.8,'independent candidate estimate'),(122.0216,'unverified forum assertion converted from 4.804 in; NOT accepted datum')]:
 y,z=90*center/base,72*center/base
 hyp.append(dict(center_mm=center,evidence_class=kind,conditional_same_direction_yz_mm=[y,z],conditional_delta_yz_mm=[y-90,z-72],direction_is_estimated=True))
print(json.dumps({'schema_version':1,'status':'PASS read-only datum extraction; migration NOT RUN','baseline_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'manifest_sha256':sha('inventory/engine/full-assembly.json'),'scope':'#32 dependency audit only; local occurrence positions are not world positions','input_sha256':{p:sha(p) for p in files},'current_cam_center_mm':base,'hypotheses':hyp,'assemblies':{k:a[k] for k in ['cam-motion','cam-retention-assembly','distributor-assembly','oil-drive-assembly','oil-pump-assembly']},'occurrences':{k:{f:o[k].get(f) for f in ['definition','parent','position_cad_mm','rotation_cad_deg','valvetrain']} for k in ids},'dependency_groups':{'axis_support':['block','camshaft','cam-bearing','rear-cam-plug'],'front_retention':['cam-thrust-plate','cam-thrust-bolt','cam-thrust-washer','cam-gear-spacer','cam-timing-key','cam-timing-gear','crank-timing-gear'],'valvetrain':['lifter-body and all internal occurrences','pushrod','rocker-arm','rocker-fulcrum','rocker-bolt','rocker-guide','cylinder-head','head-gasket','valve-cover'],'oil_drive':['distributor-assembly','oil-drive-assembly','oil-pump-assembly','oil-pickup-assembly','block drive bosses/tunnels/pump sockets','pump outlet joint'],'cover_boundary':['timing-cover','front-seal','cover flange/block seat','pan gasket/bridge'],'shared_authorities':['full_engine.py','assembly_math.py','valvetrain_dispatch.py','valve_source_integration.py','viewer/engine-valve-source.js','viewer/atlas.js']},'motion_counts':{role:sum(x.get('valvetrain',{}).get('role')==role for x in o.values()) for role in ['lifter','pushrod','rocker','valve','spring']},'limits':['No solids loaded, no clearance or migration pass claimed','Rear exhaust integration may change whole manifest hash; scope must be rebound explicitly','No production datum inferred from replacement diameters or forum lead']},indent=2))
