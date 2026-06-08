from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from ..metadata import FamilyMetadata


FAMILY_METADATA = FamilyMetadata(
    family_id="seeded_lowfreq_noise",
    family_version="0.1.0",
    status="active",
    differentiable=False,
    continuous_parameters=False,
    seeded=True,
    diffraction_oriented=False,
    orthogonal_basis=True,
    recommended_for_capture=True,
    recommended_for_optimization=False,
    notes=(
        "Seeded low-frequency pseudo-random family for capture diversity and "
        "forward-model generalization. The seed is part of deterministic mask "
        "identity and is not a continuous optimization coordinate."
    ),
)


def render_seeded_lowfreq_noise(
    params: Mapping[str, Any],
    grid_arrays: Mapping[str, np.ndarray],
) -> np.ndarray:
    seed = _integer(params.get("seed"), "seed")
    max_frequency = _integer(params.get("max_frequency", 3), "max_frequency")
    spectrum_decay = _finite_float(params.get("spectrum_decay", 1.0), "spectrum_decay")
    coefficient_scale = _finite_float(
        params.get("coefficient_scale", 1.0),
        "coefficient_scale",
    )
    bias = _finite_float(params.get("bias", 0.0), "bias")
    contrast = _finite_float(params.get("contrast", 1.0), "contrast")
    activation = str(params.get("activation", "sigmoid"))

    if max_frequency <= 0:
        raise ValueError("max_frequency must be positive")
    if spectrum_decay < 0.0:
        raise ValueError("spectrum_decay must be nonnegative")
    if coefficient_scale < 0.0:
        raise ValueError("coefficient_scale must be nonnegative")
    if contrast <= 0.0:
        raise ValueError("contrast must be positive")
    if activation not in {"sigmoid", "linear_clip"}:
        raise ValueError(f"unsupported activation: {activation!r}")

    x = np.asarray(grid_arrays["x"], dtype=np.float64)
    y = np.asarray(grid_arrays["y"], dtype=np.float64)
    field = np.full_like(x, bias, dtype=np.float64)
    rng = np.random.default_rng(seed)

    for kx in range(-max_frequency, max_frequency + 1):
        for ky in range(-max_frequency, max_frequency + 1):
            if (kx, ky) == (0, 0):
                continue
            radius = float(np.sqrt(kx * kx + ky * ky))
            weight = coefficient_scale / (1.0 + radius) ** spectrum_decay
            cos_coeff = rng.standard_normal()
            sin_coeff = rng.standard_normal()
            phase = np.pi * (kx * x + ky * y)
            field += weight * (cos_coeff * np.cos(phase) + sin_coeff * np.sin(phase))

    scaled = contrast * field
    if activation == "sigmoid":
        mask = _sigmoid(scaled)
    else:
        mask = np.clip(scaled, 0.0, 1.0)

    if not np.all(np.isfinite(mask)):
        raise ValueError("rendered mask contains non-finite values")
    return np.asarray(np.clip(mask, 0.0, 1.0), dtype=np.float64)


def _integer(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
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
