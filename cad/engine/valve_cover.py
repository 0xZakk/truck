"""Provisional rocker-cover envelope with the corrected cam-side clearance.

The lower flange stays on the existing head datum. Upper profiles lean toward
the +Y pushrod side; these offsets are clearance-study assumptions, not stamping
measurements. Used by the full-engine generator.
"""
import build123d as b


def cover_shape():
    outer=b.loft([b.Pos(0,offset,z)*b.RectangleRounded(x,y,r)
                  for z,x,y,r,offset in [
                      (-38,734,232,28,0),(-28,728,222,28,0),
                      (24,698,186,32,22),(38,680,174,35,22)]],ruled=True)
    inner=b.loft([b.Pos(0,offset,z)*b.RectangleRounded(x,y,r)
                  for z,x,y,r,offset in [
                      (-42,728,226,25,0),(-28,722,216,25,0),
                      (24,692,180,29,22),(35,674,168,32,22)]],ruled=True)
    cover=outer-inner
    # Retain the existing cap/PCV interface datums while reconciling shoulders.
    cover-=b.Pos(240,0,38)*b.Cylinder(17,20)
    cover-=b.Pos(-240,0,38)*b.Cylinder(14.2,20)
    return cover
