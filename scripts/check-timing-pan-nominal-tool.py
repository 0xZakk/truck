"""Separate manufacturer-nominal socket envelope, not a relaxed prior test."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
from timing_cover_attachment_v2 import RELOCATIONS,cz,norm
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'reference/engine/tekton-shd03013-access-review.json'
spec=json.loads(ledger.read_text())['nominal_mm'];radius=spec['outside_diameter']/2
panpath=ROOT/'cad/engine/generated/timing-pan-access-candidate/pan.step'
if not panpath.exists():
 print(list(panpath.parent.glob('*.step')));raise FileNotFoundError(panpath)
pan=norm(b.import_step(panpath));rows=[]
for n,p in RELOCATIONS.items():
 # Head top/washer underside are localZ0. Old estimate overran this by1.6.
 # Solid containing cylinder deliberately includes the hex void; checked only
 # against pan, never against the fastener it is intended to surround.
 envelope=b.Pos(*p)*cz(radius,-90-spec['overall_length'],0)
 common=envelope.intersect(pan);volume=None;error=None
 try:volume=sum(abs(solid_volume(s,'adaptive')) for s in common.solids()) if common else 0.
 except Exception as exc:error=str(exc)
 row={'station':n,'pan_distance_mm':envelope.distance_to(pan),'overlap_mm3':volume,'volume_error':error};rows.append(row);print(row,flush=True)
inputs={str(p.relative_to(ROOT)):sha(p)for p in [Path(__file__),ledger,panpath,ROOT/'cad/engine/timing_cover_attachment_v2.py']}
r={'scope':'Nominal Tekton SHD03013 containing cylinder through90mm axial approach; no ratchet/vehicle access proof','source':str(ledger.relative_to(ROOT)),'radius_mm':radius,'socket_length_mm':spec['overall_length'],'mouth_local_z_mm':0,'approach_mm':90,'results':rows,'inputs':inputs,'prior_R11_result':'Preserved unchanged; different estimated diameter and washer-overrun placement','status':'PASS nominal pan-only envelope' if all(x['overlap_mm3'] is not None and x['overlap_mm3']<.1 and x['pan_distance_mm']>0 for x in rows) else 'FAIL or unresolved nominal access','installed':False}
(ROOT/'inventory/engine/timing-pan-nominal-tool-validation.json').write_text(json.dumps(r,indent=2)+'\n')
