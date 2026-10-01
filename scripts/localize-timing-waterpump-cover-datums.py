from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import water_pump_inlet_v3_candidate as inlet
O=R/'cad/engine/generated/timing-waterpump-cover-datum-audit';rows={}
for name in ['water-pump-housing','water-pump-gasket']:
 p=O/('pan21__'+name+'.step');s=b.import_step(p);rows[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bodies':[{'volume_mm3':q.volume,'bounds_mm':[list(q.bounding_box().min),list(q.bounding_box().max)]}for q in s.solids()]}
 if name.endswith('housing'):
  region=b.Pos(440,-32,170)*(inlet.outer()-inlet.passage());hit=s.intersect(region);rows[name]['inlet_construction_overlap_mm3']=hit.volume if hit else 0
  rear=s.intersect(b.Pos(376.4,0,0)*b.Box(2.8,1000,1000));rows[name]['rear_flange_X375_to377_8_overlap_mm3']=rear.volume if rear else 0
r={'witnesses':rows,'scope':'Actual collision solids and intersection with declared analytical inlet construction; no clearance subtraction','inputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),R/'cad/engine/water_pump_inlet_v3_candidate.py']}};(R/'inventory/engine/timing-waterpump-cover-localization.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
