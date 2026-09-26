"""Depth-buffered orthographic mesh previews, independent of browser rendering."""
import math
import numpy as np
from numba import njit


@njit(cache=False)
def rasterize(projected, colors, width, height):
    pixels = np.ones((height, width, 3), dtype=np.float64)
    depths = np.full((height, width), -np.inf)
    for triangle_index in range(projected.shape[0]):
        triangle = projected[triangle_index]
        lower_x = max(0, math.floor(np.min(triangle[:, 0])))
        upper_x = min(width - 1, math.ceil(np.max(triangle[:, 0])))
        lower_y = max(0, math.floor(np.min(triangle[:, 1])))
        upper_y = min(height - 1, math.ceil(np.max(triangle[:, 1])))
        denominator = ((triangle[1, 1] - triangle[2, 1]) * (triangle[0, 0] - triangle[2, 0])
                       + (triangle[2, 0] - triangle[1, 0]) * (triangle[0, 1] - triangle[2, 1]))
        if abs(denominator) < 1e-12:
            continue
        for row in range(lower_y, upper_y + 1):
            for column in range(lower_x, upper_x + 1):
                first_weight = ((triangle[1, 1] - triangle[2, 1]) * (column + .5 - triangle[2, 0])
                                + (triangle[2, 0] - triangle[1, 0]) * (row + .5 - triangle[2, 1])) / denominator
                second_weight = ((triangle[2, 1] - triangle[0, 1]) * (column + .5 - triangle[2, 0])
                                 + (triangle[0, 0] - triangle[2, 0]) * (row + .5 - triangle[2, 1])) / denominator
                third_weight = 1 - first_weight - second_weight
                if min(first_weight, second_weight, third_weight) < -1e-10:
                    continue
                depth = first_weight * triangle[0, 2] + second_weight * triangle[1, 2] + third_weight * triangle[2, 2]
                if depth > depths[row, column]:
                    depths[row, column] = depth
                    pixels[row, column] = colors[triangle_index]
    return pixels


def render_mesh(triangles, colors, size=1000, elevation=24, azimuth=-35):
    elevation, azimuth = math.radians(elevation), math.radians(azimuth)
    camera = np.array([math.cos(elevation) * math.cos(azimuth),
                       math.cos(elevation) * math.sin(azimuth), math.sin(elevation)])
    right = np.array([-math.sin(azimuth), math.cos(azimuth), 0])
    upward = np.cross(camera, right)
    projected = np.asarray(triangles, dtype=np.float64) @ np.stack([right, -upward, camera]).T
    bounds = projected.reshape(-1, 3)
    lower, upper = bounds.min(axis=0), bounds.max(axis=0)
    scale = (size - 1) * .9 / max(np.max(upper[:2] - lower[:2]), 1e-9)
    projected[:, :, :2] = (projected[:, :, :2] - (lower[:2] + upper[:2]) / 2) * scale + (size - 1) / 2
    return rasterize(projected, np.asarray(colors, dtype=np.float64), size, size)
