# lcd_mask_families

`lcd_mask_families` is a small library for reproducible parameterized LCD mask families.

It provides pure mask-generation functions and declarative specs. It does not implement capture, calibration, PSF measurement, forward surrogate learning, reconstruction, or mask optimization.

## Project role

This repository is the shared mask-definition layer for a larger mono-LCD programmable diffraction imaging system.

```text
lcd_mask_families
  -> defines mask families, parameters, grids, projections, and deterministic mask identity

optic_system
  -> wraps these definitions for capture plans and physical LCD display

LCD_forward
  -> wraps these definitions for differentiable mask-family optimization and LCD-to-operator modelling

reconstruction
  -> may consume mask sequence identity when evaluating operator or reconstruction experiments
```

The core rule is:

```text
one mathematical mask-generation process;
different repositories may wrap it for different purposes.
```

## What this repository owns

`lcd_mask_families` owns:

* Mask family definitions.
* Parameter schemas.
* Coordinate grids.
* Continuous mask rendering.
* Display projection / quantization.
* Mask instance and mask sequence specs.
* Deterministic mask hashes and provenance.
* Small reference examples and tests.

It should answer:

```text
Given a family, parameters, grid, and projection policy, what mask is produced?
```

## What this repository does not own

This repository does not own:

* Camera, LCD, or TLS control.
* Capture plans as experimental workflows.
* Raw HDF5 or measured artifact generation.
* PSF dictionaries.
* Peak-cluster extraction.
* LCD-to-PSF or LCD-to-operator surrogate training.
* H-matrix diagnostics.
* Reconstruction algorithms.
* End-to-end mask optimization.

Those responsibilities belong to `optic_system`, `LCD_forward`, and `reconstruction`.

## Conceptual API

The stable conceptual API is:

```python
render_continuous_mask(
    family,
    params,
    grid,
    *,
    backend,
)

project_display_mask(
    mask,
    projection,
    *,
    backend,
)

render_display_mask(
    family,
    params,
    grid,
    projection,
    *,
    backend,
)
```

`render_continuous_mask` should produce a differentiable continuous mask when used with a differentiable backend.

`project_display_mask` should isolate deployment-oriented clipping, normalization, binarization, or uint8 quantization.

`render_display_mask` is a convenience composition:

```text
render_continuous_mask -> project_display_mask
```

## Specs

A minimal mask instance spec should record:

```yaml
family_id: stripes
family_version: 0.1.0

parameters:
  angle_rad: 0.785398163
  period_px: 32.0
  phase_rad: 0.0
  duty: 0.5

grid:
  coordinate_frame: normalized_lcd_pupil
  shape_hw: [64, 64]

projection:
  output_dtype: uint8
  value_range: [0, 255]
  quantization: round

identity:
  mask_id: stripes_example_000
  seed: null
```

The exact schema may evolve, but the spec must remain independent of `optic_system` and `LCD_forward` internals.

## Intended repository structure

```text
src/lcd_mask_families/
  __init__.py
  specs.py
  grids.py
  projection.py
  hashing.py
  backends.py
  families/
    __init__.py
    stripes.py
    radial_zones.py
    fourier_lowfreq.py
    blocks.py
    seeded_noise.py

schemas/
  mask_family_spec.schema.json
  mask_instance_spec.schema.json
  mask_sequence_spec.schema.json

examples/
  stripes.yaml
  radial_zones.yaml
  lowfreq_fourier.yaml

tests/
  test_determinism.py
  test_projection.py
  test_hash_identity.py
  test_backend_parity.py
```

This structure is a target, not a requirement for the initial commit.

## Consumer usage model

### optic_system side

`optic_system` should use this library through its own service or capture-plan adapter.

Example conceptual flow:

```text
capture plan references mask spec
  -> optic_system adapter loads spec
  -> lcd_mask_families renders display mask
  -> optic_system LCDService displays physical mask
  -> optic_system records mask spec, hash, and projection metadata
```

`lcd_mask_families` should not parse full optic_system capture plans.

### LCD_forward side

`LCD_forward` should use this library through its own differentiable wrapper.

Example conceptual flow:

```text
optimization variable θ
  -> lcd_mask_families continuous mask renderer
  -> LCD_forward relaxed / differentiable projection policy
  -> LCD-to-peak-cluster/operator surrogate
  -> H-matrix or reconstruction loss
```

`lcd_mask_families` should not implement surrogate models, losses, or optimizers.

## Determinism

For the same family, parameters, grid, projection, seed, and library version, rendering should be deterministic.

Mask identity should be computed from the spec and relevant rendering metadata, not from experiment-local filenames.

## Testing

Default tests must be hardware-free and should not require external repositories.

Expected tests:

```text
deterministic rendering
parameter validation
projection behavior
hash stability
numpy / torch parity, if torch backend exists
schema round-trip, if schemas exist
```

## Design summary

```text
lcd_mask_families defines reproducible differentiable mask maps.
Consumers decide how to execute, optimize, serialize, display, or evaluate them.
```
