from pathlib import Path
import math,json,hashlib,build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepCheck import BRepCheck_Analyzer
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r5';r={}
annulus=math.pi*(19.8**2-17**2);edge=2*math.pi*19.8*.8;rim=math.pi*(20**2-19.8**2)
for label in ['plus','minus']:
 ids=['regulator-lower-housing','regulator-upper-housing','regulator-diaphragm'];shapes={i:b.import_step(OUT/label/(i+'.step')) for i in ids};rows={}
 for a,c,expected in [(ids[0],ids[2],annulus+edge),(ids[1],ids[2],annulus),(ids[0],ids[1],rim)]:
  op=BRepAlgoAPI_Common(shapes[a].wrapped,shapes[c].wrapped);op.Build();shape=b.Compound(op.Shape());volume=sum(abs(s.volume) for s in shape.solids());area=0;contact_faces=[]
  for fa in shapes[a].faces():
   for fc in shapes[c].faces():
    if fa.distance_to(fc)>1e-6:continue
    cop=BRepAlgoAPI_Common(fa.wrapped,fc.wrapped);cop.SetFuzzyValue(1e-7);cop.Build()
    if not cop.IsDone() or not BRepCheck_Analyzer(cop.Shape()).IsValid():raise RuntimeError('face common failed')
    ff=b.Compound(cop.Shape());aa=sum(f.area for f in ff.faces())
    if aa>1e-8:contact_faces.append(aa);area+=aa
  rows[a+'/'+c]={'valid':op.IsDone() and BRepCheck_Analyzer(op.Shape()).IsValid(),'method':'exact face-pair Common with1e-7mm kernel fuzzy tolerance; whole-solid Common yields no zero-volume faces','contact_face_areas_mm2':contact_faces,'contact_area_mm2':area,'expected_mm2':expected,'area_error_mm2':abs(area-expected),'overlap_mm3':volume,'pass':abs(area-expected)<1e-4 and volume<1e-7}
 shifted=b.Pos(0,0,.01)*shapes['regulator-upper-housing'];gap=shifted.distance_to(shapes['regulator-diaphragm'])
 r[label]={'shifted_upper_negative':{'displacement_mm':.01,'actual_min_distance_mm':gap,'detected':gap>1e-6},'contacts':rows,'input_sha256':{i:hashlib.sha256((OUT/label/(i+'.step')).read_bytes()).hexdigest() for i in ids},'limit':'Ideal zero-volume mating contact; no crimp/preload/elastomer compression proof.'};print(label,r[label],flush=True)
(OUT/'clamp-check.json').write_text(json.dumps(r,indent=2)+'\n')
