"""Read-only partition of already frozen witnesses; no replacement geometry."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
np=R/'reference/engine/pump-functional-20261003-neighbors.json';n=json.loads(np.read_text());O=R/'cad/engine/generated/pump-functional-20261003';inputs={str(np.relative_to(R)):sha(np),str(Path(__file__).relative_to(R)):sha(Path(__file__))}
def load(p):
 inputs[str(p.relative_to(R))]=sha(p);return b.import_step(p)
def norm(s):return b.Compound(s)if isinstance(s,b.ShapeList)else s
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in norm(s).solids())if s else 0.
back=load(O/'region-seal_backing.step');bosses=[load(O/f'region-dry_boss_{i}.step')for i in range(1,5)];protected=back.fuse(*bosses)
rows=[]
for c in n['conflicts']:
 p=R/c['witness'];assert sha(p)==c['sha256'];w=load(p)
 row={'a':c['a'],'b':c['b'],'total_mm3':vol(w),'in_seal_backing_mm3':vol(w.intersect(back)),'in_individual_bosses_mm3':[vol(w.intersect(q))for q in bosses],'in_protected_union_mm3':vol(w.intersect(protected))}
 row['outside_protected_union_mm3']=vol(w.cut(protected))
 row['axis_depth_bins_mm3']={}
 for name,lo,hi in [('mount_backing_X375_378',375,378),('rear_body_X378_389',378,389),('forward_X389_500',389,500)]:
  slab=b.Pos((lo+hi)/2,0,0)*b.Box(hi-lo,2000,2000);row['axis_depth_bins_mm3'][name]=vol(w.intersect(slab))
 rows.append(row)
r={'status':'READ ONLY ownership diagnostic; no clearance edits','scope':'Five frozen actualv4 overlap witnesses vs declared pump protection regions. Region intersections may overlap; protected_union avoids double counting. No source shape inferred from a conflict.','rows':rows,'inputs':inputs}
(R/'reference/engine/pump-source-registration-20261003-clash-ownership.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows,indent=2))
