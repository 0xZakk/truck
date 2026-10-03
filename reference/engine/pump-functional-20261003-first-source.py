"""Uninstalled functional-region pump hypothesis. WORLD mm."""
import json
import build123d as b
import pump_height_20261002_core_trial3 as core
import pump_height_20261002_ports_trial3 as old_ports
from water_pump_joint_candidate import MOUNTING, EXTRA
from assembly_clockwise_candidate import transforms
R=core.R
O=R/'cad/engine/generated/pump-functional-20261003'
HEIGHT=98.43
cx=core.cx
norm=core.norm
DIR=old_ports.DIR
datums=old_ports.datums
sweep=old_ports.sweep
segment=old_ports.segment
def world(n):
 m=json.loads(core.MP.read_text());d={x['id']:x for x in m['definitions']};o=next(x for x in m['occurrences']if x['id']==n)
 return transforms(m,0,0)[n]*b.import_step(R/d[o['definition']]['step'].lstrip('/'))
def functional_regions():
 gasket=world('water-pump-gasket')
 faces=[f for f in gasket.faces()if abs(f.center().X-375)<1e-5 and abs(f.bounding_box().size.X)<1e-5]
 face=b.Compound(faces)
 backing=norm(b.Compound([b.Solid.extrude(f,(3,0,0))for f in faces]))
 regions={'seal_land_face':face,'seal_backing':backing}
 for i,(y,z)in enumerate(MOUNTING,1):
  regions[f'dry_boss_{i}']=b.Pos(0,y,z)*(cx(11.5,375,389)-cx(4.3,374,390))
  regions[f'dry_bore_{i}']=b.Pos(0,y,z)*cx(4.3,375,389)
  regions[f'bolt_seat_{i}']=b.Compound([f for f in regions[f'dry_boss_{i}'].faces()if abs(f.center().X-389)<1e-5])
 regions['fifth_aperture']=b.Pos(0,*EXTRA)*cx(6.5,375,389)
 return regions
def inlet(inside=False,probe=False):
 if probe:dims=[(35,397,1,1),(60,403,1,1),(96,403,1,1),(146,403,1,1)]
 elif inside:dims=[(35,397,7,21),(60,403,20,20),(96,403,20,20),(146,403,20,20)]
 else:dims=[(40,397,10,25),(60,403,24,25),(96,403,24,24),(145,403,24,24)]
 out=b.loft([old_ports.section(y,x,rx,rz)for y,x,rx,rz in dims],ruled=True)
 if not inside and not probe:out=out.fuse(b.Solid.make_cylinder(25.5,3,b.Plane(origin=(403,140,6),z_dir=(0,1,0))))
 return b.Pos(0,-32,170)*b.Rot(-130,0,0)*out
def parts(height=HEIGHT):
 out,inputs=core.parts(height);regions=functional_regions();root,end,crest,ed=datums(height)
 h=out['water-pump-housing'].fuse(inlet(),segment(12,root-42*DIR,root),regions['seal_backing'])
 for i in range(1,5):h=h.fuse(regions[f'dry_boss_{i}'])
 h=h.cut(inlet(True),segment(6.5,root-46*DIR,root+DIR),segment(8,root-12*DIR,root+DIR))
 h=h.cut(cx(24,375+height-64,513+height-147))
 inner=b.loft([core.section(x,r)for x,r in[(374,59),(383,59),(389,51),(375+height-64,24),(375+height-55,24)]],ruled=True)
 h=h.cut(inner)
 for i in range(1,5):h=h.cut(regions[f'dry_bore_{i}'])
 h=h.cut(regions['fifth_aperture'])
 out['water-pump-housing']=norm(h)
 out['heater-pump-return-elbow']=norm((sweep(8,height)+segment(8.5,end-5*ed,end-3*ed))-sweep(6.5,height))
 return out,inputs,regions
