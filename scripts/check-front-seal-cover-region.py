"""Diagnose coincident clipped Boolean result using unsplit full-shape delta."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
paths=[R/'cad/engine/generated/front-seal-2692-candidate/cover.step',R/'cad/engine/generated/timing-pan21-lateral-candidate/cover.step']
a,z=[b.import_step(p)for p in paths]
mask=b.Solid.make_cylinder(43,31,b.Plane(origin=(405,0,0),z_dir=(1,0,0)))
def vol(q):return sum(abs(solid_volume(s,'adaptive'))for s in q.solids())if q else 0
rows=[]
for name,shape in [('removed',a.cut(z)),('added',z.cut(a))]:
 parts=[]
 for s in shape.solids():
  bb=s.bounding_box();parts.append({'volume_mm3':vol(s),'bounds_mm':[list(bb.min),list(bb.max)],'seal_region_intersection_mm3':vol(s.intersect(mask))})
 rows.append({'delta':name,'parts':parts,'total_mm3':vol(shape),'seal_region_intersection_mm3':sum(p['seal_region_intersection_mm3']for p in parts)})
out={'scope':'Alternative fullshape delta first; clipped coplanar failure retained','rows':rows,'bindings':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(__file__)]}}
(R/'inventory/engine/front-seal-cover-full-delta-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
