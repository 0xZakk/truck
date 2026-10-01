#!/usr/bin/env python3
"""Bind final prototype export, all named seats, bounded clearance certificate and blind floors."""
from pathlib import Path
import json,sys,hashlib
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_psac_carrier_trial1 as src
import accessory_brackets as base
from cad_metrics import solid_volume
O=R/'cad/engine/generated/accessory-psac-carrier';sp=O/'trial1-carrier.step';rp=R/'inventory/engine/accessory-psac-carrier-trial1-check.json';fp=R/'inventory/engine/accessory-psac-carrier-trial1-fasteners.json';certp=R/'inventory/engine/accessory-psac-carrier-pump-separation.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads(rp.read_text());f=json.loads(fp.read_text());cert=json.loads(certp.read_text());assert r['status'].startswith('COMPLETE')and f['status'].startswith('COMPLETE');s=b.import_step(sp);inputs={str(p.relative_to(R)):sha(p)for p in [sp,rp,fp,certp,Path(__file__),Path(src.__file__),R/'cad/engine/accessory_carrier_1994.py',Path(base.__file__),R/'cad/engine/tensioner_arm.py',R/'cad/engine/tensioner_engine_support.py',R/'cad/engine/cad_metrics.py',R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py']}
for report in [r,f,cert]:
 for n,h in report['inputs'].items():assert sha(R/n)==h,n;inputs[n]=h
v,faces=s.tessellate(.08,.12);mesh=trimesh.Trimesh(np.array([tuple(p)for p in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(faces));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=O/'trial1-carrier.glb';mesh.export(gp);back=trimesh.load(gp,force='mesh');back.merge_vertices(digits_vertex=8);vv=np.array(back.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=s.bounding_box();error=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert s.is_valid and len(s.solids())==1 and back.is_watertight and error<.1
floor=[];ty,tz=src.PIVOT
for name,y,rad,x,voidrad in [('mount',ty,5.8,383.56,5.5),('locator',ty+20,6.35,387.56,6.2)]:
 w=base.axial(rad,2,(x,y,tz));c=s.intersect(base.axial(voidrad,2,(x+2,y,tz)));floor.append({'name':name,'minimum2mm_floor_missing_mm3':solid_volume(w.cut(s)),'tip_clearance2mm_overlap_mm3':solid_volume(c)if c else 0})
# Prove the proposed opposite-side carrier disjoint directly by actual STEP bounds.
p=R/'cad/engine/generated/accessory-matched-carriers/trial6-carrier.step';inputs[str(p.relative_to(R))]=sha(p);other=b.import_step(p);ob=other.bounding_box();altap_gap=bb.min.Y-ob.max.Y;assert altap_gap>1
named={'block','cylinder-head','ps-pump-housing','ac-compressor-front-cylinder','tensioner-spring-cartridge','tensioner-pivot-sleeve','tensioner-mounting-bolt','tensioner-locating-bushing'};clearance=[]
for x in r['neighbors']:
 n=x['neighbor']
 if n in named or n.startswith('carrier-')or 'bracket-bolt'in n:continue
 if n=='water-pump-housing':continue # Invalid raw closest point, replaced only by certificate.
 if x.get('distance_mm',0)<1-1e-7:clearance.append(x)
fail=[x for x in r['neighbors']if x.get('overlap_mm3',0)>.1 or 'error'in x]
out={'status':'COMPLETE conditional prototype; installed PS/AC tool access FAIL; no installation','exports':{'step_sha256':sha(sp),'glb_sha256':sha(gp),'valid':s.is_valid,'solids':len(s.solids()),'watertight':back.is_watertight,'winding_consistent':back.is_winding_consistent,'mesh_components':len(back.split()),'bounds_error_mm':error},'actual_overlap_failures':fail,'nonmating_1mm_failures':clearance,'v3_pump_distance_certificate':cert,'proposed_ALTAP_minimum_box_gap_mm':altap_gap,'named_seats':r['seats'],'blind_floors':floor,'tools':f['tools'],'holes':f['holes'],'wrong_seat_gap_control_missing_mm3':f['wrong_seat_gap_control_missing_mm3'],'inputs':inputs}
(R/'inventory/engine/accessory-psac-carrier-final-check.json').write_text(json.dumps(out,indent=2)+'\n');print(out['exports'],fail,clearance,floor)
