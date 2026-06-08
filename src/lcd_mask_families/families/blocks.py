from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from ..metadata import FamilyMetadata

FAMILY_METADATA = FamilyMetadata(
    family_id="blocks",
    family_version="0.1.0",
    status="active",
    differentiable=False,
    continuous_parameters=False,
    seeded=False,
    diffraction_oriented=False,
    orthogonal_basis=False,
    recommended_for_capture=True,
    recommended_for_optimization=False,
    notes=(
        "Structured periodic block/checker family for capture diversity and "
        "generalization tests, not ordinary gradient-based optimization."
    ),
)


def render_blocks(
    params: Mapping[str, Any],
    grid_arrays: Mapping[str, np.ndarray],
) -> np.ndarray:
    block_h = int(params["block_h"])
    block_w = int(params["block_w"])
    offset_y = int(params.get("offset_y", 0))
    offset_x = int(params.get("offset_x", 0))
    invert = bool(params.get("invert", False))

    if block_h <= 0 or block_w <= 0:
        raise ValueError("block_h and block_w must be positive")

    x = np.asarray(grid_arrays["x"])
    y = np.asarray(grid_arrays["y"])
    height, width = x.shape
    yy, xx = np.indices((height, width))

    block_y = np.floor_divide(yy + offset_y, block_h)
    block_x = np.floor_divide(xx + offset_x, block_w)
    mask = ((block_y + block_x) % 2) == 0
    if invert:
        mask = ~mask
    return mask.astype(np.float64)
