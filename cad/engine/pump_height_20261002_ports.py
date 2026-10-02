"""Estimated short-chamber ports under qualified replacement height."""
import math,numpy as np,build123d as b
import pump_height_20261002_trial2 as core
from waterpump_heater_source_candidate import segment
R=core.R;O=R/'cad/engine/generated/pump-height-20261002-ports'
DIR=np.array([0.,math.cos(math.radians(145)),math.sin(math.radians(145))])
def datums(height):
 root=np.array([375+44*height/180,-80.,230.3]);end=np.array([375-34*height/180,-171.,415.]);crest=375+69*height/180
 radial=np.linalg.norm(end[1:]-root[1:]);slope=(76/100)*(height/180)/(radial/178)
 ed=np.array([-slope,-.28,.67]);ed[1:]/=np.linalg.norm(ed[1:]);ed/=np.linalg.norm(ed)
 return root,end,crest,ed

def path(height):
 root,end,crest,ed=datums(height);start=root-12*DIR;p0=root+25*DIR;mid=root+90*DIR;mid[0]=crest;tangent=ed.copy();tangent[0]=0;tangent/=np.linalg.norm(tangent);p3=end-25*ed;p2=p3-65*ed
 return b.Wire([b.Edge.make_line(tuple(start),tuple(p0)),b.Edge.make_bezier(*map(tuple,[p0,p0+25*DIR,mid-20*tangent,mid])),b.Edge.make_bezier(*map(tuple,[mid,mid+25*tangent,p2,p3])),b.Edge.make_line(tuple(p3),tuple(end))])
def sweep(r,height):
 root,*_=datums(height);return b.sweep(b.Plane(origin=tuple(root-12*DIR),z_dir=tuple(DIR))*b.Circle(r),path(height))
def section(rad,x,rx,rz):return b.Plane(origin=(x,rad,6),x_dir=(1,0,0),z_dir=(0,1,0))*b.Ellipse(rx,rz)
def inlet(height,inside=False,probe=False):
 rootx=(389+375+height-64)/2 # newfrontwall = hubface-64
 if probe:rs=(1.,1.,1.)
 elif inside:rs=(7.,20.,20.)
 else:rs=(10.,29.,24.)
 a,z,r=rs;ys=(10,60,146)if inside or probe else(20,60,96,145)
 sections=[section(y,rootx if i==0 else 403,a if i==0 else r,z if i==0 else r)for i,y in enumerate(ys)]
 result=b.loft(sections,ruled=True)
 if not inside and not probe:result+=b.Solid.make_cylinder(25.5,3,b.Plane(origin=(403,140,6),z_dir=(0,1,0)))
 return b.Pos(0,-32,170)*b.Rot(-130,0,0)*result

def parts(height=98.43):
 out,inputs=core.parts(height);root,end,crest,ed=datums(height)
 housing=out['water-pump-housing'].fuse(inlet(height),segment(12,root-42*DIR,root))
 housing=housing.cut(inlet(height,True),segment(6.5,root-46*DIR,root+DIR),segment(8,root-12*DIR,root+DIR))
 out['water-pump-housing']=core.norm(housing)
 out['heater-pump-return-elbow']=core.norm((sweep(8,height)+segment(8.5,end-5*ed,end-3*ed))-sweep(6.5,height))
 return out,inputs
