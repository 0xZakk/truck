"""Root saved STEP witness for screw revision; no worker builder imported."""
from pathlib import Path
import json,hashlib
import build123d as b
R=Path(__file__).resolve().parents[1];P=R/'cad/engine/generated/fuel-rail-candidate-20261003-r8';old=R/'cad/engine/generated/fuel-rail-candidate-20261003-r7/plus'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((R/'reference/engine/fuel-rail-candidate-20261003-review-r8.json').read_text())
for p,h in review['hashes'].items():assert sha(R/p)==h,p
rail=b.import_step(P/'plus/fuel-supply-rail.step')
def vol(q):
 if isinstance(q,b.ShapeList):return sum(vol(x) for x in q)
 return abs(q.volume) if q and q.solids() else 0.
rows=[]
for i in range(1,4):
 p=P/f'plus/regulator-screw-{i}.step';s=b.import_step(p);bb=s.bounding_box();v=vol(s.intersect(rail));assert s.is_valid and len(s.solids())==1 and v<.1;assert abs(bb.min.Z-378)<1e-6 and abs(bb.max.Z-388)<1e-6
 rows.append({'id':f'regulator-screw-{i}','sha256':sha(p),'rail_overlap_mm3':v,'min_z':bb.min.Z,'max_z':bb.max.Z})
prior=b.import_step(old/'regulator-screw-3.step');v=vol(prior.intersect(rail));assert v>.1
out={'status':'PASS saved screw bounds/rail clearance witness','rows':rows,'previous_screw_negative_mm3':v,'rail_sha256':sha(P/'plus/fuel-supply-rail.step'),'actual_visual':'Reviewed actual-screw.png: complete estimated shank/head and hex recess; threads absent.','limits':['Estimated8mm length; factory length/thread engagement unknown.','Three other fullcontext conflicts remain.','Not installed acceptance.']}
(R/'reference/engine/fuel-rail-candidate-20261003-root-screw-r8.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
