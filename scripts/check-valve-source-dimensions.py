"""Independent saved-STEP envelope checks against source-v2 constraints."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import valve_source_layout as v
OUT=ROOT/'cad/engine/candidates/valve-source-all12';rows=[];failures=[]
for name,axis,expected in [('intake-valve','Z',v.LENGTHS['intake']),('exhaust-valve','Z',v.LENGTHS['exhaust']),('pushrod','Z',v.PUSHROD_OVERALL),('pushrod','X',v.PUSHROD_D),('lifter-body','Z',v.LIFTER_HEIGHT),('lifter-body','X',.874*25.4)]:
 path=OUT/(name+'.step');shape=b.import_step(path);value=getattr(shape.bounding_box().size,axis);error=abs(value-expected);row={'part':name,'axis':axis,'expected_mm':expected,'actual_mm':value,'error_mm':error,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};rows.append(row)
 if error>.002 or not shape.is_valid or len(shape.solids())!=1:failures.append(row)
# OCC helix surface bounds include trimmed-away underlying surfaces, so test
# ground axial extent by exact outside-solid volume rather than loose bbox.
for kind,h in v.INSTALLED.items():
 path=OUT/(kind+'-spring.step');shape=b.import_step(path)
 slab=b.Pos(0,0,h/2)*b.Box(60,60,h);outside=shape-slab;vol=sum(s.volume for s in outside.solids()) if hasattr(outside,'solids') else sum(x.volume for x in outside)
 planar=[]
 for face in shape.faces():
  bb=face.bounding_box()
  if bb.size.Z<1e-5 and (abs(bb.min.Z)<1e-5 or abs(bb.min.Z-h)<1e-5):planar.append({'z_mm':bb.min.Z,'area_mm2':face.area})
 row={'part':kind+'-spring','height_mm':h,'outside_volume_mm3':vol,'ground_faces':planar};rows.append(row)
 if vol>.001 or len(planar)<2 or not all(any(abs(x['z_mm']-z)<1e-5 and x['area_mm2']>.1 for x in planar) for z in [0,h]):failures.append(row)
report={'status':'PASS' if not failures else 'FAIL','rows':rows,'failures':failures};(OUT/'dimension-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));sys.exit(bool(failures))
