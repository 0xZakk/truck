"""Isolated MPS-59-A replacement envelope; all section dimensions estimated."""
from __future__ import annotations
from cadgen import build123d as bd
from cadgen import step, glb

OD = 52.578
HEIGHT = 8.7122
THICKNESS = 1.0
OUTER_RADIUS = 1.5
INNER_RADIUS = 0.5
OUT = '../../../../cad/engine/generated/text-to-cad-20261003/plugin/'


def make_cup(od=OD, height=HEIGHT, thickness=THICKNESS,
             outer_radius=OUTER_RADIUS, inner_radius=INNER_RADIUS):
    outer = bd.Cylinder(od / 2, height, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    bottom = [e for e in outer.edges() if e.geom_type == bd.GeomType.CIRCLE and abs(e.center().Z) < 1e-7]
    outer = bd.fillet(bottom, outer_radius)
    cavity = bd.Cylinder(od / 2 - thickness, height,
                         align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(bd.Location((0, 0, thickness)))
    lower = [e for e in cavity.edges() if e.geom_type == bd.GeomType.CIRCLE and abs(e.center().Z-thickness) < 1e-7]
    cavity = bd.fillet(lower, inner_radius)
    cup = outer - cavity
    cup.label = 'block-core-cup-mps59a'
    cup.color = bd.Color(0.60, 0.63, 0.67)
    return cup


@step(out=OUT+'block_core_cup_mps59a.step', mesh_tolerance=0.0001, mesh_angular_tolerance=0.10)
@glb(out=OUT+'block_core_cup_mps59a.glb', mesh_tolerance=0.0001, mesh_angular_tolerance=0.10)
def block_core_cup_mps59a():
    return make_cup()


if __name__ == '__main__':
    block_core_cup_mps59a()
