from pathlib import Path
import sys,json,hashlib,collections
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
from OCP.TopExp import TopExp
from OCP.TopAbs import TopAbs_EDGE,TopAbs_FACE
from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
import pump_cover_candidate_20261003 as c
vol=lambda s:sum(abs(solid_volume(q,'adaptive'))for q in c.norm(s).solids())if s else 0
p=c.O/'water-pump-housing.step';h=b.import_step(p);l=c.T*c.inlet(True);q=c.norm(h.cut(l));out=c.O/'housing-inlet-recut-diagnostic.step';b.export_step(q,out);probe=c.T*c.inlet(probe=True);mp=TopTools_IndexedDataMapOfShapeListOfShape();TopExp.MapShapesAndAncestors_s(q.wrapped,TopAbs_EDGE,TopAbs_FACE,mp);counts=collections.Counter(len({hash(f)for f in mp.FindFromIndex(i)})for i in range(1,mp.Extent()+1));r={'valid':q.is_valid,'solids':len(q.solids()),'inlet_probe_obstruction_mm3':vol(q.intersect(probe)),'removed_stock_mm3':vol(h.cut(q)),'added_stock_mm3':vol(q.cut(h)),'edge_unique_faces_counts':dict(counts),'path':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'operation':'Final independently declared own inlet lumen; no neighbor mask; fullprotectedchecks pending'};(R/'reference/engine/pump-cover-candidate-20261003-inlet-recut.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
