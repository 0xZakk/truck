"""Adaptive solid volume for stable STEP round-trip comparisons."""
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from pathlib import Path
import tempfile
import build123d as cad


def step_comparison_shape(shape):
    """Normalize analytic surfaces to STEP before comparing against STEP imports."""
    with tempfile.TemporaryDirectory(prefix='engine-step-comparison-') as directory:
        path = Path(directory) / 'expected.step'
        cad.export_step(shape, path, unit=cad.Unit.MM)
        reopened = cad.import_step(path)
    if not reopened.is_valid or len(reopened.solids()) != len(shape.solids()):
        raise ValueError('Comparison STEP conversion changed topology')
    if abs(reopened.volume - shape.volume) > max(1e-5, abs(shape.volume) * 1e-5):
        raise ValueError('Comparison STEP conversion changed volume')
    return reopened


def solid_volume(shape, method="default"):
    if method == "default":
        # STEP may reopen a located solid as nested compounds. build123d
        # Compound.volume can report zero despite a valid enclosed solid.
        # Measure the actual solids; callers still enforce their count/validity.
        return sum(solid.volume for solid in shape.solids())
    if method != "adaptive":
        raise ValueError(f"Unknown volume method: {method}")
    props = GProp_GProps()
    # Default nonadaptive integration drifts on trimmed, reflected surfaces.
    # Keep geometry validation strict and improve the measurement instead.
    error = BRepGProp.VolumeProperties_s(shape.wrapped, props, 1e-9, True, False)
    if error > 1e-7:
        raise ValueError(f'Volume integration did not converge: {error}')
    return props.Mass()


def support_bounds(shape):
    """Continuous CAD extrema from distances to enclosing planar supports.

    OCC bounding boxes can retain extrema of the untrimmed surface of a clipped
    sweep. Each support face spans the entire conservative box in its plane, so
    its minimum distance to material measures the corresponding axis extremum.
    Reject impossible OCC distance results and require agreement from two
    differently spaced planes. No tessellation or export mesh enters this bound.
    """
    import math
    from OCP.Bnd import Bnd_Box
    box = shape.bounding_box()
    lower, upper = list(box.min), list(box.max)
    spans = [high - low for low, high in zip(lower, upper)]
    span = max(spans)
    if not math.isfinite(span) or span <= 0:
        raise ValueError('Support bounds require a finite nonempty shape')
    center = [(low + high) / 2 for low, high in zip(lower, upper)]
    result = [lower.copy(), upper.copy()]
    for axis in range(3):
        normal = [0, 0, 0]
        normal[axis] = 1
        for side in (0, 1):
            values = []
            for gap in (1., span + 1., 2 * span + 1., 3 * span + 1., 5 * span + 1.):
                point = center.copy()
                point[axis] = lower[axis] - gap if side == 0 else upper[axis] + gap
                face = cad.Face.make_rect(4 * (span + 1), 4 * (span + 1),
                                         cad.Plane(origin=point, z_dir=normal))
                distance = shape.distance_to(face)
                # Some trimmed-spline extrema solves incorrectly return zero.
                # A support strictly outside the conservative enclosure cannot
                # have distance smaller than gap; fail closed on such results.
                if not math.isfinite(distance) or not gap - 1e-6 <= distance <= gap + spans[axis] + 1e-6:
                    continue
                value = point[axis] + distance if side == 0 else point[axis] - distance
                if any(abs(value - previous) < 1e-5 for previous in values):
                    result[side][axis] = value
                    break
                values.append(value)
            else:
                raise ValueError(f'CAD support extrema did not converge: axis={axis}, side={side}, values={values}')
    exact = Bnd_Box()
    exact.Update(*result[0], *result[1])
    return cad.BoundBox(exact)
