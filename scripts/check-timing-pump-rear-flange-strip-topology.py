"""Distinguish connected erosion from preserved wet/dry separation topology."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import timing_pump_rear_flange_candidate as c
old,paths,m,poses=c.load();rows={}
for k,x in [('main-gasket',373.4),('pump-gasket',374)]:
 rows[k]={}
 for name,s in [('old',old[k]),('candidate',b.import_step(c.O/(k+'.step')))]:
  section=b.section(s,b.Plane.YZ.offset(x));eroded=b.offset(section,amount=-1.52)
  rows[k][name]={'before_holes':sum(len(f.inner_wires())for f in section.faces()),'eroded_components':len(eroded.faces()),'eroded_holes':sum(len(f.inner_wires())for f in eroded.faces()),'eroded_valid':eroded.is_valid}
  q=rows[k][name];q['same_separation_topology']=q['eroded_components']==1 and q['before_holes']==q['eroded_holes']
r={'status':'FAIL pump3.04mm separationstrip inherited; mainstripPASS','rows':rows,'meaning':'Connected eroded stock alone does not prove a closed3.04mm sealing path around each opening. Pump erosion merges openings already in oldgeometry. No threshold reduced; originalconnectedstrip metric remainstrue but insufficient.','inputs':{str(p.relative_to(R)):c.sha(p)for p in [Path(__file__),Path(c.__file__),*paths.values(),c.O/'main-gasket.step',c.O/'pump-gasket.step']}};(R/'inventory/engine/timing-pump-rear-flange-strip-topology.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
