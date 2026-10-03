"""Independent saved-artifact replay; does not generate or install geometry."""
from pathlib import Path
import hashlib
import json
import build123d as cad
import numpy as np
import trimesh
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / 'reference/engine/valve-spring-reconciliation-20261003'
report_path = Path(str(PREFIX) + '-candidate-build.json')
source = json.loads(report_path.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
out = {'scope': 'Saved STEP/GLB replay only; source end form and installed context remain open',
       'build_report_sha256': sha(report_path), 'states': {}}
for name, row in source['states'].items():
    step = Path(str(PREFIX) + '-' + name + '.step')
    glb = Path(str(PREFIX) + '-' + name + '.glb')
    assert sha(step) == row['step_sha256']
    assert sha(glb) == row['glb_sha256']
    shape = cad.import_step(step)
    props = GProp_GProps()
    error = BRepGProp.VolumePropertiesGK_s(shape.wrapped, props, 1e-9, True, True, False, False, False)
    assert 0 <= error < 1e-7
    expected = row['independent_volume_mm3']
    volume = props.Mass()
    assert abs(volume - expected) / expected <= .0001
    scene = trimesh.load(glb, force='scene')
    mesh = scene.to_geometry()
    # Invert exporter millimeter XYZ -> meter (X,Z,-Y), preserving axis identity.
    points = mesh.vertices[:, [0, 2, 1]] * np.array([1, -1, 1]) * 1000
    bounds = np.array([points.min(axis=0), points.max(axis=0)])
    bb = shape.bounding_box()
    cad_bounds = np.array([list(bb.min), list(bb.max)])
    delta = float(np.abs(bounds - cad_bounds).max())
    scaled_negative_delta = float(np.abs(bounds * 1.01 - cad_bounds).max())
    assert scaled_negative_delta > .01, 'Bounds gate failed to reject 1% scale error'
    assert shape.is_valid and len(shape.solids()) == 1
    assert mesh.is_watertight and mesh.is_winding_consistent and delta < .01
    out['states'][name] = {'step_sha256': sha(step), 'glb_sha256': sha(glb),
        'volume_mm3': volume, 'volume_relative_error': abs(volume-expected)/expected,
        'quadrature_error': error, 'axis_preserving_bounds_delta_mm': delta,
        'one_percent_scale_negative_rejected': scaled_negative_delta > .01,
        'watertight': mesh.is_watertight, 'winding_consistent': mesh.is_winding_consistent,
        'valid_single_solid': True}
    print(name, out['states'][name], flush=True)
Path(str(PREFIX) + '-root-replay.json').write_text(json.dumps(out, indent=2) + '\n')
