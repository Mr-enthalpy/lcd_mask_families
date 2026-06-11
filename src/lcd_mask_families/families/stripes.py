from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from ..metadata import FamilyMetadata

FAMILY_METADATA = FamilyMetadata(
    family_id="stripes",
    family_version="0.1.0",
    status="active",
    differentiability={
        "continuous_parameters": True,
        "differentiable_render": True,
        "differentiable_projection": "none",
        "seed_is_optimization_variable": False,
    },
    design_intent={
        "diffraction_oriented": True,
        "orthogonal_basis": False,
        "seeded_random": False,
        "recommended_for_capture": True,
        "recommended_for_optimization": True,
        "random_walk_risk": "low",
    },
    response_prior={
        "expected_effect": [
            "diffraction_order_shift",
            "diffraction_order_strength_change",
        ],
        "validated_by_measured_psf": False,
    },
    parameter_schema={
        "required": ["angle_rad", "period"],
        "optional": ["phase_rad", "duty", "softness"],
    },
    notes=(
        "Single periodic stripe family. Binary rendering is piecewise constant; "
        "softness > 0 provides a relaxed mathematical interface that still "
        "requires downstream differentiability review before serious optimization."
    ),
)


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
