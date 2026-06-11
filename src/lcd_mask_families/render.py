from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from .backends import require_numpy_backend
from .families.registry import FAMILY_METADATA_REGISTRY, FAMILY_REGISTRY
from .grids import make_grid
from .hashing import hash_mask_instance
from .projection import project_display_mask
from .specs import GridSpec, MaskInstanceSpec, MaskSequenceSpec, ProjectionSpec, RenderedMask


def render_continuous_mask(
    family: str,
    params: Mapping[str, Any],
    grid: GridSpec | Mapping[str, Any],
    *,
    backend: str = "numpy",
) -> np.ndarray:
    require_numpy_backend(backend)
    if not isinstance(grid, GridSpec):
        grid = GridSpec.from_dict(grid)
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
    grid: GridSpec | Mapping[str, Any],
    projection: ProjectionSpec | Mapping[str, Any],
    *,
    backend: str = "numpy",
) -> np.ndarray:
    continuous = render_continuous_mask(family, params, grid, backend=backend)
    return project_display_mask(continuous, projection, backend=backend)


def render_mask_instance(
    spec: MaskInstanceSpec | Mapping[str, Any],
    *,
    backend: str = "numpy",
) -> RenderedMask:
    if not isinstance(spec, MaskInstanceSpec):
        spec = MaskInstanceSpec.from_dict(spec)
    display = render_display_mask(
        spec.family_id,
        spec.parameters,
        spec.grid,
        spec.projection,
        backend=backend,
    )
    spec_hash = hash_mask_instance(spec)
    mask_id = spec.identity.mask_id or spec_hash
    metadata = {
        "contract_hash": spec_hash,
        "family_metadata": FAMILY_METADATA_REGISTRY[spec.family_id].to_dict(),
    }
    if spec.metadata:
        metadata["spec_metadata"] = dict(spec.metadata)
    return RenderedMask(
        mask=display,
        mask_id=mask_id,
        hash=spec_hash,
        family_id=spec.family_id,
        family_version=spec.family_version,
        grid=spec.grid,
        projection=spec.projection,
        dtype=str(display.dtype),
        shape_hw=tuple(display.shape),
        metadata=metadata,
    )


def render_mask_sequence(
    sequence: MaskSequenceSpec | Mapping[str, Any],
    *,
    backend: str = "numpy",
) -> list[RenderedMask]:
    if not isinstance(sequence, MaskSequenceSpec):
        sequence = MaskSequenceSpec.from_dict(sequence)
    return [render_mask_instance(mask, backend=backend) for mask in sequence.masks]
