"""Check assembly-axis tilt followed by local distributor motion and nesting."""
import math
from pathlib import Path
import sys

import build123d as cad

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cad/engine'))
from assembly_math import transforms

manifest = {
    'mechanism': {'stroke_mm': 100, 'rod_length_mm': 200},
    'assemblies': [
        {'id': 'engine', 'parent': None, 'position_cad_mm': [10, 20, 30]},
        {'id': 'housing', 'parent': 'engine', 'position_cad_mm': [1, 2, 3],
         'rotation_cad_deg': [-20, 0, 0]},
        {'id': 'rotor', 'parent': 'housing', 'position_cad_mm': [0, 0, 5],
         'motion': {'type': 'distributor'}}
    ],
    'occurrences': [
        {'id': 'tip', 'parent': 'rotor', 'position_cad_mm': [10, 0, 0]}
    ]
}
tilt = math.radians(-20)
for degrees in range(0, 721, 15):
    rotation = math.radians(-degrees / 2)
    local_x, local_y, local_z = 10 * math.cos(rotation), 10 * math.sin(rotation), 5
    expected = cad.Vector(11 + local_x,
                          22 + local_y * math.cos(tilt) - local_z * math.sin(tilt),
                          33 + local_y * math.sin(tilt) + local_z * math.cos(tilt))
    actual = cad.Vertex(0, 0, 0).moved(transforms(manifest, degrees)['tip']).center()
    assert (actual - expected).length < 1e-8, (degrees, actual, expected)
print('Assembly tilt, nested translation and local distributor motion: 49 poses passed')
