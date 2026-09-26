"""Export CAD-space mesh previews, then render offline assembled/exploded QC."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('assembly')
parser.add_argument('--export', type=Path)
parser.add_argument('--render', type=Path)
parser.add_argument('--output', type=Path)
parser.add_argument('--degrees', type=float, default=0)
parser.add_argument('--compressor-degrees', type=float, default=0)
parser.add_argument('--compressor-disengaged', action='store_true')
parser.add_argument('--azimuth', type=float, default=-35)
parser.add_argument('--elevation', type=float, default=24)
arguments = parser.parse_args()
if not all(math.isfinite(value) for value in (arguments.azimuth, arguments.elevation)):
    parser.error('Camera angles must be finite')

if arguments.export:
    import build123d as cad
    import trimesh
    sys.path.insert(0, str(ROOT / 'cad/engine'))
    from assembly_math import transforms

    manifest_path = ROOT / 'inventory/engine/full-assembly.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    definitions = {entry['id']: entry for entry in manifest['definitions']}
    descendants = {arguments.assembly}
    while True:
        expanded = descendants | {entry['id'] for entry in manifest['assemblies']
                                  if entry['parent'] in descendants}
        if expanded == descendants:
            break
        descendants = expanded
    occurrences = [entry for entry in manifest['occurrences']
                   if entry['parent'] in descendants or entry['id'] == arguments.assembly]
    assert occurrences, arguments.assembly
    poses = transforms(manifest, arguments.degrees, compressor_degrees=arguments.compressor_degrees,
                       compressor_engaged=not arguments.compressor_disengaged)
    arrays = {}
    colors = []
    mesh_hashes = {}
    for index, occurrence in enumerate(occurrences):
        definition = definitions[occurrence['definition']]
        mesh_path = ROOT / definition['glb'].lstrip('/')
        if mesh_path not in mesh_hashes:
            mesh_hashes[mesh_path] = hashlib.sha256(mesh_path.read_bytes()).hexdigest()
        scene = trimesh.load(mesh_path, force='scene')
        mesh = scene.to_geometry()
        vertices = np.asarray(mesh.vertices)[:, [0, 2, 1]] * [1000, -1000, 1000]
        transform = poses[occurrence['id']].wrapped.Transformation()
        matrix = np.array([[transform.Value(row, column) for column in range(1, 5)]
                           for row in range(1, 4)])
        arrays[f'vertices_{index}'] = vertices @ matrix[:, :3].T + matrix[:, 3]
        arrays[f'faces_{index}'] = np.asarray(mesh.faces)
        parent = poses[occurrence['id']] * cad.Rot(*occurrence.get('rotation_cad_deg', [0, 0, 0])).inverse()
        rotation = parent.wrapped.Transformation()
        rotation_matrix = np.array([[rotation.Value(row, column) for column in range(1, 4)]
                                    for row in range(1, 4)])
        arrays[f'explode_{index}'] = rotation_matrix @ occurrence['explode_cad_mm']
        colors.append(definition['color'])
    assert manifest_path.read_bytes() == manifest_bytes, 'Manifest changed during mesh export'
    assert all(hashlib.sha256(path.read_bytes()).hexdigest() == digest for path, digest in mesh_hashes.items()), 'Mesh changed during export'
    arrays['metadata'] = np.array(json.dumps({'assembly': arguments.assembly, 'colors': colors,
                                             'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
                                             'mesh_sha256': {str(path.relative_to(ROOT)): digest for path, digest in mesh_hashes.items()},
                                             'parts': len(occurrences), 'crank_degrees': arguments.degrees,
                                             'compressor_degrees': arguments.compressor_degrees,
                                             'compressor_engaged': not arguments.compressor_disengaged}))
    np.savez_compressed(arguments.export, **arrays)
    print(f'Exported {len(occurrences)} parts to {arguments.export}')
elif arguments.render:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plot
    from matplotlib.colors import to_rgb
    from engine_qc_raster import render_mesh

    assert arguments.output, '--output is required with --render'
    archive = np.load(arguments.render, allow_pickle=False)
    metadata = json.loads(str(archive['metadata']))
    figure = plot.figure(figsize=(16, 9), facecolor='#eef1f4')
    light = np.array([.5, -.4, .8])
    light /= np.linalg.norm(light)
    for panel, explosion in enumerate((0, .6), 1):
        axes = figure.add_subplot(1, 2, panel)
        all_triangles = []
        all_colors = []
        for index, color in enumerate(metadata['colors']):
            vertices = archive[f'vertices_{index}'] + explosion * archive[f'explode_{index}']
            triangles = vertices[archive[f'faces_{index}']]
            normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
            lengths = np.linalg.norm(normals, axis=1)
            normals /= np.maximum(lengths[:, None], 1e-12)
            shade = .35 + .65 * np.abs(normals @ light)
            colors = np.clip(shade[:, None] * np.array(to_rgb(color)), 0, 1)
            all_triangles.append(triangles)
            all_colors.append(colors)
        axes.imshow(render_mesh(np.concatenate(all_triangles), np.concatenate(all_colors),
                                elevation=arguments.elevation, azimuth=arguments.azimuth))
        axes.set_axis_off()
        axes.set_title('Assembled' if not explosion else 'Exploded 60%')
    phase_label = f"crank {metadata.get('crank_degrees',0):g}°"
    if metadata['assembly'].startswith('ac-compressor'):
        engagement = 'engaged' if metadata.get('compressor_engaged', True) else 'disengaged reference'
        phase_label = f"compressor {metadata.get('compressor_degrees',0):g}° · {engagement}"
    revision = metadata.get('manifest_sha256', 'unrecorded')[:12]
    figure.suptitle(f"{metadata['assembly']} · {metadata['parts']} modeled parts · {phase_label}\nOffline geometry QC · provisional reconstruction · {revision} · camera {arguments.azimuth:g}°/{arguments.elevation:g}°", fontsize=16)
    figure.tight_layout()
    figure.savefig(arguments.output, dpi=150, facecolor=figure.get_facecolor())
    print(arguments.output)
else:
    parser.error('Specify --export or --render')
