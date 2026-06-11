from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from ..metadata import FamilyMetadata


FAMILY_METADATA = FamilyMetadata(
    family_id="radial_zones",
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
            "peak_spread_change",
        ],
        "validated_by_measured_psf": False,
    },
    parameter_schema={
        "required": [],
        "optional": [
            "center_x",
            "center_y",
            "scale_x",
            "scale_y",
            "radial_frequency",
            "quadratic_rate",
            "phase_rad",
            "duty",
            "softness",
        ],
    },
    notes=(
        "Radial zone family for concentric or chirped ring-like masks. "
        "Hard zones are piecewise constant; softness > 0 provides a relaxed "
        "mathematical interface that requires downstream differentiability review."
    ),
)


def render_radial_zones(
    params: Mapping[str, Any],
    grid_arrays: Mapping[str, np.ndarray],
) -> np.ndarray:
    center_x = _finite_float(params.get("center_x", 0.0), "center_x")
    center_y = _finite_float(params.get("center_y", 0.0), "center_y")
    scale_x = _finite_float(params.get("scale_x", 1.0), "scale_x")
    scale_y = _finite_float(params.get("scale_y", 1.0), "scale_y")
    radial_frequency = _finite_float(
        params.get("radial_frequency", 4.0),
        "radial_frequency",
    )
    quadratic_rate = _finite_float(params.get("quadratic_rate", 0.0), "quadratic_rate")
    phase_rad = _finite_float(params.get("phase_rad", 0.0), "phase_rad")
    duty = _finite_float(params.get("duty", 0.5), "duty")
    softness = _finite_float(params.get("softness", 0.0), "softness")

    if scale_x <= 0.0:
        raise ValueError("scale_x must be positive")
    if scale_y <= 0.0:
        raise ValueError("scale_y must be positive")
    if radial_frequency < 0.0:
        raise ValueError("radial_frequency must be nonnegative")
    if not 0.0 < duty < 1.0:
        raise ValueError("duty must be in (0, 1)")
    if softness < 0.0:
        raise ValueError("softness must be nonnegative")
    if radial_frequency == 0.0 and quadratic_rate == 0.0:
        raise ValueError("radial_frequency and quadratic_rate must not both be zero")

    x = np.asarray(grid_arrays["x"], dtype=np.float64)
    y = np.asarray(grid_arrays["y"], dtype=np.float64)
    rx = (x - center_x) / scale_x
    ry = (y - center_y) / scale_y
    radius = np.sqrt(rx * rx + ry * ry)

    cycles = radial_frequency * radius + quadratic_rate * radius * radius
    cycles += phase_rad / (2.0 * np.pi)
    phase = np.mod(cycles, 1.0)

    if softness <= 0.0:
        mask = phase < duty
    else:
        edge_a = _sigmoid(phase / softness)
        edge_b = _sigmoid((duty - phase) / softness)
        wrap = _sigmoid((phase - (1.0 - softness)) / softness)
        mask = np.maximum(edge_a * edge_b, wrap)

    if not np.all(np.isfinite(mask)):
        raise ValueError("rendered mask contains non-finite values")
    return np.asarray(np.clip(mask, 0.0, 1.0), dtype=np.float64)


def _finite_float(value: Any, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be finite") from exc
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _sigmoid(value: np.ndarray) -> np.ndarray:
    positive = value >= 0
    result = np.empty_like(value, dtype=np.float64)
    result[positive] = 1.0 / (1.0 + np.exp(-value[positive]))
    exp_value = np.exp(value[~positive])
    result[~positive] = exp_value / (1.0 + exp_value)
    return result
