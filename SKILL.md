# lcd_mask_families skill

## Purpose

`lcd_mask_families` defines small, deterministic, parameterized LCD mask families.

Its core responsibility is the map:

```text
mask-family parameters θ
  -> continuous mask M_cont
  -> projected / quantized display mask M_display
```

The same core function is used from two sides:

```text
optic_system:
  evaluate a mask spec at concrete parameters and display the resulting mask

LCD_forward:
  keep the same map inside a differentiable computation graph
```

This repository does not decide how masks are captured, optimized, evaluated, reconstructed, or displayed in a specific experimental system.

## Core principle

The library should expose a small set of pure functions and declarative specs.

Do not create separate APIs such as:

```text
render_for_optic_system(...)
render_for_LCD_forward(...)
```

Instead, define one canonical family-rendering process. Consumers may wrap it for their own runtime:

```text
optic_system wraps it with a capture-plan / LCD-service adapter
LCD_forward wraps it with a differentiable mask-family module
```

## In scope

Allowed work:

* Parameterized mask-family definitions.
* Deterministic rendering from family parameters to mask arrays.
* Continuous masks for differentiable optimization.
* Projection and quantization utilities.
* Declarative mask family, mask instance, and mask sequence specs.
* Deterministic hash / provenance identity for rendered masks.
* Minimal numpy reference implementation.
* Optional torch-compatible implementation or backend dispatch when it preserves the same mathematical definition.
* Small examples and tests.

Typical families:

```text
stripes
radial_zones
low-frequency Fourier masks
block / tiled patterns
seeded smooth noise
```

## Out of scope

Do not add:

* optic_system capture-plan execution logic.
* optic_system LCDService wrappers.
* camera, TLS, HDF5, raw capture, profile, or artifact logic.
* LCD_forward surrogate models.
* H-matrix diagnostics.
* reconstruction algorithms.
* mask optimization loops.
* GenerMask training code.
* learned mask generators.
* hardware-specific scheduling.
* large datasets or measured PSF files.

This repository may define what a mask family is. It must not decide how a specific experiment uses that family.

## Desired minimal API shape

The exact names may evolve, but the conceptual API should remain close to:

```python
render_continuous_mask(family, params, grid, *, backend)
project_display_mask(mask, projection, *, backend)
render_display_mask(family, params, grid, projection, *, backend)
```

The output should be deterministic for the same:

```text
family id
family version
parameters
grid spec
projection spec
library version
```

## Differentiability policy

Differentiability belongs to the core mathematical map, not to a special LCD_forward-only API.

Continuous rendering should avoid unnecessary discrete operations. Hard quantization should be isolated in projection utilities.

For deployment:

```text
continuous mask -> display projection -> uint8 or binary mask
```

For optimization:

```text
continuous mask -> optional relaxed / soft projection in LCD_forward adapter
```

If straight-through estimators, quantization-aware losses, or reconstruction-driven objectives are needed, they belong in LCD_forward, not in this core library.

## Backend policy

Keep backend support minimal.

The preferred rule is:

```text
same mathematical function
same family parameters
same grid
same projection
same mask values up to numerical tolerance
```

If both numpy and torch are supported, add parity tests.

Do not build a large backend framework. Prefer a small array namespace or clearly separated reference implementations.

## Spec policy

Specs should be declarative and portable.

A mask instance spec should be enough to regenerate the mask without knowing optic_system or LCD_forward internals.

It should record at least:

```text
family_id
family_version
parameters
grid
projection
seed, if any
mask_id or deterministic hash
```

A mask sequence spec should record an ordered list of mask instances.

## Testing policy

Default tests should be hardware-free and data-free.

Required test categories:

```text
determinism
parameter bounds
projection / quantization
hash identity
numpy / torch parity, if torch support exists
schema round-trip, if schemas exist
```

No test should require optic_system, LCD_forward, reconstruction, camera hardware, LCD hardware, TLS hardware, or measured PSF artifacts.

## Repository boundary summary

```text
lcd_mask_families defines reproducible differentiable mask maps.
Consumers decide how to execute, optimize, serialize, display, or evaluate them.
```
