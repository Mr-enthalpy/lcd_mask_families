# lcd_mask_families

`lcd_mask_families` is a small pure-function kernel library for deterministic,
parameterized LCD mask families.

It owns the mathematical map from family parameters to continuous masks and
display-projected masks. It does not implement capture plans, LCD services, PSF
measurement, surrogate learning, reconstruction, H-matrix diagnostics, or mask
optimization loops. Downstream repositories should wrap this core API for their
own runtime needs.

The v0.2 family set is complete. The repository is currently in a
pre-integration stabilization stage: active families, metadata, examples,
deterministic hashing, and tests should remain stable while downstream
repositories decide how to wrap the core API.

This stage should not add downstream adapters or begin v0.3 family expansion.
The implementation is NumPy-only. Torch or other differentiable backends may be
added later as optional work, provided they preserve the same mathematical
definitions and deterministic behavior.

The active public API is intentionally small. Family-specific integration into
capture plans, differentiable training loops, or reconstruction experiments
belongs in downstream repositories.

All consumers use the same core functions and wrap them independently. This
package should not grow separate APIs for capture, forward-model training, or
reconstruction use cases.

## Install

```bash
pip install -e .
```

For tests:

```bash
pip install -e ".[dev]"
pytest -q
```

## Minimal Usage

```python
from lcd_mask_families import (
    GridSpec,
    ProjectionSpec,
    render_display_mask,
)

grid = GridSpec(coordinate_frame="normalized_lcd_pupil", shape_hw=(64, 64))
projection = ProjectionSpec(output_dtype="uint8")

mask = render_display_mask(
    "stripes",
    {
        "angle_rad": 0.0,
        "period": 0.25,
        "phase_rad": 0.0,
        "duty": 0.5,
    },
    grid,
    projection,
)
```

## Public API

```python
render_continuous_mask(family, params, grid, *, backend="numpy")
project_display_mask(mask, projection, *, backend="numpy")
render_display_mask(family, params, grid, projection, *, backend="numpy")
list_families()
get_family_metadata(family)
mask_spec_hash(spec)
array_hash(mask)
```

## Current Stage

The active v0.2 family set is complete:

* `stripes`: periodic stripe masks with optional smooth relaxation.
* `blocks`: deterministic periodic block/checker masks.
* `fourier_lowfreq`: smooth low-frequency Fourier basis masks.
* `radial_zones`: concentric or chirped radial zone masks.
* `seeded_lowfreq_noise`: seeded smooth pseudo-random low-frequency masks.

Mask identity should come from portable specs and rendering metadata, not from
experiment-local filenames. Use `mask_spec_hash` for specs and `array_hash` for
rendered arrays.

Active family metadata is queryable:

```python
from lcd_mask_families import get_family_metadata, list_families

assert list_families() == (
    "blocks",
    "fourier_lowfreq",
    "radial_zones",
    "seeded_lowfreq_noise",
    "stripes",
)
metadata = get_family_metadata("seeded_lowfreq_noise")
```

## Planning Docs

Detailed planning lives outside the README:

* [Current stage](docs/current_stage.md)
* [Mask family taxonomy](docs/family_taxonomy.md)
* [Family metadata policy](docs/family_metadata.md)
* [Implementation plan](docs/implementation_plan.md)
