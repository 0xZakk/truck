"""Uninstalled MPS-126 replacement envelope; no host bore or placement inference."""
import build123d as b
OD_MM=1.640*25.4
OD_RANGE_MM=(1.640*25.4,1.642*25.4)
HEIGHT_MM=.365*25.4
ILLUSTRATIVE_WALL_MM=1.
def build(wall_mm=ILLUSTRATIVE_WALL_MM):
 if not 0<wall_mm<min(HEIGHT_MM,OD_MM/2):raise ValueError('positive cup wall required')
 outer=b.Cylinder(OD_MM/2,HEIGHT_MM,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 void=b.Pos(0,0,wall_mm)*b.Cylinder(OD_MM/2-wall_mm,HEIGHT_MM,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 return outer-void
