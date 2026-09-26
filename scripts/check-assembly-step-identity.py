"""Regression: repeated STEP instances retain distinct labels and placements."""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'cad/engine'))
from assembly_step import placed_occurrences, verify_roundtrip

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)/'instances.step'
    base = b.Box(3, 4, 5)
    manifest = {'mechanism': {'stroke_mm': 10, 'rod_length_mm': 20},
                'assemblies': [{'id': 'root', 'parent': None}],
                'occurrences': [
                    {'id': f'repeated-part-{i}', 'definition': 'base',
                     'parent': 'root', 'position_cad_mm': [i*10, i*2, i]}
                    for i in range(3)]}
    expected = placed_occurrences(manifest, {'base': base})
    b.export_step(b.Compound(children=expected), path)
    print(verify_roundtrip(path, expected))
    shifted = list(expected)
    shifted[1] = deepcopy(expected[1]).moved(b.Pos(1, 0, 0))
    try:
        verify_roundtrip(path, shifted)
    except AssertionError as error:
        assert 'placement/bounds changed' in str(error), str(error)
    else:
        raise AssertionError('Shifted occurrence escaped placement validation')
    repeated = list(expected)
    repeated[1] = deepcopy(expected[1])
    repeated[1].label = expected[0].label
    try:
        verify_roundtrip(path, repeated)
    except AssertionError as error:
        assert 'Duplicate STEP occurrence labels' in str(error), str(error)
    else:
        raise AssertionError('Duplicate occurrence escaped identity validation')
print('STEP identity/placement checks and both fault controls passed')
