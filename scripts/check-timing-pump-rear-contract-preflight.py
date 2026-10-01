"""Analytic rear-flange hypothesis feasibility only; no exported replacement assets."""
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
import timing_cover_seven_fastener_candidate as main
import water_pump_joint_candidate as pump
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
O=R/'cad/engine/generated/timing-pump-rear-contract-preflight';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
 if not s:return None
 return b.Compound(list(s.solids()))
def vol(s):return abs(s.volume)if s else 0.
def contact(a,c):
 op=BRepAlgoAPI_Common(b.Compound(list(a.faces())).wrapped,b.Compound(list(c.faces())).wrapped);op.Build();return sum(f.area for f in b.Compound(op.Shape()).faces())
mp=R/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());poses=transforms(m);defs={q['id']:q for q in m['definitions']};paths={'housing':R/defs['water-pump-housing']['step'].lstrip('/'),'pump-gasket':R/defs['water-pump-gasket']['step'].lstrip('/'),'cover':R/'cad/engine/generated/timing-pan21-lateral-candidate/cover.step','main-gasket':R/'cad/engine/generated/timing-cover-attachment-v2/main-gasket.step','block':R/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step'}
parts={k:b.import_step(p)for k,p in paths.items()}
for k,n in [('housing','water-pump-housing'),('pump-gasket','water-pump-gasket')]:parts[k]=poses[n]*parts[k]
axis=(-32,170);bottom=(pump.MOUNTING[0][0]-32,pump.MOUNTING[0][1]+170);assert bottom[1]<120
cx=main.front.c.cx
# Replace only estimated boss protrusion outside the original coaxial rear wall;
# all stock within the analytic R66 rear chamber stays intact.
stock=cx(66,375,389,*axis)
annulus=cx(11.5,375,389,*bottom).cut(cx(8.75,374,390,*bottom)).cut(stock)
newpump=norm(parts['housing'].cut(annulus))
gannulus=cx(9.5,373,375,*bottom).cut(cx(8.75,372,376,*bottom)).cut(cx(65,372,376,*axis))
newpg=norm(parts['pump-gasket'].cut(gannulus))
# Fixed analytical boundary, limited to the already diagnosed lower-right sector.
sector=b.Pos(5,0,0) # documented rectangle below
window=b.Pos(379.5,5,120)*b.Box(13,60,60) # X373..386,Y−25..35,Z90..150
boundary=cx(66.25,372,387,*axis).intersect(window)
newcover=norm(parts['cover'].cut(boundary));newmg=norm(parts['main-gasket'].cut(boundary))
rear=b.Pos(379.5,0,0)*b.Box(13,1000,1000)
checks={};checks['housing_rear_overlap_mm3']=vol(norm(newcover.intersect(newpump).intersect(rear)));checks['pump_gasket_overlap_mm3']=vol(norm(newcover.intersect(newpg)));checks['two_gaskets_overlap_mm3']=vol(norm(newmg.intersect(newpg)))
checks['source_bore_R59_preserved_mm3']=vol(norm(parts['housing'].cut(newpump).intersect(cx(59,374,390,*axis))))
checks['main_hole_R9_guards_removed_mm3']={str(n):vol(norm(parts['cover'].cut(newcover).intersect(cx(9,373.8,379.8,*a))))for n,a in enumerate(main.AXES,1)}
checks['gasket_block_contact_mm2']=contact(newmg,parts['block']);checks['gasket_cover_contact_mm2']=contact(newmg,newcover)
checks['pump_gasket_block_contact_mm2']=contact(newpg,parts['block']);checks['pump_gasket_housing_contact_mm2']=contact(newpg,newpump)
checks['valid_connected']={k:bool(s and s.is_valid and len(s.solids())==1)for k,s in [('cover',newcover),('main-gasket',newmg),('housing',newpump),('pump-gasket',newpg)]}
checks['removed_mm3']={k:vol(norm(parts[k].cut(s)))for k,s in [('cover',newcover),('main-gasket',newmg),('housing',newpump),('pump-gasket',newpg)]}
checks['main3_to_pump_axis_mm']=math.dist(main.AXES[2],axis);checks['main3_to_bottom_mount_mm']=math.dist(main.AXES[2],bottom)
# Source fasteners and headseat integrity are tested directly, not inferred fromcircle alone.
checks['main_screw_rear_pump_overlap_mm3']={}
for n in [3]:
 p=R/f'cad/engine/generated/timing-cover-seven-fastener-candidate/main-cover-screw-{n}.step';paths[f'main-screw-{n}']=p;s=b.import_step(p);checks['main_screw_rear_pump_overlap_mm3'][str(n)]=vol(norm(s.intersect(newpump)))
p=R/defs['water-pump-mounting-screw']['step'].lstrip('/');paths['pump-screw']=p
male=poses['water-pump-mounting-screw-1']*b.import_step(p)
checks['lower_pump_screw_housing_clearance_mm3']=vol(norm(male.intersect(newpump)))
checks['pump_boss_full_R8_75_stock_unchanged_mm3']=vol(norm(parts['housing'].cut(newpump).intersect(cx(8.75,375,389,*bottom))))
checks['main_gasket_width_samples_mm']={}
for z in [112,115,120,125,130,135,140]:
 ys=np.arange(-25,60,.05);inside=[float(y)for y in ys if newmg.is_inside((373.4,y,z),tolerance=1e-7)]
 checks['main_gasket_width_samples_mm'][str(z)]=max(inside)-min(inside)if inside else 0.

# Perimeter mesh section for readable preflight comparison, not a replacement CADexport.
data={}
for name,s in [('cover-old',parts['cover']),('cover-trial',newcover),('pump-old',parts['housing']),('pump-trial',newpump),('gasket-trial',newmg)]:
 for x in [374,376,380]:
  sec=b.section(s,b.Plane.YZ.offset(x));edges=[np.array([tuple(e.position_at(t))for t in np.linspace(0,1,65)])for e in sec.edges()]
  if edges:data[f'{name}_{x}']=np.array(edges)
np.savez_compressed(O/'sections.npz',**data)
r={'status':'PREFLIGHT ONLY; full candidate not exported','contract':{'pump_axis_yz_mm':axis,'bottom_mount_yz_mm':bottom,'boss_radius_mm':8.75,'gasket_lug_radius_mm':8.75,'cover_separation_radius_mm':66.25,'window_mm':[[373,-25,90],[386,35,150]],'all_axes_fixed':True,'forward_inlet_unchanged':True},'checks':checks,'inputs':{str(p.relative_to(R)):sha(p)for p in [mp,Path(__file__),*paths.values(),R/'cad/engine/water_pump_joint_candidate.py']}};(R/'inventory/engine/timing-pump-rear-contract-preflight.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
