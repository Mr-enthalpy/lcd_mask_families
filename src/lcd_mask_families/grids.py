from __future__ import annotations

import numpy as np

from .backends import require_numpy_backend
from .specs import GridSpec


def make_grid(grid: GridSpec, *, backend: str = "numpy") -> dict[str, np.ndarray]:
    """Create deterministic coordinate arrays.

    The normalized frame uses pixel centers. For size N, coordinates are
    (i + 0.5) / N * 2 - 1, so the samples lie inside [-1, 1].
    """

    require_numpy_backend(backend)
    height, width = grid.shape_hw

    if grid.coordinate_frame == "normalized_lcd_pupil":
        y_1d = (np.arange(height, dtype=np.float64) + 0.5) / height * 2.0 - 1.0
        x_1d = (np.arange(width, dtype=np.float64) + 0.5) / width * 2.0 - 1.0
    elif grid.coordinate_frame == "pixel_index":
        y_1d = np.arange(height, dtype=np.float64)
        x_1d = np.arange(width, dtype=np.float64)
    else:
        raise ValueError(f"unsupported coordinate_frame: {grid.coordinate_frame!r}")

    x, y = np.meshgrid(x_1d, y_1d)
    return {"x": x, "y": y}
