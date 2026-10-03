"""Check explicit diagnostic sealing bands; render the actual saved mesh."""
from pathlib import Path
import json,hashlib
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[1];NAME='intake-gasket-outline-20261003'
folder=ROOT/'cad/engine/generated'/NAME
sp=folder/'efi-upper-intake-gasket.step';gp=folder/'efi-upper-intake-gasket.glb'
g=b.import_step(sp);p=json.loads((ROOT/'cad/engine/intake-joint-candidate-20261003-parameters.json').read_text())
hosts={n:b.import_step(ROOT/'cad/engine/generated/intake-joint-candidate-20261003'/f'{n}.step') for n in ['efi-lower-intake','efi-upper-intake']}
rows=[]
for i,u in enumerate(p['port_stations']):
    x=284.48-568.96*u
    ring=b.Pos(x,-228)* (b.Circle(26.5)-b.Circle(25.5))
    checks={}
    for name,host,z in [('gasket',g,360.5),('efi-lower-intake',hosts['efi-lower-intake'],359.8),('efi-upper-intake',hosts['efi-upper-intake'],361.6)]:
        required=b.Pos(0,0,z)*b.extrude(ring,amount=.1)
        missing=required-host
        area=sum(s.volume for s in missing.solids())/.1
        checks[name]={'missing_area_mm2':area,'covered':area<.001}
    # Disturb only the required band: sensitivity to a displaced seal region.
    shifted=b.Pos(0,150,360.5)*b.extrude(ring,amount=.1)
    checks['shifted_band_control_rejected']=sum(s.volume for s in (shifted-g).solids())>.1
    rows.append({'port':i+1,'diagnostic_radial_band_mm':[25.5,26.5],'checks':checks})
m=trimesh.load(gp,force='mesh');v=m.vertices[:,[0,2,1]]*[1,-1,1]*1000
np.savez_compressed(folder/'review-data.npz',vertices=v,faces=m.faces)
report={'scope':'one-mm illustrative annular contact band, not manufacturer sealing requirement','bands':rows,'full_outline_support':'Prior full-footprint FAIL includes overhang; does not alone establish a leak. No automatic manifold growth permitted.','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [sp,gp,Path(__file__)]}}
for name in hosts:
 f=ROOT/'cad/engine/generated/intake-joint-candidate-20261003'/f'{name}.step';report['hashes'][str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
(ROOT/'reference/engine'/f'{NAME}-bands.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
