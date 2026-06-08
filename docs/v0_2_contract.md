# v0.2 Contract

This document defines the v0.2 contract for `lcd_mask_families`.

The package is a pure deterministic mask-generation kernel library:

```text
family + parameters + grid + projection policy -> mask
```

It is not an experiment framework and does not own downstream capture,
forward-model, reconstruction, or optimization workflows.

## Active Public API

Downstream consumers should use the top-level package API unless a future
version explicitly exports more:

```python
GridSpec
ProjectionSpec
MaskInstanceSpec
render_continuous_mask
project_display_mask
render_display_mask
mask_spec_hash
array_hash
```

Family listing and metadata queries are also supported for active families:

```python
list_families
get_family_metadata
get_family_metadata_dict
```

The rendering API should remain consumer-neutral. Do not add separate public
APIs for `optic_system`, `LCD_forward`, or `reconstruction`.

## Active Families

The active v0.2 family set is:

```text
stripes
blocks
fourier_lowfreq
radial_zones
seeded_lowfreq_noise
```

Roles:

```text
stripes:
  differentiable, diffraction-oriented, capture + optimization candidate

blocks:
  non-differentiable, structured capture/generalization family

fourier_lowfreq:
  differentiable, orthogonal/low-dimensional basis family,
  capture + optimization candidate

radial_zones:
  differentiable, diffraction-oriented / radial basis-like family,
  capture + optimization candidate

seeded_lowfreq_noise:
  seeded, deterministic pseudo-random low-frequency family,
  capture/generalization family,
  not ordinary gradient-optimization family
```

These roles are design-intent metadata. They are not measured optical
performance claims.

## Contracted Behavior

The following behavior should remain stable across v0.2 patch changes:

* same spec gives the same spec hash;
* same family, parameters, grid, and projection policy gives the same rendered
  display mask;
* continuous masks are finite and clipped or normalized into `[0, 1]`;
* projection is explicitly separate from continuous rendering;
* display projection supports `uint8` and `float32`;
* NumPy is the only required backend;
* no external repository dependency is allowed;
* active family metadata is available through the active metadata registry;
* active examples are JSON and should round-trip through `MaskInstanceSpec`.

Mask identity should come from portable specs and rendering metadata, not from
experiment-local filenames.

## Non-Contract Behavior

The following are not promised by v0.2:

* no torch backend;
* no differentiability guarantee at the array backend level beyond mathematical
  intent;
* no final JSON schema stability;
* no downstream adapter stability;
* no physical LCD display packing;
* no PSF response guarantee;
* no claim that any family empirically produces good PSF diversity before
  `optic_system` measurements or `LCD_forward` validation;
* no capture-plan parsing;
* no reconstruction or optimization interface.

Downstream repositories should wrap this contract in their own adapter layers.
