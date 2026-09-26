"""Seat, dry-bore, adapter idempotence and deliberate displacement controls."""
import hashlib,json,sys
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_carrier_1994 as c
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);defs={d['id']:d for d in m['definitions']};source=Path(c.__file__).read_bytes();parts=c.parts();results=[]
def volume(shape):return sum(s.volume for s in shape.solids()) if shape else 0
for i,(x,z) in enumerate(c.BLOCK_STATIONS,1):
 washer=parts[f'carrier-block-washer-{i}'];nut=parts[f'carrier-block-nut-{i}'];carrier=parts['ps-ac-support-bracket']
 d1=carrier.distance_to(washer);d2=washer.distance_to(nut)
 assert d1<1e-6 and d2<1e-6,(i,d1,d2)
 penetrated=carrier.intersect(cad.Pos(0,-.2,0)*washer);assert volume(penetrated)>.01
 withdrawn=carrier.distance_to(cad.Pos(0,2,0)*washer);assert withdrawn>.1
 results.append({'station':i,'washer_carrier_distance_mm':d1,'nut_washer_distance_mm':d2,'deliberate_0_2mm_penetration_volume_mm3':volume(penetrated),'deliberate_2mm_withdrawal_gap_mm':withdrawn})
for identifier,adapter,stations,zshift in [('block',c.block_interface,c.BLOCK_STATIONS,0),('cylinder-head',c.head_interface,[c.HEAD_SIDE],255.5)]:
 old=cad.import_step(ROOT/defs[identifier]['step'].lstrip('/'));new=adapter(old);twice=adapter(new)
 assert abs(new.volume-twice.volume)<.01
 for x,z in stations:
  # A cavity probe terminates0.5mm shy of the modeled bore floor. The floor
  # probe lies wholly behind it in the external dry boss, not at a boundary.
  void=c.sideways(4.8,23,x,123,z-zshift);floor=c.sideways(4.8,2,x,109,z-zshift)
  assert volume(new.intersect(void))<.01,(identifier,'bore obstructed')
  assert abs(volume(new.intersect(floor))-floor.volume)<.01,(identifier,'floor open')
  results.append({'part':identifier,'station_x_mm':x,'void_probe_volume_mm3':void.volume,'solid_floor_probe_volume_mm3':floor.volume,'adapter_twice_volume_delta_mm3':abs(new.volume-twice.volume)})
assert (ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw
assert Path(c.__file__).read_bytes()==source
report={'passed':True,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'candidate_source_sha256':hashlib.sha256(source).hexdigest(),'results':results,'limits':'These checks validate provisional CAD seats and blind-bore construction, not thread geometry, tightening requirements or factory dimensions.'}
(ROOT/'inventory/engine/accessory-carrier-1994-joint-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
