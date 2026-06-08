# lcd_mask_families

`lcd_mask_families` is a small pure-function kernel library for deterministic,
parameterized LCD mask families.

It owns the mathematical map from family parameters to continuous masks and
display-projected masks. It does not implement capture plans, LCD services, PSF
measurement, surrogate learning, reconstruction, H-matrix diagnostics, or mask
optimization loops. Downstream repositories should wrap this core API for their
own runtime needs.

The initial implementation is NumPy-only. Torch or other differentiable backends
may be added later as optional work, provided they preserve the same mathematical
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
```

The current package includes three small families:

* `stripes`: periodic stripe masks with optional smooth relaxation.
* `blocks`: deterministic periodic block/checker masks.
* `fourier_lowfreq`: smooth low-frequency Fourier basis masks.

Mask identity should come from portable specs and rendering metadata, not from
experiment-local filenames. Use `mask_spec_hash` for specs and `array_hash` for
rendered arrays.

Active family metadata is queryable:

```python
from lcd_mask_families import get_family_metadata, list_families

assert list_families() == ("blocks", "fourier_lowfreq", "stripes")
metadata = get_family_metadata("fourier_lowfreq")
```

## Planning Docs

Detailed planning lives outside the README:

* [Mask family taxonomy](docs/family_taxonomy.md)
* [Family metadata policy](docs/family_metadata.md)
* [Implementation plan](docs/implementation_plan.md)
