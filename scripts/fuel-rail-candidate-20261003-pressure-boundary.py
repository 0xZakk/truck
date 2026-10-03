"""Probe actual retained housing gap; no enclosing test envelope hides external leak."""
from pathlib import Path
import build123d as b,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r4';r={}
ids=['fuel-supply-rail','fuel-return-tube','regulator-lower-housing','regulator-upper-housing','regulator-diaphragm','regulator-gasket','regulator-inlet-screen','regulator-valve-seat','regulator-valve','regulator-o-ring']
for label,sign in [('plus',1),('minus',-1)]:
 gx=174.136;gy=-163+24*sign;shapes={i:b.import_step(OUT/label/(i+'.step')) for i in ids}
 # Continuous cylindrical bore along radial +X, entirely below diaphragm and
 # above lower housing top. Test exact finite-volume intersection with solids.
 probe=b.Pos(gx+14.5,gy,388.5)*b.Rot(0,90,0)*b.Cylinder(.15,13)
 hits={}
 for i,s in shapes.items():
  hit=s&probe;hits[i]=sum(abs(a.volume) for a in hit.solids()) if hit else 0
 r[label]={'probe_start_mm':[gx+8,gy,388.5],'probe_end_mm':[gx+21,gy,388.5],'probe_radius_mm':.15,'probe_intersection_volumes_mm3':hits,'open_pressure_chamber_to_external_envelope':sum(hits.values())<1e-7,'status':'FAIL pressure enclosure' if sum(hits.values())<1e-7 else 'REVIEW','input_sha256':{i:hashlib.sha256((OUT/label/(i+'.step')).read_bytes()).hexdigest() for i in ids}}
 print(label,r[label],flush=True)
(OUT/'pressure-boundary.json').write_text(json.dumps(r,indent=2)+'\n')
