from __future__ import annotations

from typing import Any, Mapping

import numpy as np


FAMILY_METADATA = {
    "family_id": "stripes",
    "family_version": "0.1.0",
    "differentiable": True,
}


def render_stripes(
    params: Mapping[str, Any],
    grid_arrays: Mapping[str, np.ndarray],
) -> np.ndarray:
    angle_rad = float(params["angle_rad"])
    period = float(params["period"])
    phase_rad = float(params.get("phase_rad", 0.0))
    duty = float(params.get("duty", 0.5))
    softness = float(params.get("softness", 0.0))

    if period <= 0:
        raise ValueError("period must be positive")
    if not 0.0 < duty < 1.0:
        raise ValueError("duty must be in (0, 1)")

    x = np.asarray(grid_arrays["x"], dtype=np.float64)
    y = np.asarray(grid_arrays["y"], dtype=np.float64)
    coordinate = x * np.cos(angle_rad) + y * np.sin(angle_rad)
    cycles = coordinate / period + phase_rad / (2.0 * np.pi)
    phase = np.mod(cycles, 1.0)

    if softness <= 0:
        mask = phase < duty
    else:
        edge_a = _sigmoid((phase - 0.0) / softness)
        edge_b = _sigmoid((duty - phase) / softness)
        wrap = _sigmoid((phase - (1.0 - softness)) / softness)
        mask = np.maximum(edge_a * edge_b, wrap)

    return np.asarray(mask, dtype=np.float64)


def _sigmoid(value: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-value))
