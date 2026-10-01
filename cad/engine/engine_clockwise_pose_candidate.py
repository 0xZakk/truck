"""Isolated corrected-direction poses. Geometry stays caller-owned and unchanged.

Positive event angle q retains firing order. Crank CAD must have physical rest
throws -event_phase before `corrected_slider_frames` can be used in assembly.
Use `slider_frames` with measured legacy rest phase only to diagnose old CAD.
No crossed distributor/oil-drive gear compatibility is implied.
"""
import math
import build123d as b
from timing_coupled_core_candidate import AXIS, GEAR_X, K


def _finite(*values):
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Finite millimeter/degree values required')


def crank_frame(event_degrees):
    _finite(event_degrees)
    return b.Rot(-event_degrees, 0, 0)


def cam_frame(event_degrees, axial_mm=0):
    _finite(event_degrees, axial_mm)
    return b.Pos(axial_mm, *AXIS)*b.Rot(event_degrees/2+math.degrees(K*axial_mm), 0, 0)*b.Pos(0, -AXIS[0], -AXIS[1])


def gear_frames(event_degrees, axial_mm=0):
    """For frozen LOCAL crank.step/cam.step; built-in tooth phase applied once."""
    return {'crank': crank_frame(event_degrees)*b.Pos(GEAR_X, 0, 0),
            'cam': cam_frame(event_degrees, axial_mm)*b.Pos(GEAR_X, *AXIS)}


def slider_frames(event_degrees, physical_rest_phase_degrees, radius_mm, rod_length_mm, station_x_mm):
    """Rod centered at its big end; piston centered at pin. Explicit CAD rest phase."""
    _finite(event_degrees, physical_rest_phase_degrees, radius_mm, rod_length_mm, station_x_mm)
    if not 0 < radius_mm < rod_length_mm:
        raise ValueError('Require rod length > positive crank radius')
    t=math.radians(-event_degrees+physical_rest_phase_degrees)
    y=-radius_mm*math.sin(t);z=radius_mm*math.cos(t)
    height=z+math.sqrt(rod_length_mm**2-y**2)
    return {'rod': b.Pos(station_x_mm, y, z)*b.Rot(math.degrees(math.asin(y/rod_length_mm)), 0, 0),
            'piston': b.Pos(station_x_mm, 0, height)}


def corrected_slider_frames(event_degrees, event_phase_degrees, radius_mm, rod_length_mm, station_x_mm, *, measured_cad_rest_phase_degrees):
    """Reject unrephased CAD explicitly rather than moving rods off old journals."""
    _finite(event_phase_degrees, measured_cad_rest_phase_degrees)
    error=(measured_cad_rest_phase_degrees+event_phase_degrees+180)%360-180
    if abs(error)>1e-7:
        raise ValueError('Crank CAD rest phase does not equal negative event phase; regenerate bounded throws first')
    return slider_frames(event_degrees, -event_phase_degrees, radius_mm, rod_length_mm, station_x_mm)


def distributor_frame(event_degrees):
    """Local shaft frame only, CW from cap; drive handedness remains unresolved."""
    _finite(event_degrees)
    return b.Rot(0, 0, -event_degrees/2)
