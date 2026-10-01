"""Saved candidate contact, locality, dry/wet and mesh checks; no regeneration."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_pan21_lateral_candidate as c
from oil_pan_joint_v9_candidate import STATIONS
OUT=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate';paths=[OUT/(n+'.step')for n in ['cover','pan','pan-gasket']];cover,pan,gasket=[b.import_step(p)for p in paths];errors={}
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 v=0.
 for t in s.solids():
  for eps in [1e-9,1e-11,1e-13]:
   q=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,q,eps,True,False)
   if e<=1e-7:v+=abs(q.Mass());break
  else:raise ValueError(e)
 return v
def cut(s,d):return s if s is None else c.norm(s.cut(d))
def m(k,s):
 try:return vol(s)
 except Exception as e:errors[k]=repr(e);return None
def box(a,d):return b.Pos(*((np.array(a)+d)/2))*b.Box(*(np.array(d)-a))
def tube(a,d,r):
 delta=b.Vector(d)-b.Vector(a);return b.Solid.make_cylinder(r,delta.length,b.Plane(origin=a,z_dir=delta))
male=b.import_step(c.MALE);washer=b.import_step(c.WASHER);paths +=[c.MALE,c.WASHER];rows=[];positions={n:p for n,p in enumerate(STATIONS,1)};positions.update(c.owner.RELOCATIONS);positions[21]=c.NEW
for n,p in positions.items():
 loc=b.Pos(*p);seat=loc*(c.owner.cz(7.5,1.6,1.62)-c.owner.cz(4.3,1,2));gp=loc*(c.owner.cz(7.5,5.6,5.62)-c.owner.cz(4.3,5,6))
 row={'station':n,'position_mm':p,'male_pan':m(str(n)+'male',pan.intersect(loc*male)),'washer_pan':m(str(n)+'washer',pan.intersect(loc*washer)),'pan_seat_missing':m(str(n)+'seat',seat.cut(pan)),'gasket_seat_missing':m(str(n)+'gasket',gp.cut(gasket))};rows.append(row);print(row,flush=True)
print('locality',flush=True);locality={};masks={}
for n,p in [('cover',c.COVER),('pan',c.PAN),('pan-gasket',c.GASKET)]:
 q={'cover':cover,'pan':pan,'pan-gasket':gasket}[n];old=b.import_step(p);paths.append(p)
 if n=='cover':mask=c.norm(c.stock(c.OLD).fuse(c.stock(c.NEW),c.main.front.c.cx(c.main.ACCESS_RADIUS,c.main.SEAT,435,*c.main.AXES[0])))
 else:mask=c.norm((b.Pos(c.OLD[0],c.OLD[1])*c.owner.cz(4.31,-31,-24)).fuse(b.Pos(c.NEW[0],c.NEW[1])*c.owner.cz(4.31,-31,-24)))
 masks[n]=mask;locality[n]={'added_outside':m(n+'addout',cut(cut(q,old),mask)),'removed_outside':m(n+'remout',cut(cut(old,q),mask))}
print('witnesses',flush=True);loc=b.Pos(*c.NEW);washerseat=loc*(c.owner.cz(7.5,1.6,1.62)-c.owner.cz(4.3,1,2));top=loc*(c.owner.cz(10,7.6,7.62)-c.owner.cz(4.3,7,8));bottom=loc*(c.owner.cz(10,5.58,5.6)-c.owner.cz(4.3,5,6))
contact={'new_upper_gasket_backing_missing':m('top',top.cut(cover)),'new_lower_gasket_backing_missing':m('bottom',bottom.cut(pan)),'male_washer_distance_mm':(loc*male).distance_to(loc*washer),'washer_pan_distance_mm':(loc*washer).distance_to(pan)}
tool=loc*c.owner.cz(17.526/2,-138.26,0);start=(390,-95,-34.85);end=(370,-95,-34.85);dry=tube(start,end,.25);bad=c.norm(pan.cut(box((373,-96,-36),(379,-94,-33))))
wet={'nominal_pan_tool_overlap':m('tool',tool.intersect(pan)),'dry_to_wet_wall_obstruction':m('drywall',dry.intersect(pan)),'breached_wall_negative_control_obstruction':m('breach',dry.intersect(bad)),'head_point_inside_pan_material':pan.is_inside(start,tolerance=1e-7),'cavity_bypass':[]}
for a,d in [((390,-80,-11),(390,-70,0)),((390,-70,0),(390,-50,20)),((370,0,-70),(350,0,-70)),((350,0,-70),(350,0,-82)),((350,0,-82),(330,0,-90))]:
 path=tube(a,d,.5);block=box(tuple(np.array(a)-1),tuple(np.array(a)+1));wet['cavity_bypass'].append({'a':a,'b':d,'cover_obstruction':m('wetcover'+str(a),path.intersect(cover)),'pan_obstruction':m('wetpan'+str(a),path.intersect(pan)),'blocked_negative_control':m('wetcontrol'+str(a),path.intersect(block))})
print('mesh',flush=True);meshes={}
for n,s in [('cover',cover),('pan',pan),('pan-gasket',gasket)]:
 v,f=s.tessellate(.08,.12);mesh=trimesh.Trimesh(np.array([tuple(q)for q in v]),np.array(f));mesh.merge_vertices(digits_vertex=6);np.savez_compressed(OUT/(n+'-preview.npz'),vertices=mesh.vertices,faces=mesh.faces);meshes[n]={'watertight':mesh.is_watertight,'winding_consistent':mesh.is_winding_consistent,'components':len(mesh.split(only_watertight=False)),'signed_volume_mm3':float(mesh.volume),'euler_number':mesh.euler_number,'cad_bounds_error_mm':float(np.max(np.abs(mesh.bounds-np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)]))))}
 if mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0:trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces).export(OUT/(n+'.glb'))
r={'hardware25':rows,'bom':{'pan_screws':len(positions),'pan_washers':len(positions),'unique_axes':len(set(positions.values())),'changed_station_ids':[21],'main_cover_screws':7},'locality':locality,'contact':contact,'wet_dry_witnesses':wet,'meshes':meshes,'errors':errors,'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(__file__),Path(c.__file__)]},'limits':['Finite positive-radius connectivity witnesses do not establish whole oil containment','Inherited rear gasket support gap unchanged; full joint acceptance remains open','Nominal matched threads and estimated boss, no strength/factory claim','Actual moving-core neighbors reported separately']}
(ROOT/'inventory/engine/timing-pan21-lateral-interfaces.json').write_text(json.dumps(r,indent=2)+'\n');print('wrote',flush=True)
