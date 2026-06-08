from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from .backends import require_numpy_backend
from .families import FAMILY_REGISTRY
from .grids import make_grid
from .projection import project_display_mask
from .specs import GridSpec, ProjectionSpec


def render_continuous_mask(
    family: str,
    params: Mapping[str, Any],
    grid: GridSpec,
    *,
    backend: str = "numpy",
) -> np.ndarray:
    require_numpy_backend(backend)
    if family not in FAMILY_REGISTRY:
        raise ValueError(f"unknown mask family: {family!r}")

    grid_arrays = make_grid(grid, backend=backend)
    mask = np.asarray(FAMILY_REGISTRY[family](params, grid_arrays), dtype=np.float64)
    if not np.all(np.isfinite(mask)):
        raise ValueError("rendered mask contains non-finite values")
    return np.clip(mask, 0.0, 1.0)


def render_display_mask(
    family: str,
    params: Mapping[str, Any],
    grid: GridSpec,
    projection: ProjectionSpec,
    *,
    backend: str = "numpy",
) -> np.ndarray:
    continuous = render_continuous_mask(family, params, grid, backend=backend)
    return project_display_mask(continuous, projection, backend=backend)
