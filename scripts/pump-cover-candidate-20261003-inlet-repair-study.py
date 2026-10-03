"""Frozen option B local lumen Boolean diagnosis, no neighbors or integrated exports."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_cover_candidate_20261003 as c
from cad_metrics import solid_volume
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
vol=lambda s:sum(abs(solid_volume(q,'adaptive')) for q in c.norm(s).solids()) if s else 0
p=c.O/'water-pump-housing.step';h=b.import_step(p);l=c.T*c.inlet(True);probe=c.T*c.inlet(probe=True)
r={'scope':'Independent own-lumen cutters; frozen optionB pose; no neighbor masks','inputs':{str(q.relative_to(R)):sha(q) for q in [p,Path(__file__),Path(c.__file__)]},'lumen':{'valid':l.is_valid,'volume':vol(l),'solids':len(l.solids())},'attempts':{}}
# Cutter rebuilt as one independent first-span loft, with explicit endpoints.
ps=[b.Plane(origin=(x,y*c.G,6*c.G),x_dir=(1,0,0),z_dir=(0,1,0))*b.Ellipse(rx,rz*c.G) for y,x,rx,rz in [(35,397,7,21),(60,403,20,20)]]
first=c.T*b.Pos(0,-32,170)*b.Rot(-130,0,0)*b.loft(ps,ruled=True)
for name,tool in [('whole_lumen',l),('first_span',first)]:
 cut=BRepAlgoAPI_Cut(h.wrapped,tool.wrapped);cut.SetFuzzyValue(1e-6);cut.Build();q=b.Compound.cast(cut.Shape());out=c.O/('housing-inlet-study-'+name+'.step');b.export_step(q,out)
 r['attempts'][name]={'valid':q.is_valid,'solids':len(q.solids()),'tool_volume':vol(tool),'original_tool_overlap':vol(h.intersect(tool)),'probe_obstruction':vol(q.intersect(probe)),'stock_removed':vol(h.cut(q)),'stock_added':vol(q.cut(h)),'path':str(out.relative_to(R)),'sha256':sha(out)}
 (R/'reference/engine/pump-cover-candidate-20261003-inlet-repair-study.json').write_text(json.dumps(r,indent=2)+'\n');print(name,r['attempts'][name],flush=True)
