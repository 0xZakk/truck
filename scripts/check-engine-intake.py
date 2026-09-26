"""Check saved intake solids have open mating ports, not merely hollow-looking skins."""
from pathlib import Path
import json
import hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
ids=['efi-upper-intake','efi-lower-intake','efi-upper-intake-gasket','efi-head-intake-gasket']
shapes={id:b.import_step(ROOT/'cad/engine/generated'/f'{id}.step') for id in ids}
head=b.import_step(ROOT/'cad/engine/generated/cylinder-head.step').moved(b.Location((0,0,255.5)))
checks=[]
def clear(label,probe,targets):
    for id,shape in targets.items():
        overlap=shape.intersect(probe)
        volume=sum(s.volume for s in overlap.solids()) if overlap else 0
        assert volume<.01,(label,id,volume)
    checks.append(label)
for i in range(6):
    x=(2.5-i)*m['mechanism']['bore_pitch_mm']
    clear(f'Cylinder {i+1}: upper/lower joint',b.Pos(x,-228,361)*b.Cylinder(2,24),shapes)
    clear(f'Cylinder {i+1}: head joint',b.Pos(x-25,-134,277.5)*b.Rot(90,0,0)*b.Cylinder(2,24),{'head':head,'lower':shapes['efi-lower-intake'],'gasket':shapes['efi-head-intake-gasket']})
    clear(f'Cylinder {i+1}: runner/plenum opening',b.Pos(x,-30,490)*b.Rot(90,0,0)*b.Cylinder(2,20),{'upper':shapes['efi-upper-intake']})
report={'status':'pass','manifest_sha256':hashlib.sha256((ROOT/'inventory/engine/full-assembly.json').read_bytes()).hexdigest(),'checked_open_interfaces':checks,'scope':'Small clearance probes at modeled mating interfaces only; not a flow simulation or OEM geometry verification.'}
(ROOT/'inventory/engine/intake-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{len(checks)} intake mating-interface probes passed.')
