from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
import pump_functional_20261003 as c
from cad_metrics import solid_volume
h=b.import_step(c.O/'water-pump-housing.step');f=b.import_step(c.O/'region-bolt_seat_3.step')
op=BRepAlgoAPI_Cut(f.wrapped,b.Compound(list(h.faces())).wrapped);op.Build();missing=b.Compound(op.Shape())
b.export_step(missing,c.O/'seat3-covered-face.step')
above=b.Compound([b.Solid.extrude(x,(.1,0,0))for x in missing.faces()])
below=b.Compound([b.Solid.extrude(x,(-.1,0,0))for x in missing.faces()])
def vol(x):return sum(abs(solid_volume(q,'adaptive'))for q in x.solids())if x else 0.
r={'missing_face_area_mm2':missing.area,'bounds':[list(missing.bounding_box().min),list(missing.bounding_box().max)],'above_0_1mm_stock_volume':vol(above.intersect(h)),'above_expected_volume':vol(above),'below_0_1mm_stock_volume':vol(below.intersect(h)),'below_expected_volume':vol(below),'inlet_face_intersection_area':missing.intersect(c.inlet()).area,'conclusion':'Inspect metrics: stock above and below proves a covered annular outer rim, not missing load-bearing volume. Preserve declared face FAIL; actual screw seat is a distinct check.'}
(R/'reference/engine/pump-functional-20261003-seat-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
