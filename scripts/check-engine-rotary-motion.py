"""Verify generic local shaft rotation under a tilted assembly frame."""
import math
from pathlib import Path
import sys

import build123d as cad

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cad/engine'))
from assembly_math import transforms

manifest = {
    'mechanism': {'stroke_mm': 100, 'rod_length_mm': 200},
    'assemblies': [
        {'id': 'engine', 'parent': None, 'position_cad_mm': [11, 22, 33],
         'rotation_cad_deg': [-20, 0, 0]},
        {'id': 'shaft', 'parent': 'engine', 'position_cad_mm': [0, 0, 5],
         'motion': {'type': 'rotary', 'axis': 'z', 'ratio': -.5, 'phase_deg': 13}}
    ],
    'occurrences': [{'id': 'probe', 'parent': 'shaft', 'position_cad_mm': [10, 20, 30]}]
}
motion = manifest['assemblies'][1]['motion']
tilt = math.radians(-20)
checks = 0
for axis in ('x', 'y', 'z'):
    motion['axis'] = axis
    for ratio in (-.5, -.4, 1):
        motion['ratio'] = ratio
        for degrees in range(0, 721, 15):
            angle = math.radians(degrees * ratio + 13)
            cosine, sine = math.cos(angle), math.sin(angle)
            if axis == 'x':
                horizontal, lateral, vertical = 10, 20 * cosine - 30 * sine, 20 * sine + 30 * cosine
            elif axis == 'y':
                horizontal, lateral, vertical = 10 * cosine + 30 * sine, 20, -10 * sine + 30 * cosine
            else:
                horizontal, lateral, vertical = 10 * cosine - 20 * sine, 10 * sine + 20 * cosine, 30
            vertical += 5
            expected = cad.Vector(11 + horizontal, 22 + lateral * math.cos(tilt) - vertical * math.sin(tilt),
                                  33 + lateral * math.sin(tilt) + vertical * math.cos(tilt))
            actual = cad.Vertex(0, 0, 0).moved(transforms(manifest, degrees)['probe']).center()
            assert (actual - expected).length < 1e-8, (axis, ratio, degrees)
            checks += 1
print(f'Generic CAD shaft ratios, phase and tilted hierarchy: {checks} poses passed')
