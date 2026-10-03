"""Conservative interpolation bound for the declared analytic helical tube."""
import math,json
from pathlib import Path
R=15.5;w=.4;h=1.4/(2*math.pi);L=math.hypot(R,h);D=4.5/h;A=w*R/(h*L)
# Norm bounds: f(theta,phi)=C(theta)+w(N cos(phi)+B sin(phi)).
Ftt=R+w*(1+h/L);Ft=L+w*(1+h/L);Ftp=w*(1+h/L)
Huu=Ftt*D*D;Hup=Ftt*D*A+Ftp*D;Hpp=Ftt*A*A+Ft*A+2*Ftp*A+w
# Barycentric interpolation remainder uses coordinate variances <=range^2/4.
def bound(n,m):
 du=1/n;dp=2*math.pi/m
 return (Huu*du*du+2*Hup*du*dp+Hpp*dp*dp)/8
r={'scope':'Ideal analytic surface tessellation only; not a whole-STEP or factory-fidelity proof','derivation':'Taylor remainder at barycentric mean; Hessian norm bounds and range-variance bound1/4; mixed covariance bounded by product of standard deviations','hessian_norm_bounds':[Huu,Hup,Hpp],'longitudinal_intervals':1024,'circumferential_intervals':256,'side_surface_bound_mm':bound(1024,256),'cap_boundary_chord_bound_mm':Hpp*(2*math.pi/256)**2/8,'gate_mm':.025,'coarse_negative_control_bound_mm':bound(128,32)}
assert r['side_surface_bound_mm']<.025 and r['coarse_negative_control_bound_mm']>.025
Path(__file__).resolve().parents[1].joinpath('reference/engine/pump-spring-sweep-20261003-bound.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
