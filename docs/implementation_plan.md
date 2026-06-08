# Implementation Plan

This plan stages the growth of `lcd_mask_families` while preserving its role as
a pure, deterministic mask-generation kernel library.

Implementation order is guided by:

* physical interpretability;
* expected PSF / diffraction-peak sensitivity as design intent;
* low-dimensional parameterization;
* deterministic rendering;
* testability;
* lack of consumer-specific assumptions.

No stage should add capture-plan parsing, LCD display integration, PSF artifact
handling, surrogate training, H-matrix diagnostics, reconstruction code, or
optimization loops.

## v0.1

Current minimal core:

* `GridSpec`, `ProjectionSpec`, and `MaskInstanceSpec`;
* `render_continuous_mask`;
* `project_display_mask`;
* `render_display_mask`;
* `stripes`;
* `blocks`;
* active family metadata registry;
* NumPy backend;
* projection and quantization;
* deterministic spec and array hashing;
* hardware-free tests.

## v0.2

Partially completed core expansion:

* `fourier_lowfreq` completed as the first active v0.2 family;
* `radial_zones`;
* `seeded_lowfreq_noise`;
* tests for each active family;
* examples only in JSON unless a YAML dependency is intentionally added.

This stage should reuse the active metadata registry before adding many
families. `radial_zones` and `seeded_lowfreq_noise` remain planned.

## v0.3

Planned structured family expansion:

* `multi_stripes`;
* `lattice_grating`;
* `zernike_amplitude`;
* `seeded_binary_noise`;
* active/planned registry audit.

`zernike_amplitude` should remain amplitude or transmission oriented. Do not
rename it to a phase Zernike family unless the physical LCD model supports phase
modulation.

## v0.4

Planned advanced and capture-diversity expansion:

* `chirped_stripes`;
* `hadamard_tiles` / `walsh_tiles`;
* `radial_basis`;
* `seeded_blue_noise`.

Structured non-differentiable families should be documented as capture and
generalization tools, not ordinary gradient-optimization spaces.

## Future Optional Work

Optional work after the core remains stable:

* torch backend as an optional extra;
* differentiability parity tests;
* relaxed projection policies.

Torch must not become a required dependency. Differentiable projection policies
must remain separate from hard display projection and should not introduce
downstream optimization objectives into this package.

## Release Discipline

Each new active family should include:

* family metadata;
* deterministic rendering;
* parameter validation;
* JSON example if useful;
* tests for shape, bounds, determinism, and meaningful parameter changes;
* hash compatibility through `MaskInstanceSpec`.

Planned family names should not imply active API support. A family becomes active
only when it is registered, documented, and tested.
