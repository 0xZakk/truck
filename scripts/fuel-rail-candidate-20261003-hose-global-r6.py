"""Conservative curvature bounds plus exact subdivided-sweep overlap checks."""
from pathlib import Path
import numpy as np,math,json,hashlib,ast,build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepCheck import BRepCheck_Analyzer
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r6';r={}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
builder=ROOT/'cad/engine/fuel-rail-candidate-20261003-r6.py'
parameter=ROOT/'cad/engine/fuel-rail-candidate-20261003-parameters-r2.json'
tree=ast.parse(builder.read_text())
controls_node=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='controls' for t in n.targets))
def split(c):
 layers=[np.array(c)]
 while len(layers[-1])>1:layers.append((layers[-1][:-1]+layers[-1][1:])/2)
 return np.array([q[0] for q in layers]),np.array([q[-1] for q in layers[::-1]])
def prove_curvature(c,depth=0):
 d=5*np.diff(c,axis=0);dd=20*np.diff(c,n=2,axis=0);lo=d.min(0);hi=d.max(0);low=np.maximum(np.maximum(lo,-hi),0);speed_lower=float(np.linalg.norm(low));accel_upper=float(np.linalg.norm(np.maximum(abs(dd.min(0)),abs(dd.max(0)))))
 radius_lower=speed_lower**2/accel_upper if accel_upper else 1e99
 if radius_lower>6:return [radius_lower]
 if depth>=18:raise RuntimeError('Cannot certify local curvature')
 a,z=split(c);return prove_curvature(a,depth+1)+prove_curvature(z,depth+1)
for label,sign in [('plus',1),('minus',-1)]:
 controls=np.array([(174.136,-163+24*sign,420),(174.136,-163+24*sign,444),(145,(-120 if sign==1 else -170),460),(0,-115,460),(0,-95,460),(0,-75,460)],dtype=float)
 actual_controls=np.array(eval(compile(ast.Expression(controls_node),str(builder),'eval'),{'__builtins__':{}},{'gx':174.136,'gy':-163+24*sign,'sign':sign}),dtype=float)
 assert np.array_equal(actual_controls,controls)
 build=json.loads((OUT/label/'build.json').read_text())
 assert build['builder_sha256']==sha(builder) and build['parameters_sha256']==sha(parameter)
 step=OUT/label/'local-regulator-vacuum-hose.step'
 assert build['definitions']['regulator-vacuum-hose']['sha256']==sha(step)
 curve=b.Bezier(*[tuple(q) for q in controls]);route=b.Wire([curve,b.Line((0,-75,460),(0,-55,460))]);plane=b.Plane(origin=route@0,z_dir=route%0)
 reconstructed=b.sweep(plane*b.Circle(6),path=route,is_frenet=True)-b.sweep(plane*b.Circle(4.1),path=route,is_frenet=True)
 reconstructed-=b.Pos(174.136,-163+24*sign,(419+430)/2)*b.Cylinder(4.15,11)
 actual=b.import_step(step)
 def volume(shape):return sum(abs(s.volume) for s in shape.solids()) if shape is not None else 0.0
 difference=volume(reconstructed-actual)+volume(actual-reconstructed)
 assert difference<1e-5, difference
 binding={'builder':str(builder.relative_to(ROOT)),'builder_sha256':sha(builder),'parameters_sha256':sha(parameter),'step':str(step.relative_to(ROOT)),'step_sha256':sha(step),'checker_sha256':sha(Path(__file__)),'actual_builder_controls_equal':True,'actual_saved_step_symmetric_difference_mm3':difference,'contract':'outer radius6; bore4.1; straight leadY-75..-55 atX0 Z460; regulator socket radius4.15 Z419..430, exact reconstructed subtraction compared with saved STEP'}
 bounds=prove_curvature(controls);chunks=[controls]
 for _ in range(3):chunks=[s for c in chunks for s in split(c)]
 solids=[]
 for c in chunks:
  curve=b.Bezier(*[tuple(q) for q in c]);shape=b.sweep(b.Plane(origin=curve@0,z_dir=curve%0)*b.Circle(6),path=curve,is_frenet=True)
  if not shape.is_valid or len(shape.solids())!=1:raise RuntimeError('invalid split sweep')
  solids.append(shape)
 solids.append(b.Pos(0,-65,460)*b.Rot(90,0,0)*b.Cylinder(6,20));pairs=[]
 for i,a in enumerate(solids):
  for j,c in enumerate(solids[i+1:],i+1):
   op=BRepAlgoAPI_Common(a.wrapped,c.wrapped);op.Build()
   if not op.IsDone() or not BRepCheck_Analyzer(op.Shape()).IsValid():raise RuntimeError('invalid split-sweep Common')
   result=b.Compound(op.Shape());vol=sum(abs(s.volume) for s in result.solids());pairs.append({'a':i,'b':j,'overlap_mm3':vol,'pass':vol<1e-5})
 delta=10*.6**3*.4**2*math.sqrt(80**2+25**2)
 r[label]={'actual_artifact_binding':binding,'curvature_bound_method':'Derivative/second-derivative Bezier convex hull bounds recursively bisected; radius >= lower_speed_squared / upper_acceleration','conservative_radius_lower_mm':min(bounds),'certified_subintervals':len(bounds),'outer_radius_mm':6,'monotone_controls':{'x_nonincreasing':bool(np.all(np.diff(controls[:,0])<=0)),'y_nondecreasing':bool(np.all(np.diff(controls[:,1])>=0)),'z_nondecreasing':bool(np.all(np.diff(controls[:,2])>=0))},'global_method':'8 exact de Casteljau Bezier sub-sweeps plus straight lead, every pair including adjacent checked by OCC; each valid positive single solid and analytic local curvature certificate. Conservative geometry audit, no production bend limit.','pairs':pairs,'all_pairs_pass':all(p['pass'] for p in pairs),'exact_max_equal_parameter_path_displacement_mm':delta,'t_at_displacement_max':.6,'note':'No neighbor geometry consulted in path correction.'};print(label,r[label],flush=True);(OUT/'hose-global.json').write_text(json.dumps(r,indent=2)+'\n')
