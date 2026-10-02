"""Issue80 local shape refinement. All dimensions estimated; no installed frame."""
from pathlib import Path
import numpy as np
import build123d as b
from functools import lru_cache
R=Path(__file__).resolve().parents[2];O=Path(__file__).parent/'generated/airbox-refined-20261002'
OLD=Path(__file__).parent/'generated/online-airbox-duct-specimen'
WALL=3.
def smooth(t):
 t=np.clip(t,0,1);return t*t*(3-2*t)
def interp(x,xs,ys):
 for a,z,ya,yz in zip(xs[:-1],xs[1:],ys[:-1],ys[1:]):
  if a<=x<=z:return float(ya+(yz-ya)*smooth((x-a)/(z-a)))
 return float(ys[0] if x<xs[0] else ys[-1])
def profile(x,short=False):
 start=26 if short else 0;first=110 if short else 86;last=290 if short else 254
 y=interp(x,[start,start+24,first,first+60,last,350,440,543,559],[-48,-48,-46,-50,-69,-74,-68,-66,-66] if short else [60,60,65,58,29,17,20,20,20])
 if x<first:r=interp(x,[start,start+24,first-25,first],[42.5,42.5,44,35])
 elif x<=last:r=35-3*smooth((x-first)/(last-first))+7*(1-np.cos(2*np.pi*(x-first)/12))/2
 else:r=interp(x,[last,last+32,380,490,543,559],[32,33.5,30,28.5,28.5,28.5])
 return y,float(r)
def section(x,short=False,inner=False,extra=0):
 y,r=profile(x,short);return b.Plane(origin=(x,y,0),x_dir=(0,1,0),z_dir=(1,0,0))*b.Circle((r-WALL if inner else r)+extra)
@lru_cache(maxsize=8)
def body(short=False,inner=False,extra=0):
 # Rational quadratic circle x cubic axial spline: exact circular sections,
 # avoiding native loft's degree14 polynomial circle approximation.
 from scipy.interpolate import make_interp_spline
 from OCP.TColgp import TColgp_Array2OfPnt
 from OCP.TColStd import TColStd_Array2OfReal,TColStd_Array1OfReal,TColStd_Array1OfInteger
 from OCP.gp import gp_Pnt
 from OCP.Geom import Geom_BSplineSurface
 from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace,BRepBuilderAPI_Sewing,BRepBuilderAPI_MakeSolid
 from OCP.TopoDS import TopoDS
 from OCP.ShapeFix import ShapeFix_Solid
 start=26 if short else 0;first=110 if short else 86;last=290 if short else 254
 xs=sorted(set(list(np.arange(start+24,544,2.))+[first-25,first,last,last+16,last+32,350,380,440,490,520,543]))
 values=[[x,profile(x,short)[0],profile(x,short)[1]-(WALL if inner else 0)+extra] for x in xs]
 spline=make_interp_spline(xs,values,k=3)
 cir=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)]
 poles=TColgp_Array2OfPnt(1,len(spline.c),1,9);weights=TColStd_Array2OfReal(1,len(spline.c),1,9)
 for i,(x,y,r) in enumerate(spline.c,1):
  for j,(cy,cz) in enumerate(cir,1):
   poles.SetValue(i,j,gp_Pnt(float(x),float(y+r*cy),float(r*cz)));weights.SetValue(i,j,1. if j%2 else np.sqrt(.5))
 def array(vals,integer=False):
  arr=(TColStd_Array1OfInteger if integer else TColStd_Array1OfReal)(1,len(vals))
  for i,v in enumerate(vals,1):arr.SetValue(i,int(v) if integer else float(v))
  return arr
 knots,mults=np.unique(spline.t,return_counts=True)
 surf=Geom_BSplineSurface(poles,weights,array(knots),array([0,1,2,3,4]),array(mults,True),array([3,2,2,2,3],True),3,2,False,False)
 sew=BRepBuilderAPI_Sewing(1e-6)
 # Restrict the identical surface into local patches; prevents global adaptive
 # mesh grids from multiplying all corrugation extrema across the entire tube.
 cuts=sorted(set([xs[0],first]+list(range(first,last+1,12))+[last,last+32,380,440,xs[-1]]))
 for aa,zz in zip(cuts[:-1],cuts[1:]):
  patch=surf.Copy();patch.Segment(float(aa),float(zz),0.,4.)
  sew.Add(BRepBuilderAPI_MakeFace(patch,1e-7).Face())
 for x in (xs[0],xs[-1]):sew.Add(section(x,short,inner,extra).face().wrapped)
 sew.Perform();solid=BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(sew.SewedShape())).Solid();fix=ShapeFix_Solid(solid);fix.Perform();middle=b.Solid(fix.Solid())
 for aa,zz in [(start,start+24),(543,559)]:middle=middle+b.extrude(section(aa,short,inner,extra),amount=zz-aa)
 return middle
def tube(short=False):return body(short)-body(short,True)
def build():
 p={'online-airbox-duct-long':tube(),'online-airbox-duct-short':tube(True)}
 # Waisted, rounded outline; material terminates on external tube faces.
 pts=[(334,1),(343,-15),(350,-34),(344,-54),(363,-66),(383,-56),(380,-38),(386,-19),(402,-3),(389,5)]
 face=b.make_face(b.Polygon(*pts,align=None));face=b.fillet(face.vertices(),radius=5)
 web=b.extrude(b.Pos(0,0,-3.5)*face,amount=7)
 web=web-body()-body(True);p['online-airbox-joining-web']=web
 # Broad open channel in XZ with outward lips, mounted on exterior saddle.
 q=[(260,53),(269,53),(278,35),(310,35),(319,53),(328,53),(328,57),(317,57),(307,39),(281,39),(271,57),(260,57)]
 face=b.make_face(b.Polygon(*q,align=None));face=b.fillet(face.vertices(),radius=1.2)
 channel=b.extrude(b.Plane(origin=(0,29,0),x_dir=(1,0,0),z_dir=(0,-1,0))*face,amount=18)
 # Saddle conforms to noncircular-in-X outer skin rather than encroaching on duct lumen.
 strap=b.Pos(294,25,0)*b.Box(40,95,76)
 outer=body();saddle=(strap & body(extra=2.0))-outer
 # Upper base connects channel to saddle; trim everything to outer skin.
 saddle=(saddle+channel+b.Pos(294,20,35)*b.Box(34,20,8))-outer
 p['online-airbox-retainer']=saddle
 for f in sorted(OLD.glob('online-airbox-clamp-*.step')):p[f.stem]=b.import_step(f)
 return p
