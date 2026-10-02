from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from cad_metrics import solid_volume
import pump_height_20261002_ports_trial3 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.core.norm(s).solids())if s else 0.
r={'scope':'Local finite passage/seat witnesses only; no containment/pressure claim','variants':{},'inputs':{str(p.relative_to(R)):sha(p)for p in[Path(__file__),Path(c.__file__),R/'reference/engine/pump-height-20261002-ports-trial3.json']}}
for name,H in [('nominal',98.43),('inch-value',98.552)]:
 def load(n):
  p=c.O/(name+'-'+n+'.step');r['inputs'][str(p.relative_to(R))]=sha(p);return b.import_step(p)
 h=load('water-pump-housing');tube=load('heater-pump-return-elbow');root,end,crest,ed=c.datums(H)
 probes={'inlet':c.inlet(H,probe=True),'heater':c.sweep(.7,H).fuse(c.segment(.7,root-46*c.DIR,root-12*c.DIR))}
 socket=c.segment(8,root-12*c.DIR,root);face=b.Compound([f for f in socket.faces()if f.geom_type==b.GeomType.CYLINDER]);seats={}
 for label,s in [('housing',h),('tube',tube)]:
  op=BRepAlgoAPI_Cut(face.wrapped,b.Compound(list(s.faces())).wrapped);op.Build();seats[label]={'area_mm2':face.area,'missing_mm2':b.Compound(op.Shape()).area,'boolean_done':op.IsDone()}
 plug=b.Pos(*(root+10*c.DIR))*b.Sphere(2)
 r['variants'][name]={'valid':h.is_valid and tube.is_valid,'solid_counts':[len(h.solids()),len(tube.solids())],'socket':seats,'passage_obstruction_mm3':{k:vol(p.intersect(h.fuse(tube)))for k,p in probes.items()},'blocked_heater_control_mm3':vol(probes['heater'].intersect(plug)),'shaft_axial_gauge_obstruction_mm3':vol(c.core.cx(7.9,365,375+H-3).intersect(h)),'body_tube_overlap_mm3':vol(h.intersect(tube))}
(R/'reference/engine/pump-height-20261002-interfaces-trial3.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['variants'],indent=2))
