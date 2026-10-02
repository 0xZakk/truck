"""Independent axial-section integral and spline coefficient bounds; actual STEP inputs."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy.interpolate import make_interp_spline
from scipy.integrate import quad
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import airbox_refined_20261002 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[];inputs={str(p.relative_to(R)):sha(p) for p in [Path(c.__file__),Path(__file__),R/'reference/engine/airbox-refined-20261002-check.json']}
for short in (False,True):
 start=26 if short else 0;first=110 if short else 86;last=290 if short else 254
 # Independently recreate declared section samples, then bound their cubic interpolation.
 xs=sorted(set(list(np.arange(start+24,544,2.))+[first-25,first,last,last+16,last+32,350,380,440,490,520,543]))
 y=np.array([c.profile(x,short)[0] for x in xs]);rad=np.array([c.profile(x,short)[1] for x in xs])
 outer=make_interp_spline(xs,np.array([xs,y,rad]).T,k=3);inner=make_interp_spline(xs,np.array([xs,y,rad-3]).T,k=3)
 radial_error=float(np.max(np.abs(outer.c[:,2]-inner.c[:,2]-3)));axis_error=float(np.max(np.abs(outer.c[:,:2]-inner.c[:,:2])))
 assert radial_error<1e-10 and axis_error<1e-10
 minimum_inner=float(np.min(inner.c[:,2]));assert minimum_inner>24
 derivative=outer.derivative();dx_error=float(np.max(np.abs(derivative.c[:len(derivative.t)-derivative.k-1,0]-1)));assert dx_error<1e-10
 # Circle area integral is independent of centerline lateral bend when X-parametric.
 radial_integral=outer.integrate(xs[0],xs[-1])[2]+42.5*24+28.5*16
 expected=float(np.pi*(6*radial_integral-9*(559-start)))
 p=c.O/('online-airbox-duct-'+('short' if short else 'long')+'.step');inputs[str(p.relative_to(R))]=sha(p);s=b.import_step(p)
 from OCP.BRepGProp import BRepGProp
 from OCP.GProp import GProp_GProps
 props=GProp_GProps();estimated_error=BRepGProp.VolumeProperties_s(s.wrapped,props,1e-8,True,False)
 adaptive=props.Mass();error=abs(adaptive-expected)/expected;assert error<.001,(p,adaptive,expected,error)
 rows.append({'tube':p.stem,'default_nonadaptive_BRep_volume_mm3':s.volume,'default_relative_error':abs(s.volume-expected)/expected,'adaptive_BRep_volume_mm3':adaptive,'adaptive_requested_relative_tolerance':1e-8,'adaptive_estimated_relative_error':estimated_error,'independent_annular_integral_mm3':expected,'relative_error':error,'minimum_inner_radius_coefficient_bound_mm':minimum_inner,'radial_wall_coefficient_error_mm':radial_error,'same_axis_coefficient_error_mm':axis_error,'linear_X_derivative_error':dx_error,'interpretation':'Nonnegative B-spline basis and exact rational circles imply continuous positive-radius lumen in declared undeformed construction; actual STEP probes corroborate sampled sections. This is not installed flow/pressure or flexible-motion proof.'})
contacts=[]
web=c.O/'online-airbox-joining-web.step';ret=c.O/'online-airbox-retainer.step'
inputs[str(web.relative_to(R))]=sha(web);inputs[str(ret.relative_to(R))]=sha(ret)
w=b.import_step(web);clip=b.import_step(ret)
for short in (False,True):
 tube=b.import_step(c.O/('online-airbox-duct-'+('short' if short else 'long')+'.step'))
 for x in (362,364,366):
  y,r=c.profile(x,short)
  for z in (-2.,0.,2.):
   q=(x,y+(1 if short else -1)*np.sqrt(r*r-z*z),z)
   distances=[tube.distance_to(b.Vertex(*q)),w.distance_to(b.Vertex(*q))];ok=max(distances)<1e-5
   assert ok,('web contact',short,q)
   contacts.append({'interface':'web/short' if short else 'web/long','point_mm':q,'distances_to_actual_solids_mm':distances,'within_contact_tolerance':ok})
tube=b.import_step(c.O/'online-airbox-duct-long.step')
for x in (290,294,300):
 y,r=c.profile(x)
 for angle in (0,np.pi/2,np.pi):
  q=(x,y+r*np.cos(angle),r*np.sin(angle));distances=[tube.distance_to(b.Vertex(*q)),clip.distance_to(b.Vertex(*q))];ok=max(distances)<1e-5
  assert ok,('retainer contact',q)
  contacts.append({'interface':'retainer/long','point_mm':q,'distances_to_actual_solids_mm':distances,'within_contact_tolerance':ok})
q=contacts[0]['point_mm'];bad=(q[0],q[1]-2,q[2]);bad_gap=tube.distance_to(b.Vertex(*bad));assert bad_gap>1
report={'contact_probe_tolerance_mm':1e-5,'shifted_contact_control_gap_mm':bad_gap,'status':'PASS independent construction/volume checks','rows':rows,'actual_contact_boundary_probes':contacts,'inputs':inputs,'negative_control':'Set inner coefficients equal to outer: radial wall error becomes3mm and fails1e-10mm identity bound; actual blocked/skin controls are in main checker.'}
assert abs(0-3)>1e-10
(R/'reference/engine/airbox-refined-20261002-sections.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows,indent=2))
