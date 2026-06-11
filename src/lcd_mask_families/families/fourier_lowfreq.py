from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from ..metadata import FamilyMetadata


FAMILY_METADATA = FamilyMetadata(
    family_id="fourier_lowfreq",
    family_version="0.1.0",
    status="active",
    differentiability={
        "continuous_parameters": True,
        "differentiable_render": True,
        "differentiable_projection": "none",
        "seed_is_optimization_variable": False,
    },
    design_intent={
        "diffraction_oriented": False,
        "orthogonal_basis": True,
        "seeded_random": False,
        "recommended_for_capture": True,
        "recommended_for_optimization": True,
        "random_walk_risk": "low",
    },
    response_prior={
        "expected_effect": ["peak_spread_change", "response_space_coverage"],
        "validated_by_measured_psf": False,
    },
    parameter_schema={
        "required": ["modes"],
        "optional": ["max_frequency", "bias", "contrast", "activation"],
    },
    notes=(
        "Low-frequency Fourier basis family for smooth structured mask variation. "
        "It is a baseline optimization and response-space exploration family, not "
        "a diffraction-specialized grating family."
    ),
)


def render_fourier_lowfreq(
    params: Mapping[str, Any],
    grid_arrays: Mapping[str, np.ndarray],
) -> np.ndarray:
    """Render a bounded low-frequency Fourier basis mask.

    Phase convention: phase = pi * (kx * x + ky * y). On the normalized
    [-1, 1] coordinate frame, kx=1 or ky=1 gives one full cosine cycle across
    the corresponding axis.
    """

    modes = _validate_modes(params.get("modes"), _max_frequency(params.get("max_frequency", 4)))
    bias = _finite_float(params.get("bias", 0.0), "bias")
    contrast = _finite_float(params.get("contrast", 1.0), "contrast")
    activation = str(params.get("activation", "sigmoid"))

    if contrast <= 0.0:
        raise ValueError("contrast must be positive")
    if activation not in {"sigmoid", "linear_clip"}:
        raise ValueError(f"unsupported activation: {activation!r}")

    x = np.asarray(grid_arrays["x"], dtype=np.float64)
    y = np.asarray(grid_arrays["y"], dtype=np.float64)
    field = np.full_like(x, bias, dtype=np.float64)

    for mode in modes:
        phase = np.pi * (mode["kx"] * x + mode["ky"] * y)
        field += mode["cos"] * np.cos(phase) + mode["sin"] * np.sin(phase)

    scaled = contrast * field
    if activation == "sigmoid":
        mask = _sigmoid(scaled)
    else:
        mask = np.clip(scaled, 0.0, 1.0)

    if not np.all(np.isfinite(mask)):
        raise ValueError("rendered mask contains non-finite values")
    return np.asarray(np.clip(mask, 0.0, 1.0), dtype=np.float64)


def _validate_modes(value: Any, max_frequency: int) -> tuple[dict[str, float | int], ...]:
    if max_frequency <= 0:
        raise ValueError("max_frequency must be positive")
    if not isinstance(value, list) or not value:
        raise ValueError("modes must be a non-empty list")

    modes = []
    for index, mode in enumerate(value):
        if not isinstance(mode, Mapping):
            raise ValueError(f"mode {index} must be a mapping")
        kx = _integer_frequency(mode.get("kx"), f"modes[{index}].kx")
        ky = _integer_frequency(mode.get("ky"), f"modes[{index}].ky")
        if (kx, ky) == (0, 0):
            raise ValueError("mode frequency (kx, ky) must not be (0, 0); use bias for DC")
        if abs(kx) > max_frequency or abs(ky) > max_frequency:
            raise ValueError("mode frequency exceeds max_frequency")
        modes.append(
            {
                "kx": kx,
                "ky": ky,
                "cos": _finite_float(mode.get("cos", 0.0), f"modes[{index}].cos"),
                "sin": _finite_float(mode.get("sin", 0.0), f"modes[{index}].sin"),
            }
        )
    return tuple(modes)


def _integer_frequency(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    return value


def _max_frequency(value: Any) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("max_frequency must be an integer")
    if value <= 0:
        raise ValueError("max_frequency must be positive")
    return value


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
