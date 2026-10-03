"""Source-led optionB trial. WORLDmm, no shared writes or neighbor-derived masks."""
from pathlib import Path
import json,math,hashlib
import build123d as b
import pump_functional_20261003 as old
from assembly_clockwise_candidate import transforms
R=Path(__file__).resolve().parents[2];O=R/'cad/engine/generated/pump-cover-candidate-20261003'
MP=R/'inventory/engine/corrected-engine-stage-v4.json'
D=json.loads((R/'reference/engine/pump-cover-joint-20261003-datums.json').read_text())['options'][1]
G=D['global_scale_relative_pump_rectification'];Y,Z=D['pump_center_yz_mm'];ANGLE=D['pump_clock_delta_deg'];HEIGHT=98.43
T=b.Pos(0,Y,Z)*b.Rot(ANGLE,0,0)*b.Pos(0,32,-170)
MOUNTING=old.MOUNTING;EXTRA=old.EXTRA
norm=old.norm;cx=old.cx
PUMP_AXIS=(Y,Z)
def original(n):return old.world(n)
def frozen(n):
 j=json.loads((R/'reference/engine/pump-functional-20261003-build.json').read_text());p=R/j['parts'][n]['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==j['parts'][n]['sha256'];return b.import_step(p)
def point(p):return T*b.Vector(*p)
def cylinder(r,a,z,y=0,zz=0):return b.Pos(0,y,zz)*cx(r,a,z)
def inlet(inside=False,probe=False):
 if probe:dims=[(35,397,1,1),(60,403,1,1),(96,403,1,1),(146,403,1,1)]
 elif inside:dims=[(35,397,7,21),(60,403,20,20),(96,403,20,20),(146,403,20,20)]
 else:dims=[(40,397,10,25),(60,403,24,25),(96,403,24,24),(145,403,24,24)]
 # Transverse footprint scales; X-depth and hardware do not. Last rim remains
 # estimated cast neck, not a newly sourced hose specification.
 profiles=[b.Plane(origin=(x,y*G,6*G),x_dir=(1,0,0),z_dir=(0,1,0))*b.Ellipse(rx,rz*G)for y,x,rx,rz in dims]
 out=b.loft(profiles,ruled=True)
 if not inside and not probe:
  rim=b.Plane(origin=(403,140*G,6*G),x_dir=(1,0,0),z_dir=(0,1,0))*b.Ellipse(25.5,25.5*G)
  out=out.fuse(b.extrude(rim,amount=3*G))
 return b.Pos(0,-32,170)*b.Rot(-130,0,0)*out

def gasket_oldframe():
 q=cx(65*G,373,375)
 for y,z in MOUNTING:q=q.fuse(cylinder(9.5*G,373,375,y*G,z*G))
 q=q.fuse(cylinder(11.5*G,373,375,EXTRA[0]*G,EXTRA[1]*G)).cut(cx(59*G,372,376))
 for y,z in MOUNTING:q=q.cut(cylinder(5.2,372,376,y*G,z*G))
 return norm(q.cut(cylinder(6.5,372,376,EXTRA[0]*G,EXTRA[1]*G)))

def regions_oldframe(gasket):
 faces=[f for f in gasket.faces()if abs(f.center().X-375)<1e-5 and f.bounding_box().size.X<1e-5]
 r={'seal_land_face':b.Compound(faces),'seal_backing':norm(b.Compound([b.Solid.extrude(f,(3,0,0))for f in faces]))}
 for i,(y,z)in enumerate(MOUNTING,1):
  r[f'dry_boss_{i}']=norm(cylinder(11.5,375,389,y*G,z*G).cut(cylinder(4.3,374,390,y*G,z*G)))
  r[f'dry_bore_{i}']=cylinder(4.3,375,389,y*G,z*G)
  r[f'bolt_seat_{i}']=b.Compound([f for f in r[f'dry_boss_{i}'].faces()if abs(f.center().X-389)<1e-5])
 r['fifth_aperture']=cylinder(6.5,375,389,EXTRA[0]*G,EXTRA[1]*G)
 return r

def housing(gasket,regions):
 # Original frontbearing nose preserves all measured-by-model fitted dimensions.
 front=norm(frozen('water-pump-housing').intersect(cx(29.01,409.43,464)))
 outer=b.loft([old.core.section(x,r)for x,r in [(375,66*G),(383,66*G),(389,55*G),(409.43,29)]],ruled=True)
 inner=b.loft([old.core.section(x,r)for x,r in [(374,59*G),(383,59*G),(389,51),(409.43,24),(418.43,24)]],ruled=True)
 root,end,crest,ed=old.datums(HEIGHT)
 h=norm(outer.fuse(front).cut(inner))
 # Equivalent sequential set operations avoid the trial1 four-face junction.
 port=norm(inlet().cut(inlet(True)));port=norm(port.cut(inner))
 h=norm(h.fuse(port,old.segment(12,root-42*old.DIR,root),regions['seal_backing']))
 for tool in [inlet(True),old.segment(6.5,root-46*old.DIR,root+old.DIR),old.segment(8,root-12*old.DIR,root+old.DIR),cx(24,409.43,464.43)]:h=norm(h.cut(tool))
 y,z=EXTRA[0]*G,EXTRA[1]*G
 h=norm(h.fuse(cylinder(11.5*G,375,394,y,z)))
 # Declared short radial fifth passage remains an unidentified illustrative route.
 h=norm(h.cut(b.Solid.make_cylinder(6.5,math.hypot(.25*y,.25*z),b.Plane(origin=(386,y-32,z+170),z_dir=(0,-y,-z)))))
 for i in range(1,5):h=norm(h.fuse(regions[f'dry_boss_{i}']))
 for i in range(1,5):h=norm(h.cut(regions[f'dry_bore_{i}']))
 h=norm(h.cut(regions['fifth_aperture']))
 for y,z in MOUNTING:h=norm(h.cut(cylinder(11.5,389,430,y*G,z*G)))
 return h

def pump_parts():
 j=json.loads((R/'reference/engine/pump-functional-20261003-build.json').read_text());out={}
 for n in j['parts']:
  if n!='water-pump-housing':out[n]=T*frozen(n)
 gasket=gasket_oldframe();regions=regions_oldframe(gasket);out['water-pump-housing']=T*housing(gasket,regions);out['water-pump-gasket']=T*gasket;out['water-pump-impeller']=T*original('water-pump-impeller')
 for i,(y,z)in enumerate(MOUNTING,1):out[f'water-pump-mounting-screw-{i}']=T*b.Pos(0,(G-1)*y,(G-1)*z)*original(f'water-pump-mounting-screw-{i}')
 return out,{n:T*s for n,s in regions.items()}

def block_parts():
 oldblock=original('block');fills=[cx(59,359.5,373),cylinder(6.5,359.5,373,*EXTRA)]
 for y,z in MOUNTING:fills.append(cylinder(4.3,356,373,y,z))
 q=norm(oldblock.fuse(*fills))
 # Positive new seating land is declared from the independent gasket footprint.
 ga=gasket_oldframe();rearfaces=[f for f in ga.faces()if abs(f.center().X-373)<1e-5 and f.bounding_box().size.X<1e-5]
 land=T*norm(b.Compound([b.Solid.extrude(f,(-13.5,0,0))for f in rearfaces]));supports=[T*cylinder(10,350,373,y*G,z*G)for y,z in MOUNTING]
 q=norm(q.fuse(land,*supports));voids={'chamber':T*cx(59*G,359.5,374),'fifth':T*cylinder(6.5,359.5,374,EXTRA[0]*G,EXTRA[1]*G)}
 for i,(y,z)in enumerate(MOUNTING,1):voids[f'socket_{i}']=T*cylinder(4.3,356,374,y*G,z*G)
 for v in voids.values():q=norm(q.cut(v))
 return q,{'old_block':oldblock,'retired_void_fills':b.Compound(fills),'new_land':land,**{f'new_support_{i}':v for i,v in enumerate(supports,1)},**{f'new_void_{n}':v for n,v in voids.items()}}
