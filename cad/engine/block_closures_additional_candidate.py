"""Parameterized cup law; free-state replacement envelopes, never host bores."""
import build123d as b
MPS126={'od_mm':1.640*25.4,'height_mm':.365*25.4}
MPS59A={'od_mm':2.070*25.4,'height_mm':.343*25.4}
def cup(od_mm,height_mm,wall_mm):
 if not 0<wall_mm<min(height_mm,od_mm/2):raise ValueError('invalid wall')
 outer=b.Cylinder(od_mm/2,height_mm,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 void=b.Pos(0,0,wall_mm)*b.Cylinder(od_mm/2-wall_mm,height_mm,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 return outer-void
def build(wall_mm=1.):return cup(**MPS59A,wall_mm=wall_mm)
