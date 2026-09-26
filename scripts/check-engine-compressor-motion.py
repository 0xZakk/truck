"""Check independent compressor motion in a rotated CAD assembly frame."""
import math
from pathlib import Path
import sys

import build123d as cad

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cad/engine'))
from assembly_math import transforms

amplitude = 37 * math.tan(math.radians(18))
motion = {'type': 'fs10', 'role': 'shaft'}
manifest = {
    'mechanism': {'stroke_mm': 100, 'rod_length_mm': 200},
    'assemblies': [
        {'id': 'engine', 'parent': None, 'position_cad_mm': [7, 11, 13], 'rotation_cad_deg': [0, 30, 0]},
        {'id': 'compressor', 'parent': 'engine', 'motion': motion}
    ],
    'occurrences': [{'id': 'probe', 'parent': 'compressor', 'position_cad_mm': [3, 5, 7]}]
}
checks = 0
for engaged in (False, True):
    for cylinder in range(5):
        motion.update(cylinder_phase_deg=cylinder * 72, stroke_amplitude_mm=amplitude)
        for degrees in range(0, 721, 15):
            for role in ('pulley', 'shaft', 'piston', 'shoe'):
                motion['role'] = role
                phase = math.radians(degrees if engaged or role == 'pulley' else 0)
                theta = cylinder * math.tau / 5
                offset = amplitude * (math.cos(theta) - math.cos(theta - phase)) if role in ('piston', 'shoe') else 0
                rotation = 0 if role == 'piston' else phase
                local_x = 3 + offset
                local_y = 5 * math.cos(rotation) - 7 * math.sin(rotation)
                local_z = 5 * math.sin(rotation) + 7 * math.cos(rotation)
                expected = cad.Vector(7 + local_x * math.cos(math.pi / 6) + local_z * .5,
                                      11 + local_y, 13 - local_x * .5 + local_z * math.cos(math.pi / 6))
                actual = cad.Vertex(0, 0, 0).moved(transforms(manifest, 217, compressor_degrees=degrees,
                                                            compressor_engaged=engaged)['probe']).center()
                assert (actual - expected).length < 1e-8, (engaged, cylinder, degrees, role)
                checks += 1
print(f'Independent compressor CAD phase, clutch reference and rotated hierarchy: {checks} poses passed')
