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
        return shape.volume
    if method != "adaptive":
        raise ValueError(f"Unknown volume method: {method}")
    props = GProp_GProps()
    # Default nonadaptive integration drifts on trimmed, reflected surfaces.
    # Keep geometry validation strict and improve the measurement instead.
    error = BRepGProp.VolumeProperties_s(shape.wrapped, props, 1e-9, True, False)
    if error > 1e-7:
        raise ValueError(f'Volume integration did not converge: {error}')
    return props.Mass()
