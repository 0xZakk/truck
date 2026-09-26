"""Offline rear-interface QC of the isolated manifold candidate."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--export', type=Path)
parser.add_argument('--render', type=Path)
parser.add_argument('--output', type=Path)
arguments = parser.parse_args()
if arguments.export:
    sys.path.insert(0, str(ROOT / 'cad/engine'))
    import ac_compressor_manifold as candidate
    arrays = {}
    identifiers = []
    for index, (identifier, shape) in enumerate(candidate.replacements().items()):
        vertices, faces = shape.tessellate(.12)
        arrays[f'vertices_{index}'] = np.asarray([tuple(vertex) for vertex in vertices])
        arrays[f'faces_{index}'] = np.asarray(faces)
        identifiers.append(identifier)
    arrays['metadata'] = np.array(json.dumps({'identifiers': identifiers, 'sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest()}))
    np.savez_compressed(arguments.export, **arrays)
else:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plot
    from engine_qc_raster import render_mesh
    archive = np.load(arguments.render, allow_pickle=False)
    metadata = json.loads(str(archive['metadata']))
    figure, axes = plot.subplots(1, 2, figsize=(14, 7))
    for panel, explosion in enumerate((False, True)):
        triangles = []
        colors = []
        for index, identifier in enumerate(metadata['identifiers']):
            vertices = archive[f'vertices_{index}'].copy()
            offset = 0
            if explosion:
                offset = -38 if 'seal' in identifier else -80 if 'manifold' in identifier else 0
                if 'bolt' in identifier:
                    offset = -120
            vertices[:, 0] += offset
            faces = vertices[archive[f'faces_{index}']]
            normals = np.cross(faces[:, 1] - faces[:, 0], faces[:, 2] - faces[:, 0])
            normals /= np.maximum(np.linalg.norm(normals, axis=1)[:, None], 1e-12)
            shade = .4 + .6 * np.abs(normals @ np.array([-.5, -.4, .768]))
            color = np.array([.2, .55, .25]) if 'seal' in identifier else np.array([.65, .69, .74])
            triangles.append(faces)
            colors.append(shade[:, None] * color)
        axes[panel].imshow(render_mesh(np.concatenate(triangles), np.concatenate(colors), azimuth=145))
        axes[panel].set_axis_off()
        axes[panel].set_title('Separated interface' if explosion else 'Assembled rear interface')
    figure.suptitle('FS10 rear manifold study · offline QC · provisional geometry\n' + metadata['sha256'][:12])
    figure.tight_layout()
    figure.savefig(arguments.output, dpi=140)
