from pathlib import Path
import build123d as b,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r6';report={}
def stats(s):
 bb=s.bounding_box();return {'volume':s.volume,'solids':[q.volume for q in s.solids()],'valid':s.is_valid,'bounds':[list(bb.min),list(bb.max)]}
for label,sign in [('plus',1),('minus',-1)]:
 c=[(174.136,-163+24*sign,420),(174.136,-163+24*sign,444),(145,(-120 if sign==1 else -170),460),(0,-115,460),(0,-95,460),(0,-75,460)]
 curve=b.Bezier(*c);line=b.Edge.make_line((0,-75,460),(0,-55,460));route=b.Wire([curve,line]);p=b.Plane(origin=route@0,z_dir=route%0)
 outer=b.sweep(p*b.Circle(6),path=route,is_frenet=True);inner=b.sweep(p*b.Circle(4.1),path=route,is_frenet=True);shell=outer-inner
 row={'outer':stats(outer),'inner':stats(inner),'shell':stats(shell)}
 for name,s in [('outer',outer),('inner',inner),('shell',shell)]:b.export_step(s,OUT/label/f'failed-hose-{name}.step')
 curve_outer=b.sweep(p*b.Circle(6),path=curve,is_frenet=True);curve_inner=b.sweep(p*b.Circle(4.1),path=curve,is_frenet=True)
 row['curve_outer']=stats(curve_outer);row['curve_inner']=stats(curve_inner);row['curve_shell']=stats(curve_outer-curve_inner)
 report[label]=row;(OUT/'hose-failure-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print(label,row,flush=True)
