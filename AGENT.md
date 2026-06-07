# Agent instructions for lcd_mask_families

## Repository identity

`lcd_mask_families` is a small pure-function library for parameterized LCD mask families.

Treat this repository as a narrow mathematical/specification layer, not as an experiment framework.

The central object is:

```text
θ -> M
```

where `θ` is a low-dimensional mask-family parameter object and `M` is a continuous or projected LCD mask.

## Boundary

In scope:

* Mask family specs.
* Mask instance specs.
* Mask sequence specs.
* Continuous mask rendering.
* Display projection / quantization.
* Deterministic identity / hashing.
* Small examples.
* Hardware-free tests.

Out of scope:

* optic_system service wrappers.
* capture task logic.
* camera, LCD, TLS, or HDF5 handling.
* measured PSF or peak-cluster artifacts.
* LCD_forward surrogate models.
* H-matrix diagnostics.
* reconstruction.
* end-to-end optimization.
* large datasets.

Do not add code that imports or depends on `optic_system`, `LCD_forward`, or `reconstruction`.

## Architectural rule

Do not create separate APIs for different consumers.

Wrong direction:

```text
render_for_optic_system(...)
render_for_LCD_forward(...)
```

Preferred direction:

```text
render_continuous_mask(...)
project_display_mask(...)
render_display_mask(...)
```

Each downstream repository may wrap the same core functions:

```text
optic_system:
  capture-plan adapter + LCDService wrapper

LCD_forward:
  differentiable module + optimizer/surrogate wrapper
```

The wrapper belongs downstream, not in this repository.

## Differentiability rule

The family renderer should be written so that the continuous path can be differentiable under a differentiable backend.

Keep hard display operations isolated:

```text
continuous rendering:
  should preserve gradients where possible

projection / quantization:
  deployment-oriented; may be non-differentiable
```

Do not implement straight-through estimators, reconstruction losses, H-matrix losses, or optimization policies here. Those belong in LCD_forward.

## Backend rule

Keep backend logic minimal.

If adding backend support, preserve one mathematical definition. Do not duplicate family logic into diverging numpy and torch versions unless parity tests are added.

Prefer small array-namespace style code when feasible.

Do not introduce heavy framework abstractions.

## Spec rule

Specs must remain independent of experimental systems.

A spec may include:

```text
family_id
family_version
parameters
grid
projection
seed
mask_id / hash
```

A spec must not include:

```text
camera profile
TLS state
capture run status
PSF path
reconstruction loss
surrogate checkpoint
H-matrix target
```

Those are downstream concerns.

## File and package policy

Prefer a small package layout:

```text
src/lcd_mask_families/
  specs.py
  grids.py
  projection.py
  hashing.py
  families/
```

Do not add directories that imply external ownership, such as:

```text
optic_system/
lcd_forward/
reconstruction/
capture/
training/
psf/
h_matrix/
```

Examples and schemas are allowed if they remain small and declarative.

## Testing policy

Default tests must not require:

```text
optic_system
LCD_forward
reconstruction
camera hardware
LCD hardware
TLS hardware
measured PSF files
large generated masks
```

Add tests for:

```text
determinism
parameter bounds
projection behavior
hash stability
spec round-trip
backend parity, if multiple backends exist
```

## Data policy

Do not commit large masks, generated datasets, PSF dictionaries, measured artifacts, or rendered experimental outputs.

Small YAML examples and tiny test fixtures are allowed.

## Documentation policy

Documentation should emphasize:

```text
pure parameterized mask maps
deterministic mask identity
consumer-side wrapping
no experiment-framework ownership
```

Avoid language implying that this repository owns capture plans, forward surrogate training, reconstruction, or mask optimization loops.

## Review checklist

Before finalizing a change, verify:

* The change does not import external project repositories.
* The change does not add experiment-specific adapters.
* The change preserves deterministic rendering.
* The same mask family definition can be used by both optic_system and LCD_forward.
* Hard projection and continuous rendering remain conceptually separate.
* Tests remain hardware-free and small.
* Documentation still describes a pure mask-family library, not a pipeline repository.
