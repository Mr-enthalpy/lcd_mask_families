from __future__ import annotations

import numpy as np

from .backends import require_numpy_backend
from .specs import ProjectionSpec


def project_display_mask(
    mask: np.ndarray,
    projection: ProjectionSpec | dict[str, object],
    *,
    backend: str = "numpy",
) -> np.ndarray:
    require_numpy_backend(backend)
    if not isinstance(projection, ProjectionSpec):
        projection = ProjectionSpec.from_dict(projection)

    values = np.asarray(mask, dtype=np.float64)
    if projection.normalize == "minmax":
        low = float(np.min(values))
        high = float(np.max(values))
        if high > low:
            values = (values - low) / (high - low)
        else:
            values = np.zeros_like(values, dtype=np.float64)

    if projection.clip:
        values = np.clip(values, 0.0, 1.0)

    low, high = projection.value_range

    if projection.quantization == "threshold":
        values = values >= float(projection.threshold)

    projected = values * (high - low) + low

    if projection.quantization in {"round", "threshold"}:
        projected = np.rint(projected)
    elif projection.quantization != "none":
        raise ValueError(f"unsupported quantization: {projection.quantization!r}")

    if projection.output_dtype == "uint8":
        return np.asarray(projected, dtype=np.uint8)
    if projection.output_dtype == "float32":
        return np.asarray(projected, dtype=np.float32)
    raise ValueError(f"unsupported output_dtype: {projection.output_dtype!r}")
