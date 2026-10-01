"""Exact local contacts and unchanged-material checks; retain every failure."""
from pathlib import Path
import sys,json,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
import timing_pump_rear_flange_candidate as c
old,paths,m,poses=c.load();parts={k:b.import_step(c.O/(k+'.step'))for k in old};defs={d['id']:d for d in m['definitions']};cutters=c.masks();inputs=[Path(__file__),Path(c.__file__),*paths.values(),*[c.O/(k+'.step')for k in parts],R/'inventory/engine/full-assembly.json'];errors={}
def vol(s):return sum(abs(q.volume)for q in s.solids())if s else 0.
def intersect(a,z):return c.norm(a.intersect(z))if a and z else None
def op(kind,a,z):
 q=kind(a.wrapped,z.wrapped);q.Build();assert q.IsDone();return b.Compound(q.Shape())
def faces(s):return b.Compound(list(s.faces()))
def surface(s,x):return b.Compound([f for f in s.faces()if abs(f.normal_at().X)>.999 and abs(f.center().X-x)<1e-5])
def support(g,x,owner):
 f=surface(g,x);common=op(BRepAlgoAPI_Common,f,faces(owner));missing=op(BRepAlgoAPI_Cut,f,faces(owner));return {'face_mm2':f.area,'contact_mm2':common.area,'missing_mm2':missing.area}
blockpath=R/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step';inputs.append(blockpath);block=b.import_step(blockpath)
rear=b.Pos(381,0,0)*b.Box(16,1000,1000) # X373..389
pair={}
for a,z in [('cover','housing'),('cover','pump-gasket'),('main-gasket','pump-gasket'),('main-gasket','housing')]:
 q=intersect(parts[a],parts[z]);pair[a+'__'+z]={'full_overlap_mm3':vol(q),'rear_overlap_mm3':vol(intersect(q,rear)),'old_rear_negative_control_mm3':vol(intersect(intersect(old[a],old[z]),rear))}
contacts={'main-block':support(parts['main-gasket'],373,block),'main-cover':support(parts['main-gasket'],373.8,parts['cover']),'pump-block':support(parts['pump-gasket'],373,block),'pump-housing':support(parts['pump-gasket'],375,parts['housing'])}
locality={};removed={}
for k in parts:
 d=c.norm(old[k].cut(parts[k]));removed[k]=d;locality[k]={'added_mm3':vol(parts[k].cut(old[k])),'removed_outside_mask_mm3':vol(d.cut(cutters[k]))if d else 0.,'removed_mm3':vol(d)}
main=[]
for n,(y,z)in enumerate(c.main.AXES,1):
 p=R/f'cad/engine/generated/timing-cover-seven-fastener-candidate/main-cover-screw-{n}.step';inputs.append(p);male=b.import_step(p);seat=c.cx(8.75,379.78,379.8,y,z).cut(c.cx(4.2,379.77,379.81,y,z));tool=c.cx(10.5,379.8,435,y,z)
 row={'station':n,'cover_overlap_mm3':vol(intersect(male,parts['cover'])),'block_overlap_mm3':vol(intersect(male,block)),'pump_overlap_mm3':vol(intersect(male,parts['housing'])),'headseat_missing_mm3':vol(seat.cut(parts['cover'])),'tool_cover_mm3':vol(intersect(tool,parts['cover'])),'tool_pump_rear_mm3':vol(intersect(intersect(tool,parts['housing']),rear)),'tool_pump_full_mm3':vol(intersect(tool,parts['housing'])),'R9_land_removed_mm3':vol(intersect(removed['cover'],c.cx(9,373.8,379.8,y,z)))}
 main.append(row);print('MAIN',row,flush=True)
pump=[];p=R/defs['water-pump-mounting-screw']['step'].lstrip('/');inputs.append(p);localmale=b.import_step(p)
for n in range(1,5):
 male=poses[f'water-pump-mounting-screw-{n}']*localmale;f=surface(male,389);actual=op(BRepAlgoAPI_Common,f,faces(parts['housing']));missing=op(BRepAlgoAPI_Cut,f,faces(parts['housing']));a=c.pump.MOUNTING[n-1];y,z=a[0]-32,a[1]+170;tool=c.cx(10.5,389,449,y,z)
 row={'station':n,'housing_overlap_mm3':vol(intersect(male,parts['housing'])),'cover_overlap_mm3':vol(intersect(male,parts['cover'])),'headseat_mm2':f.area,'headseat_missing_mm2':missing.area,'headseat_contact_mm2':actual.area,'tool_housing_mm3':vol(intersect(tool,parts['housing'])),'tool_cover_mm3':vol(intersect(tool,parts['cover']))};pump.append(row);print('PUMP',row,flush=True)
# Exact planar offsets test a connected 3mm sealing strip with0.04mm extra diameter.
strip={}
for k,x in [('main-gasket',373.4),('pump-gasket',374)]:
 try:
  sk=b.section(parts[k],b.Plane.YZ.offset(x));base=b.section(old[k],b.Plane.YZ.offset(x));assert len(sk.faces())==1 and len(base.faces())==1
  eroded=b.offset(sk,amount=-1.52);be=b.offset(base,amount=-1.52)
  strip[k]={'method':'Exact CAD planar inwardoffset1.52mm, testing connected3.04mmstrip; not pressure proof.','valid':eroded.is_valid,'holes':len(sk.faces()[0].inner_wires()),'old_holes':len(base.faces()[0].inner_wires()),'eroded_components':len(eroded.faces()),'old_eroded_components':len(be.faces()),'eroded_area_mm2':eroded.area,'empty':not bool(eroded.faces())}
 except Exception as e:strip[k]={'error':str(e),'valid':False,'empty':True,'eroded_components':0,'holes':-1,'old_holes':0}
 print('STRIP',k,strip[k],flush=True)
# Sensitivity: this margin protects fullrearR9 stock, independently fromphysicalheadR8.75.
y,z=c.main.AXES[2];d=math.dist(c.AXIS,(y,z));sensitivity=[]
for offset in [-.25,0,.1,.16,.25,.5,1.]:
 mask=c.masks(c.BOUNDARY_RADIUS+offset)['cover'];sensitivity.append({'radius_offset_mm':offset,'R9_nominal_margin_mm':d-9-c.BOUNDARY_RADIUS-offset,'R8_75_nominal_margin_mm':d-8.75-c.BOUNDARY_RADIUS-offset,'R9_guard_material_removed_mm3':vol(intersect(intersect(old['cover'],c.cx(9,373.8,379.8,y,z)),mask)),'required_headseat_removed_mm3':vol(intersect(c.cx(8.75,379.78,379.8,y,z).cut(c.cx(4.2,379.77,379.81,y,z)),mask))})
gates={'rear_no_overlap':all(v['rear_overlap_mm3']<.1 for v in pair.values()),'complete_gasket_faces':all(v['missing_mm2']<1e-5 for v in contacts.values()),'locality':all(v['added_mm3']<1e-5 and v['removed_outside_mask_mm3']<1e-5 for v in locality.values()),'main_actual_seats_and_rear_tools':all(v[k]<1e-5 for v in main for k in ['cover_overlap_mm3','block_overlap_mm3','headseat_missing_mm3','tool_cover_mm3','tool_pump_rear_mm3','R9_land_removed_mm3']),'pump_seats_and_tools':all(v[k]<1e-5 for v in pump for k in ['housing_overlap_mm3','cover_overlap_mm3','headseat_missing_mm2','tool_housing_mm3','tool_cover_mm3']),'connected_3mm_strip':all(v['valid']and not v['empty']and v['eroded_components']==1 and v['holes']==v['old_holes']for v in strip.values())}
r={'status':'PASS bounded rear-only gates'if all(gates.values())else'FAIL bounded rear candidate gates','gates':gates,'pairs':pair,'gasket_face_support':contacts,'locality':locality,'main_hardware':main,'pump_hardware':pump,'strip':strip,'sensitivity':sensitivity,'inputs':{str(p.relative_to(R)):c.sha(p)for p in inputs},'limits':['Forward inlet remains independent knownFAIL.','R10.5 tool envelopes are declared estimates; preserve obstruction failures.','0.1556mm nominalguardmargin is not production clearance.','No force, fluid pressure, tolerance class or factory-contour claim.']};(R/'inventory/engine/timing-pump-rear-flange-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],gates,flush=True)
