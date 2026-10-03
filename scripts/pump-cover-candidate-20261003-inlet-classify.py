from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.gp import gp_Pnt
import pump_cover_candidate_20261003 as c
h=b.import_step(c.O/'water-pump-housing.step');l=c.T*c.inlet(True);probe=c.T*c.inlet(probe=True)
def inside(s,p):q=BRepClass3d_SolidClassifier(s.wrapped,gp_Pnt(*p),1e-7);return str(q.State())
def world(p):return tuple((c.T*(b.Pos(0,-32,170)*b.Rot(-130,0,0)*b.Vertex(*p))).center())
rows=[]
for y in np.linspace(35*c.G,60*c.G,101):
 x=397+6*(y-35*c.G)/(25*c.G);p=world((x,float(y),6*c.G));rows.append({'inlet_local':[x,float(y),6*c.G],'world':p,'housing':inside(h,p),'lumen':inside(l,p),'probe':inside(probe,p)})
r={'tolerance_mm':1e-7,'samples':rows,'in_housing':sum('TopAbs_IN' in q['housing']for q in rows),'in_lumen':sum('TopAbs_IN'in q['lumen']for q in rows),'limit':'Finite centerline classification only; contradictory Boolean volume remains explicit','inputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),c.O/'water-pump-housing.step']}};(R/'reference/engine/pump-cover-candidate-20261003-inlet-classify.json').write_text(json.dumps(r,indent=2)+'\n');print('counts',r['in_housing'],r['in_lumen']);print([q for q in rows if'TopAbs_IN'in q['housing']][:3])
