"""Independent frozen seven-screw block material and protected-interface checks."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_cover_seven_fastener_candidate as c
import timing_block_axis_feature_candidate as masks
import timing_block_support_machining_candidate as journals
import water_pump_joint_candidate as pump
import cam_retention as retention
import timing_cover_attachment_v2 as ownership
from oil_pan_joint_v9_candidate import STATIONS
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-seven-block-guard-study';OUT.mkdir(exist_ok=True)
newpath=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step';old=b.import_step(c.BLOCK);q=b.import_step(newpath);paths=[c.BLOCK,newpath,Path(c.__file__),Path(__file__)];errors={};r={'scope':'Frozen comparison block, no geometry mutations','guards':[],'measurement_errors':errors}
def norm(s):return c.norm(s)
def cut(s,d):return None if s is None else norm(s.cut(d))
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 v=0.
 for t in s.solids():
  for eps in [1e-9,1e-11,1e-13]:
   prop=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,prop,eps,True,False)
   if e<=1e-7:v+=abs(prop.Mass());break
  else:raise ValueError(f'Strict integration failed: {e}')
 return v
def m(k,s):
 try:return vol(s)
 except Exception as e:errors[k]=repr(e);return None
def save():
 r['input_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths};(ROOT/'inventory/engine/timing-seven-block-guard-study.json').write_text(json.dumps(r,indent=2)+'\n')
print('material difference',flush=True);added=norm(q.cut(old));removed=norm(old.cut(q));supports=[c.front.c.cx(c.SUPPORT_RADIUS,c.SUPPORT_BACK,373,y,z)for y,z in c.AXES];outside_a=added;outside_r=removed
for s in supports:outside_a=cut(outside_a,s);outside_r=cut(outside_r,s)
r['material']={'added_mm3':m('added',added),'removed_mm3':m('removed',removed),'added_outside_declared_support_mm3':m('outsideadded',outside_a),'removed_outside_declared_support_mm3':m('outsideremoved',outside_r)};save();print(r['material'],flush=True)
guards,spec=masks.protected_masks();guards={k:v for k,v in guards.items()if not k.startswith('pan-socket-') and k not in ['pan-front-end-land']}
for i,s in journals.backing_shells().items():guards[f'cam-bearing-backing-{i}']=s
for i,p in enumerate(STATIONS,1):
 p=ownership.RELOCATIONS.get(i,p)
 if i in[21,22,23]:continue
 guards[f'active-pan-interface-{i}']=b.Pos(p[0],p[1])*ownership.cz(12,p[2]+7.6,p[2]+25)
for i,(y,z)in enumerate(pump.MOUNTING,1):guards[f'pump-actual-mount-{i}']=pump.cx(10,350,373,y-32,z+170)
guards['pump-chamber-wall']=pump.cx(61,357.5,376,-32,170);guards['pump-fifth-passage-wall']=pump.cx(8.5,357.5,376,pump.EXTRA[0]-32,pump.EXTRA[1]+170)
guards['pump-fluid-chamber']=pump.cx(59,359.5,374,-32,170);guards['pump-fifth-fluid-opening']=pump.cx(6.5,359.5,374,pump.EXTRA[0]-32,pump.EXTRA[1]+170)
frame=b.Pos(*journals.DELTA)*retention.MOUNT;guards['cam-thrust-seat-backing']=frame*(b.Pos(0,0,-2)*retention.plate_shape())
for i,x in enumerate(retention.BOLT_STATIONS,1):guards[f'cam-thrust-socket-wall-{i}']=frame*(b.Pos(x,0,-6)*b.Cylinder(6.05,12.2))
guards['deck244-254']=b.Pos(0,0,249)*b.Box(1500,1000,10)
for i in[0,1]:
 p=ROOT/f'cad/engine/generated/timing-pump-foot-faceted-candidate/support-{i}.step';paths.append(p);guards[f'faceted-pump-foot-{i}']=b.import_step(p)
for name,g in guards.items():
 row={'name':name,'added_mm3':m(name+'added',None if added is None else added.intersect(g)),'removed_mm3':m(name+'removed',None if removed is None else removed.intersect(g))};row['unchanged']=row['added_mm3']is not None and row['removed_mm3']is not None and row['added_mm3']+row['removed_mm3']<1e-5;r['guards'].append(row)
 if not row['unchanged']:
  print('GUARD',row,flush=True)
  for label,s in [('added',added),('removed',removed)]:
   witness=None if s is None else s.intersect(g)
   if witness is not None and witness.solids():b.export_step(norm(witness),OUT/f'{name}-{label}.step')
 save()
print('source female and blind enclosure',flush=True);male=c.male();coupon=c.one(c.cz(4.17,c.SEAT-373,c.SEAT-c.HOLE_BACK).cut(c.one(male.fuse(c.cz(4.,c.LENGTH-.1,c.LENGTH+1)))));cavity=norm(c.cz(4.17,c.SEAT-373,c.SEAT-c.HOLE_BACK).cut(coupon));rows=[];outside_void=removed
for n,(y,z)in enumerate(c.AXES,1):
 loc=c.frame(y,z);female=loc*coupon;void=loc*cavity;outside_void=cut(outside_void,void);wall=loc*(c.cz(6.2,c.SEAT-373,c.LENGTH+3)-c.cz(4.17,c.SEAT-373-.1,c.LENGTH+3.1));floor=loc*c.cz(4.17,c.LENGTH+1,c.LENGTH+3)
 row={'station':n,'female_missing':m(f'female{n}',female.cut(q)),'cavity_filled':m(f'void{n}',q.intersect(void)),'wall_missing':m(f'wall{n}',wall.cut(q)),'floor_missing':m(f'floor{n}',floor.cut(q))};rows.append(row);print(row,flush=True)
r['sockets']=rows;r['removed_outside_analytic_cavities_mm3']=m('outsidevoid',outside_void);r['valid_single_solid']=q.is_valid and len(q.solids())==1
for mod in list(sys.modules.values()):
 p=Path(getattr(mod,'__file__','')or'')
 if p.is_file()and p.is_relative_to(ROOT/'cad/engine')and p.suffix=='.py':paths.append(p)
r['gates']={'material_locality':r['material']['added_outside_declared_support_mm3']==0 and r['removed_outside_analytic_cavities_mm3']==0,'all_declared_guards_unchanged':all(x['unchanged']for x in r['guards']),'source_female_blind_wall_floor':all(v is not None and v<1e-5 for row in rows for k,v in row.items()if k!='station'),'material_metrics_verified':not errors,'valid':r['valid_single_solid']};r['status']='PASS bounded guards'if all(r['gates'].values())else'FAIL or NOT VERIFIED bounded guards';save();print(r['status'],r['gates'],flush=True)
