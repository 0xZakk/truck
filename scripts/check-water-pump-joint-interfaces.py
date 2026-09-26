"""Pump joint sealing boundary/retained cylinder/dry socket controls."""
from pathlib import Path
import sys,hashlib,json
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_joint_candidate as p
import water_pump_thermactor_foot_candidate as t
from cad_metrics import solid_volume
paths=[Path(__file__),Path(p.__file__),Path(t.__file__),ROOT/'cad/engine/generated/block.step',ROOT/'cad/engine/generated/water-pump-housing.step']
hashes={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths}
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
old=b.import_step(ROOT/'cad/engine/generated/block.step');block=p.block_interface(t.block_interface(old));frame=b.Pos(*p.PUMP_POSITION)
housing=frame*p.housing_interface(b.import_step(ROOT/'cad/engine/generated/water-pump-housing.step'));gasket=frame*p.gasket_shape()
# Entire cylinder1wall and bore remain unchanged, not simply a central probe.
zone=b.Pos(284.48,0,170)*b.Box(116,122,210);a=old&zone;c=block&zone
retained=vol(a-c)+vol(c-a);assert retained<.02,retained
# Translate the2mm gasket into each mating surface to measure complete support.
gv=vol(gasket);supported={}
for role,shape,dx in [('block',block,-2),('pump',housing,2)]:
 material=vol(shape&(b.Pos(dx,0,0)*gasket));supported[role]={'gasket_mm3':gv,'supported_mm3':material}
 assert abs(material-gv)<.02,(role,material,gv)
# Main and fifth front apertures open through the face without manufacturing
# a whole-jacket model. Probes only certify these local boundaries.
probes=[]
for y,z,r in [(-32,170,5),(p.EXTRA[0]-32,p.EXTRA[1]+170,3)]:
 v=vol(block&p.cx(r,360,374,y,z));assert v<1e-6,v;probes.append(v)
seats=[]
for y,z in p.MOUNTING:
 y-=32;z+=170
 open_v=vol(block&p.cx(3.9,356.01,374,y,z));assert open_v<1e-6,open_v
 floor=p.cx(3.9,354,355,y,z);floor_v=vol(block&floor);assert abs(floor_v-floor.volume)<1e-6,floor_v
 seats.append({'open_socket_mm3':open_v,'retained_floor_mm3':floor_v})
# New accessory foot socket is dry and blind, and former socket is closed
# except for any material intentionally cut by the new pump flange interfaces.
y,z=t.UPPER
q=p.cx(4.9,357.01,374,y,z);assert vol(block&q)<1e-6
floor=p.cx(4.9,355,356,y,z);assert abs(vol(block&floor)-floor.volume)<1e-6
assert all(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h for q,h in hashes.items())
result={'input_hashes':hashes,'inputs_unchanged':True,'cylinder1_region_difference_mm3':retained,'full_gasket_support':supported,'front_aperture_probes_mm3':probes,'four_mounting_socket_controls':seats,'new_accessory_dry_socket_pass':True,'scope':'Local joint boundaries and cylinder preservation only; deeper coolant jacket, pressure sealing, actual aperture function and manufacturing dimensions remain unverified.'}
(ROOT/'inventory/engine/water-pump-joint-interfaces-validation.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS pump local joint boundary controls')
