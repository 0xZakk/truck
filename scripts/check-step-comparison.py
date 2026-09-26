"""Check serialized geometry equivalence without accepting displaced starter parts."""
from pathlib import Path
import sys
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import starter_engagement as linkage
from cad_metrics import solid_volume, step_comparison_shape

expected = linkage.parts()['starter-drive-lever']
saved = cad.import_step(ROOT / 'cad/engine/generated/starter-drive-lever.step')
canonical = step_comparison_shape(expected)
common = saved.intersect(canonical)
assert common and abs(common.volume - expected.volume) < .02
for displacement in (.01, 1, 100):
    common = saved.intersect(cad.Pos(displacement, 0, 0) * canonical)
    assert not common or abs(common.volume - expected.volume) > .02, displacement
print('PASS STEP comparison preserves pose sensitivity')

import exhaust_front_profile as manifold

saved_casting = cad.import_step(ROOT / 'cad/engine/generated/exhaust-front.step')
expected_casting = step_comparison_shape(manifold.front_casting())
for displacement in (0, .01, 1, 100):
    placed = cad.Pos(displacement, 0, 0) * expected_casting
    common = saved_casting.intersect(placed)
    volume = sum(solid_volume(solid, 'adaptive') for solid in common.solids()) if common else 0
    difference = solid_volume(saved_casting, 'adaptive') + solid_volume(placed, 'adaptive') - 2 * volume
    if displacement == 0:
        assert abs(difference) < .01, difference
    else:
        assert difference > .01, (displacement, difference)
print('PASS adaptive casting comparison rejects displaced geometry')
