#!/usr/bin/env python3
"""Verify final trial6 export, guarded tool rebind and independent seat-gap control."""
from pathlib import Path
import json,sys,hashlib,ast
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_matched_carriers_trial6 as src
import accessory_brackets as base
from cad_metrics import solid_volume
O=R/'cad/engine/generated/accessory-matched-carriers';sp=O/'trial6-carrier.step';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=b.import_step(sp);rp=R/'inventory/engine/accessory-matched-carriers-trial6-check.json';r=json.loads(rp.read_text());fp=R/'inventory/engine/accessory-matched-carriers-fasteners.json';old=json.loads(fp.read_text());inputs={str(p.relative_to(R)):sha(p)for p in [sp,rp,fp,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py',R/'cad/engine/cad_metrics.py',R/'cad/engine/thermactor_pump.py']}
# Carrier changed; stationary/moved neighbors and tool poses did not. Rebind only
# exact same old neighbor inputs; carrier results are recomputed below.
for name,h in old['inputs'].items():
 if name.endswith('trial4-carrier.step'):continue
 assert sha(R/name)==h,name
 inputs[name]=h
for p in (R/'cad/engine').glob('accessory_matched_carriers*.py'):inputs[str(p.relative_to(R))]=sha(p);ast.parse(p.read_text())
for p in (R/'scripts').glob('accessory-matched-carriers*.py'):ast.parse(p.read_text())
vv,ff=s.tessellate(.08,.12);v=np.array([tuple(p)for p in vv]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.array(ff));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=O/'trial6-carrier.glb';mesh.export(gp);back=trimesh.load(gp,force='mesh');back.merge_vertices(digits_vertex=8);v=np.array(back.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=s.bounding_box();err=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
seats=[('engine-'+str(i),373,12,y,z)for i,(y,z)in enumerate(src.ENGINE_SEATS)]+[(g+'-'+str(i),src.FACES[g],10,y,z)for g in src.EARS for i,(y,z)in enumerate(src.EARS[g])];checks=[]
for name,x,width,y,z in seats:
 probe=base.axial(5.4,width,(x+width/2,y,z));a=probe.intersect(s);tool=base.axial(11,40,(x+width+26,y,z));c=tool.intersect(s);checks.append({'seat':name,'hole_probe_overlap_mm3':solid_volume(a)if a else 0,'carrier_tool_overlap_mm3':solid_volume(c)if c else 0})
w=base.boss(373,-100,220,12,5.5,width=.02);fault=solid_volume(w.cut(b.Pos(1,0,0)*s));assert fault>.1
mates={'block','cylinder-head','alternator-drive-housing','thermactor-front-plate'};nonmating=[x for x in r['neighbors']if x['neighbor']not in mates and not any(q in x['neighbor']for q in ['bracket-bolt','mount-bolt','engine-bolt'])];fails=[x for x in r['neighbors']if 'error'in x or x.get('overlap_mm3',0)>.1];reserve=[x for x in nonmating if x.get('distance_mm',0)<1-1e-7]
# Resolve exact owner of each engine annulus independently of union-of-neighbors.
from assembly_clockwise_candidate import transforms
mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());tt=transforms(m,0,0);dd={d['id']:d for d in m['definitions']};oo={o['id']:o for o in m['occurrences']};owner_rows=[]
for i,(y,z) in enumerate(src.ENGINE_SEATS):
 name='cylinder-head'if i==1 else'block';p=R/dd[oo[name]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);actual=tt[name]*b.import_step(p);owner_witness=base.boss(372.98,y,z,12,5.5,width=.02);owner_rows.append({'seat':'engine-'+str(i),'owner':name,'missing_mm3':solid_volume(owner_witness.cut(actual))})
out={'status':'COMPLETE conditional geometry; new-pump lower-engine-bolt tool access FAIL','exports':{'STEP':{'valid':s.is_valid,'solids':len(s.solids()),'sha256':sha(sp)},'GLB':{'watertight':back.is_watertight,'winding_consistent':back.is_winding_consistent,'components':len(back.split()),'bounds_error_mm':err,'sha256':sha(gp)}},'actual_neighbor_failures':fails,'nonmating_1mm_reserve_failures':reserve,'named_seats':r['seats'],'resolved_engine_owners':owner_rows,'pump_solid_sensitivity':r['pump_sensitivity'],'holes_and_carrier_tools':checks,'rebound_tool_neighbor_results':old['tools'],'wrong_seat_gap_missing_mm3':fault,'source_class':'All support routes/sections estimated; smooth insertion only, retention/strength unknown','inputs':inputs}
assert s.is_valid and len(s.solids())==1 and back.is_watertight and err<.1
(R/'inventory/engine/accessory-matched-carriers-trial6-final-check.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(fails),len(reserve),err)
