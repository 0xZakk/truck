"""Actual local gasket geometry, avoiding unsupported full-R10 disk assumption."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_pan21_lateral_candidate as c
OUT=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate';paths=[OUT/(n+'.step')for n in ['cover','pan','pan-gasket']];cover,pan,gasket=[b.import_step(p)for p in paths]
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 v=0.
 for t in s.solids():
  q=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,q,1e-9,True,False);assert e<=1e-7,e;v+=abs(q.Mass())
 return v
rows=[]
for name,p in [('retired21',c.OLD),('new21',c.NEW)]:
 mask=b.Pos(p[0],p[1])*c.owner.cz(12,-27,-24);local=c.norm(gasket.intersect(mask));upper=c.norm((b.Pos(0,0,.02)*local).cut(gasket));lower=c.norm((b.Pos(0,0,-.02)*local).cut(gasket));rows.append({'region':name,'actual_upper_gasket_unbacked_mm3':vol(upper.cut(cover)),'actual_lower_gasket_unbacked_mm3':vol(lower.cut(pan))})
r={'rows':rows,'status':'PASS'if all(v<1e-5 for row in rows for k,v in row.items()if k.endswith('mm3'))else'FAIL','earlier_probe_limitation':'FullR10 bottom disk extends toX400 although actual gasket front isX399 at newY−95. Its0.1174518138mm3 absent material is an overbroad analytic witness, retained in interface report; this check tests complete actual gasket withinR12 at both changed locations. No geometry or threshold change.','inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(__file__)]}};(ROOT/'inventory/engine/timing-pan21-actual-gasket-contact.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
