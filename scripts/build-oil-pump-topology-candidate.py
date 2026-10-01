#!/usr/bin/env python3
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
import oil_pump_topology_candidate as c
OUT=ROOT/'cad/engine/generated/oil-pump-topology-candidate';OUT.mkdir(exist_ok=True);rows=[]
for ident,q in c.build().items():
 assert q.is_valid and len(q.solids())==1,(ident,len(q.solids()))
 sp=OUT/(ident+'.step');b.export_step(q,sp);rt=b.import_step(sp);assert rt.is_valid
 v,f=rt.tessellate(.1,.12);v=np.array([tuple(x) for x in v]);m=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.array(f),process=True);m.update_faces(m.nondegenerate_faces());m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();gp=OUT/(ident+'.glb');m.export(gp);r=trimesh.load(gp,force='mesh');r.merge_vertices(digits_vertex=8)
 rows.append({'id':ident,'valid_solid':True,'solid_count':1,'volume_mm3':q.volume,'roundtrip_volume_difference_mm3':abs(q.volume-rt.volume),'watertight':bool(r.is_watertight),'winding_consistent':bool(r.is_winding_consistent),'positive_volume':bool(r.volume>0),'artifacts':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [sp,gp]}})
 print(ident,rows[-1],flush=True)
inputs=['cad/engine/oil_pump_topology_candidate.py','scripts/build-oil-pump-topology-candidate.py','cad/engine/generated/oil-pump-housing.step','reference/engine/oil-pump-topology-evidence.json'];r={'status':'TOPOLOGY ONLY; production dimensions and installed interfaces unresolved','inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},'display_estimates_mm':c.DISPLAY_ESTIMATES,'parts':rows,'limits':['No block occurrence or material changes','Mount flange is unperforated blank except inherited drive bore; bolt/dowel/outlet geometry intentionally absent','Pickup flange and gasket dimensions and holes are explicit display estimates; no mounting bolts or tube continuity modeled','Inherited rotor pocket, cover ears, relief and drive clearances are illustrative source geometry; no hydraulic function proven']};(ROOT/'inventory/engine/oil-pump-topology-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n')
