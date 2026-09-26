"""Verify per-pixel visibility, winding independence and orthographic framing."""
import numpy as np
from engine_qc_raster import rasterize, render_mesh

triangles = np.array([[[1, 1, 0], [9, 1, 0], [1, 9, 0]],
                      [[1, 1, -2.125], [9, 1, 1.875], [1, 9, 1.875]]], dtype=float)
colors = np.array([[1, 0, 0], [0, 0, 1]], dtype=float)
image = rasterize(triangles, colors, 12, 12)
np.testing.assert_array_equal(image[1, 1], colors[0])
np.testing.assert_array_equal(image[1, 7], colors[1])
np.testing.assert_array_equal(image[11, 11], [1, 1, 1])
np.testing.assert_array_equal(image, rasterize(triangles[::-1].copy(), colors[::-1].copy(), 12, 12))
np.testing.assert_array_equal(image, rasterize(triangles[:, ::-1].copy(), colors, 12, 12))
degenerate = np.concatenate([triangles, np.zeros((1, 3, 3))])
np.testing.assert_array_equal(image, rasterize(degenerate, np.vstack([colors, [0, 1, 0]]), 12, 12))
preview = render_mesh(triangles, colors, size=100)
assert preview.shape == (100, 100, 3)
assert np.any(np.all(preview == colors[0], axis=-1))
assert np.all(preview[[0, -1], :, :] == 1)
print('Depth-buffer ordering, intersecting triangles, winding, degenerate faces and framing PASS')
