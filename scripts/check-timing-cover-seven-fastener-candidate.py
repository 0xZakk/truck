from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_cover_seven_fastener_candidate as c
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate';OUT.mkdir(exist_ok=True)
errors={}
def vol(shape):
 if shape is None:return 0.
 if isinstance(shape,b.ShapeList):return sum(vol(s)for s in shape)
 total=0.
 for s in shape.solids():
  prop=GProp_GProps();err=BRepGProp.VolumeProperties_s(s.wrapped,prop,1e-9,True,False)
  if err>1e-7:raise ValueError(f'Strict volume integration did not converge: {err}')
  total+=abs(prop.Mass())
 return total
def measure(name,shape):
 try:return vol(shape)
 except Exception as exc:errors[name]=repr(exc);return None
parts,d=c.build();print('built',flush=True)
valid={n:{'valid':s.is_valid,'solids':len(s.solids())}for n,s in parts.items()}
for n,s in parts.items():
 if s.is_valid and len(s.solids())==1:b.export_step(s,OUT/(n+'.step'))
block,cover=parts['block'],parts['cover'];rows=[]
for n,(y,z)in enumerate(c.AXES,1):
 loc=c.frame(y,z);seat=c.front.c.cx(8.75,c.SEAT-.02,c.SEAT,y,z)-c.front.c.cx(4.2,c.SEAT-.03,c.SEAT+.01,y,z)
 floor=loc*c.cz(4.17,c.LENGTH+1,c.LENGTH+3)
 row={'station':n,'axis_yz_mm':[y,z],'screw_cover_overlap_mm3':measure(f'cover-screw-{n}',cover.intersect(d['screws'][n])),'screw_block_overlap_mm3':measure(f'block-screw-{n}',block.intersect(d['screws'][n])),'female_material_missing_mm3':measure(f'female-{n}',d['coupons'][n].cut(block)),'floor_missing_mm3':measure(f'floor-{n}',floor.cut(block)),'seat_missing_mm3':measure(f'seat-{n}',seat.cut(cover)),'access_envelope_blocked_mm3':measure(f'access-{n}',d['fullpockets'][n].intersect(cover))}
 rows.append(row);print(row,flush=True)
 for label,shape in [('head-cover',cover.intersect(d['screws'][n])),('access-cover',d['fullpockets'][n].intersect(cover))]:
  if shape is not None and shape.solids():b.export_step(c.norm(shape),OUT/f'{label}-{n}.step')
panrows=[]
for n,g in d['pan_guards'].items():panrows.append({'station':n,'added_mm3':measure(f'panadd-{n}',c.norm(cover.intersect(g)).cut(c.norm(d['oldcover'].intersect(g)))),'removed_mm3':measure(f'panremoved-{n}',c.norm(d['oldcover'].intersect(g)).cut(c.norm(cover.intersect(g))))})
paths=[c.BLOCK,c.COVER,Path(c.__file__),Path(__file__)]
r={'status':'SCOPED comparison trial; no integration','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'validity':valid,'stations':rows,'protected_pan_sockets':panrows,'measurement_errors':errors,'artifacts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in OUT.glob('*.step')},'not_run':['full assembly neighbors and wet/core locality pending initial head/tool feasibility','GLB/render pending initial feasibility','exact1994 BOM, strength, torque, browser and installation'],'assumptions':{'seat_x_mm':c.SEAT,'nominal_comparison_length_mm':c.LENGTH,'head_radius_height_estimate_mm':[c.HEAD_RADIUS,c.HEAD_HEIGHT],'source_application':'Ford1986 4.9 comparison;1994 transfer unverified'}}
r['initial_gates']={'cad':all(v['valid']and v['solids']==1 for v in valid.values()),'joint_and_access':all(v is not None and v<1e-5 for row in rows for k,v in row.items()if k.endswith('mm3')),'pan_socket_preserved':all(v is not None and v<1e-5 for row in panrows for k,v in row.items()if k.endswith('mm3'))};r['local_status']='PASS initial gates only'if all(r['initial_gates'].values())else'FAIL initial gates'
(ROOT/'inventory/engine/timing-cover-seven-fastener-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['initial_gates'],flush=True)
