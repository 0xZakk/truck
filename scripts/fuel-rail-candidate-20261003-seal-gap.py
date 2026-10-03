from pathlib import Path
import build123d as b,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r4';r={}
ids=['fuel-supply-rail','fuel-return-tube','regulator-lower-housing','regulator-upper-housing','regulator-diaphragm','regulator-gasket','regulator-inlet-screen','regulator-valve-seat','regulator-valve','regulator-o-ring']
for label,sign in [('plus',1),('minus',-1)]:
 gx=174.136;gy=-163+24*sign;probe=b.Pos(gx+4.525,gy,(377.3+386.6)/2)*b.Cylinder(.005,386.6-377.3);hits={}
 for ident in ids:
  s=b.import_step(OUT/label/(ident+'.step'));hit=s&probe;hits[ident]=sum(abs(a.volume) for a in hit.solids()) if hit else 0
 r[label]={'probe_center_x_offset_mm':4.525,'probe_radius_mm':.005,'z_interval_mm':[377.3,386.6],'intersections_mm3':hits,'open_external_path':sum(hits.values())<1e-9,'scope':'Geometric gap only. No elastomer compression/seal model; no real leak rate.'};print(label,r[label],flush=True)
(OUT/'seal-gap.json').write_text(json.dumps(r,indent=2)+'\n')
