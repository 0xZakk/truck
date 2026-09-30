"""Replacement seal envelope probes, not seal internals or installed parts."""

import build123d as b

SHAFT_DIAMETER = 1.875 * 25.4
HOUSING_BORE = 2.561 * 25.4
CASE_DIAMETER = 2.565 * 25.4
WIDTH = 0.528 * 25.4
FLANGE_DIAMETER = 3.16 * 25.4


def cylinder(radius, start, end):
    return b.Pos((start + end) / 2, 0, 0) * b.Rot(0, 90, 0) * b.Cylinder(radius, end - start)


def probes(front):
    """Front alignment is an explicit hypothesis, never an adopted datum.

    The annular volume encloses the unknown case/lip construction. Treating
    all of it as physical seal material would create false collision claims.
    The flange is a zero-thickness face because flange thickness is unknown.
    """
    rear = front - WIDTH
    bore = cylinder(HOUSING_BORE / 2, rear, front)
    envelope = cylinder(CASE_DIAMETER / 2, rear, front) - cylinder(SHAFT_DIAMETER / 2, rear - 1, front + 1)
    flange = b.Pos(front, 0, 0) * (b.Plane.YZ * (b.Circle(FLANGE_DIAMETER / 2) - b.Circle(HOUSING_BORE / 2)))
    return {"housing-bore-probe": bore, "seal-annular-envelope": envelope, "flange-face-probe": flange}
